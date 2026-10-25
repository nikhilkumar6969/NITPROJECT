import type { Product, ComplianceRule, Inspection, InspectionResult, Violation, EvidenceArtifact, AuditLogEntry } from '@/types';

export type Profile = {
  id: string;
  full_name: string;
  role: 'inspector' | 'admin';
  created_at: string;
};

export const INITIAL_RULES: ComplianceRule[] = [
  // PRESENCE RULES (LMPCR 2011 Rule 6(1))
  { id: 'rule-pr-001', rule_code: 'PR-001', title: 'Product Common / Generic Name Present', description: 'The label must clearly display the common or generic name of the commodity.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(b)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-002', rule_code: 'PR-002', title: 'Net Quantity Declaration', description: 'The package must declare net quantity of contents in standard metric units.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(c) & Rule 12', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-003', rule_code: 'PR-003', title: 'MRP Declaration', description: 'The retail sale price (Maximum Retail Price - MRP) must be printed on the label.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(e)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-004', rule_code: 'PR-004', title: 'Manufacturer / Packer / Importer Details', description: 'The complete name and physical address of the manufacturer/packer/importer must be present.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(a)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-005', rule_code: 'PR-005', title: 'Country of Origin Declaration', description: 'The country of origin or manufacture must be clearly declared on the package.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(g)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-006', rule_code: 'PR-006', title: 'Package Dimensions / Contents Specification', description: 'For applicable commodities, dimensions, composition or contents specification must be declared.', category: 'presence', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-007', rule_code: 'PR-007', title: 'Commodity Identification & Description', description: 'The nature and commercial identity of the commodity must be prominently stated.', category: 'presence', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)(b)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-008', rule_code: 'PR-008', title: 'Standard Metric Net Quantity Declaration', description: 'Net quantity must be declared using SI metric symbols without non-standard abbreviations.', category: 'presence', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 11 & Rule 12', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-009', rule_code: 'PR-009', title: 'Batch / Lot Identification Number', description: 'A batch or lot identification code for traceability must be present.', category: 'presence', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-010', rule_code: 'PR-010', title: 'Month & Year of Manufacture / Packing', description: 'The month and year in which the commodity is manufactured, packed or imported must be marked.', category: 'presence', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)(d)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pr-011', rule_code: 'PR-011', title: 'Consumer Care Details', description: 'The label must display consumer care contact name, address, telephone number, and email for complaints.', category: 'presence', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(f)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },

  // FORMAT RULES
  { id: 'rule-fr-001', rule_code: 'FR-001', title: 'Date Format Standard', description: 'Dates must indicate month and year in numbers or letters (e.g. MM/YYYY or MMM YYYY).', category: 'format', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)(d)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-fr-002', rule_code: 'FR-002', title: 'Quantity Unit Format Standard', description: 'Net quantity must use standard SI metric units (g, kg, ml, l, m, N).', category: 'format', severity: 'critical', regulation_reference: 'LM Act 2009 Sec 11 & LMPCR 2011 Rule 12', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-fr-003', rule_code: 'FR-003', title: 'MRP Prefix Standard', description: 'MRP must be prefixed with "MRP" or "Maximum Retail Price" followed by the retail amount.', category: 'format', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)(e)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-fr-004', rule_code: 'FR-004', title: 'Unit Sale Price (USP) Declaration', description: 'Unit sale price (e.g. ₹/g, ₹/kg, ₹/ml, ₹/l, ₹/N) must be declared alongside the Maximum Retail Price.', category: 'format', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(11)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-fr-005', rule_code: 'FR-005', title: 'Language & Script Standard', description: 'Mandatory declarations must be presented in Hindi in Devanagari script or English.', category: 'format', severity: 'minor', regulation_reference: 'LMPCR 2011 Rule 9(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },

  // QUANTITY RULES
  { id: 'rule-qr-001', rule_code: 'QR-001', title: 'Minimum Quantity Numeral Height', description: 'Net quantity numerals must satisfy minimum font height standards under Rule 13.', category: 'quantity', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 13, Table 1', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-qr-002', rule_code: 'QR-002', title: 'Quantity Prominence on Principal Display Panel', description: 'Net quantity declaration must be prominently displayed on the principal display panel.', category: 'quantity', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 7 & Rule 9', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-qr-003', rule_code: 'QR-003', title: 'No Non-Metric Imperial Dual Units', description: 'Quantity must not be declared in illegal non-metric units (e.g. ounces, pounds).', category: 'quantity', severity: 'critical', regulation_reference: 'LM Act 2009 Sec 11 & LMPCR 2011 Rule 12', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },

  // MRP RULES
  { id: 'rule-mr-001', rule_code: 'MR-001', title: 'MRP Not Overstamped or Altered', description: 'Maximum Retail Price must not be overwritten, altered, or masked with additional stickers.', category: 'mrp', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 18(2)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-mr-002', rule_code: 'MR-002', title: 'MRP Inclusive of All Taxes', description: 'MRP must explicitly denote that it is inclusive of all taxes.', category: 'mrp', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 6(1)(e)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-mr-003', rule_code: 'MR-003', title: 'MRP Numeral Font Size', description: 'MRP numerals and text must meet the minimum font height standards.', category: 'mrp', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 13, Table 1', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },

  // FONT RULES
  { id: 'rule-ft-001', rule_code: 'FT-001', title: 'Minimum Font Height Compliance (mm)', description: 'All mandatory text declarations must satisfy the physical font height baseline under Rule 13.', category: 'font', severity: 'critical', regulation_reference: 'LMPCR 2011 Rule 13, Table 1', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-ft-002', rule_code: 'FT-002', title: 'Visual Contrast Standard', description: 'Declarations must have high contrast against the packaging background for readability.', category: 'font', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 9(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-ft-003', rule_code: 'FT-003', title: 'Font Legibility Standard', description: 'Text must use clear, conspicuous fonts without deceptive or stylized obscuration.', category: 'font', severity: 'minor', regulation_reference: 'LMPCR 2011 Rule 9(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },

  // PLACEMENT RULES
  { id: 'rule-pl-001', rule_code: 'PL-001', title: 'Principal Display Panel Placement', description: 'Mandatory information must appear on the principal display panel of the package.', category: 'placement', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 7 & Rule 9', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pl-002', rule_code: 'PL-002', title: 'Declarations Not Obscured', description: 'Mandatory statutory text must not be obscured by artwork, graphics, or borders.', category: 'placement', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 9(1)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
  { id: 'rule-pl-003', rule_code: 'PL-003', title: 'Consumer Care Prominence', description: 'Consumer care contact details must be clearly visible and conspicuously placed.', category: 'placement', severity: 'major', regulation_reference: 'LMPCR 2011 Rule 6(1)(f)', is_active: true, created_at: '2026-01-01T00:00:00.000Z' },
];

export const INITIAL_PRODUCTS: Product[] = [
  {
    id: 'prod-mothers-pickle-400g',
    name: "Mother's Recipe Green Chilli Pickle",
    brand: "Mother's Recipe",
    category: 'Food & Beverage',
    barcode: '8906001021458',
    sku: 'MR-GCP-400G',
    description: 'Green Chilli Pickle in glass jar with statutory 9-declaration label (400g)',
    image_url: '/chilli-pickle.jpg',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z',
  },
  {
    id: 'prod-dettol-plaster-1n',
    name: 'Dettol Medicated Plaster Antiseptic Washproof',
    brand: 'Dettol',
    category: 'Healthcare & First Aid',
    barcode: '8901396342480',
    sku: 'DT-PLASTER-1N',
    description: 'Benzalkonium Chloride Medicated Plaster Strip (1.9 cm x 7.2 cm)',
    image_url: '/dettol-plaster.jpg',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z',
  },
  {
    id: 'prod-glucon-d-1kg',
    name: 'Glucon-D Instant Energy Tangy Orange',
    brand: 'Glucon-D',
    category: 'Food & Beverage',
    barcode: '8901548102123',
    sku: 'GD-ORANGE-1KG',
    description: 'Glucose based energy beverage refill pack with Unit Sale Price (1 kg)',
    image_url: '/glucon-d.jpg',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z',
  },
  {
    id: 'prod-parachute-oil-500ml',
    name: 'Parachute 100% Pure Coconut Oil',
    brand: 'Parachute',
    category: 'Personal Care',
    barcode: '8901088001047',
    sku: 'PC-COCO-500ML',
    description: '100% Pure Coconut Oil in rigid cylindrical bottle container (500 ml)',
    image_url: '/parachute-oil.jpg',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z',
  },
  {
    id: 'prod-crispy-crunchies-50g',
    name: 'Crispy Crunchies Snack Potato Chips (Violation Test Sample)',
    brand: 'Crispy Crunchies',
    category: 'Food & Beverage',
    barcode: '8901234567890',
    sku: 'CC-50G-ORIGINAL',
    description: 'Potato Chips Original Salted Flavor — Benchmark violation test pouch (missing MRP, date, packer)',
    image_url: '/samples/crispy_crunchies_pouch.png',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z',
  },
];

export const INITIAL_INSPECTIONS: Inspection[] = [];
export const INITIAL_RESULTS: InspectionResult[] = [];
export const INITIAL_VIOLATIONS: Violation[] = [];
export const INITIAL_EVIDENCE: EvidenceArtifact[] = [];
export const INITIAL_AUDIT_LOG: AuditLogEntry[] = [];

export const DEFAULT_USER_PROFILE: Profile = {
  id: 'usr-demo-001',
  full_name: 'Inspector R. Sharma',
  role: 'inspector',
  created_at: '2026-01-01T00:00:00.000Z',
};
