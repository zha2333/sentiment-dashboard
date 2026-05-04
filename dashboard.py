import subprocess
import sys

try:
    import plotly
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# 页面配置
st.set_page_config(page_title="小红书情绪监控看板", layout="wide")

# 标题
st.title("📊 小红书评论区情绪监控看板")
st.caption("基于情感词库分析 | 数据来源：小红书「请攻击我最薄弱的地方」话题")

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_excel("output/comments_with_sentiment.xlsx")
    return df

df = load_data()

# ====== 指标卡片 ======
col1, col2, col3, col4 = st.columns(4)

total = len(df)
positive = len(df[df['sentiment_label']=='积极'])
negative = len(df[df['sentiment_label']=='消极'])
neutral = len(df[df['sentiment_label']=='中性'])

col1.metric("📝 总评论数", total)
col2.metric("😊 积极评论", f"{positive} ({positive/total*100:.1f}%)")
col3.metric("😞 消极评论", f"{negative} ({negative/total*100:.1f}%)")
col4.metric("😐 中性评论", f"{neutral} ({neutral/total*100:.1f}%)")

# 预警：消极比例超过20%
if negative/total > 0.2:
    st.error("⚠️ **预警**：负面评论比例超过20%，请关注舆情！")
elif negative/total > 0.1:
    st.warning("⚠️ **提示**：负面评论比例超过10%，建议关注")

# ====== 情感分布饼图 ======
st.subheader("情感分布概览")
fig1 = px.pie(df, names='sentiment_label', title="评论情感占比",
              color='sentiment_label',
              color_discrete_map={'积极':'#2ecc71', '中性':'#f1c40f', '消极':'#e74c3c'})
st.plotly_chart(fig1, use_container_width=True)

# ====== 负面评论清单 ======
st.subheader("⚠️ 需关注的负面评论")
negative_comments = df[df['sentiment_label']=='消极'].head(10)

if len(negative_comments) > 0:
    for idx, row in negative_comments.iterrows():
        with st.container():
            st.markdown(f"""
            <div style='background-color:#fff3f3; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #e74c3c'>
            💬 {row['content'][:200]}
            </div>
            """, unsafe_allow_html=True)
else:
    st.success("暂无负面评论！")

# ====== 正面评论示例 ======
st.subheader("😊 正面评论示例")
positive_comments = df[df['sentiment_label']=='积极'].head(5)
for idx, row in positive_comments.iterrows():
    st.markdown(f"""
    <div style='background-color:#f0fff0; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2ecc71'>
    💬 {row['content'][:200]}
    </div>
    """, unsafe_allow_html=True)