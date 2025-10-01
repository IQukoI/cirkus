import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Kružnice s body")

# Formulář pro vstupy
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
