⚡ Viral Content Intelligence
Data-Driven Social Engagement Initiative
A data analytics and machine-learning project that explores social media engagement, audience sentiment, content performance, trend patterns, and content recommendations through an interactive Streamlit dashboard.
The goal is to turn social engagement data into practical insights that can help creators understand what resonates with their audience and plan future content more thoughtfully.
---
✨ Project Highlights
Engagement analytics: Analyse likes, shares, saves, comments, retention, and follower growth.
Interactive dashboard: Explore results through a dark, neon-inspired Streamlit interface with Plotly charts.
Content performance analysis: Compare platforms, topics, and content formats.
Audience sentiment analysis: Examine comment sentiment using the sentiment-analysis output created in the project workflow.
Viral-content classification: Use saved machine-learning models to study patterns associated with higher engagement.
Content recommendations: Review topic, format, and platform-topic recommendations generated during analysis.
Trend analysis: Explore engagement over time and inspect saved trend/forecast outputs.
A/B experiment analysis: Compare variants using the experiment data.
Creator Studio: Generate a downloadable content-planning brief from selected platform, topic, format, and publishing details.
> **Note:** Model predictions are estimates based on the available dataset. They do not guarantee that a post will go viral. If the project dataset is synthetic or simulated, results should be treated as demonstration results rather than evidence of real-world audience behaviour.
---
🧰 Tech Stack
Technology	Purpose
Python	Data processing and application logic
Pandas, NumPy	Data cleaning, transformation, and analysis
Scikit-learn	Machine-learning workflows
Streamlit	Interactive web dashboard
Plotly	Interactive charts and visualisations
Joblib / Pickle model files	Saving and loading trained models
CSV	Storing project datasets and analysis outputs
---
📁 Project Files
Keep the dashboard file and its CSV files together in the same project directory unless you update the paths in the code.
```text
Viral-Content-Intelligence/
├── app.py
├── requirements.txt
├── posts.csv
├── engagement.csv
├── comments.csv
├── audience_sentiment_analysis.csv
├── ab_tests.csv
├── trends.csv
├── viral_content_prediction_model.pkl
├── advanced_viral_content_model.pkl
├── model_performance_results.csv
├── new_post_predictions.csv
├── content_recommendations.csv
├── topic_recommendations.csv
├── format_recommendations.csv
├── platform_topic_recommendations.csv
├── daily_engagement_trends.csv
├── weekly_engagement_trends.csv
├── topic_trend_analysis.csv
└── engagement_forecast_evaluation.csv
```
Some output files are optional for the dashboard. The core files needed to start the dashboard are `app.py`, `posts.csv`, and `engagement.csv`. Other sections display insights when their corresponding CSV files are present.
---
🚀 Getting Started
1. Install Python
Install a compatible Python version and make sure Python is available from your terminal. An Anaconda environment can also be used.
2. Download or clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```
Replace the example repository URL with your own GitHub repository URL.
3. Install dependencies
Create a file named `requirements.txt` containing:
```text
streamlit
pandas
numpy
plotly
scikit-learn
joblib
```
Then run:
```bash
python -m pip install -r requirements.txt
```
4. Check the data files
Make sure `posts.csv` and `engagement.csv` are in the same directory as `app.py`. Keep the original column names and include a `post_id` column in both files so records can be joined correctly.
5. Launch the dashboard
Run this command from the project directory:
```bash
python -m streamlit run app.py
```
Streamlit will show a local URL, usually:
```text
http://localhost:8501
```
Open that address in your browser.
If using Jupyter Notebook, run the following in a notebook cell:
```python
%cd "C:\\path\\to\\your\\project"
!python -m streamlit run app.py
```
Replace the example path with the actual directory on your computer.
---
🖥️ Dashboard Sections
1. Command Center
Key performance indicators, including posts analysed and total interactions.
Engagement over time.
Breakdown of likes, shares, saves, and comments.
Platform and topic leaderboards.
Top-performing posts in the selected filters.
2. Content Lab
Compare average engagement by content format.
Explore topic performance and volume-versus-impact patterns.
Inspect platform and format combinations using a heatmap.
Review filtered post-level data.
3. Audience Signals
Visualise available sentiment labels and sentiment scores.
Inspect comment-analysis records.
View the trend watchlist when the trends data is available.
4. Experiments
Review A/B experiment variants and available performance measures.
Inspect saved daily engagement trends.
View saved forecasting evaluation results.
5. Creator Studio
Select a target platform, topic, and content format.
Set a planned posting hour and video duration.
Enter a caption or idea.
Export a content-planning brief as a CSV file.
---
📊 Data and Outputs
The dashboard uses local CSV files created or collected during the project workflow. Examples include:
`posts.csv` — post metadata such as platform, topic, format, caption, and date.
`engagement.csv` — engagement metrics associated with each post.
`comments.csv` and `audience_sentiment_analysis.csv` — audience comments and sentiment-analysis outputs.
`ab_tests.csv` — experiment variants and recorded metrics.
`trends.csv` — keywords, hashtags, and trend-related fields.
`model_performance_results.csv` — saved model evaluation results.
`new_post_predictions.csv` — example predictions generated by the modelling workflow.
`*_recommendations.csv` — recommendation outputs.
`*_trends.csv` and `engagement_forecast_evaluation.csv` — trend and forecasting outputs.
Column names may differ if your analysis notebook has been customised. Keep the dashboard code aligned with your actual CSV column names.
---
🔐 Data, Privacy, and Responsible Use
Do not commit private, confidential, or personally identifiable data to a public repository.
Check whether you have permission to use any social-media data before publishing it.
Do not include API keys, passwords, access tokens, or private credentials in the repository.
Clearly label simulated or synthetic data.
Treat model outputs as decision-support signals, not certain predictions.
---
🔮 Future Enhancements
Connect to approved, live social-media APIs.
Add model-driven predictions directly inside the dashboard.
Add more detailed evaluation metrics and model explanations.
Introduce configurable posting schedules and content experiments.
Add exportable reports and dashboard deployment.
Evaluate models on larger, representative real-world datasets.
---
