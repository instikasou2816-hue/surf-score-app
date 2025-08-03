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