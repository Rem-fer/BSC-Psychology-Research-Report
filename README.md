# BSc Psychology Research Project — Redeployment

Reanalysis and redeployment of a BSc Psychology research project investigating the relationship between **trait mindfulness**, **inhibitory control**, and **phone checking frequency**.

Originally conducted using Qualtrics and PsychoPy, this project redeploys the full pipeline in Python with an interactive Streamlit dashboard and AI-powered chatbot.

🔗 **Live Demo:** *(coming soon)*

---

## Research Overview

**Title:** Exploring the Relationship Between Trait Mindfulness, Inhibition, and Phone Checking Frequency

**Hypotheses:**
- H1: Trait mindfulness (MAAS) will predict phone checking frequency
- H2: Inhibitory control (Go/No-Go) will predict phone checking frequency
- H3: Trait mindfulness will predict inhibitory control

**Key Finding:** H3 was the only supported hypothesis — higher trait mindfulness significantly predicted better inhibitory control (R² = 0.147, p = .040).

---

## Project Structure

```
├── dashboard.py              # Streamlit app
├── analysis.py               # Statistical analysis functions
├── llm.py                    # LiteLLM chatbot with tool use
├── getinhibition_score.py    # PsychoPy CSV processing pipeline
├── content/
│   ├── study_summary.txt     # Study background and methodology
│   ├── conclusions.txt       # Hypothesis outcomes and conclusions
│   └── results.json          # Regression and descriptive stats results
├── data/
│   └── study_data_anonymised.csv  # Anonymised merged dataset
├── notebooks/
│   ├── qualtrics_cleaning.ipynb   # Qualtrics data cleaning
│   └── analysis.ipynb             # Statistical analysis notebook
├── .streamlit/
│   └── config.toml           # Theme configuration
└── requirements.txt
```

---

## Features

**Dashboard**
- Study overview and hypotheses
- Sample demographics (gender, age, device breakdown)
- Descriptive statistics and normality checks (Shapiro-Wilk)
- Distribution plots (histograms and boxplots)
- Multiple and simple regression results with scatter plots

**PsychoPy Processing Pipeline**
- Automated batch processing of raw PsychoPy CSVs
- Calculates inhibition scores (correct No-Go responses) for all participants
- Replaces original manual Excel-based scoring

**AI Chatbot**
- Powered by Claude via LiteLLM
- Three tools: study summary, results, and conclusions
- Answers questions about methodology, findings, and limitations

---

## Tech Stack

Python • Streamlit • Pandas • Statsmodels • Scipy • Plotly • LiteLLM • Anthropic Claude API

---

## Data & Privacy

Raw participant data is not included in this repository. Only anonymised, aggregated data is used in the dashboard. All participant IDs have been removed prior to deployment.

---

## Original Study

- **Institution:** University of Derby
- **Degree:** BSc Psychology (2:1)
- **Year:** 2024
- **Tools:** Qualtrics, PsychoPy, Pavlovia, SPSS

---

*Created by Remy Fernando — MSc Cognitive Science & AI applicant*
