import streamlit as st
import pandas as pd
import openai
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide")
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💸 AI-Powered Financial Reconciliation Tool")
st.write("Upload two financial files (Bank Statement & Invoices). The app will reconcile them using GPT embeddings.")

file_a = st.file_uploader("📂 Upload Bank Statement (Excel)", type=["xlsx"])
file_b = st.file_uploader("📂 Upload Invoices (Excel)", type=["xlsx"])

def get_embedding(text):
    response = openai.Embedding.create(input=[text], model="text-embedding-3-small")
    return response['data'][0]['embedding']

def preprocess_bank(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = df['Credit Amount'].fillna(0)
    df['Transaction ID'] = df['Customer Ref #'].astype(str)
    df['Description'] = df['Description'].astype(str).fillna('')
    df = df[['Date', 'Transaction ID', 'Amount', 'Description']].dropna(subset=['Date'])
    df['embedding'] = df['Description'].apply(get_embedding)
    return df

def preprocess_invoice(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Transaction ID'] = df['No.'].astype(str)
    df['Description'] = 'Invoice ' + df['Transaction ID']
    df['Amount'] = df['Amount'].astype(float)
    df = df[['Date', 'Transaction ID', 'Amount', 'Description']].dropna(subset=['Date'])
    df['embedding'] = df['Description'].apply(get_embedding)
    return df

if file_a and file_b:
    df_bank = pd.read_excel(file_a, sheet_name=0)
    df_invoice = pd.read_excel(file_b, sheet_name=0)

    with st.spinner("🔄 Processing and embedding..."):
        bank = preprocess_bank(df_bank)
        invoice = preprocess_invoice(df_invoice)

        matches = []
        used = set()

        for i, b in bank.iterrows():
            best_score, best_index, best_match = 0, None, None
            for j, inv in invoice.iterrows():
                if j in used:
                    continue
                if abs((b['Date'] - inv['Date']).days) > 5 or abs(b['Amount'] - inv['Amount']) > 10:
                    continue
                score = cosine_similarity([b['embedding']], [inv['embedding']])[0][0]
                if score > best_score:
                    best_score = score
                    best_index = j
                    best_match = inv

            if best_score > 0.75:
                used.add(best_index)
                matches.append({
                    "file_a_entry": b.drop('embedding').to_dict(),
                    "file_b_entry": best_match.drop('embedding').to_dict(),
                    "confidence_score": round(best_score, 2),
                    "match_reason": "Semantic + date/amount match"
                })

        unmatched_a = bank[~bank['Transaction ID'].isin([m['file_a_entry']['Transaction ID'] for m in matches])]
        unmatched_b = invoice.drop(index=used)

        output = {
            "matches": matches,
            "unmatched_file_a_entries": unmatched_a.drop(columns='embedding').to_dict(orient='records'),
            "unmatched_file_b_entries": unmatched_b.drop(columns='embedding').to_dict(orient='records')
        }

    st.success("✅ Reconciliation Complete!")
    st.json(output)
