import streamlit as st
import pandas as pd

st.title("📊 株主優待 利回りランキング")

df = pd.read_csv("yutai.csv")
st.subheader("🔎 カテゴリ検索")

category = st.selectbox(
    "カテゴリを選択してください",
    ["すべて"] + list(df["category"].unique())
)
st.subheader("💰 投資予算")

budget = st.slider(
    "最大投資金額",
    min_value=0,
    max_value=600000,
    value=300000,
    step=50000
)

if category != "すべて":
    df = df[df["category"] == category]

df = df[df["investment"] <= budget]
df = df.sort_values("benefit_yield", ascending=False)
st.subheader("🏆 優待利回りランキング")
if df.empty:
    st.warning("条件に合う優待がありません。")

else:
    if len(df) >= 1:
        st.write(
            f"🥇 1位　{df.iloc[0]['company']}　"
            f"優待利回り {df.iloc[0]['benefit_yield']}%"
        )

    if len(df) >= 2:
        st.write(
            f"🥈 2位　{df.iloc[1]['company']}　"
            f"優待利回り {df.iloc[1]['benefit_yield']}%"
        )

    if len(df) >= 3:
        st.write(
            f"🥉 3位　{df.iloc[2]['company']}　"
            f"優待利回り {df.iloc[2]['benefit_yield']}%"
        )

    st.subheader("⭐ おすすめ")

    if df.iloc[0]["benefit_yield"] >= 3:
        st.success(
            f"おすすめ：{df.iloc[0]['company']} "
            f"（優待利回り {df.iloc[0]['benefit_yield']}%）"
        )
    else:
        st.info(
            "現在の条件では、優待利回り3%以上の銘柄はありません。"
        )

    st.subheader("📋 詳細データ")

    st.dataframe(
        df,
        column_config={
            "rank": "順位",
            "company": "会社名",
            "investment": st.column_config.NumberColumn(
                "投資金額",
                format="¥%d"
            ),
            "benefit_yield": st.column_config.NumberColumn(
                "優待利回り",
                format="%.1f%%"
            ),
            "category": "カテゴリ"
        }
    )

    st.subheader("📈 優待利回りランキング")

    st.bar_chart(
        df.set_index("company")["benefit_yield"]
    )
