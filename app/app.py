import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="巴西电商数据分析", page_icon="🛒", layout="wide")

st.title("🛒 巴西 Olist 电商数据分析")
st.write("基于 Olist 公开数据集的分析项目，包含品类、地域、配送、复购等维度。")

# ========== 第一部分：数据概况 ==========
st.header("第一部分：数据概况")
st.write("""
- 订单表：99,441 行  
- 客户表：99,441 行  
- 订单商品表：112,650 行  
- 商品表：32,951 行  
- 数据时间范围：2016 年 9 月 — 2018 年 10 月
""")

# ========== 第二部分：热销品类 Top 10 ==========
st.header("第二部分：热销品类 Top 10")
top_categories = pd.read_csv("results/top_categories.csv")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.barh(top_categories["product_category_name_english"], top_categories["count"])
ax1.invert_yaxis()
ax1.set_xlabel("订单数量")
st.pyplot(fig1)
st.write("结论：床品、美妆、运动是平台最热销的三大品类。")

# ========== 第三部分：各州订单分布 ==========
st.header("第三部分：各州订单分布")
state_orders = pd.read_csv("results/state_orders.csv")
col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.barh(state_orders.head(10)["customer_state"], state_orders.head(10)["count"])
    ax2.invert_yaxis()
    ax2.set_xlabel("订单数量")
    st.pyplot(fig2)

with col2:
    top5 = state_orders.head(5)
    others = state_orders.iloc[5:]["count"].sum()
    labels = list(top5["customer_state"]) + ["其他"]
    sizes = list(top5["count"]) + [others]

    fig3, ax3 = plt.subplots(figsize=(8, 8))
    ax3.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax3.set_title("各州订单占比")
    st.pyplot(fig3)
    st.write("结论：SP 州订单占比约 42%，巴西电商高度集中。")

# ========== 第四部分：配送时间统计 ==========
st.header("第四部分：配送时间统计")
delivery_stats = pd.read_csv("results/delivery_stats.csv", index_col=0)
st.write(delivery_stats)
st.write("结论：平均配送时间约 12 天，一半订单在 10 天内送达。")

# ========== 第五部分：延迟与评分对比 ==========
st.header("第五部分：延迟与评分对比")
score_by_late = pd.read_csv("results/score_by_late.csv", index_col=0)
st.write(score_by_late)
st.write("结论：延迟送达会显著拉低客户评分。")

# ========== 第六部分：卖家评分与配送时间 ==========
st.header("第六部分：卖家评分与配送时间")
seller_delivery = pd.read_csv("results/seller_delivery.csv")
seller_delivery = seller_delivery.sort_values("avg_score").head(10)
st.dataframe(seller_delivery)
st.write("结论：低分卖家配送普遍较慢，但评分还受其他因素影响。")

# ========== 第七部分：复购率 ==========
st.header("第七部分：复购率")
repeat_rate = pd.read_csv("results/repeat_rate.csv")
st.write(repeat_rate)
st.write("结论：平台复购率仅约 3%，是核心问题之一。")
