"""ISO 27001 Security Control Risk Assessment - Streamlit UI.

A small portfolio project. Single page with a simple dashboard on top
and an editable security control assessment below.
"""

import pandas as pd
import streamlit as st

import controls
import risk


STATUS_COLORS = {
    "Implemented": "#3db562",
    "Partially Implemented": "#e0a63a",
    "Not Implemented": "#e05c5c",
    "Not Assessed": "#8a8f98",
    "Not Applicable": "#8a8f98",
}

SEVERITY_COLORS = {
    "Low": "#3db562",
    "Medium": "#e6c947",
    "High": "#e0a63a",
    "Critical": "#e05c5c",
}


def badge(text, color):
    st.markdown(
        f'<span style="display:inline-block;padding:2px 10px;'
        f'border-radius:12px;background:{color}22;color:{color};'
        f"font-weight:600;font-size:0.85em;\">{text}</span>",
        unsafe_allow_html=True,
    )


def build_assessment():
    """Build the current assessment list, preferring widget state."""
    assessed = []
    for c in controls.CONTROLS:
        assessed.append(
            {
                **c,
                "status": st.session_state.get(f"status_{c['id']}", c["status"]),
                "likelihood": st.session_state.get(
                    f"likelihood_{c['id']}", c["likelihood"]
                ),
                "impact": st.session_state.get(f"impact_{c['id']}", c["impact"]),
            }
        )
    return assessed


def risk_row(control):
    score = risk.calculate_risk_score(control["likelihood"], control["impact"])
    severity = risk.get_risk_severity(score)
    return score, severity


def assessment_table(assessment):
    rows = []
    for c in assessment:
        score, severity = risk_row(c)
        rows.append(
            {
                "ID": c["id"],
                "Control": c["name"],
                "Category": c["category"],
                "Status": c["status"],
                "Likelihood": c["likelihood"],
                "Impact": c["impact"],
                "Risk Score": score,
                "Severity": severity,
            }
        )
    return pd.DataFrame(rows)


def render_dashboard(assessment):
    st.subheader("Dashboard")

    score, assessed_count = risk.calculate_internal_assessment_score(assessment)
    severities = risk.count_severities(assessment)
    statuses = risk.count_statuses(assessment, controls.IMPLEMENTATION_STATUSES)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Internal Assessment Score", f"{score:.1f}%")
    m2.metric("Controls Assessed", f"{assessed_count} / {len(assessment)}")
    m3.metric("High Risks", severities["High"])
    m4.metric("Critical Risks", severities["Critical"])

    st.progress(min(score, 100.0) / 100)
    st.caption(
        "Project-defined assessment metric; not an official ISO/IEC 27001 "
        "scoring method."
    )
    st.caption(
        "Risk score = Likelihood x Impact (1-5 each). Severity bands: "
        "1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical. This simplified "
        "risk model is defined by the project, not by ISO 27001."
    )

    left, right = st.columns(2)

    def summary_row(label, count, color):
        parts = st.columns([3, 2])
        parts[0].markdown(
            f'<span style="color:{color};font-weight:600;">{label}</span>',
            unsafe_allow_html=True,
        )
        parts[1].markdown(f"**{count}** control(s)")
        st.progress(count / len(assessment))

    with left:
        st.markdown("**Control Status Summary**")
        for status in controls.IMPLEMENTATION_STATUSES:
            summary_row(status, statuses[status], STATUS_COLORS[status])

    with right:
        st.markdown("**Risk Summary**")
        for severity in risk.RISK_SCORING:
            summary_row(severity, severities[severity], SEVERITY_COLORS[severity])

    st.bar_chart(
        pd.DataFrame(
            {
                "Controls": list(severities.values()),
            },
            index=list(severities.keys()),
        )
    )


def render_controls(assessment):
    st.subheader("Security Control Assessment")
    st.caption("Demo / Simulated Data - editable. Select a status and 1-5 values for each control.")

    table = assessment_table(assessment)
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={"Control": st.column_config.TextColumn(width="large")},
    )

    for c in assessment:
        key = c["id"]
        with st.expander(f"{key} - {c['name']}"):
            st.caption(f"Category: {c['category']}")
            st.markdown(f"*Evidence:* {c['evidence']}")

            col_s, col_l, col_i = st.columns([2, 1, 1])
            status = col_s.selectbox(
                "Implementation status",
                controls.IMPLEMENTATION_STATUSES,
                index=controls.IMPLEMENTATION_STATUSES.index(c["status"]),
                key=f"status_{key}",
            )
            likelihood = col_l.select_slider(
                "Likelihood",
                options=[1, 2, 3, 4, 5],
                value=c["likelihood"],
                key=f"likelihood_{key}",
            )
            impact = col_i.select_slider(
                "Impact",
                options=[1, 2, 3, 4, 5],
                value=c["impact"],
                key=f"impact_{key}",
            )

            score = risk.calculate_risk_score(likelihood, impact)
            severity = risk.get_risk_severity(score)
            status_score = risk.STATUS_SCORES.get(status)

            col_r, col_v, col_s2 = st.columns(3)
            col_r.metric("Risk Score", score)
            col_v.metric("Severity", severity)
            col_s2.metric(
                "Status Score",
                f"{status_score} / 100" if status_score is not None else "Excluded",
            )

            parts = st.columns(3)
            with parts[1]:
                badge(severity, SEVERITY_COLORS[severity])


def main():
    st.set_page_config(
        page_title="ISO 27001 Security Control Risk Assessment",
        page_icon=":shield:",
        layout="wide",
    )

    st.title("ISO 27001 Security Control Risk Assessment")
    st.markdown("**Internal Control Assessment**")
    st.caption(
        "This is a portfolio project using selected ISO/IEC 27001:2022 Annex A "
        "controls and simulated data. It is not an ISO certification or audit tool."
    )
    st.divider()

    assessment = build_assessment()
    render_dashboard(assessment)

    st.divider()
    render_controls(assessment)


main()