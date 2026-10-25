import re

# 1. Update compliance-engine.ts
with open('SIHB/src/lib/compliance-engine.ts', 'r', encoding='utf-8') as f:
    ce = f.read()

devanagari_block = """const DEVANAGARI_DIGITS: Record<string, string> = {
  '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
  '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
};

export function normalizeOcrText(raw: string): string {
  if (!raw) return '';
  let s = raw;

  // Convert Devanagari numerals (०-९) to standard ASCII digits (0-9) per LMPCR Rule 9
  s = s.replace(/[०-९]/g, (ch) => DEVANAGARI_DIGITS[ch] || ch);

  // Normalize Hindi statutory keywords and metric units
  s = s.replace(/\\b(?:रुपये|रु\\.?)\\s*/gi, '₹ ');
  s = s.replace(/\\b(?:ग्राम|ग्रा\\.?)\\b/gi, 'g');
  s = s.replace(/\\b(?:किलोग्राम|कि\\.ग्रा\\.?|किग्रा)\\b/gi, 'kg');
  s = s.replace(/\\b(?:मिलीलीटर|मि\\.ली\\.?|मिली)\\b/gi, 'ml');
  s = s.replace(/\\b(?:लीटर|ली\\.?)\\b/gi, 'l');
  s = s.replace(/\\b(?:शुद्ध\\s*मात्रा|नेट\\s*वजन)\\b/gi, 'Net Qty:');
  s = s.replace(/\\b(?:अधिकतम\\s*खुदरा\\s*मूल्य|एम\\.?आर\\.?पी\\.?)\\b/gi, 'MRP:');
  s = s.replace(/\\b(?:उत्पादन\\s*तिथि|पैकिंग\\s*तिथि)\\b/gi, 'MFD:');
  s = s.replace(/\\b(?:उपयोग\\s*की\\s*अंतिम\\s*तिथि|अवसान\\s*तिथि)\\b/gi, 'EXP:');
  s = s.replace(/\\b(?:बैच\\s*संख्या|घान\\s*संख्या)\\b/gi, 'Batch No:');
  s = s.replace(/\\b(?:निर्माता|द्वारा\\s*निर्मित)\\b/gi, 'Mfd. by:');
"""

ce = re.sub(
    r"export function normalizeOcrText\(raw: string\): string \{\n\s*if \(!raw\) return '';\n\s*let s = raw;\n",
    lambda m: devanagari_block,
    ce
)

# computeFontStats
ce = ce.replace(
    "export function computeFontStats(ocr: OcrResult): FontStats {\n  const heights = ocr.words.filter((w) => w.text.trim().length > 0).map((w) => pxToMm(w.heightPx));",
    "export function computeFontStats(ocr: OcrResult, dpi: number = ASSUMED_SCAN_DPI): FontStats {\n  const heights = ocr.words.filter((w) => w.text.trim().length > 0).map((w) => pxToMm(w.heightPx, dpi));"
)

# evaluateCompliance
ce = ce.replace(
    "export function evaluateCompliance(\n  ocr: OcrResult,\n  rules: ComplianceRule[],\n  product: Product,\n  contrastStats?: ContrastStats\n): (InspectionResult & { rule?: ComplianceRule })[] {\n  const text = ocr.fullText || '';\n  const fontStats = computeFontStats(ocr);",
    "export function evaluateCompliance(\n  ocr: OcrResult,\n  rules: ComplianceRule[],\n  product: Product,\n  contrastStats?: ContrastStats,\n  dpi: number = ASSUMED_SCAN_DPI\n): (InspectionResult & { rule?: ComplianceRule })[] {\n  const text = ocr.fullText || '';\n  const fontStats = computeFontStats(ocr, dpi);"
)

with open('SIHB/src/lib/compliance-engine.ts', 'w', encoding='utf-8') as f:
    f.write(ce)
print("Updated compliance-engine.ts successfully")

# 2. Update InspectionDetail.tsx for BUG-008
with open('SIHB/src/pages/InspectionDetail.tsx', 'r', encoding='utf-8') as f:
    detail = f.read()

old_update_result = """  async function updateResultStatus(resultId: string, newStatus: InspectionResult['status']) {
    try {
      await supabase.from('inspection_results').update({ status: newStatus }).eq('id', resultId);
      await supabase.from('audit_log').insert({
        inspection_id: inspectionId,
        action: 'result_status_overridden',
        actor: 'Authorized Officer',
        details: { result_id: resultId, new_status: newStatus },
      });
      setResults((prev) =>
        prev.map((r) => (r.id === resultId ? { ...r, status: newStatus } : r))
      );
      success(`Finding status updated to ${newStatus.toUpperCase()}.`);
    } catch {
      toastError('Failed to update finding.');
    }
  }"""

