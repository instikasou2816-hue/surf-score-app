import streamlit as st
import json
import os

DATA_PATH = "data/scores.json"

st.title("🏄‍♂️ 選手用：スコア閲覧ページ")

# データ読み込み
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        scores = json.load(f)
else:
    scores = {}

for player, rides in scores.items():
    st.subheader(f"📊 {player}")
    avg_scores = []

    for ride, judge_scores in rides.items():
        values = list(judge_scores.values())
        avg = round(sum(values) / len(values), 2)
        avg_scores.append(avg)
        st.markdown(f"✅ {ride}本目：平均 {avg} 点")

    # ベスト2本の合計
    best2 = sorted(avg_scores, reverse=True)[:2]
    total = round(sum(best2), 2) if len(best2) >= 2 else "記録不足"
    st.markdown(f"🏅 合計得点（ベスト2）：**{total}**")