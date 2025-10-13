import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import io
import time
import lammps_logfile

element_options = ['Au', 'Cu', 'Pt']
temp_options = ['3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']
 
st.title('Element selection')

# Element select dropdown
selected_elements = st.multiselect(
    'Select one or more elements',
    element_options,
    default=['Au']
)
if selected_elements:
    st.write(f'Selected elements: {", ".join(selected_elements)}')


st.title('Temperature selection')

# Temp select dropdown
selected_temps = st.multiselect(
    'Select one or more temperatures',
    temp_options,
    default=['3000']
)
if selected_temps:
    st.write(f'Selected temperatures: {", ".join(selected_temps)}')


fig, ax = plt.subplots()
for element in selected_elements:
    for temp in selected_temps:
        file_path=f'./{element}/{element}-{temp}K.log'
        log = lammps_logfile.File(file_path)
        x = log.get("Time", run_num=2)
        y = log.get("c_Msd[4]", run_num=2)
        ax.plot(x, y)

ax.grid(False)
st.pyplot(fig)

