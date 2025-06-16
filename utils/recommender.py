from sentence_transformers import SentenceTransformer, util
from utils.soft_skill_extractor import extract_keywords

# Load pre-trained semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(user_skills, role_skills, threshold=0.6):
    user_skills = [s.strip().lower() for s in user_skills]
    role_skills = [s.strip().lower() for s in role_skills]

    # Encode user and role skills
    user_embs = model.encode(user_skills, convert_to_tensor=True)
    role_embs = model.encode(role_skills, convert_to_tensor=True)

    matched = set()
    for i, role_skill in enumerate(role_skills):
        cos_scores = util.cos_sim(role_embs[i], user_embs)
        max_score = float(cos_scores.max())
        if max_score >= threshold:
            matched.add(role_skill)

    return list(matched)

def recommend_roles(user_text, df_roles, threshold=0.6):
    # Extract user skills from input text
    user_skills = extract_keywords(user_text)

    results = []

    for _, row in df_roles.iterrows():
        role_skills = [s.strip().lower() for s in row["required_skills"].split(",")]

        matched = semantic_match(user_skills, role_skills, threshold)

        match_percent = round(100 * len(matched) / len(role_skills), 2)
        missing = list(set(role_skills) - set(matched))

        results.append({
            "role": row["role"],
            "match": match_percent,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommended_courses": row["recommended_courses"],
            "required_skills": role_skills  # Needed for radar charts
        })

    return sorted(results, key=lambda x: x["match"], reverse=True)
