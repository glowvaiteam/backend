def build_report(predictions: dict):
    return {
        "portrait_score": predictions["portrait_score"],
        "snapshot_overview": snapshot_overview(predictions),
        "feature_analysis": feature_analysis(predictions),
        "skin_concerns": skin_concerns(predictions),
        "personalized_recommendations": recommendations(predictions),
        "recommended_products": products(predictions),
    }


# --------------------------------------------------
# SNAPSHOT OVERVIEW
# --------------------------------------------------
def snapshot_overview(p):
    return {
        "skin_tone": p["skin_tone"],
        "skin_type": p["skin_type"],
        "acne_level": acne_label(p["acne_severity"]),
        "dark_spots": dark_spots_label(p["dark_spots"]),
        "texture_quality": clarity_label(p["skin_clarity"]),
    }


# --------------------------------------------------
# FEATURE ANALYSIS
# --------------------------------------------------
def feature_analysis(p):
    return {
        "eyes": score_label(p["eyes"]),
        "eyebrows": score_label(p["eyebrows"]),
        "nose": score_label(p["nose"]),
        "lips": score_label(p["lips"]),
        "jawline": score_label(p["jawline"]),
        "cheekbones": score_label(p["cheekbones"]),
    }


# --------------------------------------------------
# SKIN CONCERNS
# --------------------------------------------------
def skin_concerns(p):
    return {
        "acne": acne_label(p["acne_severity"]),
        "dark_spots": dark_spots_label(p["dark_spots"]),
        "skin_clarity": clarity_label(p["skin_clarity"]),
    }


# --------------------------------------------------
# RECOMMENDATIONS (TEXT)
# --------------------------------------------------
def recommendations(p):
    recs = []

    if p["acne_severity"] >= 3:
        recs.append("Use a gentle salicylic acid cleanser daily")

    if p["dark_spots"] >= 3:
        recs.append("Add niacinamide or vitamin C serum to your routine")

    if p["skin_type"] in ["Dry", "Combination"]:
        recs.append("Use a lightweight hydrating moisturizer")

    if p["skin_type"] == "Oily":
        recs.append("Use oil-free and non-comedogenic products")

    recs.append("Always apply SPF 30+ sunscreen during the day")

    return recs


# --------------------------------------------------
# PRODUCT SUGGESTIONS (LOGIC ONLY)
# --------------------------------------------------
def products(p):
    items = []

    if p["acne_severity"] >= 3:
        items.append("Salicylic Acid Cleanser")

    if p["dark_spots"] >= 3:
        items.append("Vitamin C Serum")

    if p["skin_type"] in ["Dry", "Combination"]:
        items.append("Hydrating Moisturizer")

    if p["skin_type"] == "Oily":
        items.append("Oil Control Gel")

    items.append("Broad Spectrum Sunscreen SPF 50")

    return items


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def score_label(value):
    if value >= 8:
        return "Excellent"
    if value >= 6:
        return "Good"
    if value >= 4:
        return "Average"
    return "Needs Improvement"


def acne_label(value):
    if value == 0:
        return "Clear"
    if value <= 2:
        return "Mild"
    if value <= 4:
        return "Moderate"
    return "Severe"


def dark_spots_label(value):
    if value <= 1:
        return "None"
    if value <= 3:
        return "Light"
    return "Visible"


def clarity_label(value):
    if value >= 8:
        return "Very Clear"
    if value >= 6:
        return "Good"
    if value >= 4:
        return "Average"
    return "Uneven"
