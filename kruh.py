import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import streamlit.components.v1 as components
import io

st.set_page_config(page_title="Kružnice s body", layout="centered")

st.title("Kružnice s body")

# --- SIDEBAR s informacemi ---
st.sidebar.header("Informace o aplikaci")
st.sidebar.markdown("""
**Autor aplikace:** Vaše jméno  
**Kontakt:** vas.email@example.com  

**Použité technologie:**  
- [Streamlit](https://streamlit.io)  
- [NumPy](https://numpy.org)  
- [Matplotlib](https://matplotlib.org)  
- [ReportLab](https://www.reportlab.com) pro export PDF  
""")

# --- Formulář pro zadání parametrů ---
with st.form("circle_form"):
    st.subheader("Parametry kružnice")
    x_center = st.number_input("Souřadnice středu X:", value=0.0)
    y_center = st.number_input("Souřadnice středu Y:", value=0.0)
    radius = st.number_input("Poloměr kružnice:", value=10.0, min_value=0.1)
    num_points = st.number_input("Počet bodů na kružnici:", value=8, min_value=1, step=1)
    color = st.color_picker("Vyber barvu bodů:", "#ff0000")
    units = st.selectbox("Jednotka:", ["mm", "cm", "m"])

    st.subheader("Údaje pro PDF")
    user_name = st.text_input("Vaše jméno:")
    user_email = st.text_input("Váš e-mail:")

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

    # --- Export PDF do paměti (s grafem a údaji uživatele) ---
    def make_pdf():
        buffer = io.BytesIO()

        # uložit graf do obrázku
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)

        # ReportLab dokument
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        flow = []

        flow.append(Paragraph("<b>Výstup z aplikace Kružnice s body</b>", styles["Title"]))
        flow.append(Spacer(1, 12))

        # Parametry úlohy
        flow.append(Paragraph(f"Souřadnice středu: ({x_center} mm, {y_center} mm)", styles["Normal"]))
        flow.append(Paragraph(f"Poloměr: {radius} mm", styles["Normal"]))
        flow.append(Paragraph(f"Počet bodů: {num_points}", styles["Normal"]))
        flow.append(Paragraph(f"Barva bodů: {color}", styles["Normal"]))
        flow.append(Paragraph(f"Jednotka zadaná uživatelem: {units}", styles["Normal"]))
        flow.append(Spacer(1, 12))

        # Údaje uživatele
        flow.append(Paragraph(f"Jméno uživatele: {user_name if user_name else 'Neuvedeno'}", styles["Normal"]))
        flow.append(Paragraph(f"E-mail uživatele: {user_email if user_email else 'Neuvedeno'}", styles["Normal"]))
        flow.append(Spacer(1, 12))

        # Autor aplikace
        flow.append(Paragraph("Autor aplikace: Vaše jméno", styles["Normal"]))
        flow.append(Paragraph("Kontakt: vas.email@example.com", styles["Normal"]))
        flow.append(Spacer(1, 12))

        # Datum generování
        flow.append(Paragraph(f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", styles["Italic"]))
        flow.append(Spacer(1, 24))

        # vložit obrázek grafu
        flow.append(Image(img_buffer, width=400, height=400))

        doc.build(flow)
        buffer.seek(0)
        return buffer

    pdf_buffer = make_pdf()

    # Tlačítka vedle sebe
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Exportovat do PDF",
            data=pdf_buffer,
            file_name=f"kruznice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

    with col2:
        if st.button("🖨️ Tisk"):
            components.html(
                """
                <script>
                window.print();
                </script>
                """,
                height=0,
            )
