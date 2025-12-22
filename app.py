import streamlit as st
import json
import os
from urllib.parse import quote

# 1. Page Config
st.set_page_config(page_title="Mateco Hardware", page_icon="🏗️", layout="centered")

# 2. Function to read data directly from the JSON file
def load_data():
    if os.path.exists('inventory.json'):
        with open('inventory.json', 'r') as f:
            return json.load(f)
    return []

# 3. Professional UI Styling (Clean White Theme)
st.markdown("""
    <style>
    /* Light Theme Background */
    .stApp { background-color: #FFFFFF; color: #333333; }
    
    /* Search Bar - Rounded & Light Grey */
    .stTextInput input {
        background-color: #F0F2F5 !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 20px !important;
        color: #333 !important;
    }

    /* Category Section Styling */
    .cat-item { text-align: center; width: 80px; }
    .cat-circle {
        width: 65px; height: 65px; background-color: #F8F9FA;
        border-radius: 50%; margin: 0 auto; display: flex;
        align-items: center; justify-content: center; font-size: 24px;
        border: 1px solid #E9ECEF;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .cat-label { font-size: 10px; font-weight: 700; margin-top: 8px; color: #444; text-transform: uppercase; }

    /* Promo Banner */
    .promo-banner {
        background: linear-gradient(135deg, #1a1a1a 0%, #444 100%);
        border-radius: 15px; padding: 25px; color: white; margin-bottom: 25px;
    }

    /* Bottom Navigation Bar */
    .bottom-nav {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: white; border-top: 1px solid #EEE;
        padding: 10px 0; display: flex; justify-content: space-around; z-index: 1000;
    }
    .nav-item { text-align: center; font-size: 10px; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# --- TOP SECTION ---
st.markdown("<h2 style='text-align: center; color: #1a1a1a; margin-bottom: 0;'>MATECO</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; color: #888; margin-top: 0;'>CONSTRUCTION MATERIALS</p>", unsafe_allow_html=True)

# Search Bar
search_query = st.text_input("", placeholder="🔍 Search for steel, cement, tools...")

# --- PROMO BANNER ---
st.markdown("""
    <div class="promo-banner">
        <h3 style="margin:0; font-size: 20px;">Quality Steel Materials</h3>
        <p style="margin:0; opacity:0.8; font-size: 12px;">Fast Delivery · Best Prices in Kigali</p>
    </div>
    """, unsafe_allow_html=True)

# --- CATEGORIES SECTION ---
st.markdown("<p style='font-weight: bold; margin-bottom: 15px;'>Shop By Categories</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<div class="cat-item"><div class="cat-circle">⬛</div><div class="cat-label">Steel<br>Tubes</div></div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="cat-item"><div class="cat-circle">⭕</div><div class="cat-label">Steel<br>Pipes</div></div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="cat-item"><div class="cat-circle">📄</div><div class="cat-label">Steel<br>Plates</div></div>', unsafe_allow_html=True)
with col4: st.markdown('<div class="cat-item"><div class="cat-circle">🦯</div><div class="cat-label">Iron<br>Bars</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PRODUCT LISTING ---
all_products = load_data()

# Simple Filter
if search_query:
    products = [p for p in all_products if search_query.lower() in p['name'].lower()]
else:
    products = all_products

if products:
    for p in products:
        with st.container():
            c1, c2 = st.columns([1.2, 2])
            
            with c1:
                # SAFE IMAGE LOADING
                img_name = p.get('image_url', '').strip()
                if img_name:
                    img_path = os.path.join("images", img_name)
                    if os.path.exists(img_path) and os.path.isfile(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/150/f8f9fa/cccccc?text=Mateco", use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150/f8f9fa/cccccc?text=Mateco", use_container_width=True)
            
            with c2:
                st.markdown(f"**{p['name']} {p['w']}x{p['h']}**")
                st.markdown(f"<p style='color:#B08D3E; font-weight:bold; font-size:18px; margin:0;'>{p['price']:,} RWF</p>", unsafe_allow_html=True)
                st.caption(f"{p['t']}mm gauge | 6m length")
                
                # Qty and Order
                q_col, b_col = st.columns([1, 2.5])
                with q_col:
                    qty = st.number_input("Qty", min_value=1, value=1, key=f"q_{p['id']}", label_visibility="collapsed")
                with b_col:
                    msg = quote(f"Hello! I'd like to order {qty} pcs of {p['name']} {p['w']}x{p['h']} ({p['t']}mm).")
                    st.link_button("Order Now", f"https://wa.me/250788000000?text={msg}")
            
            st.markdown("<hr style='border: 0.1px solid #F0F2F5;'>", unsafe_allow_html=True)
else:
    st.info("No products found.")

# --- BOTTOM NAVIGATION ---
st.markdown("""
    <div style="height: 80px;"></div>
    <div class="bottom-nav">
        <div class="nav-item">🏠<br>Home</div>
        <div class="nav-item">📑<br>Categories</div>
        <div class="nav-item">🛒<br>Cart</div>
        <div class="nav-item">👤<br>Account</div>
    </div>
    """, unsafe_allow_html=True)