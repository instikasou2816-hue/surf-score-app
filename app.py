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