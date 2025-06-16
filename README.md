# 🎓 AI MentorBot: Career Role Recommender

AI MentorBot is a smart resume analyzer that recommends the best-fit career roles based on your skills. Upload your resume or paste your experience, and get:

- 🎯 Top 3 matching job roles with match percentage
- 📚 Missing skills with YouTube & roadmap links
- 📈 Radar charts to compare your skills vs. role needs
- 📥 Downloadable role recommendation CSV

---

## 🚀 Live Demo

👉 [Click here to try the app!](https://your-app-url.streamlit.app)  
*(Update this link after deployment to Streamlit Cloud or other hosting)*

---

## 🧠 How It Works

1. Upload your resume (PDF) or paste your experience text.
2. The app extracts your technical and soft skills using NLP.
3. Semantic matching compares your skills to role requirements.
4. Visual insights and learning paths are suggested.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/MentorBot.git
cd ai-mentorbot
pip install -r requirements.txt
streamlit run app.py
````

---

## 📁 Folder Structure

```
ai-mentorbot/
├── app.py
├── data/
│   └── roles_data.csv
├── utils/
│   ├── recommender.py
│   ├── soft_skill_extractor.py
│   └── visuals.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – frontend & UI
* **Sentence Transformers** – for semantic matching
* **Plotly** – radar charts
* **pdfplumber** – extract resume text
* **pandas** – data processing

---

## 📚 Data Format: `roles_data.csv`

| role               | required\_skills                                     | recommended\_courses                                    |
| ------------------ | ---------------------------------------------------- | ------------------------------------------------------- |
| Data Scientist     | python, pandas, statistics, machine learning         | Coursera: Applied Data Science, Udemy: Python for DS    |
| AI Researcher      | python, deep learning, pytorch, tensorflow, nlp      | Coursera: Deep Learning Specialization, HuggingFace NLP |
| Frontend Developer | html, css, javascript, react, git, responsive design | FreeCodeCamp: Frontend Dev, Udemy: React Bootcamp       |

---

## 🔗 Resources

* [Streamlit Documentation](https://docs.streamlit.io/)
* [HuggingFace Transformers](https://huggingface.co/sentence-transformers)
---

## 📬 Contact

Built with ❤️ by [Syed Mohammad Nasir Hussain](https://www.linkedin.com/in/syed-mohammad-nasir-hussain-920b2a132/)

Email: [mdnasir020396@gmail.com](mailto:mdnasir020396@gmail.com)

Feel free to contribute, suggest ideas, or raise issues!

---
