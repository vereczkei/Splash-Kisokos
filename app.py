import streamlit as st
import os

# 1. Oldal alapbeállításai
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧", layout="centered")

# CSS a vizuális tuninghoz (Gomb és beviteli mező)
st.markdown("""
    <style>
    /* Keresőmező és OK gomb egy sorba rendezése */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3.1em;
        background-color: #007bff;
        color: white;
        border: none;
        margin-top: 1px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #007bff;
        background-color: #121212;
        color: white;
    }
    /* Szabályzat kártya */
    .partner-card {
        background-color: #1e1e1e;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #007bff;
        color: #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-size: 1.1em;
    }
    h1 { text-align: center; color: white; font-family: 'Arial Black'; }
    </style>
    """, unsafe_allow_html=True)

# Logó
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h1>Splash Mosoda Kisokos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Gyors, pontos, digitális tudástár</p>", unsafe_allow_html=True)
st.markdown("---")

# Adatbázis betöltése
@st.cache_data
def get_data():
    fajl = 'mosoda_adatbazis.txt'
    if not os.path.exists(fajl): return {}
    with open(fajl, 'r', encoding='utf-8') as f:
        content = f.read()
    partners = {}
    sections = content.split('#')
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            name = lines[0].strip()
            info = '\n'.join(lines[1:]).strip()
            partners[name.lower()] = {"original_name": name, "info": info}
    return partners

data = get_data()

# KERESŐ SÁV ÉS A KÉRT NYILAS GOMB
st.write("### 🔍 Melyik partnert keresed?")
col_input, col_button = st.columns([5, 1.2])

with col_input:
    # A gépeléshez használt mező
    ceg_nev = st.text_input("", placeholder="Partner neve...", label_visibility="collapsed")

with col_button:
    # A fektetett háromszög/nyíl gomb
    kereses_indit = st.button("OK ➔")

# Keresési logika
if ceg_nev or kereses_indit:
    keresett = ceg_nev.lower().strip()
    talalat = None
    
    if keresett:
        for kulcs in data:
            if keresett in kulcs:
                talalat = data[kulcs]
                break
        
        if talalat:
            st.write("") # Térköz
            st.markdown(f"### 📋 {talalat['original_name']} szabályzata:")
            st.markdown(f'<div class="partner-card">{talalat["info"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            # Kép keresése (ha van feltöltve)
            for ext in ['.jpg', '.png', '.jpeg']:
                img_path = f"{talalat['original_name'].lower()}{ext}"
                if os.path.exists(img_path):
                    st.write("")
                    st.image(img_path, use_container_width=True)
        else:
            st.error("Nincs találat. Próbáld meg máshogy írni!")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("🫧 Splash Mosoda - 2026 | Minden jog fenntartva")