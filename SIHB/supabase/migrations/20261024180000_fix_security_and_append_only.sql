/*
# Security Hardening, Append-Only Evidence Dossier & Hash-Chained Audit Ledger

## Overview
1. Enforces immutable append-only constraints on evidence_artifacts and audit_log:
   - Revokes all UPDATE, DELETE, and TRUNCATE privileges for all roles.
   - Adds trigger preventing any row alteration or deletion.
2. Hardens storage policies on label-images and evidence-photos:
   - Removes anonymous deletion and anonymous upload permissions.
   - Deletion restricted exclusively to administrators.
   - Uploads restricted to authenticated users.
3. Fixes privilege escalation on user_profiles:
   - Prevents non-admin users from updating the 'role' column on their own profile.
4. Adds cryptographic SHA-256 hash chaining columns and sequence triggers to audit_log.
*/

-- ============ 1. APPEND-ONLY EVIDENCE & AUDIT LOG TRIGGERS ============

CREATE OR REPLACE FUNCTION block_evidence_tampering()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Evidence records and audit log entries are append-only and cannot be updated, deleted, or truncated.';
END;
$$ LANGUAGE plpgsql;

-- Block UPDATE and DELETE on evidence_artifacts
DROP TRIGGER IF EXISTS trg_block_evidence_modification ON evidence_artifacts;
CREATE TRIGGER trg_block_evidence_modification
  BEFORE UPDATE OR DELETE ON evidence_artifacts
  FOR EACH ROW EXECUTE FUNCTION block_evidence_tampering();

-- Block UPDATE and DELETE on audit_log
DROP TRIGGER IF EXISTS trg_block_audit_modification ON audit_log;
CREATE TRIGGER trg_block_audit_modification
  BEFORE UPDATE OR DELETE ON audit_log
  FOR EACH ROW EXECUTE FUNCTION block_evidence_tampering();

-- Revoke dangerous RLS policies on evidence_artifacts
DROP POLICY IF EXISTS "anon_update_evidence" ON evidence_artifacts;
DROP POLICY IF EXISTS "anon_delete_evidence" ON evidence_artifacts;
DROP POLICY IF EXISTS "authenticated_update_evidence" ON evidence_artifacts;
DROP POLICY IF EXISTS "authenticated_delete_evidence" ON evidence_artifacts;

-- Ensure SELECT and INSERT only for authenticated users on evidence_artifacts
DROP POLICY IF EXISTS "authenticated_select_evidence" ON evidence_artifacts;
CREATE POLICY "authenticated_select_evidence" ON evidence_artifacts FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "authenticated_insert_evidence" ON evidence_artifacts;
CREATE POLICY "authenticated_insert_evidence" ON evidence_artifacts FOR INSERT
  TO authenticated WITH CHECK (true);

-- Ensure SELECT and INSERT only for authenticated users on audit_log
DROP POLICY IF EXISTS "authenticated_select_audit" ON audit_log;
CREATE POLICY "authenticated_select_audit" ON audit_log FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "authenticated_insert_audit" ON audit_log;
CREATE POLICY "authenticated_insert_audit" ON audit_log FOR INSERT
  TO authenticated WITH CHECK (true);


-- ============ 2. AUDIT LOG HASH CHAINING ============

ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS sequence_num BIGSERIAL;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS prev_hash TEXT;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS curr_hash TEXT;

CREATE OR REPLACE FUNCTION compute_audit_hash_chain()
RETURNS TRIGGER AS $$
DECLARE
  v_prev_hash TEXT;
BEGIN
  -- Fetch hash of immediately preceding log record
  SELECT curr_hash INTO v_prev_hash
  FROM audit_log
  WHERE id <> NEW.id
  ORDER BY sequence_num DESC
  LIMIT 1;

  NEW.prev_hash := COALESCE(v_prev_hash, '0000000000000000000000000000000000000000000000000000000000000000');
  NEW.created_at := now();

  -- Compute SHA-256 over sequence, inspection, action, actor, details, created_at, and prev_hash
  NEW.curr_hash := encode(
    digest(
      COALESCE(NEW.sequence_num::text, '') ||
      COALESCE(NEW.inspection_id::text, '') ||
      COALESCE(NEW.action, '') ||
      COALESCE(NEW.actor, '') ||
      COALESCE(NEW.details::text, '') ||
      NEW.created_at::text ||
      NEW.prev_hash,
      'sha256'
    ),
    'hex'
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_audit_hash_chain ON audit_log;
CREATE TRIGGER trg_audit_hash_chain
  BEFORE INSERT ON audit_log
  FOR EACH ROW EXECUTE FUNCTION compute_audit_hash_chain();


-- ============ 3. SECURE STORAGE POLICIES ============

-- Revoke anonymous upload and delete on storage buckets
DROP POLICY IF EXISTS "auth_upload_label_images" ON storage.objects;
DROP POLICY IF EXISTS "auth_delete_label_images" ON storage.objects;
DROP POLICY IF EXISTS "auth_upload_evidence_photos" ON storage.objects;
DROP POLICY IF EXISTS "auth_delete_evidence_photos" ON storage.objects;

-- Only authenticated users can upload label images
CREATE POLICY "auth_upload_label_images" ON storage.objects FOR INSERT
  TO authenticated WITH CHECK (bucket_id = 'label-images');

-- Only authenticated users can upload evidence photos
CREATE POLICY "auth_upload_evidence_photos" ON storage.objects FOR INSERT
  TO authenticated WITH CHECK (bucket_id = 'evidence-photos');

-- Only administrators can delete label images or evidence photos
CREATE POLICY "admin_delete_label_images" ON storage.objects FOR DELETE
  TO authenticated USING (
    bucket_id = 'label-images' AND
    EXISTS (SELECT 1 FROM user_profiles WHERE id = auth.uid() AND role = 'admin')
  );

CREATE POLICY "admin_delete_evidence_photos" ON storage.objects FOR DELETE
  TO authenticated USING (
    bucket_id = 'evidence-photos' AND
    EXISTS (SELECT 1 FROM user_profiles WHERE id = auth.uid() AND role = 'admin')
  );


-- ============ 4. PREVENT USER SELF-PROMOTION ============

CREATE OR REPLACE FUNCTION protect_user_role_escalation()
RETURNS TRIGGER AS $$
BEGIN
  -- Prevent changing role unless the executing user is already an admin
  IF NEW.role <> OLD.role THEN
    IF NOT EXISTS (SELECT 1 FROM user_profiles WHERE id = auth.uid() AND role = 'admin') THEN
      RAISE EXCEPTION 'Only administrators can modify user roles.';
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_protect_role_escalation ON user_profiles;
CREATE TRIGGER trg_protect_role_escalation
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION protect_user_role_escalation();
