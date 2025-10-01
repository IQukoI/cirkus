import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

st.set_page_config(page_title="Kružnice s body", layout="centered")

st.title("Kružnice s body")

# --- SIDEBAR s informacemi ---
st.sidebar.header("Informace o aplikaci")
st.sidebar.markdown("""
**Autor:** Martin Říha  
**Kontakt:** 278328@vutbr.cz  

**Použité technologie:**  
- [Streamlit](https://streamlit.io)  
- [NumPy](https://numpy.org)  
- [Matplotlib](https://matplotlib.org)  
- [ReportLab](https://www.reportlab.com) pro export PDF  
""")

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

    # --- Export do PDF ---
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
        flow.append(Paragraph("Kontakt: váš.email@example.com", styles["Normal"]))
        flow.append(Spacer(1, 12))
        flow.append(Paragraph(f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", styles["Italic"]))

        doc.build(flow)
        return filename

    if st.button("Exportovat do PDF"):
        pdf_file = export_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Stáhnout PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
