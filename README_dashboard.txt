# Viral Content Intelligence Dashboard

## Run
Keep `app.py`, `requirements_dashboard.txt`, the CSV files, and `advanced_viral_content_model.pkl` together in one folder. Then run:

```bash
python -m pip install -r requirements_dashboard.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Corrections and notes
- The uploaded `app.py` was actually Jupyter Notebook JSON, not runnable Python. This is a replacement Streamlit dashboard.
- In the notebook, the plain `python -m pip install ...` line was invalid Python syntax; it is now `%pip install ...`.
- Notebook outputs were cleared to prevent stale errors from being mistaken for current results.
- The dashboard has Overview, Content Performance, Audience Insights, A/B Experiments, and Plan a Post tabs, with filters and charts.
- `posts.csv` has no `post_id`; the dashboard assigns IDs in row order to join `engagement.csv`. Verify row order if replacing these generated files.
- The model was saved under scikit-learn 1.7.2; use the pinned version to reduce pickle compatibility issues.
- The notebook has hard-coded MySQL credentials (`root` / `12345`) and direct insert statements. Do not commit real credentials; use environment variables and avoid duplicate inserts.
- Some recommendation CSVs are empty or contain very few rows, so the dashboard computes core metrics from the main post and engagement files.
- The sample data appears programmatically generated; treat insights as a demo until validated with real data.
