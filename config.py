"""Audit configuration: the buyer jobs Arcessio's agents do, and where engineers talk about them."""

# Arcessio reads a drawing or CAD model and returns a manufacturing decision:
# process, material, supplier, price. Each theme is one of those decisions.
THEMES = {
    "quoting_from_drawings": ["quote", "quoting", "rfq", "price a part", "pricing", "cost estimate", "how much"],
    "process_selection": ["cnc vs", "3d print vs", "vs injection", "vs machining", "which process", "sheet metal vs", "casting vs"],
    "design_for_manufacturing": ["dfm", "manufacturability", "design for manufacturing", "tolerance", "gd&t", "undercut"],
    "material_selection": ["material", "aluminum vs", "6061", "which plastic", "steel vs"],
    "finding_suppliers": ["supplier", "machine shop", "vendor", "manufacturer for", "where to get", "outsourc"],
    "files_for_manufacturing": ["step file", "drawing for", "technical drawing", "send to machine shop", "cad file", "2d drawing"],
    "lead_time": ["lead time", "turnaround", "how long does"],
}

# Seeds expanded through Google autocomplete (real queries people type).
SUGGEST_SEEDS = [
    "how to get a quote for cnc parts", "cnc machining quote", "sheet metal quote",
    "how much does cnc machining cost", "cnc vs 3d printing", "injection molding vs 3d printing",
    "design for manufacturing checklist", "dfm analysis", "tolerance cost machining",
    "best material for machined parts", "how to find a machine shop", "how to find a manufacturer for a part",
    "how to send a drawing to a machine shop", "step file vs drawing", "cnc machining lead time",
    "ai for manufacturing quoting", "ai cad to quote",
]

SUBREDDITS = ["machining", "manufacturing", "engineering", "mechanicalengineering",
              "SolidWorks", "3Dprinting", "CNC", "sheetmetal"]
REDDIT_TITLE_TERMS = ["quote", "DFM", "manufacturability", "machine shop", "supplier",
                      "tolerance", "material", "lead time"]
REDDIT_AFTER = "2024-01-01"

BRAND = {"name": "Arcessio", "domains": ["arcessio.ai", "arcessio.com", "accio3d"]}
QUESTIONS_PER_THEME_FOR_AI = 2
