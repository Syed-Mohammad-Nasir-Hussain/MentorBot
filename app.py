import streamlit as st
import pandas as pd
import pdfplumber
from utils.recommender import recommend_roles
from utils.soft_skill_extractor import extract_keywords
import io
import re
import altair as alt

# 🎯 Page Config
st.set_page_config(page_title="AI MentorBot", layout="centered")
st.title("🎓 AI MentorBot: Career Role Recommender")

# 📄 Resume Upload
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    st.text_area("📋 Extracted Resume Text", resume_text, height=300)

# 📝 Manual Input Fallback
user_input = st.text_area("✍️ Or paste your resume or skills manually:", value=resume_text, height=200)

# 📊 Load roles dataset
try:
    df_roles = pd.read_csv("data/roles_data.csv")
except FileNotFoundError:
    st.error("❌ roles_data.csv not found. Please place it in the `data/` folder.")
    st.stop()

# 🔎 Learning Link Suggestions — YouTube only
def suggest_learning_links(missing_skills):
    suggestions = []
    for skill in missing_skills:
        query = skill.replace(" ", "+")
        youtube = f"https://www.youtube.com/results?search_query={query}+for+beginners"
        suggestions.append(f"- 🔗 [{skill.title()} on YouTube]({youtube})")
    return "\n".join(suggestions)

# 🔍 Recommend Button
if st.button("🔍 Find Suitable Roles"):
    if not user_input.strip():
        st.warning("⚠️ Please enter your resume or skills.")
    else:
        soft_skills = extract_keywords(user_input)
        st.markdown(f"🧠 **Extracted Skills:** `{', '.join(soft_skills)}`")

        recommendations = recommend_roles(user_input, df_roles)

        top_roles = recommendations[:3]
        df_out = pd.DataFrame(top_roles)
        st.download_button("📥 Download Top Role Matches", df_out.to_csv(index=False), "role_recommendations.csv", "text/csv")

        for rec in top_roles:
            st.subheader(f"🎯 {rec['role']} — {rec['match']}% match")
            st.metric("✅ Skills Matched", f"{len(rec['matched_skills'])}/{len(rec['matched_skills']) + len(rec['missing_skills'])}")
            st.markdown(f"**Missing Skills**: {', '.join(rec['missing_skills']) or 'None 🎉'}")
            st.markdown(f"**Recommended Courses**: {rec['recommended_courses']}")
            st.markdown("### 📎 YouTube Learning Resources")
            st.markdown(suggest_learning_links(rec['missing_skills']))
            st.markdown("---")

        # 📊 Radar Chart
        if top_roles:
            radar_data = pd.DataFrame({
                'Role': [r['role'] for r in top_roles],
                'Match %': [r['match'] for r in top_roles]
            })
            chart = alt.Chart(radar_data).mark_bar().encode(
                x='Role',
                y='Match %',
                color='Role'
            ).properties(title='🔍 Skill Match % Across Top Roles')
            st.altair_chart(chart, use_container_width=True)

        st.session_state["soft_skills"] = soft_skills
        st.session_state["user_input"] = user_input
