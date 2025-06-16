import re
from difflib import get_close_matches

# Sample curated skill list (expand as needed)
KNOWN_SKILLS = [
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving", "adaptability",
    "time management", "critical thinking", "creativity", "collaboration",
    
    # Technical skills (for bonus matching)
    "python", "sql", "tableau", "excel", "power bi", "pandas", "numpy",
    "machine learning", "deep learning", "tensorflow", "pytorch", "aws",
    "data visualization", "statistics", "scikit-learn", "cloud", "nlp"
]

def extract_keywords(text):
    text = text.lower()
    words = set(re.findall(r"\b[a-zA-Z\#\+\-\.]{2,}\b", text))

    extracted = set()
    for word in words:
        matches = get_close_matches(word, KNOWN_SKILLS, n=1, cutoff=0.8)
        if matches:
            extracted.add(matches[0])

    return list(extracted)
