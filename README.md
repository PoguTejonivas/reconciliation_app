# 💸 AI-Powered Financial Reconciliation Tool

This Streamlit web app allows users to upload two Excel files — a **Bank Statement** and an **Invoice Report** — and uses OpenAI's embedding model to intelligently reconcile financial transactions based on:
- Fuzzy matching of descriptions
- Date proximity
- Amount similarity

---

## 🚀 Features
- Upload `.xlsx` files for reconciliation.
- Uses OpenAI's `text-embedding-3-small` model for semantic matching.
- Outputs matched transactions with:
  - `file_a_entry`
  - `file_b_entry`
  - `confidence_score`
  - `match_reason`
- Displays unmatched entries from both files.

---

## 📁 File Structure
```
reconciliation_app/
├── app.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

## 🔧 Environment Variables

Set your OpenAI API key before running the app:

```bash
export OPENAI_API_KEY="your-key-here"
```

In Vercel:
- Go to Settings → Environment Variables
- Add: `OPENAI_API_KEY = your-key`

---

## 🧪 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment (Vercel Recommended)

1. Push this folder to GitHub.
2. Import the repo into [Vercel](https://vercel.com).
3. Set environment variable `OPENAI_API_KEY`.
4. Deploy.

---

## 📬 Contact
For questions or issues, contact your hackathon team or post in the support channel.
