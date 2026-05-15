# Actual Wrapped 2021-2025

Five years of personal Spotify streaming history pulled apart and actually analyzed. Goes well beyond the canned Wrapped summary: theme and energy distributions, skip behavior, and a machine-learning model trained to predict whether I will skip a song before it ends.

**55,392 plays across 2021-2025. 9,594 songs enriched with audio features for 2024.**

---

## What it covers

1. **Full-history EDA** - top songs, top artists, listening volume over time, platform and geography breakdown
2. **2024 deep-dive** - theme distributions (Romantic, Hopeful, Empowered, etc.), energy scores, daily mood patterns
3. **Skip behavior** - which themes get skipped most, skip rate vs energy correlation, played vs skipped energy gap (t-test confirms it)
4. **Skip prediction** - Random Forest, XGBoost, LightGBM, and a soft-voting ensemble. Best honest accuracy ~70-75% without data leakage. SHAP explains which features actually drive the model.
5. **Causal DAG** - manually specified directed graph of the feature relationships

---

## Repo structure

```
data/
  raw/streaming/      # Original JSON export files from Spotify (gitignored)
  processed/          # Cleaned and enriched CSVs (gitignored)

notebooks/
  01_json_to_csv.ipynb      # Converts Spotify JSON exports to a single CSV
  02_data_cleaning.ipynb    # Cleans and enriches with OpenAI (theme, language labels)
  03_merging.ipynb          # Merges audio features and playlist data
  04_analysis.ipynb         # Main analysis: EDA, skip behavior, ML models

scripts/
  interactive_hist.py       # Standalone Plotly histogram
  interactive_line_plot.py  # Standalone Plotly line chart

reports/
  final_report.pdf          # 6-page written report
  presentation.pdf          # Slide deck

archive/                    # Old drafts and experiments, not maintained
docs/
  references.txt            # Academic references
```

---

## Setup

```bash
git clone <repo>
cd SpotifyProject

pip install pandas numpy matplotlib plotly scikit-learn xgboost lightgbm shap scipy networkx openai python-dotenv
```

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

---

## Running the pipeline

Run notebooks in order:

| Notebook | Input | Output |
|---|---|---|
| `01_json_to_csv` | `data/raw/streaming/*.json` | `data/processed/streaming2125.csv` |
| `02_data_cleaning` | `streaming2125.csv` | `data/processed/dfSCleaned.csv` |
| `03_merging` | `dfSCleaned.csv` + playlist CSVs | `data/processed/df24.csv` |
| `04_analysis` | `dfSCleaned.csv`, `df24.csv` | charts, model outputs |

The main notebook (`04_analysis`) reads data from `./data/processed/` by default. Override with the env var:

```bash
export SPOTIFY_DATA_DIR=./data/processed/
jupyter notebook notebooks/04_analysis.ipynb
```

---

## Try it with your own Spotify data

1. Go to `spotify.com/account/privacy` and request your **Extended Streaming History** (takes a few days to arrive).
2. Drop the JSON files into `data/raw/streaming/`.
3. Run notebooks 01 through 04 in order.
4. The 2024 enrichment step in `02_data_cleaning` uses the OpenAI API to assign theme and language labels. You need an API key for that step. Everything else runs without it.

---

## Key findings

- **Romantic** and **Hopeful** themes dominate 2024 play-time. Higher-energy themes (Empowered, Euphoric) trend upward across the year.
- Skipped songs have a slightly **higher average energy** than completed songs. The gap is statistically significant (p < 0.01).
- Including `ms_played` as a feature inflates skip prediction accuracy to 92%, but it leaks the label since play-time is downstream of the skip decision. Without it, honest accuracy lands around 70-75%.
- **`daily_avg_energy`** and **`is_english`** are the two most important non-leaky predictors per SHAP.
- Genre alone has essentially no predictive power.

---

## Tech stack

Python, pandas, scikit-learn, XGBoost, LightGBM, SHAP, Plotly, matplotlib, scipy, networkx, OpenAI API
