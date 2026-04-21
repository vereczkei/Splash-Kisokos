import streamlit as st
import os
import base64

# 1. Oldal alapbeállításai
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

# CSS - MOBILBARÁT DESIGN
st.markdown("""
    <style>
    /* Oldalsó díszek CSAK nagy képernyőn (1000px felett) */
    @media (min-width: 1000px) {
        .side-decor-left {
            position: fixed; left: 10px; top: 50%; transform: translateY(-50%);
            width: 200px; opacity: 0.6; z-index: -1;
        }
        .side-decor-right {
            position: fixed; right: 10px; top: 50%; transform: translateY(-50%);
            width: 200px; opacity: 0.6; z-index: -1;
        }
    }
    
    /* Mobilon (1000px alatt) elrejtjük a díszeket */
    @media (max-width: 999px) {
        .side-decor-left, .side-decor-right { display: none !important; }
        h1 { font-size: 1.8em !important; } /* Kisebb cím mobilon */
    }
    
    /* Tartalom kerete */
    .main-container {
        max-width: 700px;
        margin: auto;
        padding: 10px;
    }

    /* Kereső gomb és mező */
    div.stButton > button {
        width: 100%; border-radius: 15px; height: 3.2em;
        background-color: #007bff; color: white; border: none; font-weight: bold;
    }
    .stTextInput > div > div > input {
        border-radius: 15px; border: 2px solid #007bff; background-color: #121212; color: white;
    }

    /* Partner kártya - mobilon is jól olvasható */
    .partner-card {
        background-color: #1e1e1e; padding: 20px; border-radius: 15px;
        border-left: 8px solid #007bff; color: #f0f0f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        font-size: 1.05em; line-height: 1.5;
    }
    h1 { text-align: center; color: white; font-family: 'Arial Black'; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# Díszítő képek betöltése (gep.jpeg és tori.jpeg)
img_l = get_base64("gep.jpeg")
if img_l: st.markdown(f'<img src="data:image/jpeg;base64,{img_l}" class="side-decor-left">', unsafe_allow_html=True)

img_r = get_base64("tori.jpeg")
if img_r: st.markdown(f'<img src="data:image/jpeg;base64,{img_r}" class="side-decor-right">', unsafe_allow_html=True)

# TARTALOM
st.markdown('<div class="main-container">', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.image("logo.png", use_container_width=True)

st.markdown("<h1>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def get_data():
    fajl = 'mosoda_adatbazis.txt'
    if not os.path.exists(fajl): return {}
    with open(fajl, 'r', encoding='utf-8') as f: content = f.read()
    partners = {}
    for section in content.split('#'):
        if section.strip():
            lines = section.strip().split('\n')
            name = lines[0].strip()
            info = '\n'.join(lines[1:]).strip()
            partners[name.lower()] = {"original_name": name, "info": info}
    return partners

data = get_data()

st.write("### 🔍 Keresés")
# Mobilon a két oszlop egymás alá kerülhet, ha túl szűk, de a Streamlit jól kezeli
c_in, c_btn = st.columns([4, 1.5])
with c_in:
    ceg_nev = st.text_input("", placeholder="Név...", label_visibility="collapsed")
with c_btn:
    ok = st.button("OK ➔")

if ceg_nev or ok:
    k = ceg_nev.lower().strip()
    res = None
    if k:
        for key in data:
            if k in key:
                res = data[key]
                break
        if res:
            st.markdown(f"### 📋 {res['original_name']}")
            st.markdown(f'<div class="partner-card">{res["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            # Partner fotók (pl. mika.jpg)
            for ext in ['.jpg', '.jpeg', '.png']:
                path = f"{res['original_name'].lower()}{ext}"
                if os.path.exists(path):
                    st.write("")
                    st.image(path, use_container_width=True)
        else:
            st.error("Nincs találat.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>---")
st.caption("🫧 Splash Mosoda - Mobil-optimalizált verzió")