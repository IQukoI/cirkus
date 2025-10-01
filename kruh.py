import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Kružnice s body", layout="centered")

st.title("Kružnice s body")

# --- SIDEBAR s informacemi ---
st.sidebar.header("Informace o aplikaci")
st.sidebar.markdown("""
**Autor:** Vaše jméno  
**Kontakt:** vas.email@example.com  

**Použité technologie:**  
- [Streamlit](https://streamlit.io)  
- [NumPy](https://numpy.org)  
- [Matplotlib](https://matplotlib.org)  
- [ReportLab](https://www.reportlab.com) pro export PDF  
""")

# Inicializace stavů
if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False
if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None
if "print_ready" not in st.session_state:
    st.session_state.print_ready = False

# --- Formulář pro zadání parametrů ---
with st.form("circle_form"):
    x_center = st.number_input("Souřadnice středu X:", value=0.0)
    y_center = st.number_input("Souřadnice středu Y:", value=0.0)
    radius = st.number_input("Poloměr kružnice:", value=10.0, min_value=0.1)
    num_points = st.number_input("Počet bodů na kružnici:", value=8, min_value=1, step=1)
    color = st.color_picker("Vyber barvu bodů:", "#ff0000")
    units = st.selectbox("Jednotka:", ["mm", "cm", "m"])
    submit = st.form_submit_button("Vykreslit")

if submit:
    # Převod na milimetry
    if units == "m":
        factor = 1000
    elif units == "cm":
        factor = 10
    else:
        factor = 1

    x_center *= factor
    y_center *= factor
    radius *= factor

    # Výpočet bodů
    angles = np.linspace(0, 2*np.pi, int(num_points), endpoint=False)
    x_points = x_center + radius * np.cos(angles)
    y_points = y_center + radius * np.sin(angles)

    # Vykreslení
    fig, ax = plt.subplots()
    circle = plt.Circle((x_center, y_center), radius, fill=False, linestyle="--")
    ax.add_artist(circle)
    ax.scatter(x_points, y_points, c=color, s=100)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.grid(True)

    st.pyplot(fig)

    # --- Export do PDF funkce ---
    def export_pdf():
        filename = f"kruznice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()
        flow = []

        flow.append(Paragraph("<b>Výstup z aplikace Kružnice s body</b>", styles["Title"]))
        flow.append(Spacer(1, 12))
        flow.append(Paragraph(f"Souřadnice středu: ({x_center} mm, {y_center} mm)", styles["Normal"]))
        flow.append(Paragraph(f"Poloměr: {radius} mm", styles["Normal"]))
        flow.append(Paragraph(f"Počet bodů: {num_points}", styles["Normal"]))
        flow.append(Paragraph(f"Barva bodů: {color}", styles["Normal"]))
        flow.append(Paragraph(f"Jednotka zadaná uživatelem: {units}", styles["Normal"]))
        flow.append(Spacer(1, 12))
        flow.append(Paragraph("Autor: Vaše jméno", styles["Normal"]))
        flow.append(Paragraph("Kontakt: vas.email@example.com", styles["Normal"]))
        flow.append(Spacer(1, 12))
        flow.append(Paragraph(f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", styles["Italic"]))

        doc.build(flow)
        return filename

    # Sloupce s tlačítky
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Exportovat do PDF"):
            pdf_file = export_pdf()
            st.session_state.pdf_file = pdf_file
            st.session_state.pdf_ready = True

    with col2:
        if st.button("🖨️ Tisk"):
            st.session_state.print_ready = True

# --- Po kliknutí na PDF tlačítko ukázat download ---
if st.session_state.pdf_ready and st.session_state.pdf_file and os.path.exists(st.session_state.pdf_file):
    with open(st.session_state.pdf_file, "rb") as f:
        st.download_button(
            label="📥 Stáhnout PDF",
            data=f,
            file_name=st.session_state.pdf_file,
            mime="application/pdf"
        )
    # reset
    st.session_state.pdf_ready = False

# --- Po kliknutí na Tisk ---
if st.session_state.print_ready:
    components.html(
        """
        <script>
        window.print();
        </script>
        """,
        height=0,
    )
    st.session_state.print_ready = False
