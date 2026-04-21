import streamlit as st
import os
import base64

# 1. Beállítás: 'wide' mód, hogy legyen hely kétoldalt
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

# Segédfüggvény a képek háttérbe rakásához
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

gep_64 = get_base64("gep.jpeg")
tori_64 = get_base64("tori.jpeg")

# 2. BRUTÁLIS DESIGN CSS
# Itt adjuk meg, hogy a képek fixen bal és jobb szélen legyenek
st.markdown(f"""
    <style>
    /* Háttérképek beállítása */
    .stApp {{
        background-color: #0e1117;
    }}
    
    /* Bal oldali kép dekoráció */
    .stApp::before {{
        content: "";
        position: fixed;
        left: 0;
        top: 0;
        width: 20%; /* A képernyő 20%-át foglalja el */
        height: 100vh;
        background-image: url("data:image/jpeg;base64,{gep_64}");
        background-size: cover;
        background-position: center;
        opacity: 0.4; /* Kicsit átlátszó, hogy ne legyen zavaró */
        z-index: 0;
    }}

    /* Jobb oldali kép dekoráció */
    .stApp::after {{
        content: "";
        position: fixed;
        right: 0;
        top: 0;
        width: 20%;
        height: 100vh;
        background-image: url("data:image/jpeg;base64,{tori_64}");
        background-size: cover;
        background-position: center;
        opacity: 0.4;
        z-index: 0;
    }}

    /* A tartalom középre kényszerítése és elválasztása a háttértől */
    .block-container {{
        max-width: 800px !important;
        padding-top: 2rem !important;
        background-color: rgba(14, 17, 23, 0.9); /* Kissé sötétített háttér a tartalom alatt */
        z-index: 1;
        position: relative;
        box-shadow: 0 0 50px rgba(0,0,0,1);
    }}

    /* Mobil optimalizálás: Mobilon ne legyenek ott az oldalsó képek */
    @media (max-width: 1100px) {{
        .stApp::before, .stApp::after {{
            display: none !important;
        }}
        .block-container {{
            max-width: 100% !important;
        }}
    }}

    /* Kártya és Gomb stílusok */
    .partner-card {{
        background-color: #1e1e1e;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #007bff;
        color: #f0f0f0;
    }}
    div.stButton > button {{
        border-radius: 15px;
        background-color: #007bff;
        color: white;
        height: 3.2em;
        width: 100%;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. TARTALOM (Csak a lényeg)
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def get_data():
    fajl = 'mosoda_adatbazis.txt'
    if not os.path.exists(fajl): return {}
    with open(fajl, 'r', encoding='utf-8') as f:
        content = f.read()
    partners = {}
    for section in content.split('#'):
        if section.strip():
            lines = section.strip().split('\n')
            name = lines[0].strip()
            info = '\n'.join(lines[1:]).strip()
            partners[name.lower()] = {"original_name": name, "info": info}
    return partners

data = get_data()

# Kereső
col_in, col_btn = st.columns([4, 1.2])
with col_in:
    ceg_nev = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")
with col_btn:
    ok = st.button("OK ➔")

if ceg_nev or ok:
    k = ceg_nev.lower().strip()
    res = None
    for key in data:
        if k in key:
            res = data[key]
            break
    
    if res:
        st.markdown(f"### 📋 {res['original_name']}")
        st.markdown(f'<div class="partner-card">{res["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        # Partner saját képe
        for ext in ['.jpg', '.jpeg', '.png']:
            p = f"{res['original_name'].lower()}{ext}"
            if os.path.exists(p):
                st.write("")
                st.image(p, use_container_width=True)
    elif k:
        st.error("Nincs találat.")

st.markdown("<br><br>---")
st.caption("🫧 Splash Mosoda - 2026")