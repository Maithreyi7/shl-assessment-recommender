import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM PROFESSIONAL CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background-color: #f4f6fb;
}

/* Header styling */
.header-box {
    background: linear-gradient(90deg, #0052cc, #0073e6);
    padding: 30px;
    border-radius: 12px;
    color: white;
    margin-bottom: 25px;
}

/* Card styling */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Badge */
.badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 10px;
}

.top-match {
    background-color: #d4edda;
    color: #155724;
}

.strong-match {
    background-color: #fff3cd;
    color: #856404;
}

.match {
    background-color: #e2e3e5;
    color: #383d41;
}

/* Button styling */
.stButton>button {
    background-color: #0052cc;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #003d99;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
<div class="header-box">
    <h1>🎯 SHL Assessment Recommendation Engine</h1>
    <p>Smart recommendations powered by keyword-based relevance scoring</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("shl_products.csv")

df["Name"] = df["Name"].astype(str)
df["Job Levels"] = df["Job Levels"].astype(str)
df["Languages"] = df["Languages"].astype(str)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔎 Search Filters")

role = st.sidebar.text_input("Job Role")

# Extract levels
all_levels = set()
for levels in df["Job Levels"]:
    for level_item in levels.split(","):
        cleaned = level_item.strip()
        if cleaned:
            all_levels.add(cleaned)

level_options = sorted(all_levels)

# Extract languages
all_languages = set()
for langs in df["Languages"]:
    for lang_item in langs.split(","):
        cleaned = lang_item.strip()
        if cleaned:
            all_languages.add(cleaned)

language_options = sorted(all_languages)

level = st.sidebar.selectbox("Job Level", [""] + level_options)
language = st.sidebar.selectbox("Language", [""] + language_options)

recommend = st.sidebar.button("🚀 Generate Recommendations")

# ---------------------------------------------------
# RECOMMENDATION LOGIC
# ---------------------------------------------------
if recommend:

    role = role.strip().lower()
    level = level.strip().lower()
    language = language.strip().lower()

    results = df.copy()
    results["Score"] = 0

    # Role = 2 points
    if role:
        results.loc[
            results["Name"].str.lower().str.contains(role, na=False),
            "Score"
        ] += 2

    # Level = 1 point
    if level:
        results.loc[
            results["Job Levels"].str.lower().str.contains(level, na=False),
            "Score"
        ] += 1

    # Language = 1 point
    if language:
        results.loc[
            results["Languages"].str.lower().str.contains(language, na=False),
            "Score"
        ] += 1

    results = results[results["Score"] > 0]
    results = results.sort_values(by="Score", ascending=False)

    # ---------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------
    if results.empty:
        st.error("❌ No relevant assessments found.")
    else:
        st.success(f"🎉 {len(results)} relevant assessments found")

        for index, row in results.head(5).iterrows():

            score = row["Score"]

            # Determine badge
            if score >= 3:
                badge_class = "top-match"
                badge_text = "🏆 Top Match"
            elif score == 2:
                badge_class = "strong-match"
                badge_text = "⭐ Strong Match"
            else:
                badge_class = "match"
                badge_text = "✔ Match"

            st.markdown(f"""
            <div class="card">
                <div class="badge {badge_class}">{badge_text}</div>
                <h3>{row['Name']}</h3>
                <p><b>📌 Job Level:</b> {row['Job Levels']}</p>
                <p><b>🌍 Language:</b> {row['Languages']}</p>
                <p><b>⏱ Assessment Length:</b> {row['Assessment Length']}</p>
                <p><b>Relevance Score:</b> {score} / 4</p>
            </div>
            """, unsafe_allow_html=True)

            # Score Progress Bar
            st.progress(score / 4)

            st.link_button("🔗 View Assessment", row["URL"])

            with st.expander("Why this was recommended"):
                if role and role in row["Name"].lower():
                    st.write("✔ Matches job role keyword")

                if level and level in row["Job Levels"].lower():
                    st.write("✔ Suitable for selected job level")

                if language and language in row["Languages"].lower():
                    st.write("✔ Available in preferred language")

            st.markdown("---")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed as part of SHL Research Engineer Assessment")
st.caption("~Maithreyi Adluri")