import streamlit as st
from supabase import create_client   # ← ①追加

# ← ①追加：Supabase 接続
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.set_page_config(page_title="音楽ジャンル診断", page_icon="🎵")

st.title("🎵 データで見る音楽ジャンル診断")
st.write("いくつかの質問に答えると、あなたに合った音楽ジャンルとおすすめアーティストを診断します。")

# --- 質問と選択肢 ---
questions = {
    # （ここは元のままなので省略）
}

# --- ジャンル一覧 ---
all_genres = set()
for opts in questions.values():
    for gmap in opts.values():
        all_genres.update(gmap.keys())

# --- 質問表示 ---
answers = {}
for q, options in questions.items():
    answers[q] = st.radio(q, list(options.keys()))

# --- 診断ボタン ---
if st.button("診断する"):
    scores = {g: 0 for g in all_genres}

    for q, answer in answers.items():
        for genre, point in questions[q][answer].items():
            scores[genre] += point

    best_genre = max(scores, key=scores.get)

    st.subheader("🎧 診断結果")
    st.write(f"あなたにおすすめの音楽ジャンルは **{best_genre}** です！")

    # ← ②追加：Supabase に保存
    supabase.table("app_data").insert({
        "result": best_genre
    }).execute()

    st.success("診断結果を保存しました")

    recommendations = {
        "J-POP": ["YOASOBI", "米津玄師", "Official髭男dism"],
        "POP": ["Taylor Swift", "Ariana Grande", "Ed Sheeran"],
        "ROCK": ["ONE OK ROCK", "Foo Fighters", "RADWIMPS"],
        "HIPHOP": ["Kendrick Lamar", "Creepy Nuts", "Drake"],
        "EDM": ["Avicii", "The Chainsmokers", "Zedd"]
    }

    st.write("**おすすめアーティスト:**")
    for artist in recommendations[best_genre]:
        st.write(f"・{artist}")

    st.subheader("ジャンル別スコア")
    st.bar_chart(scores)