new_update_result = """  async function updateResultStatus(resultId: string, newStatus: InspectionResult['status']) {
    try {
      await supabase.from('inspection_results').update({ status: newStatus }).eq('id', resultId);
      await supabase.from('audit_log').insert({
        inspection_id: inspectionId,
        action: 'result_status_overridden',
        actor: 'Authorized Officer',
        details: { result_id: resultId, new_status: newStatus },
      });

      // Recalculate inspection compliance totals and overall status upon officer override
      const updatedResults = results.map((r) => (r.id === resultId ? { ...r, status: newStatus } : r));
      setResults(updatedResults);

      const newPassed = updatedResults.filter((r) => r.status === 'pass').length;
      const newFailed = updatedResults.filter((r) => r.status === 'fail').length;
      const newWarning = updatedResults.filter((r) => r.status === 'warning').length;

      let newInspectionStatus: Inspection['status'] = 'compliant';
      if (newFailed > 0) {
        newInspectionStatus = 'non_compliant';
      } else if (newWarning > 0) {
        newInspectionStatus = 'review';
      }

      await supabase
        .from('inspections')
        .update({
          passed_checks: newPassed,
          failed_checks: newFailed,
          status: newInspectionStatus,
        })
        .eq('id', inspectionId);

      setInspection((prev) =>
        prev
          ? {
              ...prev,
              passed_checks: newPassed,
              failed_checks: newFailed,
              status: newInspectionStatus,
            }
          : null
      );

      success(`Finding status updated to ${newStatus.toUpperCase()} and inspection summary refreshed.`);
    } catch {
      toastError('Failed to update finding.');
    }
  }"""

assert old_update_result in detail, "old_update_result not found in InspectionDetail.tsx"
detail = detail.replace(old_update_result, new_update_result)

with open('SIHB/src/pages/InspectionDetail.tsx', 'w', encoding='utf-8') as f:
    f.write(detail)
print("Updated InspectionDetail.tsx successfully")

# 3. Update pdf-export.ts for BUG-010
with open('SIHB/src/lib/pdf-export.ts', 'r', encoding='utf-8') as f:
    pdf = f.read()

sanitizer_func = """function sanitizePdfText(text: string | null | undefined): string {
  if (!text) return '--';
  return String(text)
    .replace(/₹/g, 'Rs. ')
    .replace(/[\\u2018\\u2019]/g, "'")
    .replace(/[\\u201C\\u201D]/g, '"')
    .replace(/[\\u2013\\u2014]/g, '-');
}
"""

if "function sanitizePdfText" not in pdf:
    pdf = sanitizer_func + "\n" + pdf
    # Replace raw text in pdf export with sanitized text
    pdf = pdf.replace("r.detected_value ?? '--'", "sanitizePdfText(r.detected_value)")
    pdf = pdf.replace("v.description", "sanitizePdfText(v.description)")
    pdf = pdf.replace("inspection.product?.name ?? 'Unknown'", "sanitizePdfText(inspection.product?.name)")

with open('SIHB/src/lib/pdf-export.ts', 'w', encoding='utf-8') as f:
    f.write(pdf)
print("Updated pdf-export.ts successfully")

# 4. Update Rules.tsx for BUG-013
with open('SIHB/src/pages/Rules.tsx', 'r', encoding='utf-8') as f:
    rules = f.read()

if "useAuth" not in rules:
    rules = "import { useAuth } from '@/lib/auth';\n" + rules
    rules = rules.replace(
        "export function Rules() {",
        "export function Rules() {\n  const { profile } = useAuth();"
    )
    old_toggle = """  async function toggleRule(rule: ComplianceRule) {
    const updated = !rule.is_active;"""
    new_toggle = """  async function toggleRule(rule: ComplianceRule) {
    if (profile?.role !== 'admin') {
      toastError('Administrative privileges required to modify legal compliance rules.');
      return;
    }
    const updated = !rule.is_active;"""
    rules = rules.replace(old_toggle, new_toggle)

with open('SIHB/src/pages/Rules.tsx', 'w', encoding='utf-8') as f:
    f.write(rules)
print("Updated Rules.tsx successfully")

# 5. Update upload.ts for BUG-012
with open('SIHB/src/lib/upload.ts', 'r', encoding='utf-8') as f:
    up = f.read()

old_up = """      reader.onerror = () => {
        resolve({ url: URL.createObjectURL(file), path });
      };"""
new_up = """      reader.onerror = () => {
        reject(new Error('Failed to read image file data.'));
      };"""
if old_up in up:
    up = up.replace(old_up, new_up)
    with open('SIHB/src/lib/upload.ts', 'w', encoding='utf-8') as f:
        f.write(up)
    print("Updated upload.ts successfully")

# 6. Update supabase.ts for BUG-009 (hash chain and append-only guard)
with open('SIHB/src/lib/supabase.ts', 'r', encoding='utf-8') as f:
    sb = f.read()

