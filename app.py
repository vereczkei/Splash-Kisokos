import streamlit as st
import os
import base64

# 1. Oldal alapbeállításai
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

# Képkereső függvény a háttérképekhez
def get_bg_img(name_no_ext):
    for ext in [".jpg", ".jpeg", ".png"]:
        path = name_no_ext + ext
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""

gep_bg = get_bg_img("gep")
tori_bg = get_bg_img("tori")
logo_bg = get_bg_img("logo") # Beolvassuk a logót is kódként a biztos központosításhoz

# 2. DESIGN CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; overflow-x: hidden; }}

    /* HÁTTÉRKÉPEK A SZÉLEKEN */
    .stApp::before {{
        content: ""; position: fixed; left: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{gep_bg}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}
    .stApp::after {{
        content: ""; position: fixed; right: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{tori_bg}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}

    /* KÖZÉPSŐ TARTALOM */
    .block-container {{
        max-width: 750px !important; padding: 2rem !important;
        background-color: rgba(14, 17, 23, 0.9);
        position: relative; z-index: 2; min-height: 100vh;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
        margin: auto;
    }}

    /* LOGÓ ABSZOLÚT KÖZÉPRE IGAZÍTÁSA */
    .centered-logo-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 25px;
    }}
    .centered-logo-wrapper img {{
        max-width: 350px;
        height: auto;
    }}

    /* UI ELEMEK */
    .partner-card {{
        background-color: #1e1e1e; padding: 25px; border-radius: 15px;
        border-left: 8px solid #007bff; color: white;
    }}
    div.stButton > button {{
        border-radius: 12px; background-color: #007bff; color: white;
        height: 3.2em; width: 100%; font-weight: bold; border: none;
    }}

    @media (max-width: 1100px) {{
        .stApp::before, .stApp::after {{ display: none !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. TARTALOM
# Logó megjelenítése fix középre igazítással
if logo_bg:
    st.markdown(f"""
        <div class="centered-logo-wrapper">
            <img src="data:image/png;base64,{logo_bg}" alt="Logo">
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def get_partners():
    if not os.path.exists('mosoda_adatbazis.txt'): return {}
    with open('mosoda_adatbazis.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    db = {}
    for item in txt.split('#'):
        if item.strip():
            rows = item.strip().split('\n')
            db[rows[0].strip().lower()] = {"name": rows[0].strip(), "txt": '\n'.join(rows[1:]).strip()}
    return db

db = get_partners()

st.write("### 🔍 Keresés")
c1, c2 = st.columns([4, 1.2])
with c1:
    search = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")
with c2:
    trigger = st.button("OK ➔")

if search or trigger:
    key = search.lower().strip()
    match = None
    for k in db:
        if key in k:
            match = db[k]
            break
    
    if match:
        st.write(f"### 📋 {match['name']}")
        st.markdown(f'<div class="partner-card">{match["txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        
        # Partner saját képe
        for e in ['.jpg', '.jpeg', '.png']:
            img_path = f"{match['name'].lower()}{e}"
            if os.path.exists(img_path):
                st.write("")
                st.image(img_path, use_container_width=True)
    elif key:
        st.error("Nincs ilyen partner.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>🫧 Splash Mosoda - 2026</p>", unsafe_allow_html=True)