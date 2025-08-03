import streamlit as st
import pandas as pd

st.set_page_config(page_title="Surf Score App", layout="wide")
st.title("🏄 サーフィンジャッジ集計アプリ（LiveHeats風）")

# セッション内に保存されたスコア一覧を保持
if 'scores' not in st.session_state:
    st.session_state['scores'] = []

# ---------------------
# ヒート＆選手情報入力
# ---------------------
with st.form("score_form"):
    st.subheader("📝 スコア入力")

    heat = st.selectbox("ヒート番号", [f"Heat {i}" for i in range(1, 21)])
    player = st.text_input("選手名")
    score_a = st.number_input("ジャッジA", 0.0, 10.0, step=0.1)
    score_b = st.number_input("ジャッジB", 0.0, 10.0, step=0.1)
    score_c = st.number_input("ジャッジC", 0.0, 10.0, step=0.1)

    submitted = st.form_submit_button("スコア追加")

    if submitted and player:
        avg = round((score_a + score_b + score_c) / 3, 2)
        st.session_state['scores'].append({
            "ヒート": heat,
            "選手": player,
            "ジャッジA": score_a,
            "ジャッジB": score_b,
            "ジャッジC": score_c,
            "平均点": avg
        })
        st.success(f"{player} のスコアを追加しました！（平均：{avg}）")

# ---------------------
# スコア一覧表示
# ---------------------
st.subheader("📋 ヒート別スコア一覧")

if st.session_state['scores']:
    df = pd.DataFrame(st.session_state['scores'])
    for heat_name in sorted(df["ヒート"].unique()):
        st.markdown(f"### {heat_name}")
        st.dataframe(df[df["ヒート"] == heat_name].sort_values("平均点", ascending=False), use_container_width=True)
else:
    st.info("まだスコアが登録されていません。")

st.markdown("---")
st.subheader("🏁 5人ヒートの一括スコア入力（ジャッジ用）")

選手数 = 5
選手名リスト = []
スコアリスト = []

with st.form("five_player_form"):
    heat_name = st.text_input("ヒート名（例: Heat 3）", value="Heat 1")

    for i in range(選手数):
        st.markdown(f"#### 選手{i+1}")
        name = st.text_input(f"選手{i+1}の名前", key=f"name_{i}")
        score_a = st.number_input(f"ジャッジAの点数（選手{i+1}）", 0.0, 10.0, step=0.1, key=f"scoreA_{i}")
        score_b = st.number_input(f"ジャッジBの点数（選手{i+1}）", 0.0, 10.0, step=0.1, key=f"scoreB_{i}")
        score_c = st.number_input(f"ジャッジCの点数（選手{i+1}）", 0.0, 10.0, step=0.1, key=f"scoreC_{i}")

        if name:
            avg = round((score_a + score_b + score_c) / 3, 2)
            スコアリスト.append({
                "ヒート": heat_name,
                "選手": name,
                "ジャッジA": score_a,
                "ジャッジB": score_b,
                "ジャッジC": score_c,
                "平均点": avg
            })

    submitted_five = st.form_submit_button("5人分を一括追加")

    if submitted_five and スコアリスト:
        st.session_state['scores'].extend(スコアリスト)
        st.success(f"{heat_name} に 5人分のスコアを追加しました！")

import streamlit as st
import pandas as pd
import numpy as np

st.title("サーフスコアアプリ 🏄‍♂️")

# ヒート設定
heat_name = st.text_input("ヒート名", "Round 1: ヒート 1")
riders = st.text_area("選手名（1行ずつ）", "武藤波琉\n木下嵩道\n小松一絆\n中鉢晴心").splitlines()
num_judges = 3
num_waves = st.slider("最大ライディング数", 1, 5, 3)

# スコア入力
scores = {}

st.write(f"### {heat_name}")

for rider in riders:
    st.subheader(f"選手: {rider}")
    rider_scores = []

    for wave in range(1, num_waves + 1):
        st.write(f"**Wave {wave}**")
        wave_scores = []

        cols = st.columns(num_judges)
        for j in range(num_judges):
            with cols[j]:
                score = st.number_input(f"Judge {j+1}", min_value=0.0, max_value=10.0, step=0.01, key=f"{rider}_w{wave}_j{j}")
                wave_scores.append(score)

        avg_score = np.round(np.mean(wave_scores), 2)
        st.write(f"→ 平均点: **{avg_score}**")
        rider_scores.append(avg_score)

    scores[rider] = rider_scores

# 結果表示
st.write("## 結果一覧")

result_data = []
for rider, avg_scores in scores.items():
    total = np.round(sum(avg_scores), 2)
    result_data.append([rider] + avg_scores + [total])

columns = ["選手名"] + [f"Wave {i+1}" for i in range(num_waves)] + ["合計"]
result_df = pd.DataFrame(result_data, columns=columns)

# 合計点でソート
result_df = result_df.sort_values("合計", ascending=False).reset_index(drop=True)
result_df.index = result_df.index + 1  # ランクを1始まりに

st.table(result_df)