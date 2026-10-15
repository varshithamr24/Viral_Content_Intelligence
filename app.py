from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Viral Content Intelligence", page_icon="⚡", layout="wide")
ROOT = Path(__file__).resolve().parent
BG, PURPLE, CYAN, MINT, PINK = "#070914", "#9B5CFF", "#21D4FD", "#43F7B5", "#FF5CB8"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
.stApp{color:#F4F7FF;background:radial-gradient(ellipse at 12% -5%,#6d5dfb33,transparent 34%),radial-gradient(ellipse at 95% 0%,#21d4fd1c,transparent 30%),#070914;font-family:Manrope,sans-serif}
.block-container{max-width:1700px;padding:1.4rem 2rem 2.5rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c1020,#090c18);border-right:1px solid #9b5cff44}
[data-testid="stMetric"]{background:linear-gradient(145deg,#171f3b,#0b1020);border:1px solid #9b5cff55;border-radius:18px;padding:18px;box-shadow:0 12px 35px #0005,inset 0 1px #ffffff0b;min-height:118px}
[data-testid="stMetricLabel"]{color:#9ba9ca!important;font-size:.75rem!important;font-weight:700!important;letter-spacing:.06em}
[data-testid="stMetricValue"]{color:#fff!important;font-size:1.8rem!important;font-weight:800!important;letter-spacing:-.04em}
[data-baseweb="tab-list"]{gap:8px;background:#0c1020bb;padding:7px;border:1px solid #9b5cff33;border-radius:15px}
[data-baseweb="tab"]{height:43px;border-radius:10px;color:#aab7d5;padding:0 13px;font-weight:700}
[aria-selected="true"][data-baseweb="tab"]{background:linear-gradient(105deg,#6d5dfb,#9b5cff 55%,#087fa3)!important;color:white!important;box-shadow:0 0 20px #6d5dfb44}
.stButton button,.stDownloadButton button,.stFormSubmitButton button{background:linear-gradient(100deg,#6d5dfb,#9b5cff 58%,#087fa3);border:1px solid #a78bfa88;border-radius:11px;color:white;font-weight:800;box-shadow:0 5px 22px #6d5dfb2b}
.stButton button:hover,.stDownloadButton button:hover{border-color:#21d4fd;box-shadow:0 0 22px #21d4fd44;color:white}
.stSelectbox label,.stMultiSelect label,.stDateInput label,.stSlider label,.stTextArea label,.stNumberInput label{color:#c2cbe0!important;font-weight:700!important}
div[data-testid="stDataFrame"]{border:1px solid #9b5cff33;border-radius:13px;overflow:hidden}
hr{border-color:#9b5cff33}
.hero{position:relative;overflow:hidden;padding:30px 32px;border-radius:24px;border:1px solid #9b5cff88;background:linear-gradient(112deg,#6d5dfb33,#9b5cff18 48%,#21d4fd16),linear-gradient(145deg,#0f152b,#080c19);box-shadow:0 20px 70px #0006,inset 0 1px #ffffff0b;margin-bottom:22px}
.hero:before{content:"";position:absolute;right:-90px;top:-205px;width:420px;height:420px;border:1px solid #21d4fd44;border-radius:50%;box-shadow:0 0 0 35px #21d4fd08,0 0 0 80px #9b5cff08,0 0 80px #21d4fd22}
.hero-top{color:#9ba9ca;font-family:'DM Mono',monospace;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase}
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#43f7b5;box-shadow:0 0 13px #43f7b5;margin-right:8px}
.hero-title{font-size:clamp(2.2rem,4vw,3.45rem);line-height:1.04;font-weight:800;letter-spacing:-.07em;color:white;margin:15px 0 10px;position:relative}
.gradient-text{background:linear-gradient(95deg,#c4b5fd,#a78bfa 35%,#21d4fd 88%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-sub{color:#aab7d3;max-width:760px;font-size:.94rem;line-height:1.7;position:relative}
.hero-meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;position:relative}
.tag{font-family:'DM Mono',monospace;font-size:.68rem;color:#dde5ff;padding:7px 10px;border-radius:8px;border:1px solid #a78bfa44;background:#0a0f20bb}
.kicker{font-family:'DM Mono',monospace;text-transform:uppercase;font-size:.67rem;letter-spacing:.18em;color:#8b8dfe;margin-bottom:4px}
.section-title{font-size:1.25rem;font-weight:800;letter-spacing:-.04em;color:#f5f7ff;margin-bottom:2px}
.note{font-size:.82rem;color:#8492b1;margin-bottom:13px}
.panel-title{font-size:.9rem;font-weight:800;color:#eef2ff;margin-bottom:3px}
.panel-sub{font-size:.74rem;color:#8190b0;margin-bottom:8px}
.insight{border:1px solid #21d4fd44;border-left:3px solid #21d4fd;border-radius:13px;padding:16px 18px;background:linear-gradient(100deg,#21d4fd12,#6d5dfb12);color:#c9d6f2;line-height:1.65}
.insight b{color:white}
.footer{text-align:center;color:#5f6d8b;font-size:.7rem;line-height:1.8;padding-top:12px;font-family:'DM Mono',monospace;letter-spacing:.04em}
</style>
""", unsafe_allow_html=True)

def read_csv(name):
    p = ROOT / name
    if not p.exists():
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return None

def find_col(df, options):
    return next((c for c in options if c in df.columns), None)

def section(title, subtitle, kicker="SIGNAL / ANALYTICS"):
    st.markdown(f'<div class="kicker">{kicker}</div><div class="section-title">{title}</div><div class="note">{subtitle}</div>', unsafe_allow_html=True)

def panel(title, subtitle=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-sub">{subtitle}</div>', unsafe_allow_html=True)

def style_fig(fig, height=330, legend=None):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope,sans-serif",color="#AEBBD7",size=11),margin=dict(l=8,r=16,t=20,b=8),
        xaxis=dict(showgrid=False,zeroline=False,linecolor="#30364D",tickfont=dict(color="#8290AF")),
        yaxis=dict(showgrid=True,gridcolor="rgba(148,163,184,0.10)",zeroline=False,tickfont=dict(color="#AAB7D3")),
        hoverlabel=dict(bgcolor="#111A31",bordercolor="#8B5CF6",font_color="#F4F7FF"),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#AEBBD7",size=10)))
    if legend is not None:
        fig.update_layout(showlegend=legend)
    return fig

@st.cache_data
def load_data():
    posts, eng = read_csv("posts.csv"), read_csv("engagement.csv")
    if posts is None: raise FileNotFoundError("posts.csv is missing beside app.py.")
    if eng is None: raise FileNotFoundError("engagement.csv is missing beside app.py.")
    posts, eng = posts.copy(), eng.copy()
    if "post_id" not in posts: posts.insert(0,"post_id",np.arange(1,len(posts)+1))
    if "post_id" not in eng: raise ValueError("engagement.csv needs a post_id column.")
    posts["post_id"] = pd.to_numeric(posts["post_id"],errors="coerce")
    eng["post_id"] = pd.to_numeric(eng["post_id"],errors="coerce")
    df = posts.merge(eng,on="post_id",how="left",suffixes=("","_eng"))
    for c in ["likes","shares","saves","comments_count"]:
        src = c if c in df.columns else c+"_eng"
        df[c] = pd.to_numeric(df[src],errors="coerce").fillna(0) if src in df else 0
    df["total_engagement"] = df[["likes","shares","saves","comments_count"]].sum(axis=1)
    for c in ["retention_rate","follower_growth"]:
        src = c if c in df.columns else c+"_eng"
        if src in df: df[c] = pd.to_numeric(df[src],errors="coerce")
    if "post_date" in df: df["post_date"] = pd.to_datetime(df["post_date"],errors="coerce")
    return df

def mean_or_none(series):
    x = pd.to_numeric(series,errors="coerce").dropna()
    return float(x.mean()) if not x.empty else None

st.markdown("""
<div class="hero">
  <div class="hero-top"><span class="live-dot"></span> CREATOR INTELLIGENCE SYSTEM &nbsp; / &nbsp; ANALYTICS WORKSPACE</div>
  <div class="hero-title">VIRAL CONTENT<br><span class="gradient-text">INTELLIGENCE.</span></div>
  <div class="hero-sub">Decode engagement. Find your strongest content signals. Turn audience behavior into a smarter publishing strategy.</div>
  <div class="hero-meta"><span class="tag">01 / PERFORMANCE</span><span class="tag">02 / AUDIENCE SIGNALS</span><span class="tag">03 / EXPERIMENTS</span><span class="tag">04 / CONTENT PLANNER</span></div>
</div>
""",unsafe_allow_html=True)

try:
    source = load_data()
except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
    st.info("Keep app.py, posts.csv, and engagement.csv in the same Project folder.")
    st.stop()
if source.empty:
    st.warning("The post dataset is empty.")
    st.stop()

# Sidebar filters
st.sidebar.markdown('<div style="font-size:1.3rem;font-weight:800;color:white">⚡ VCI <span style="color:#21D4FD">/</span> FILTERS</div><div style="color:#8290AF;font-size:.78rem;margin:5px 0 18px">Control the view. Explore the signal.</div>',unsafe_allow_html=True)
df = source.copy()
for col,label in [("platform","PLATFORM"),("topic","TOPIC"),("content_type","FORMAT")]:
    if col in df:
        opts = sorted(df[col].dropna().astype(str).unique())
        selected = st.sidebar.multiselect(label,opts,default=list(opts),key=f"filter_{col}")
        df = df[df[col].astype(str).isin(selected)]
if "post_date" in df and df["post_date"].notna().any():
    dates = df["post_date"].dropna()
    low,high = dates.min().date(),dates.max().date()
    picked = st.sidebar.date_input("DATE WINDOW",value=(low,high),min_value=low,max_value=high)
    if isinstance(picked,(tuple,list)) and len(picked)==2:
        start,end = pd.Timestamp(picked[0]),pd.Timestamp(picked[1])+pd.Timedelta(days=1)-pd.Timedelta(microseconds=1)
        df = df[df["post_date"].between(start,end)]
st.sidebar.divider()
st.sidebar.markdown(f'<span style="color:#8BF5CC;font-family:monospace">● DATA CONNECTED</span><br><br><span style="color:#8290AF;font-size:.76rem">Source records: {len(source):,}<br>Visible records: {len(df):,}<br>Engine: Streamlit + Plotly</span>',unsafe_allow_html=True)
if df.empty:
    st.warning("No records match the filters. Select more options in the sidebar.")
    st.stop()

ret = mean_or_none(df["retention_rate"]) if "retention_rate" in df else None
followers = pd.to_numeric(df["follower_growth"],errors="coerce").fillna(0).sum() if "follower_growth" in df else None
k = st.columns(5)
k[0].metric("POSTS ANALYSED",f"{len(df):,}")
k[1].metric("TOTAL INTERACTIONS",f"{int(df.total_engagement.sum()):,}")
k[2].metric("AVG. ENGAGEMENT",f"{df.total_engagement.mean():,.0f}")
k[3].metric("AVG. RETENTION",f"{ret:.1f}%" if ret is not None else "N/A")
k[4].metric("FOLLOWER GROWTH",f"{followers:,.0f}" if followers is not None else "N/A")

overview,content,audience,experiments,studio = st.tabs(["◈ COMMAND CENTER","▥ CONTENT LAB","◎ AUDIENCE SIGNALS","⌁ EXPERIMENTS","✦ CREATOR STUDIO"])

with overview:
    section("Performance command center","A live view of the dataset selected in the filter panel.","SYSTEM / 01")
    left,right = st.columns([1.5,1])
    with left:
        panel("ENGAGEMENT MOMENTUM","Interaction volume across the timeline")
        if "post_date" in df and df["post_date"].notna().any():
            timeline = df.dropna(subset=["post_date"]).groupby("post_date",as_index=False)["total_engagement"].sum().sort_values("post_date")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=timeline.post_date,y=timeline.total_engagement,mode="lines",line=dict(color=CYAN,width=2.8,shape="spline"),fill="tozeroy",fillcolor="rgba(33,212,253,.09)",hovertemplate="%{x|%d %b %Y}<br><b>%{y:,.0f}</b><extra></extra>"))
            fig.add_trace(go.Scatter(x=timeline.post_date,y=timeline.total_engagement,mode="markers",marker=dict(color=PURPLE,size=4),hoverinfo="skip"))
            st.plotly_chart(style_fig(fig,360,False),use_container_width=True)
        else: st.info("Valid post_date values are needed for this chart.")
    with right:
        panel("ENGAGEMENT DNA","Share of interactions by action")
        vals = [int(df[c].sum()) for c in ["likes","shares","saves","comments_count"]]
        fig = go.Figure(go.Pie(labels=["Likes","Shares","Saves","Comments"],values=vals,hole=.72,sort=False,marker=dict(colors=[PURPLE,CYAN,PINK,MINT],line=dict(color=BG,width=3)),textinfo="percent",textfont=dict(color="white",size=11),hovertemplate="%{label}<br><b>%{value:,.0f}</b> (%{percent})<extra></extra>"))
        fig.add_annotation(text=f"<b>{sum(vals):,.0f}</b><br><span style='font-size:10px'>ACTIONS</span>",x=.5,y=.5,showarrow=False,font=dict(size=19,color="#F4F7FF"))
        st.plotly_chart(style_fig(fig,360,True),use_container_width=True)
    a,b = st.columns(2)
    with a:
        panel("CHANNEL LEADERBOARD","Platforms ranked by total interactions")
        if "platform" in df:
            p = df.groupby("platform",as_index=False).agg(Interactions=("total_engagement","sum"),Posts=("post_id","count")).sort_values("Interactions")
            fig = go.Figure(go.Bar(x=p.Interactions,y=p.platform,orientation="h",marker=dict(color=p.Interactions,colorscale=[[0,"#5145CD"],[.55,PURPLE],[1,CYAN]]),text=p.Interactions.map(lambda x:f"{x:,.0f}"),textposition="outside",hovertemplate="%{y}<br><b>%{x:,.0f}</b> interactions<extra></extra>"))
            fig.update_layout(xaxis_title="Interactions",yaxis_title="",margin=dict(l=5,r=35,t=10,b=5))
            st.plotly_chart(style_fig(fig,300,False),use_container_width=True)
    with b:
        panel("TOPIC SIGNALS","Topics ranked by average interactions")
        if "topic" in df:
            t = df.groupby("topic",as_index=False).agg(Average=("total_engagement","mean"),Posts=("post_id","count")).sort_values("Average").tail(9)
            fig = go.Figure(go.Bar(x=t.Average,y=t.topic,orientation="h",marker=dict(color=CYAN,line=dict(color=PURPLE,width=.5)),text=t.Average.map(lambda x:f"{x:,.0f}"),textposition="outside",customdata=t[["Posts"]].values,hovertemplate="%{y}<br>Average: <b>%{x:,.0f}</b><br>Posts: %{customdata[0]}<extra></extra>"))
            fig.update_layout(xaxis_title="Average interactions",yaxis_title="",margin=dict(l=5,r=35,t=10,b=5))
            st.plotly_chart(style_fig(fig,300,False),use_container_width=True)
    st.markdown('<div class="insight"><b>✦ SIGNAL TO ACTION</b><br>Use the platform leaderboard to prioritize channels and the topic ranking to identify themes worth testing. Historical engagement is a useful signal, not a guarantee of future virality.</div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    section("Top-performing posts","Highest interaction posts in the selected view.","SYSTEM / RANKINGS")
    cols = [c for c in ["post_id","platform","topic","content_type","post_date","likes","shares","saves","comments_count","total_engagement"] if c in df]
    top = df.sort_values("total_engagement",ascending=False)[cols].head(10).copy()
    if "post_date" in top: top["post_date"] = top["post_date"].dt.strftime("%d %b %Y")
    st.dataframe(top,use_container_width=True,hide_index=True)
    st.download_button("↓ EXPORT FILTERED DATA",df.to_csv(index=False).encode("utf-8"),"filtered_social_engagement.csv","text/csv")

with content:
    section("Content performance lab","Compare formats and topics to discover patterns worth testing.","SYSTEM / 02")
    a,b = st.columns(2)
    with a:
        panel("FORMAT PERFORMANCE","Average interactions per format")
        if "content_type" in df:
            f = df.groupby("content_type",as_index=False).agg(Average=("total_engagement","mean"),Total=("total_engagement","sum"),Posts=("post_id","count")).sort_values("Average")
            fig = go.Figure(go.Bar(x=f.Average,y=f.content_type,orientation="h",marker=dict(color=[CYAN if i==len(f)-1 else PURPLE for i in range(len(f))]),text=f.Average.map(lambda x:f"{x:,.0f}"),textposition="outside"))
            fig.update_layout(xaxis_title="Average interactions",yaxis_title="",margin=dict(l=5,r=35,t=10,b=5))
            st.plotly_chart(style_fig(fig,320,False),use_container_width=True)
    with b:
        panel("VOLUME VS. IMPACT","Bubble size represents total engagement")
        if "topic" in df:
            t = df.groupby("topic",as_index=False).agg(Posts=("post_id","count"),Average=("total_engagement","mean"),Total=("total_engagement","sum"))
            fig = px.scatter(t,x="Posts",y="Average",size="Total",color="topic",hover_name="topic",size_max=42,color_discrete_sequence=[PURPLE,CYAN,PINK,MINT,"#FFC857", "#6D5DFB"])
            fig.update_traces(marker=dict(line=dict(color="#D9D5FF",width=.7),opacity=.85))
            st.plotly_chart(style_fig(fig,320,False),use_container_width=True)
    if "platform" in df and "content_type" in df:
        panel("PLATFORM × FORMAT MATRIX","Average interactions for each combination")
        matrix = df.pivot_table(index="platform",columns="content_type",values="total_engagement",aggfunc="mean",fill_value=0)
        fig = px.imshow(matrix,text_auto=".0f",aspect="auto",color_continuous_scale=[[0,"#11162B"],[.45,"#6246EA"],[1,CYAN]])
        fig.update_traces(textfont=dict(color="white",size=12))
        st.plotly_chart(style_fig(fig,330),use_container_width=True)
    section("Content explorer","Interactive view of your filtered records.","SYSTEM / DATA")
    cols = [c for c in ["post_id","post_date","platform","topic","content_type","total_engagement","likes","shares","saves","comments_count","retention_rate","follower_growth"] if c in df]
    st.dataframe(df.sort_values("total_engagement",ascending=False)[cols],use_container_width=True,hide_index=True)

with audience:
    section("Audience signal monitor","Review sentiment and comment data produced by your analysis workflow.","SYSTEM / 03")
    sent = read_csv("audience_sentiment_analysis.csv")
    if sent is None or sent.empty: sent = read_csv("comments.csv")
    if sent is not None and not sent.empty:
        label = find_col(sent,["predicted_sentiment","sentiment"])
        score = find_col(sent,["sentiment_score","polarity"])
        relatability = find_col(sent,["relatability"])
        a,b = st.columns(2)
        with a:
            panel("SENTIMENT DISTRIBUTION","How audience comments are classified")
            if label:
                counts = sent[label].fillna("Unknown").astype(str).value_counts().rename_axis("Sentiment").reset_index(name="Comments")
                fig = go.Figure(go.Pie(labels=counts.Sentiment,values=counts.Comments,hole=.65,marker=dict(colors=[MINT,"#FFC857",PINK,CYAN,PURPLE],line=dict(color=BG,width=3)),textinfo="percent+label",textfont=dict(color="white",size=10)))
                st.plotly_chart(style_fig(fig,320),use_container_width=True)
            else: st.info("No sentiment label column was found.")
        with b:
            panel("SENTIMENT SCORE","Distribution of numeric polarity scores")
            if score:
                sent[score] = pd.to_numeric(sent[score],errors="coerce")
                fig = px.histogram(sent.dropna(subset=[score]),x=score,nbins=30,color_discrete_sequence=[CYAN])
                fig.update_traces(marker_line_color=PURPLE,marker_line_width=.7)
                fig.update_layout(xaxis_title="Sentiment score",yaxis_title="Comment count")
                st.plotly_chart(style_fig(fig,320,False),use_container_width=True)
            elif relatability:
                r = sent[relatability].fillna("Unknown").astype(str).value_counts().rename_axis("Relatability").reset_index(name="Comments")
                fig = px.bar(r,x="Relatability",y="Comments",color="Relatability",color_discrete_sequence=[PURPLE,CYAN,MINT,PINK])
                st.plotly_chart(style_fig(fig,320,False),use_container_width=True)
            else: st.info("No sentiment score or relatability column was found.")
        section("Audience voice","Preview of the comment-analysis dataset.","SYSTEM / COMMENTS")
        cols = [c for c in ["comment_id","post_id","comment_text",label,score,relatability] if c and c in sent]
        if cols: st.dataframe(sent[cols].head(100),use_container_width=True,hide_index=True)
    else:
        st.info("Add audience_sentiment_analysis.csv or comments.csv beside app.py.")
    trends = read_csv("trends.csv")
    if trends is not None and not trends.empty:
        section("Trend watchlist","Keywords and hashtags from your trend dataset.","SYSTEM / DISCOVERY")
        st.dataframe(trends,use_container_width=True,hide_index=True)

with experiments:
    section("Experiment control room","Inspect A/B variants and saved trend-analysis outputs.","SYSTEM / 04")
    ab = read_csv("ab_tests.csv")
    if ab is not None and not ab.empty:
        ab = ab.copy()
        for c in ["impressions","likes","shares","saves","retention_rate"]:
            if c in ab: ab[c] = pd.to_numeric(ab[c],errors="coerce")
        if "variant" in ab:
            metrics = [c for c in ["impressions","likes","shares","saves","retention_rate"] if c in ab]
            if metrics:
                panel("VARIANT SCORECARD","Mean recorded performance for each variant")
                score = ab.groupby("variant",as_index=False)[metrics].mean()
                st.dataframe(score.round(2),use_container_width=True,hide_index=True)
                metric = find_col(score,["retention_rate","shares","likes","impressions"])
                if metric:
                    fig = px.bar(score,x="variant",y=metric,color="variant",text_auto=".2f",color_discrete_sequence=[PURPLE,CYAN,PINK,MINT])
                    fig.update_layout(showlegend=False,xaxis_title="Experiment variant",yaxis_title=metric.replace("_"," ").title())
                    st.plotly_chart(style_fig(fig,300,False),use_container_width=True)
        else: st.info("The A/B test file needs a variant column.")
        with st.expander("Inspect raw experiment records"): st.dataframe(ab,use_container_width=True,hide_index=True)
    else: st.info("No populated ab_tests.csv was found.")
    daily = read_csv("daily_engagement_trends.csv")
    if daily is not None and not daily.empty:
        section("Engagement trend line","Visualization of the saved daily trend output.","SYSTEM / MOMENTUM")
        dc = find_col(daily,["post_date","date","day"])
        vc = find_col(daily,["total_engagement","average_engagement","engagement","daily_engagement"])
        if dc and vc:
            daily[dc] = pd.to_datetime(daily[dc],errors="coerce")
            daily[vc] = pd.to_numeric(daily[vc],errors="coerce")
            valid = daily.dropna(subset=[dc,vc]).sort_values(dc)
            if not valid.empty:
                fig = go.Figure(go.Scatter(x=valid[dc],y=valid[vc],mode="lines+markers",line=dict(color=PURPLE,width=2.6),marker=dict(color=CYAN,size=5),fill="tozeroy",fillcolor="rgba(155,92,255,.08)"))
                fig.update_layout(xaxis_title="",yaxis_title=vc.replace("_"," ").title())
                st.plotly_chart(style_fig(fig,310,False),use_container_width=True)
            else: st.dataframe(daily,use_container_width=True,hide_index=True)
        else: st.dataframe(daily,use_container_width=True,hide_index=True)
    forecast = read_csv("engagement_forecast_evaluation.csv")
    if forecast is not None and not forecast.empty:
        section("Forecast model evaluation","Saved metrics from your forecasting step.","SYSTEM / MODEL HEALTH")
        st.dataframe(forecast,use_container_width=True,hide_index=True)

with studio:
    section("Creator studio","Build a structured publishing brief using your dataset's available categories.","SYSTEM / 05")
    st.markdown('<div class="insight"><b>CREATOR PLAYBOOK</b><br>Plan one clear audience benefit, lead with a specific hook, and review engagement after publishing. This brief is a planning aid, not a promise of virality.</div>',unsafe_allow_html=True)
    platforms = sorted(source.platform.dropna().astype(str).unique()) if "platform" in source else ["Instagram","YouTube"]
    topics = sorted(source.topic.dropna().astype(str).unique()) if "topic" in source else ["Education","Entertainment"]
    formats = sorted(source.content_type.dropna().astype(str).unique()) if "content_type" in source else ["Reel","Short"]
    with st.form("creator_brief"):
        a,b = st.columns(2)
        with a:
            platform = st.selectbox("TARGET PLATFORM",platforms)
            topic = st.selectbox("CONTENT TOPIC",topics)
            fmt = st.selectbox("CONTENT FORMAT",formats)
        with b:
            hour = st.slider("PLANNED POSTING HOUR",0,23,18)
            seconds = st.number_input("VIDEO LENGTH (SECONDS)",min_value=0,max_value=3600,value=30,step=5)
            caption = st.text_area("CAPTION / IDEA",placeholder="Write the hook or the core idea for this post.")
        submit = st.form_submit_button("✦ GENERATE CONTENT BRIEF",use_container_width=True)
    if submit:
        brief = pd.DataFrame([{"platform":platform,"topic":topic,"content_type":fmt,"post_hour":hour,"video_length_seconds":seconds,"caption":caption,"caption_length":len(caption)}])
        a,b,c = st.columns(3)
        a.metric("CAPTION CHARACTERS",f"{len(caption):,}")
        b.metric("PLANNED TIME",f"{hour:02d}:00")
        c.metric("VIDEO LENGTH",f"{seconds:,} sec")
        st.markdown("### Pre-publish checklist")
        st.markdown("- [ ] Open with a specific hook.\n- [ ] Deliver one useful or entertaining idea.\n- [ ] Keep the caption clear.\n- [ ] Invite a relevant response.\n- [ ] Review results after publishing.")
        st.dataframe(brief,use_container_width=True,hide_index=True)
        st.download_button("↓ DOWNLOAD CONTENT BRIEF",brief.to_csv(index=False).encode("utf-8"),"content_planning_brief.csv","text/csv")

st.markdown("<hr>",unsafe_allow_html=True)
st.markdown('<div class="footer">VIRAL CONTENT INTELLIGENCE / VCI-01<br>DATA-DRIVEN SOCIAL ENGAGEMENT INITIATIVE · ANALYTICS WORKSPACE<br>HISTORICAL DATA IS A SIGNAL, NOT A GUARANTEE</div>',unsafe_allow_html=True)
