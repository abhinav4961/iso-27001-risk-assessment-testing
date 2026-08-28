# ISO 27001 Security Control Risk Assessment

A small cybersecurity/GRC portfolio project that walks through a simplified
security control assessment using 15 selected ISO/IEC 27001:2022 Annex A
controls.

## Project Overview

View 15 Annex A controls, assess their implementation status, review example
evidence, set likelihood/impact, and see automatically calculated risk scores,
risk severity, and an internal assessment score.

## Features

- 15 real ISO/IEC 27001:2022 Annex A controls (verified reference IDs/titles)
- Implementation status per control (Not Assessed / Implemented / Partially
  Implemented / Not Implemented / Not Applicable)
- Example evidence for each control (short, original descriptions)
- Likelihood and impact sliders (1-5) with automatic risk score and severity
- Internal Assessment Score (project-defined)
- Simple dashboard with metric cards, status summary, risk summary, and chart

## Technology

- Python 3
- Streamlit (single dependency)
- Data stored in simple Python lists/dictionaries
- No database, backend, APIs, or authentication

## ISO 27001 Approach

Only 15 selected Annex A controls are included. They are the official
2022-edition titles. Evidence strings are original summaries, not ISO text.
This is **not** a full Statement of Applicability or compliance assessment.

## Risk Calculation

Risk Score = Likelihood x Impact (each 1-5).

- 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical

This simplified model is project-defined and is not an official ISO/IEC 27001
scoring method.

## Assessment Scoring

Implemented = 100, Partially Implemented = 50, Not Implemented = 0.
Not Assessed and Not Applicable controls are excluded.

Internal Assessment Score = sum of assessed scores / number of assessed,
applicable controls. This is a project-defined metric, not an official ISO
scoring method.

## Limitations

- Data is simulated ("Demo / Simulated Data")
- Not a certification or audit tool
- No remediation tracking, findings, user accounts, or reporting
- Risk/assessment scoring is simplified

## How to Run

```
pip install -r requirements.txt
streamlit run app.py
```

The app opens locally in your browser.