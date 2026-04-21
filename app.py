import streamlit as st
import os

# 1. Oldal alapbeállításai
st.set_page_config(
    page_title="Splash Mosoda Kisokos", 
    page_icon="🫧", 
    layout="centered"
)

# 2. Logó megjelenítése (ha létezik logo.png a mappában)
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

# 3. Egyedi stílusok (CSS) a szép megjelenéshez
st.markdown("""
    <style>
    /* Keresőmező kerekítése */
    .stTextInput > div > div > input { 
        border-radius: 20px; 
        border: 2px solid #007bff; 
    }
    /* Partner kártya formázása */
    .partner-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        border-left: 8px solid #007bff; 
        color: black; 
        line-height: 1.6;
    }
    /* Cím stílusa */
    h1 { 
        color: #004085; 
        text-align: center; 
        font-family: 'Arial Black', sans-serif;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🧺 Splash Mosoda Kisokos 🫧</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Gyors, pontos, digitális tudástár</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Adatbázis betöltése és feldolgozása a TXT fájlból
@st.cache_data
def get_data():
    fajl = 'mosoda_adatbazis.txt'
    if not os.path.exists(fajl):
        return {}
    
    try:
        with open(fajl, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Ha gond lenne az ékezetekkel, megpróbáljuk más kódolással
        with open(fajl, 'r', encoding='latin-1') as f:
            content = f.read()
    
    partners = {}
    # A partnereket a # jel mentén választjuk szét
    sections = content.split('#')
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            name = lines[0].strip()
            info = '\n'.join(lines[1:]).strip()
            # Eltároljuk kisbetűs kulccsal a kereséshez
            partners[name.lower()] = {"original_name": name, "info": info}
    return partners

data = get_data()

# 5. Kereső felület
st.write("### 🔍 Melyik partnert keresed?")
ceg_nev = st.text_input("", placeholder="Írd be a nevet (pl. Mika, Airport, BQA...)")

if ceg_nev:
    keresett = ceg_nev.lower().strip()
    
    # Megkeressük a partnert a kulcsok között (részleges egyezés is ér)
    talalat = None
    for kulcs in data:
        if keresett in kulcs:
            talalat = data[kulcs]
            break
    
    if talalat:
        st.markdown(f"### 📋 {talalat['original_name']} szabályzata:")
        
        # A szöveges tartalom megjelenítése a kártyában
        st.markdown(f"""
            <div class="partner-card">
                {talalat['info'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
        
        # 6. KÉP MEGJELENÍTÉSE (ha létezik kép a partner nevével, pl. mika.jpg)
        image_extensions = ['.jpg', '.jpeg', '.png']
        found_image = False
        
        for ext in image_extensions:
            img_filename = f"{talalat['original_name'].lower()}{ext}"
            if os.path.exists(img_filename):
                st.write("") # Kis helyköz
                st.image(img_filename, caption=f"Fotós segédlet: {talalat['original_name']}", use_container_width=True)
                found_image = True
                break
                
    elif len(ceg_nev) > 2:
        st.warning("⚠️ Sajnos nincs ilyen nevű partner a rendszerben. Ellenőrizd a gépelést!")

# 7. Lábléc
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("🫧 Splash Mosoda - Belső használatra | 2026")