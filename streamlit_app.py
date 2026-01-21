import streamlit as st

st.set_page_config(page_title="音楽ジャンル診断", page_icon="🎵")

st.title("🎵 データで見る音楽ジャンル診断")
st.write("いくつかの質問に答えると、あなたに合った音楽ジャンルとおすすめアーティストを診断します。")

# --- 質問と選択肢 ---
questions = {
    "Q1. 曲を聴くときに一番重視するのは？": {
        "メロディ": {"J-POP": 2, "POP": 2},
        "歌詞": {"J-POP": 3, "HIPHOP": 1},
        "リズム": {"HIPHOP": 3, "EDM": 2},
        "サウンドの迫力": {"ROCK": 3, "EDM": 2}
    },
    "Q2. 音楽をよく聴くシーンは？": {
        "勉強・作業中": {"POP": 2, "J-POP": 1},
        "通学・移動中": {"HIPHOP": 2, "ROCK": 2},
        "運動・トレーニング": {"EDM": 3, "ROCK": 2},
        "リラックスしたい時": {"J-POP": 2, "POP": 2}
    },
    "Q3. 好きな雰囲気は？": {
        "明るくて楽しい": {"POP": 3},
        "クールでかっこいい": {"HIPHOP": 3, "ROCK": 2},
        "感情的・エモい": {"J-POP": 3, "ROCK": 1},
        "非日常・クラブ系": {"EDM": 3}
    }
}

# --- 初期スコア ---
if "scores" not in st.session_state:
    st.session_state.scores = {"J-POP": 0, "POP": 0, "ROCK": 0, "HIPHOP": 0, "EDM": 0}

# --- 質問表示 ---
answers = {}
for q, options in questions.items():
    answers[q] = st.radio(q, list(options.keys()))

# --- 診断ボタン ---
if st.button("診断する"):
    # スコアリセット
    scores = {"J-POP": 0, "POP": 0, "ROCK": 0, "HIPHOP": 0, "EDM": 0}

    # スコア計算
    for q, answer in answers.items():
        for genre, point in questions[q][answer].items():
            scores[genre] += point

    # 結果
    best_genre = max(scores, key=scores.get)

    st.subheader("🎧 診断結果")
    st.write(f"あなたにおすすめの音楽ジャンルは **{best_genre}** です！")

    # アーティスト推薦
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

    # スコア可視化
    st.subheader("ジャンル別スコア")
    st.bar_chart(scores)
