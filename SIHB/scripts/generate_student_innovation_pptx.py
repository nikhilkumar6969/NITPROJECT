import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Palette (Student Innovation - Health, AI, Consumer Safety)
    COLOR_BG_DARK = RGBColor(11, 19, 43)        # #0B132B Deep Midnight Navy
    COLOR_BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC Slate 50
    COLOR_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    COLOR_CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0 Slate 200

    COLOR_EMERALD = RGBColor(16, 185, 129)      # #10B981 Emerald 500
    COLOR_TEAL = RGBColor(13, 148, 136)         # #0D9488 Teal 600
    COLOR_BLUE = RGBColor(37, 99, 235)          # #2563EB Blue 600
    COLOR_PURPLE = RGBColor(124, 58, 237)       # #7C3AED Purple 600
    COLOR_AMBER = RGBColor(217, 119, 6)         # #D97706 Amber 600
    COLOR_ROSE = RGBColor(225, 29, 72)          # #E11D48 Rose 600
    
    COLOR_TEXT_DARK = RGBColor(15, 23, 42)      # Slate 900
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105)    # Slate 600
    COLOR_TEXT_LIGHT = RGBColor(241, 245, 249)  # Slate 100
    COLOR_TEXT_SUBTLE = RGBColor(148, 163, 184) # Slate 400

    FONT_MAIN = "Arial"
    FONT_HEADING = "Arial"

    def add_header(slide, title, category="SMART INDIA HACKATHON 2026 | STUDENT INNOVATION"):
        # Header category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        p.font.name = FONT_MAIN

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_DARK
        p.font.name = FONT_HEADING

    def add_footer(slide, current_page, total_pages=8):
        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.color.rgb = COLOR_CARD_BORDER

        # Footer Text
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(10.0), Inches(0.3))
        tf = footer_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "SIH 2026 | Student Innovation Track | Team: NEW COMERS (ID: 1111) | NutriLenz AI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.font.name = FONT_MAIN

        # Page Number
        page_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.0), Inches(1.0), Inches(0.3))
        tf = page_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        p.text = f"{current_page} / {total_pages}"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        p.font.name = FONT_MAIN

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: TITLE & PROJECT INTRODUCTION
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, COLOR_BG_DARK)

    # Decorative header shape
    dec_shape = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(1.2), Inches(0.06))
    dec_shape.fill.solid()
    dec_shape.fill.fore_color.rgb = COLOR_EMERALD
    dec_shape.line.fill.background()

    # Title & Subtitle Container
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.7), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "NUTRILENZ AI"
    p0.font.size = Pt(40)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEXT_LIGHT
    p0.font.name = FONT_HEADING

    p1 = tf.add_paragraph()
    p1.text = "Intelligent Packaging Transparency, Hidden Ingredient Decoder & Deceptive Marketing Shield"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_EMERALD
    p1.font.name = FONT_MAIN
    p1.space_before = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Empowering consumers with real-time OCR and edge vision to uncover deceptive health claims ('Zero Sugar', '100% Natural'), calculate true NOVA ultra-processing scores, and expose fine-print allergens."
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_SUBTLE
    p2.font.name = FONT_MAIN
    p2.space_before = Pt(10)

    # Card 1: Student Innovation Metadata
    card1 = add_card(slide1, 0.8, 3.7, 5.7, 2.8, bg_color=RGBColor(20, 32, 58), border_color=RGBColor(38, 56, 96))
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(3.9), Inches(5.3), Inches(2.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "STUDENT INNOVATION DETAILS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    items1 = [
        ("Competition:", " Smart India Hackathon (SIH) 2026"),
        ("Track / Category:", " Student Innovation (Software Edition)"),
        ("Innovation Theme:", " MedTech / Healthcare / Consumer Tech & Smart Automation"),
        ("Project Scope:", " AI-Driven Food & Cosmetic Label Intelligence & Health Protection")
    ]
    for label, val in items1:
        p = tf1.add_paragraph()
        p.space_before = Pt(6)
        run1 = p.add_run()
        run1.text = label
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_TEXT_LIGHT
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(10)
        run2.font.color.rgb = COLOR_TEXT_SUBTLE

    # Card 2: Team Details
    card2 = add_card(slide1, 6.8, 3.7, 5.7, 2.8, bg_color=RGBColor(20, 32, 58), border_color=RGBColor(38, 56, 96))
    tb2 = slide1.shapes.add_textbox(Inches(7.0), Inches(3.9), Inches(5.3), Inches(2.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "TEAM & ARCHITECTURE OVERVIEW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    items2 = [
        ("Team Name:", " NEW COMERS"),
        ("Team ID:", " 1111 (Registered on SIH Portal)"),
        ("Core Stack:", " React 18, FastAPI, RapidOCR (ONNX), OpenCV, Supabase"),
        ("Novelty Focus:", " Zero-Barcode OCR, Front-vs-Back Discrepancy Matrix, Contrast Audit"),
        ("Target Users:", " Diabetic/Allergy Patients, Conscious Consumers, Public Health Watchdogs")
    ]
    for label, val in items2:
        p = tf2.add_paragraph()
        p.space_before = Pt(6)
        run1 = p.add_run()
        run1.text = label
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_TEXT_LIGHT
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(10)
        run2.font.color.rgb = COLOR_TEXT_SUBTLE

    # Footer for Slide 1
    f_box = slide1.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.3))
    tf = f_box.text_frame
    p = tf.paragraphs[0]
    p.text = "STUDENT INNOVATION TRACK — CONFIDENTIAL & PROPRIETARY EVALUATION DECK"
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_SUBTLE

    # ==========================================
    # SLIDE 2: REAL-WORLD PROBLEM & INNOVATION GAP
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, COLOR_BG_LIGHT)
    add_header(slide2, "THE REAL-WORLD CRISIS & THE INNOVATION GAP")
    add_footer(slide2, 2)

    # Left Column: The Consumer Problem
    add_card(slide2, 0.8, 1.4, 5.6, 5.3)
    tb_p = slide2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "THE CRISIS IN PACKAGED FOOD TRANSPARENCY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE

    prob_points = [
        ("Predatory Health Washing: ", "80%+ of ultra-processed packaged snacks claim 'Zero Added Sugar', '100% Real Fruit', or 'High Protein' on the front, while hiding toxic sweeteners and fillers on the back."),
        ("Hidden Sugars with 50+ Names: ", "Brands use Maltodextrin, Invert Syrup, Corn Syrup Solids, and Dextrose to deceive diabetic and health-conscious consumers."),
        ("Microscopic Allergen Concealment: ", "Crucial allergen warnings (nuts, gluten, milk, soy) and sodium counts are printed in sub-1.2mm faint grey fonts on shiny reflective packaging."),
        ("Quick-Commerce Information Asymmetry: ", "Apps like Blinkit, Zepto, and Instamart show attractive promotional banners while hiding full ingredient lists and nutritional tables."),
        ("Lifestyle Disease Epidemic: ", "Childhood obesity, early-onset Type 2 Diabetes, and hypertension are skyrocketing due to uninformed consumption of ultra-processed food.")
    ]
    for title, desc in prob_points:
        p = tf_p.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = title
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_TEXT_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: The Innovation Gap & Why Old Solutions Fail
    add_card(slide2, 6.8, 1.4, 5.7, 5.3)
    tb_s = slide2.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "WHY CURRENT SOLUTIONS FAIL & OUR INNOVATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    sol_points = [
        ("Barcode Apps Are Broken: ", "Apps like Yuka or OpenFoodFacts rely on pre-existing static barcodes. If a brand changes ingredients or a local/fresh item is scanned, barcode apps fail completely."),
        ("Zero-Barcode Edge Vision: ", "NutriLenz AI runs optical character recognition directly on the physical packaging or screenshot. It works on ANY item—fresh, local, unlisted, or imported."),
        ("Front-vs-Back Discrepancy Matrix: ", "First system to cross-reference front-of-pack claims ('Low Fat', 'Immunity Booster') against back-of-pack ingredient realities to flag deception."),
        ("Mathematical Legibility Auditing: ", "Computer vision calculates font height in millimeters and WCAG luminance contrast to catch intentionally obscured warnings."),
        ("One-Click Consumer Grievance: ", "Generates official evidence dossiers ready to submit to the National Consumer Helpline (NCH) or Food Safety Authorities.")
    ]
    for title, desc in sol_points:
        p = tf_s.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = title
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_TEXT_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 3: UNIQUE VALUE PROPOSITION & NOVELTY
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, COLOR_BG_LIGHT)
    add_header(slide3, "UNIQUE VALUE PROPOSITION & TECHNICAL NOVELTY")
    add_footer(slide3, 3)

    uvp_cards = [
        ("Front-vs-Back Claim Discrepancy Matrix", 
         "Novel NLP rule engine that correlates bold marketing buzzwords on the front label with actual nutritional panels on the reverse, instantly exposing greenwashing and deceptive claims.", 
         COLOR_EMERALD, 0.8, 1.4, 5.6, 2.5),
        
        ("Sub-2.3s Edge Vision & Zero Barcode Dependency", 
         "Built on lightweight RapidOCR (PP-OCRv4 ONNX) with automated 4-way rotation detection. Operates reliably on crushed, curved, or reflective packaging without requiring any pre-cataloged barcode database.", 
         COLOR_TEAL, 6.8, 1.4, 5.7, 2.5),
        
        ("Algorithmic Legibility & Contrast Auditing", 
         "Calculates pixel font heights in physical millimeters against statutory baselines and performs off-screen WCAG luminance sampling to flag intentionally concealed warning labels and allergens.", 
         COLOR_PURPLE, 0.8, 4.2, 5.6, 2.5),
        
        ("Actionable Consumer Dossier & Whistleblower Tool", 
         "Transforms confusing raw data into an intuitive 'Truth Score' for consumers, while generating verifiable PDF/DOCX grievance dossiers with photo evidence for regulatory filing.", 
         COLOR_AMBER, 6.8, 4.2, 5.7, 2.5)
    ]

    for title, desc, color, x, y, w, h in uvp_cards:
        add_card(slide3, x, y, w, h)
        bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.12), Inches(h))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = slide3.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.2), Inches(w - 0.5), Inches(h - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.space_before = Pt(6)
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 4: SYSTEM ARCHITECTURE & DATA FLOW
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, COLOR_BG_LIGHT)
    add_header(slide4, "SYSTEM ARCHITECTURE & MULTI-MODAL PIPELINE")
    add_footer(slide4, 4)

    arch_layers = [
        ("1. INGESTION LAYER", ["Dual-Angle Camera Capture", "Gallery / PDF Upload", "Quick-Commerce PDP Scraper", "Contrast & Blur Quality Check"], COLOR_BLUE, 0.8),
        ("2. VISION & OCR PIPELINE", ["RapidOCR (PP-OCRv4 DBNet)", "ONNX Inference Engine", "Smart 4-Way Rotation Invariance", "Spatial Word Bounding Boxes"], COLOR_TEAL, 3.8),
        ("3. HEALTH TRUTH ENGINE", ["Discrepancy Matrix (Claim vs Real)", "NOVA Ultra-Processed Classifier", "Allergen & High-Sodium Radar", "Font Height & Contrast Evaluator"], COLOR_PURPLE, 6.8),
        ("4. CONSUMER ACTION LAYER", ["Interactive Truth Scorecard", "Diabetic / Allergy Alerts", "E-Commerce Transparency Flag", "One-Click NCH Complaint Dossier"], COLOR_AMBER, 9.8)
    ]

    for title, items, color, x in arch_layers:
        add_card(slide4, x, 1.4, 2.7, 4.3)
        header_shape = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.4), Inches(2.7), Inches(0.5))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = color
        header_shape.line.fill.background()

        tb_h = slide4.shapes.add_textbox(Inches(x + 0.1), Inches(1.45), Inches(2.5), Inches(0.4))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_BG

        tb_c = slide4.shapes.add_textbox(Inches(x + 0.2), Inches(2.0), Inches(2.3), Inches(3.6))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        for idx, item in enumerate(items):
            p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
            if idx > 0:
                p.space_before = Pt(8)
            p.text = f"•  {item}"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_DARK

    # Bottom Data Flow Bar
    add_card(slide4, 0.8, 5.9, 11.7, 0.8, bg_color=RGBColor(241, 245, 249), border_color=COLOR_TEAL)
    tb_df = slide4.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.7))
    tf_df = tb_df.text_frame
    tf_df.word_wrap = True

    p = tf_df.paragraphs[0]
    p.text = "DATA PERSISTENCE & PRIVACY ARCHITECTURE:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p2 = tf_df.add_paragraph()
    p2.text = "Supabase PostgreSQL Database (Row-Level Security)  ↔  Client-Side Encryption for Personal Health Profiles  ↔  Local Mock Mode for Zero-Network Offline Edge Scanning"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(2)

    # ==========================================
    # SLIDE 5: TECHNICAL WORKFLOW & STACK IMPLEMENTATION
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, COLOR_BG_LIGHT)
    add_header(slide5, "TECHNICAL WORKFLOW & VERIFIED TECH STACK")
    add_footer(slide5, 5)

    # Left Box: 6-Step Processing Pipeline
    add_card(slide5, 0.8, 1.4, 6.2, 5.3)
    tb_wf = slide5.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.8), Inches(4.9))
    tf_wf = tb_wf.text_frame
    tf_wf.word_wrap = True

    p = tf_wf.paragraphs[0]
    p.text = "6-STEP END-TO-END PROCESSING PIPELINE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    steps = [
        ("Step 1: Multi-Angle Scan & Preprocessing", "Dual-angle capture (Front & Back) or screenshot upload; automated blur and resolution verification."),
        ("Step 2: RapidOCR ONNX Text Extraction", "FastAPI microservice executing PP-OCRv4 with smart orientation alignment, extracting spatial bounding coordinates in <2.3s."),
        ("Step 3: Nutritional & Ingredient Parsing", "Extracts nutritional tables (sugar, sodium, trans fats, protein) and ingredients with chemical synonym normalization (e.g. Maltodextrin, INS 621)."),
        ("Step 4: Claim vs. Ingredient Discrepancy Matrix", "Cross-evaluates front-label claims against back ingredients; flags deceptive claims (e.g., 'No Added Sugar' containing fruit concentrate)."),
        ("Step 5: Legibility & Visual Contrast Audit", "Measures text pixel height against millimeter scale and runs WCAG luminance sampling to detect intentionally obscured warnings."),
        ("Step 6: Consumer Scorecard & Dossier Export", "Renders intuitive Truth Scorecard and generates downloadable PDF / DOCX complaint reports with embedded evidence.")
    ]
    for title, desc in steps:
        p = tf_wf.add_paragraph()
        p.space_before = Pt(6)
        run1 = p.add_run()
        run1.text = title + " — "
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_TEXT_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(9)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # Right Box: Complete Technology Stack
    add_card(slide5, 7.3, 1.4, 5.2, 5.3)
    tb_st = slide5.shapes.add_textbox(Inches(7.5), Inches(1.6), Inches(4.8), Inches(4.9))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    p = tf_st.paragraphs[0]
    p.text = "ROBUST OPEN-SOURCE TECH STACK"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    stack_items = [
        ("Frontend Application:", " React 18, TypeScript, Vite, Tailwind CSS"),
        ("Visual Analytics & UI:", " Lucide React, Recharts dynamic gauges & radar"),
        ("Computer Vision Backend:", " FastAPI (Python 3.11/3.12), RapidOCR"),
        ("Edge Inference Runtime:", " ONNX Runtime, OpenCV, PIL, NumPy"),
        ("Data, Auth & Storage:", " Supabase (PostgreSQL, RLS) + Local Edge Container"),
        ("Document Generation:", " jsPDF & AutoTable (PDF), docx.js (.docx notices)"),
        ("Regulatory Knowledgebase:", " WHO Nutrient Profiling & ICMR Dietary Norms 2024")
    ]
    for label, val in stack_items:
        p = tf_st.add_paragraph()
        p.space_before = Pt(7)
        run1 = p.add_run()
        run1.text = label
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_TEXT_DARK
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 6: FEASIBILITY, VIABILITY & SUSTAINABILITY
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, COLOR_BG_LIGHT)
    add_header(slide6, "FEASIBILITY, BUSINESS VIABILITY & SUSTAINABILITY")
    add_footer(slide6, 6)

    card_data = [
        ("TECHNICAL FEASIBILITY", COLOR_EMERALD, [
            ("Proven Lightweight Models: ", "PaddleOCR / RapidOCR runs smoothly on edge devices and standard cloud CPU instances without costly proprietary vision APIs."),
            ("Zero Barcode Dependency: ", "Functions effortlessly on physical products, unpackaged local artisan foods, and unindexed quick-commerce items."),
            ("Modular Rule Architecture: ", "Easily expands beyond food to cosmetics (parabens, sulfates) and personal care with simple JSON configuration updates.")
        ], 0.8, 1.4, 3.6, 5.3),

        ("BUSINESS VIABILITY & REVENUE", COLOR_TEAL, [
            ("B2C Freemium Model: ", "Free transparency scanner for consumers; premium tier with personalized chronic disease filters and family health lockers."),
            ("B2B Clean-Label SaaS: ", "Sold to ethical D2C food brands to pre-audit packaging artwork and avert costly recalls before mass printing."),
            ("Research & NGO Data Licensing: ", "Anonymized market deception trend analytics licensed to food research institutions and consumer rights bodies.")
        ], 4.8, 1.4, 3.7, 5.3),

        ("ETHICAL & OPERATIONAL SAFETY", COLOR_AMBER, [
            ("Objective Algorithmic Basis: ", "Transparent rule engine grounded in ICMR, WHO, and FSSAI statutory definitions—eliminates black-box AI bias."),
            ("Consumer Privacy by Design: ", "Personal dietary profiles and medical sensitivities stored locally or encrypted under Supabase Row-Level Security."),
            ("Responsible Whistleblowing: ", "Generates structured evidence files for verified consumer grievance submission rather than unverified public claims.")
        ], 8.8, 1.4, 3.7, 5.3)
    ]

    for title, color, items, x, y, w, h in card_data:
        add_card(slide6, x, y, w, h)
        bar = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb_h = slide6.shapes.add_textbox(Inches(x + 0.1), Inches(y + 0.05), Inches(w - 0.2), Inches(0.35))
        tf_h = tb_h.text_frame
        p = tf_h.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_BG

        tb_c = slide6.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.5), Inches(w - 0.4), Inches(h - 0.6))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        for idx, (head, desc) in enumerate(items):
            p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
            if idx > 0:
                p.space_before = Pt(8)
            run1 = p.add_run()
            run1.text = head + " "
            run1.font.bold = True
            run1.font.size = Pt(9)
            run1.font.color.rgb = COLOR_TEXT_DARK
            run2 = p.add_run()
            run2.text = desc
            run2.font.size = Pt(8.5)
            run2.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 7: IMPACT, USER BENEFITS & ROADMAP
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, COLOR_BG_LIGHT)
    add_header(slide7, "SOCIAL IMPACT, USER BENEFITS & FUTURE ROADMAP")
    add_footer(slide7, 7)

    impact_items = [
        ("COMBATING LIFESTYLE DISEASES", "Protects millions of pre-diabetic, hypertensive, and allergy patients by instantly decoding hidden chemical and sugar formulations.", COLOR_EMERALD, 0.8, 1.4, 3.6, 2.4),
        ("STOPPING FMCG GREENWASHING", "Dismantles misleading marketing ('Zero Added Sugar', 'Immunity Booster') by exposing reality in 3 seconds.", COLOR_TEAL, 4.8, 1.4, 3.7, 2.4),
        ("QUICK-COMMERCE TRANSPARENCY", "Eliminates digital dark patterns across Zepto, Blinkit, and Amazon grocery listings with automated PDP compliance scans.", COLOR_PURPLE, 8.8, 1.4, 3.7, 2.4)
    ]

    for title, desc, color, x, y, w, h in impact_items:
        add_card(slide7, x, y, w, h)
        bar = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.12), Inches(h))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = slide7.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.2), Inches(w - 0.4), Inches(h - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.space_before = Pt(6)
        p2.font.size = Pt(9)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Container: Future Development Roadmap
    add_card(slide7, 0.8, 4.1, 11.7, 2.6)
    tb_rm = slide7.shapes.add_textbox(Inches(1.0), Inches(4.25), Inches(11.3), Inches(2.3))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True

    p = tf_rm.paragraphs[0]
    p.text = "STRATEGIC FUTURE DEVELOPMENT ROADMAP"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    roadmap_points = [
        ("Phase 1 — Vernacular Voice & Dialect Translation: ", "Audio readout of toxic ingredients and allergens in 10+ regional Indian languages for non-English literate consumers."),
        ("Phase 2 — Multi-Modal VLM Visual Symbol Verification: ", "Integration of lightweight visual language models to verify Veg/Non-Veg green dots, organic certifications, and recyclable symbols."),
        ("Phase 3 — Crowd-Sourced Deceptive Packaging Map: ", "Public dashboard tracking repeat offending FMCG brands and unverified health claims across Indian cities."),
        ("Phase 4 — API Integration with National Consumer Helpline: ", "Direct electronic filing of misleading advertisement complaints under the Consumer Protection Act, 2019.")
    ]
    for title, desc in roadmap_points:
        p = tf_rm.add_paragraph()
        p.space_before = Pt(5)
        run1 = p.add_run()
        run1.text = title
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_TEXT_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(9)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 8: CONCLUSION, PROTOTYPE & SCIENTIFIC RIGOR
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, COLOR_BG_DARK)

    # Title & Conclusion Header
    t_box8 = slide8.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.5))
    tf8 = t_box8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "NUTRILENZ AI: STUDENT INNOVATION READY TO DEPLOY"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_LIGHT

    p2 = tf8.add_paragraph()
    p2.text = "Bridging the gap between predatory food marketing and genuine consumer health rights through cutting-edge, explainable computer vision and edge AI."
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_EMERALD
    p2.space_before = Pt(6)

    # Card 1: Implementation Status
    card8_1 = add_card(slide8, 0.8, 2.5, 5.6, 4.0, bg_color=RGBColor(20, 32, 58), border_color=RGBColor(38, 56, 96))
    tb8_1 = slide8.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.2), Inches(3.6))
    tf8_1 = tb8_1.text_frame
    tf8_1.word_wrap = True

    p = tf8_1.paragraphs[0]
    p.text = "CURRENT OPERATIONAL PROTOTYPE STATUS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    status_items = [
        ("Full-Stack React + Vite Web App:", " 100% Operational & Responsive"),
        ("FastAPI + RapidOCR Microservice:", " Live & Tested (<2.3s inference)"),
        ("Claim vs Ingredient Engine:", " Active & Validated"),
        ("Legibility & WCAG Contrast Logic:", " Implemented with OpenCV"),
        ("PDF & DOCX Evidence Exporter:", " Functional One-Click Dossiers")
    ]
    for label, val in status_items:
        p = tf8_1.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = "✓  " + label
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_TEXT_LIGHT
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_SUBTLE

    # Card 2: Scientific & Standards Grounding
    card8_2 = add_card(slide8, 6.8, 2.5, 5.7, 4.0, bg_color=RGBColor(20, 32, 58), border_color=RGBColor(38, 56, 96))
    tb8_2 = slide8.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(3.6))
    tf8_2 = tb8_2.text_frame
    tf8_2.word_wrap = True

    p = tf8_2.paragraphs[0]
    p.text = "SCIENTIFIC & REGULATORY FOUNDATIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    ref_items = [
        ("ICMR-NIN Dietary Guidelines (2024):", " Sugar, sodium, and fat thresholds for Indian diets"),
        ("NOVA Food Classification (FAO/WHO):", " Ultra-Processed Food (UPF) categorization standards"),
        ("FSSAI Claims & Advertising Rules 2018:", " Legal parameters for 'Zero Sugar', 'Natural', and 'Organic'"),
        ("Consumer Protection Act 2019:", " Guidelines on Prevention and Regulation of Misleading Ads"),
        ("Open-Source Vision Framework:", " RapidOCR (PP-OCRv4 ONNX), OpenCV, WCAG 2.1 Contrast Norms")
    ]
    for label, val in ref_items:
        p = tf8_2.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = "•  " + label
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_TEXT_LIGHT
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(9)
        run2.font.color.rgb = COLOR_TEXT_SUBTLE

    # Footer Slide 8
    f_box8 = slide8.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.3))
    tf8_f = f_box8.text_frame
    p = tf8_f.paragraphs[0]
    p.text = "THANK YOU — TEAM NEW COMERS (ID: 1111) | SMART INDIA HACKATHON 2026 STUDENT INNOVATION"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    # Save presentation
    output_path = os.path.join(os.getcwd(), "NutriLenz_SIH_Student_Innovation_Pitch_Deck.pptx")
    prs.save(output_path)
    print(f"[+] Student Innovation PPTX successfully generated at: {output_path}")

if __name__ == "__main__":
    create_deck()
