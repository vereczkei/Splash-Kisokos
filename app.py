import streamlit as st
import os

# Megjelenés beállítása
st.set_page_config(page_title="Splash Mosoda Kisokos", page_icon="🫧")

st.markdown("""
    <style>
    .stTextInput > div > div > input { border-radius: 20px; border: 2px solid #007bff; }
    .partner-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #007bff; color: black; }
    h1 { color: #004085; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# 🧺 Splash Mosoda Kisokos 🫧")

# Adatbázis betöltése és feldolgozása
@st.cache_data
def get_data():
    fajl = 'mosoda_adatbazis.txt'
    if not os.path.exists(fajl):
        return {}
    
    with open(fajl, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Szétvágjuk a partnereket a # jel mentén
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

st.write("### 🔍 Melyik partnert keresed?")
ceg_nev = st.text_input("", placeholder="Írd be a nevet: Mika, Airport, BQA...")

if ceg_nev:
    keresett = ceg_nev.lower().strip()
    # Megkeressük a partnert (pontos vagy részleges egyezés)
    talalat = None
    for kulcs in data:
        if keresett in kulcs:
            talalat = data[kulcs]
            break
    
    if talalat:
        st.markdown(f"### 📋 {talalat['original_name']} szabályzata:")
        st.markdown(f"""<div class="partner-card">{talalat['info'].replace(chr(10), '<br>')}</div>""", unsafe_allow_html=True)
    else:
        st.warning("Sajnos ilyen nevű partner nincs a listában.")

st.markdown("---")
st.caption("🫧 Splash Mosoda - Mobil verzió")