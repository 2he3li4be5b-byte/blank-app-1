import streamlit as st

from supabase import create_client

# Supabase 接続
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


st.set_page_config(page_title="音楽ジャンル診断", page_icon="🎵")

st.title("🎵 データで見る音楽ジャンル診断")
st.write("いくつかの質問に答えると、あなたに合った音楽ジャンルとおすすめアーティストを診断します。")

# --- 質問と選択肢 ---
questions = {
    "Q1. 曲を聴くときに一番重視するのは？": {
        "メロディ": {"J-POP": 2, "POP": 2},
        "歌詞": {"J-POP": 3, "HIPHOP": 1},
        "リズム": {"HIPHOP": 3, "EDM": 2},
        "サウンドの迫力": {"ROCK": 3, "METAL": 2}
    },
    "Q2. 音楽をよく聴くシーンは？": {
        "勉強・作業中": {"POP": 2, "LOFI": 3},
        "通学・移動中": {"HIPHOP": 2, "ROCK": 2},
        "運動・トレーニング": {"EDM": 3, "ROCK": 2},
        "リラックスしたい時": {"J-POP": 2, "LOFI": 3}
    },
    "Q3. 好きな雰囲気は？": {
        "明るくて楽しい": {"POP": 3},
        "クールでかっこいい": {"HIPHOP": 3, "ROCK": 2},
        "感情的・エモい": {"J-POP": 3, "INDIE": 2},
        "非日常・クラブ系": {"EDM": 3}
    },
    "Q4. ボーカルはどのタイプが好き？": {
        "男性ボーカル": {"ROCK": 2, "HIPHOP": 1},
        "女性ボーカル": {"POP": 2, "J-POP": 2},
        "男女混合": {"POP": 1, "INDIE": 2},
        "ボーカルなし": {"EDM": 2, "LOFI": 2}
    },
    "Q5. 曲のテンポは？": {
        "ゆっくり": {"LOFI": 3},
        "普通": {"J-POP": 2, "POP": 2},
        "速い": {"ROCK": 2, "EDM": 2},
        "かなり速い": {"METAL": 3}
    },
    "Q6. 歌詞の言語は？": {
        "日本語": {"J-POP": 3},
        "英語": {"POP": 2, "HIPHOP": 2},
        "特に気にしない": {"EDM": 1, "ROCK": 1}
    },
    "Q7. 気分が落ち込んだときに聴きたいのは？": {
        "元気が出る": {"POP": 2},
        "共感できる": {"J-POP": 3, "INDIE": 2},
        "無心になれる": {"LOFI": 3},
        "強くなれる": {"ROCK": 2, "METAL": 2}
    },
    "Q8. 好きな楽器は？": {
        "ピアノ": {"J-POP": 2, "POP": 2},
        "ギター": {"ROCK": 3, "INDIE": 2},
        "ベース": {"HIPHOP": 2},
        "シンセ": {"EDM": 3}
    },
    "Q9. 新しい音楽への姿勢は？": {
        "流行を追いたい": {"POP": 2},
        "マイナーも好き": {"INDIE": 3},
        "定番が安心": {"J-POP": 2},
        "刺激が欲しい": {"METAL": 2, "EDM": 2}
    },
    "Q10. 音楽を聴く時間帯は？": {
        "朝": {"POP": 2},
        "昼": {"J-POP": 1, "HIPHOP": 1},
        "夜": {"INDIE": 2, "LOFI": 2},
        "深夜": {"EDM": 2, "METAL": 1}
    }
}

# --- ジャンル一覧を質問データから自動取得 ---
all_genres = set()
for opts in questions.values():
    for gmap in opts.values():
        all_genres.update(gmap.keys())

# --- 初期スコア ---
if "scores" not in st.session_state:
    st.session_state.scores = {g: 0 for g in all_genres}

# --- 質問表示 ---
answers = {}
for q, options in questions.items():
    answers[q] = st.radio(q, list(options.keys()))

# --- 診断ボタン ---
if st.button("診断する"):
    # スコアリセット
    scores = {g: 0 for g in all_genres}

    # スコア計算
    for q, answer in answers.items():
        for genre, point in questions[q][answer].items():
            scores[genre] += point

    # 結果
    best_genre = max(scores, key=scores.get)

    st.subheader("🎧 診断結果")
    st.write(f"あなたにおすすめの音楽ジャンルは **{best_genre}** です！")

    
    # ← ②追加：Supabase に保存
    supabase.table("app_data").insert({
        "result": best_genre
    }).execute()

    st.success("診断結果を保存しました")
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
