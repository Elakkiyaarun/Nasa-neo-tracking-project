import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# ✅ Set Streamlit Page Configuration
st.set_page_config(page_title="🛍️ Product Recommender", layout="centered")


# ---------------------------------------------
# 📥 Load the cleaned Dataset
# ---------------------------------------------
df = pd.read_csv("C:/Users/admin/guvi 2025/project4/cleaned_dta.csv")  
   
# ---------------------------------------------
# 🔍 Build Item Similarity Matrix
# ---------------------------------------------
@st.cache_resource
def build_similarity_matrix(df):
    product_matrix = df.pivot_table(
        index='CustomerID',
        columns='Description',
        values='Quantity',
        aggfunc='sum',
        fill_value=0
    )
    similarity = cosine_similarity(product_matrix.T)
    sim_df = pd.DataFrame(similarity, index=product_matrix.columns, columns=product_matrix.columns)
    return sim_df

item_similarity_df = build_similarity_matrix(df)

# ---------------------------------------------
# 🔁 Recommendation Function
# ---------------------------------------------
def recommend_products(product_name, top_n=5):
    if product_name not in item_similarity_df.columns:
        return []
    scores = item_similarity_df[product_name].sort_values(ascending=False)
    return scores[1:top_n+1].index.tolist()

# -----------------------------
# 🧠 Load KMeans Model & Scaler
# -----------------------------

with open("C:/Users/admin/guvi 2025/project4/kmeans_model.pkl", "rb") as f:
    kmeans = pickle.load(f)
with open("C:/Users/admin/guvi 2025/project4/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
# -----------------------------
# 🔳 Sidebar Navigation
# -----------------------------
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "👥 Customer Clustering", "🛍️ Recommendations"])

# =====================
# 🏠 HOME PAGE
# =====================
if page == "🏠 Home":
    st.title("🛍️ Shopper Spectrum App")
    st.markdown("""
    Welcome to the **Shopper Spectrum App**!  
    Use the sidebar to explore:
    - 🛍️ Product recommendations
    - 👥 Customer segmentation
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/263/263115.png", width=150)

# =====================
# 🛍️ RECOMMENDATION PAGE
# =====================
elif page == "🛍️ Recommendations":
    st.header("📦 Product Recommendation")

    product_input = st.text_input("🔍 Enter Product Name:")

    if st.button("Get Recommendations"):
        matches = [p for p in item_similarity_df.columns if product_input.lower() in str(p).lower()]
        if not matches:
            st.error("❌ No matching product found.")
        else:
            product = matches[0]
            st.success(f"✅ Showing recommendations for: **{product}**")
            recs = recommend_products(product)
            if recs:
                for i, rec in enumerate(recs, 1):
                    st.markdown(f"""
                    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;margin:5px 0;">
                        <b>{i}. {rec}</b>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No similar products found.")

# =====================
# 👥 CUSTOMER SEGMENTATION
# =====================
elif page == "👥 Customer Clustering":
    st.header("👤 Customer Segmentation (RFM)")

    recency = st.number_input("📆 Recency (days)", min_value=0, value=30)
    frequency = st.number_input("🔁 Frequency (total purchases)", min_value=0, value=10)
    monetary = st.number_input("💰 Monetary (total spend)", min_value=0.0, value=500.0)

    if st.button("Predict Cluster"):
        input_data = [[recency, frequency, monetary]]
        input_scaled = scaler.transform(input_data)
        cluster_label = kmeans.predict(input_scaled)[0]

        cluster_names = {
            0: "High-Value",
            1: "Regular",
            2: "Occasional",
            3: "At-Risk"
        }
        segment = cluster_names.get(cluster_label, f"Cluster {cluster_label}")
        st.success(f"🧠 Predicted Segment: **{segment}** (Cluster {cluster_label})")