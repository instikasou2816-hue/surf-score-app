import streamlit as st

st.title("🏄‍♂️ サーフィン ジャッジ集計アプリ")

st.write("3人のジャッジの点数を入力すると、平均点が自動で計算されます。")

選手名 = st.text_input("選手名")
点A = st.number_input("ジャッジAの点数", min_value=0.0, max_value=10.0, step=0.1)
点B = st.number_input("ジャッジBの点数", min_value=0.0, max_value=10.0, step=0.1)
点C = st.number_input("ジャッジCの点数", min_value=0.0, max_value=10.0, step=0.1)

if st.button("平均点を計算"):
    平均 = round((点A + 点B + 点C) / 3, 2)
    st.success(f"🌊 {選手名} の平均点は {平均} 点です！")