import streamlit as st
import json
import os
from urllib.parse import quote

# 1. Page Config
st.set_page_config(page_title="Mateco Hardware", page_icon="🏗️", layout="centered")

# 2. Data Loading
def load_data():
    if os.path.exists('inventory.json'):
        with open('inventory.json', 'r') as f:
            return json.load(f)
    return []

# 3. Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1A1A; }
    .trust-bar {
        background-color: #1A1A1A; color: white; padding: 8px;
        border-radius: 8px; font-size: 11px; display: flex;
        justify-content: space-around; margin-bottom: 15px;
    }
    div[data-testid="column"] button {
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 10px !important;
    }
    .price-tag { color: #B42318; font-size: 18px; font-weight: 800; }
    .product-name { font-size: 15px; font-weight: 700; color: #101828; }
    .spec-label { color: #667085; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. TRUST HEADER ---
st.markdown('<div class="trust-bar"><span>📍 Kicukiro, Kigali</span><span>🚚 Delivery Available</span><span>✅ Official Stock</span></div>', unsafe_allow_html=True)

# --- 2. LOGO & SEARCH ---
st.markdown("<h3 style='margin-bottom:0;'>🏗️ MATECO STEEL</h3>", unsafe_allow_html=True)
search_query = st.text_input("", placeholder="Search sizes (e.g. 40x40, 1.5mm...)")

# --- 3. CATEGORY FILTERING ---
if 'filter' not in st.session_state:
    st.session_state.filter = "All"

st.write("**Shop by Category:**")
cat_cols = st.columns(4)
with cat_cols[0]:
    if st.button("🏠 ALL", use_container_width=True): st.session_state.filter = "All"
with cat_cols[1]:
    if st.button("⬛ TUBES", use_container_width=True): st.session_state.filter = "Tube"
with cat_cols[2]:
    if st.button("📐 ANGLE", use_container_width=True): st.session_state.filter = "Bar"
with cat_cols[3]:
    if st.button("⭕ PIPES", use_container_width=True): st.session_state.filter = "Pipe"

# --- 4. PRODUCT LISTING ---
all_products = load_data()
products = all_products

if st.session_state.filter != "All":
    products = [p for p in products if p.get('category') == st.session_state.filter]

if search_query:
    products = [p for p in products if search_query.lower() in p['name'].lower() or search_query in str(p['w'])]

st.markdown(f"**Showing:** `{st.session_state.filter}` ({len(products)} items)")

for p in products:
    with st.container():
        img_col, info_col, action_col = st.columns([1, 1.5, 1.2])
        
        with img_col:
            img_name = p.get('image_url', '').strip()
            img_path = os.path.join("images", img_name)
            if img_name and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/150/F2F4F7/667085?text=Mateco", use_container_width=True)
        
        with info_col:
            st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price-tag'>{p['price']:,} RWF</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='spec-label'>{p['w']}x{p['h']} | {p['t']}mm</div>", unsafe_allow_html=True)
            
        with action_col:
            qty = st.number_input("Qty", min_value=1, value=1, key=f"q_{p['id']}", label_visibility="collapsed")
            msg = quote(f"Hello Mateco! I'd like to order: {p['name']} ({p['w']}x{p['h']}x{p['t']}mm) x{qty}pcs.")
            st.link_button("ORDER", f"https://wa.me/250788000000?text={msg}", type="primary", use_container_width=True)
        
        st.markdown("<hr style='margin:10px 0; border:0.1px solid #EEE'>", unsafe_allow_html=True)

st.caption("Mateco Digital Inventory v1.3 | Kicukiro Warehouse")