import streamlit as st
import pandas as pd
import pdfplumber
from utils.recommender import recommend_roles
from utils.soft_skill_extractor import extract_keywords as extract_soft_skills
from utils.visuals import plot_skill_radar
import io

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

# 📝 Manual Input
user_input = st.text_area("✍️ Or paste your resume or skills manually:", value=resume_text, height=200)

# 📊 Load Role Data
try:
    df_roles = pd.read_csv("data/roles_data.csv")
except FileNotFoundError:
    st.error("❌ roles_data.csv not found in the `data/` folder.")
    st.stop()

# 📌 Suggest learning links
def suggest_learning_links(missing_skills):
    suggestions = []
    for skill in missing_skills:
        query = skill.replace(" ", "+")
        youtube = f"https://www.youtube.com/results?search_query={query}+for+beginners"
        roadmap = f"https://roadmap.sh/search?query={query}"
        suggestions.append(f"- 🔗 [{skill} on YouTube]({youtube}) | 🗺️ [Roadmap.sh]({roadmap})")
    return "\n".join(suggestions)

# 🚀 Recommendation Trigger
if st.button("🔍 Find Suitable Roles"):
    if not user_input.strip():
        st.warning("⚠️ Please provide resume content or list your skills.")
    else:
        soft_skills = extract_soft_skills(user_input)
        st.markdown(f"🧠 **Extracted Skills:** `{soft_skills}`")

        user_skills = set(skill.lower() for skill in soft_skills)

        recommendations = recommend_roles(user_input, df_roles)

        if not recommendations:
            st.warning("⚠️ No matching roles found.")
        else:
            st.markdown("---")
            st.markdown("## 🎯 Top Role Recommendations")

            for rec in recommendations[:3]:
                st.subheader(f"🎯 {rec['role']}")
                st.metric("Match %", f"{rec['match']}%")
                st.progress(rec['match'] / 100)

                st.markdown(f"**✅ Matched Skills**: {', '.join(rec['matched_skills']) or 'None'}")
                st.markdown(f"**❌ Missing Skills**: {', '.join(rec['missing_skills']) or 'None 🎉'}")
                st.markdown(f"**📘 Recommended Courses**: {rec['recommended_courses']}")

                # 🎯 Radar Chart
                if 'required_skills' in rec:
                    fig = plot_skill_radar(user_skills, rec['matched_skills'] + rec['missing_skills'], rec['role'])
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📚 Learn These Skills:")
                st.markdown(suggest_learning_links(rec['missing_skills']))
                st.markdown("---")

            # ⬇️ Download Button
            df_download = pd.DataFrame(recommendations[:3])
            csv_data = df_download.to_csv(index=False)
            st.download_button("📥 Download Recommendations", data=csv_data, file_name="role_recommendations.csv", mime="text/csv")

        # 🧠 Session Save
        st.session_state["soft_skills"] = soft_skills
        st.session_state["user_input"] = user_input
