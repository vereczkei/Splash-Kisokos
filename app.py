import streamlit as st
import os
import base64

# 1. Oldal alapbeállításai
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="wide")

# Képkezelő függvény a fix elemekhez (Hátterek és Logó)
def get_img_64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Háttérképek és logó betöltése
gep_path = "gep.jpg" if os.path.exists("gep.jpg") else "gep.jpeg"
tori_path = "tori.jpg" if os.path.exists("tori.jpg") else "tori.jpeg"

gep_64 = get_img_64(gep_path)
tori_64 = get_img_64(tori_path)
logo_64 = get_img_64("logo.png")

# 2. DESIGN CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; overflow-x: hidden; }}
    
    /* FIX OLDALSÓ KÉPEK */
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
        max-width: 800px !important; padding: 2rem !important;
        background-color: rgba(14, 17, 23, 0.95);
        position: relative; z-index: 2; min-height: 100vh;
        margin: auto; box-shadow: 0 0 50px rgba(0,0,0,0.9);
    }}

    .logo-box {{ display: flex; justify-content: center; width: 100%; margin-bottom: 20px; }}
    .logo-box img {{ max-width: 350px; height: auto; }}

    .partner-card {{
        background-color: #1e1e1e; padding: 25px; border-radius: 15px;
        border-left: 8px solid #007bff; color: white; margin-bottom: 20px;
        font-size: 1.1em;
    }}
    
    div.stButton > button {{
        border-radius: 12px; background-color: #007bff; color: white;
        height: 3.5em; width: 100%; font-weight: bold; border: none;
    }}

    @media (max-width: 1100px) {{
        .stApp::before, .stApp::after {{ display: none !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. TARTALOM MEGJELENÍTÉSE
if logo_64:
    st.markdown(f'<div class="logo-box"><img src="data:image/png;base64,{logo_64}"></div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_db():
    if not os.path.exists('mosoda_adatbazis.txt'): return {}
    with open('mosoda_adatbazis.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    db = {}
    for item in txt.split('#'):
        if item.strip():
            lines = item.strip().split('\n')
            name = lines[0].strip()
            db[name.lower()] = {"name": name, "txt": '\n'.join(lines[1:]).strip()}
    return db

db = load_db()

st.write("### 🔍 Keresés")
c1, c2 = st.columns([4, 1.2])
with c1:
    search = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")
with c2:
    ok = st.button("OK ➔")

if search or ok:
    k = search.lower().strip()
    match = None
    for key in db:
        if k in key:
            match = db[key]
            break
    
    if match:
        st.write(f"### 📋 {match['name']}")
        st.markdown(f'<div class="partner-card">{match["txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        
        # --- AUTOMATIKUS GALÉRIA ---
        with st.expander("🖼️ GALÉRIA - Képek megtekintése"):
            # Tisztított név a fájlkereséshez (szóközök nélkül)
            clean_name = match['name'].lower().replace(" ", "")
            
            # Megkeressük az összes képet, ami a névvel kezdődik (pl. aurea_1, aurea_2...)
            found_images = []
            # Akár 20 képig is elszámolunk, hogy később is elég legyen
            for i in range(1, 21):
                for ext in ['.jpg', '.jpeg', '.png']:
                    path = f"{clean_name}_{i}{ext}"
                    if os.path.exists(path):
                        found_images.append(path)
                        break # Ha megvan a fájl, a többi kiterjesztést nem nézzük ehhez a számhoz

            if found_images:
                # 2 oszlopos rácsba rendezzük
                cols = st.columns(2)
                for idx, img_path in enumerate(found_images):
                    with cols[idx % 2]:
                        st.image(img_path, use_container_width=True, caption=f"Fotó {idx+1}")
            else:
                st.info("Ehhez a partnerhez jelenleg nincsenek feltöltött képek.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>🫧 Splash Mosoda - 2026</p>", unsafe_allow_html=True)