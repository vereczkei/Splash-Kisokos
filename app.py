import streamlit as st
import os

# 1. Oldal alapbeállítása (layout='centered' a legjobb mobilon!)
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="centered")

# 2. Design (CSS) - Mobilon elrejtjük a díszeket, asztalin szépek
st.markdown("""
    <style>
    /* Elrejtjük az oldalsó díszeket kis képernyőn */
    @media (max-width: 1000px) {
        .decoration { display: none; }
    }
    /* Partner kártya stílusa */
    .partner-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #007bff;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* Gombok és kereső kerekítése */
    .stButton > button { border-radius: 15px; height: 3em; background-color: #007bff; color: white; border: none; }
    .stTextInput > div > div > input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Díszítő képek - Csak akkor rakjuk ki, ha NEM mobilról nézik
# (Ezt két oszloppal oldjuk meg a biztonság kedvéért)
if st.columns([1])[0].button is not None: # Trükk a szélesség ellenőrzésére
    col_left, col_main, col_right = st.columns([1, 3, 1])
else:
    col_main = st.container()

with col_main:
    # Logó és Cím
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Digitális Segédlet | 2026</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Adatbázis betöltése
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

    # Kereső rész
    st.write("### 🔍 Keresés")
    c_in, c_btn = st.columns([4, 1.2])
    with c_in:
        ceg_nev = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")
    with c_btn:
        ok = st.button("OK ➔")

    if ceg_nev or ok:
        k = ceg_nev.lower().strip()
        talalat = None
        for key in data:
            if k in key:
                talalat = data[key]
                break
        
        if talalat:
            st.markdown(f"### 📋 {talalat['original_name']}")
            st.markdown(f'<div class="partner-card">{talalat["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            # Partner képe (pl. mika.jpg)
            for ext in ['.jpg', '.jpeg', '.png']:
                p = f"{talalat['original_name'].lower()}{ext}"
                if os.path.exists(p):
                    st.image(p, use_container_width=True)
        elif k:
            st.error("Nincs ilyen partner.")

    st.markdown("---")
    st.caption("🫧 Splash Mosoda - Mobilbarát verzió")

# 4. Oldalsó díszek (Csak ha van hely és léteznek)
# A Streamlit 'sidebar'-ba rakjuk őket, így mobilon elrejthetők egy gombbal
if os.path.exists("gep.jpeg") or os.path.exists("tori.jpeg"):
    with st.sidebar:
        st.write("### 📸 Galéria")
        if os.path.exists("gep.jpeg"): st.image("gep.jpeg", caption="Gép")
        if os.path.exists("tori.jpeg"): st.image("tori.jpeg", caption="Törölközők")