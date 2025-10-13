import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import io
import time
import lammps_logfile
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator


element_options = ['Au', 'Cu', 'Pt']
temp_options = ['3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']
style_map = {'Au': '-', 'Cu': '--', 'Pt': ':'}
color_map = {'3000': 'tab:blue', '4000': 'tab:orange', '5000': 'tab:green', '6000': 'tab:red', '7000': 'tab:purple', '8000': 'tab:brown', '9000': 'tab:pink', '10000': 'tab:olive'}
 
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
        x = log.get("Time", run_num=1)
        y = log.get("c_Msd[4]", run_num=1)
        ax.plot(x, y - y[0], linestyle=style_map[element], color=color_map[temp])

style_legend_elements = [Line2D([0], [0], color='black', lw=2, linestyle=style_map[el], label=el)
                         for el in selected_elements]
color_legend_elements = [Line2D([0], [0], color=color_map[t], lw=2, label=f'{t} K')
                         for t in selected_temps]

legend1 = ax.legend(handles=style_legend_elements, title="Element", loc='upper left')
ax.add_artist(legend1)
ax.legend(handles=color_legend_elements, title="Temperature", loc='lower right')

ax.set_xlabel('Time ($ps$)', fontsize=16)
ax.set_ylabel('MSD ($A^{2}$)', fontsize=16)
ax.grid(False)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='minor', top=True, right=True, length=2, direction='out', labelsize=14)
ax.tick_params(which='major', length=4, top=True, right=True, direction='out', labelsize=14)
for spine in ax.spines.values():
    spine.set_linewidth(2)
st.pyplot(fig)

