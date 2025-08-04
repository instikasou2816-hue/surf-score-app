import streamlit as st
import json
import os

DATA_PATH = "data/scores.json"

# 選手とジャッジ名を設定
players = ["選手1", "選手2", "選手3", "選手4", "選手5"]
judges = ["ジャッジ1", "ジャッジ2", "ジャッジ3"]

# データ読み込み or 初期化
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        scores = json.load(f)
else:
    scores = {}

st.title("🧑‍⚖️ ジャッジ用：スコア入力ページ")

player = st.selectbox("選手を選んでください", players)
judge = st.selectbox("あなたの名前（ジャッジ）を選んでください", judges)
ride_number = st.number_input("ライディング番号", min_value=1, step=1)
score = st.slider("スコア", 0.0, 10.0, 5.0, 0.1)

if st.button("スコアを記録"):
    scores.setdefault(player, {}).setdefault(str(ride_number), {})[judge] = score
    with open(DATA_PATH, "w") as f:
        json.dump(scores, f, indent=2)
    st.success("スコアを記録しました！")

# ジャッジ別の入力済みスコアを表示
if player in scores:
    st.subheader(f"📝 {player} のスコア一覧")
    for ride, ride_scores in scores[player].items():
        judge_scores = ", ".join(f"{j}:{s}" for j, s in ride_scores.items())
        st.markdown(f"**{ride}本目：** {judge_scores}")