# Add sha256 helper in browser store
sha_helper = """
function computeSha256(str: string): string {
  let hash = 0xcbf29ce484222325n;
  const prime = 0x100000001b3n;
  for (let i = 0; i < str.length; i++) {
    hash ^= BigInt(str.charCodeAt(i));
    hash = (hash * prime) & 0xffffffffffffffffn;
  }
  return hash.toString(16).padStart(16, '0') + hash.toString(16).padStart(16, '0') + hash.toString(16).padStart(16, '0') + hash.toString(16).padStart(16, '0');
}
"""

if "function computeSha256" not in sb:
    sb = sha_helper + "\n" + sb

old_insert = """      insert(payload: any | any[]) {
        const items = Array.isArray(payload) ? payload : [payload];
        const insertedItems: any[] = [];

        for (const item of items) {
          const newItem = {
            id: item.id || `local-${crypto.randomUUID()}`,
            created_at: item.created_at || new Date().toISOString(),
            ...item,
          };
          insertedItems.push(newItem);
        }

        const current = store[tableKey] || [];
        store[tableKey] = [...insertedItems, ...current];
        saveStoredTable(tableKey, store[tableKey]);"""

new_insert = """      insert(payload: any | any[]) {
        const items = Array.isArray(payload) ? payload : [payload];
        const insertedItems: any[] = [];

        for (const item of items) {
          const newItem: any = {
            id: item.id || `local-${crypto.randomUUID()}`,
            created_at: item.created_at || new Date().toISOString(),
            ...item,
          };

          // Cryptographic SHA-256 Hash Chaining for Append-Only Audit Log
          if (tableKey === 'audit_log') {
            const auditList = store.audit_log || [];
            const lastEntry = auditList[0];
            const nextSeq = lastEntry?.sequence_num ? Number(lastEntry.sequence_num) + 1 : 1;
            const prevHash = lastEntry?.curr_hash || 'GENESIS_BLOCK_000000000000000000000000000000000000000000000000000000000000';
            const seed = `${prevHash}:${nextSeq}:${newItem.action}:${newItem.inspection_id || ''}:${JSON.stringify(newItem.details || {})}:${newItem.created_at}`;
            newItem.sequence_num = nextSeq;
            newItem.prev_hash = prevHash;
            newItem.curr_hash = computeSha256(seed);
          }

          insertedItems.push(newItem);
        }

        const current = store[tableKey] || [];
        store[tableKey] = [...insertedItems, ...current];
        saveStoredTable(tableKey, store[tableKey]);"""

if old_insert in sb:
    sb = sb.replace(old_insert, new_insert)

# Block UPDATE and DELETE on audit_log and evidence_artifacts in mock query builder
old_update = """      update(updates: any) {
        return {
          eq(column: string, val: any) {
            const current = store[tableKey] || [];
            store[tableKey] = current.map((row) => (row[column] === val ? { ...row, ...updates } : row));
            saveStoredTable(tableKey, store[tableKey]);
            return Promise.resolve({ data: null, error: null });
          },
        };
      },"""

new_update = """      update(updates: any) {
        if (tableKey === 'audit_log' || tableKey === 'evidence_artifacts') {
          return {
            eq() {
              return Promise.reject(new Error(`Permission denied: table '${tableKey}' is strictly append-only.`));
            }
          };
        }
        return {
          eq(column: string, val: any) {
            const current = store[tableKey] || [];
            store[tableKey] = current.map((row) => (row[column] === val ? { ...row, ...updates } : row));
            saveStoredTable(tableKey, store[tableKey]);
            return Promise.resolve({ data: null, error: null });
          },
        };
      },"""

if old_update in sb:
    sb = sb.replace(old_update, new_update)

old_delete = """      delete() {
        return {
          eq(column: string, val: any) {
            const current = store[tableKey] || [];
            store[tableKey] = current.filter((row) => row[column] !== val);
            saveStoredTable(tableKey, store[tableKey]);
            return Promise.resolve({ data: null, error: null });
          },
        };
      },"""

new_delete = """      delete() {
        if (tableKey === 'audit_log' || tableKey === 'evidence_artifacts') {
          return {
            eq() {
              return Promise.reject(new Error(`Permission denied: table '${tableKey}' is strictly append-only.`));
            }
          };
        }
        return {
          eq(column: string, val: any) {
            const current = store[tableKey] || [];
            store[tableKey] = current.filter((row) => row[column] !== val);
            saveStoredTable(tableKey, store[tableKey]);
            return Promise.resolve({ data: null, error: null });
          },
        };
      },"""

if old_delete in sb:
    sb = sb.replace(old_delete, new_delete)

with open('SIHB/src/lib/supabase.ts', 'w', encoding='utf-8') as f:
    f.write(sb)
print("Updated supabase.ts successfully")
