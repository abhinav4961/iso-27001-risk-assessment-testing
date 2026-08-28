"""Risk and assessment calculations for the portfolio project.

Mappings and thresholds are PROJECT-DEFINED for demonstration purposes.
They are not official ISO/IEC 27001 scoring methods.
"""

RISK_SCORING = {
    "Low": (1, 4),
    "Medium": (5, 9),
    "High": (10, 16),
    "Critical": (17, 25),
}

STATUS_SCORES = {
    "Implemented": 100,
    "Partially Implemented": 50,
    "Not Implemented": 0,
}

ASSESSABLE_STATUSES = ("Implemented", "Partially Implemented", "Not Implemented")


def calculate_risk_score(likelihood, impact):
    """Project-defined risk score: likelihood (1-5) x impact (1-5)."""
    return int(likelihood) * int(impact)


def get_risk_severity(score):
    """Map a risk score to a severity label using project-defined ranges."""
    for severity, (low, high) in RISK_SCORING.items():
        if low <= score <= high:
            return severity
    return "Critical"


def calculate_internal_assessment_score(controls):
    """Internal Assessment Score (0-100) for assessed, applicable controls.

    Not Applicable and Not Assessed controls are excluded from the
    calculation. Returns the average score and the number of controls
    that were included.
    """
    assessed = [c for c in controls if c["status"] in ASSESSABLE_STATUSES]
    if not assessed:
        return 0.0, 0
    total = sum(STATUS_SCORES[c["status"]] for c in assessed)
    return round(total / len(assessed), 1), len(assessed)


def count_severities(controls):
    """Return {severity: count} across all controls."""
    counts = {s: 0 for s in RISK_SCORING}
    for control in controls:
        score = calculate_risk_score(control["likelihood"], control["impact"])
        counts[get_risk_severity(score)] += 1
    return counts


def count_statuses(controls, statuses):
    """Return {status: count} for the given status list."""
    counts = {s: 0 for s in statuses}
    for control in controls:
        counts[control["status"]] += 1
    return counts