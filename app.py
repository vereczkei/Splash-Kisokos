import streamlit as st
import os
import base64

# 1. Alapbeállítások
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

# Segédfüggvény a képek beolvasásához
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

gep_base64 = get_base64("gep.jpeg")
tori_base64 = get_base64("tori.jpeg")

# 2. DESIGN ÉS ELRENDEZÉS (CSS)
st.markdown(f"""
    <style>
    /* Háttér és alap stílus */
    .stApp {{ background-color: #0e1117; }}

    /* BAL OLDALI KÉP */
    .stApp::before {{
        content: ""; position: fixed; left: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{gep_base64}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}

    /* JOBB OLDALI KÉP */
    .stApp::after {{
        content: ""; position: fixed; right: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{tori_base64}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}

    /* KÖZÉPSŐ TARTALOM */
    .block-container {{
        max-width: 750px !important; padding: 2rem !important;
        background-color: rgba(14, 17, 23, 0.85);
        position: relative; z-index: 1; min-height: 100vh;
        box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }}

    /* MOBIL NÉZET: Díszek kikapcsolása */
    @media (max-width: 1000px) {{
        .stApp::before, .stApp::after {{ display: none !important; }}
        .block-container {{ max-width: 100% !important; background-color: #0e1117; }}
    }}

    /* Kártya stílus */
    .partner-card {{
        background-color: #1e1e1e; padding: 25px; border-radius: 15px;
        border-left: 8px solid #007bff; color: white; font-size: 1.1em;
    }}
    
    /* OK Gomb */
    div.stButton > button {{
        border-radius: 12px; background-color: #007bff; color: white;
        height: 3.2em; width: 100%; font-weight: bold; border: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. TARTALOM MEGJELENÍTÉSE
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.image("logo.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
st.markdown("---")

# Adatbázis függvény
@st.cache_data
def load_data():
    if not os.path.exists('mosoda_adatbazis.txt'): return {}
    with open('mosoda_adatbazis.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    partners = {}
    for section in content.split('#'):
        if section.strip():
            lines = section.strip().split('\n')
            name = lines[0].strip()
            info = '\n'.join(lines[1:]).strip()
            partners[name.lower()] = {"name": name, "info": info}
    return partners

data = load_data()

# Keresés
st.write("### 🔍 Keresés")
c_in, c_btn = st.columns([4, 1.2])
with c_in:
    ceg_nev = st.text_input("", placeholder="Írd be a partner nevét...", label_visibility="collapsed")
with c_btn:
    ok_gomb = st.button("OK ➔")

# Találat megjelenítése
if ceg_nev or ok_gomb:
    k = ceg_nev.lower().strip()
    talalat = None
    if k:
        for key in data:
            if k in key:
                talalat = data[key]
                break
        
        if talalat:
            st.write(f"### 📋 {talalat['name']}")
            st.markdown(f'<div class="partner-card">{talalat["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            # Partner saját fotója
            for ext in ['.jpg', '.jpeg', '.png']:
                img_p = f"{talalat['name'].lower()}{ext}"
                if os.path.exists(img_p):
                    st.write("")
                    st.image(img_p, use_container_width=True)
        else:
            st.error("Nincs találat. Ellenőrizd a nevet!")

# LÁBLÉC - Tisztán, kódok nélkül
st.write("")
st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>🫧 Splash Mosoda - 2026</p>", unsafe_allow_html=True)