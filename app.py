import streamlit as st
import os
import base64

# 1. Alapbeállítások
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

# Képkezelő függvény
def get_img_64(name_without_ext):
    for ext in [".jpg", ".jpeg", ".png"]:
        path = name_without_ext + ext
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""

gep_64 = get_img_64("gep")
tori_64 = get_img_64("tori")

# 2. DESIGN + ANIMÁCIÓ (CSS)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; overflow-x: hidden; }}

    /* OLDALSÓ KÉPEK - Fixálva a széleken */
    .stApp::before {{
        content: ""; position: fixed; left: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{gep_64}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}
    .stApp::after {{
        content: ""; position: fixed; right: 0; top: 0; width: 25%; height: 100vh;
        background-image: url("data:image/jpeg;base64,{tori_64}");
        background-size: cover; background-position: center; opacity: 0.5; z-index: 0;
    }}

    /* KÖZÉPSŐ TARTALOM */
    .block-container {{
        max-width: 750px !important; padding: 2rem !important;
        background-color: rgba(14, 17, 23, 0.9);
        position: relative; z-index: 2; min-height: 100vh;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
    }}

    /* BUBORÉK ANIMÁCIÓ A LOGÓ MÖGÉ */
    .bubble-container {{
        position: relative; width: 100%; height: 250px; 
        display: flex; justify-content: center; align-items: center;
        overflow: hidden;
    }}
    .bubble {{
        position: absolute; bottom: -20px; background: rgba(255, 255, 255, 0.3);
        border-radius: 50%; animation: rise 4s infinite ease-in; z-index: 1;
    }}
    @keyframes rise {{
        0% {{ transform: translateY(0) scale(1); opacity: 0.5; }}
        100% {{ transform: translateY(-200px) scale(1.5); opacity: 0; }}
    }}

    /* Partner kártya és Gomb */
    .partner-card {{
        background-color: #1e1e1e; padding: 25px; border-radius: 15px;
        border-left: 8px solid #007bff; color: white;
    }}
    div.stButton > button {{
        border-radius: 12px; background-color: #007bff; color: white;
        height: 3.2em; width: 100%; font-weight: bold; border: none;
    }}

    @media (max-width: 1000px) {{
        .stApp::before, .stApp::after {{ display: none !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. TARTALOM MEGJELENÍTÉSE
# Buborékok generálása HTML-ben (a logó alá/mögé)
bubbles_html = "".join([f'<div class="bubble" style="left:{i*15}%; width:{10+i*5}px; height:{10+i*5}px; animation-delay:{i*0.5}s;"></div>' for i in range(6)])

st.markdown(f'<div class="bubble-container">{bubbles_html}', unsafe_allow_html=True)
if os.path.exists("logo.png"):
    st.image("logo.png", width=300) # Itt a logó a buborékok "előtt"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
st.markdown("---")

# Adatbázis betöltés
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

# Kereső felület
st.write("### 🔍 Keresés")
c_in, c_btn = st.columns([4, 1.2])
with c_in:
    ceg_nev = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")
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
            st.write(f"### 📋 {res['name']}")
            st.markdown(f'<div class="partner-card">{res["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            # Partner saját fotója
            for ext in ['.jpg', '.jpeg', '.png']:
                img_p = f"{res['name'].lower()}{ext}"
                if os.path.exists(img_p):
                    st.image(img_p, use_container_width=True)
        else:
            st.error("Nincs találat.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>🫧 Splash Mosoda - 2026</p>", unsafe_allow_html=True)