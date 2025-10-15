import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import io
import time
import lammps_logfile
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator

plt.rcParams['font.family'] = 'serif'
n=50

element_options = ['Au', 'Cu', 'Pt']
temp_options = ['3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']
style_map = {'Au': '-', 'Cu': '--', 'Pt': ':'}
marker_map = {'Au': 'o', 'Cu': 's', 'Pt': '^'}
color_map = {'3000': 'tab:blue', '4000': 'tab:orange', '5000': 'tab:green', '6000': 'tab:red', '7000': 'tab:purple', '8000': 'tab:brown', '9000': 'tab:pink', '10000': 'tab:olive'}
 
st.set_page_config(page_title="MSD and Diffusion Coefficient", layout="centered")

st.title("Mean Square Displacement and Diffusion Coefficient")

st.subheader("Mean Square Displacement")

st.markdown("""
The **Mean Square Displacement (MSD)** quantifies how far, on average, a particle moves from its initial position over time.
""")

st.latex(r"""
\langle r^2(t) \rangle = \left\langle \left[ \mathbf{r}(t) - \mathbf{r}(0) \right]^2 \right\rangle
""")

st.markdown("""
where the angle brackets $\\langle \\cdot \\rangle$ denote an ensemble average over all particles or time origins.
""")

st.markdown("---")

st.subheader("Diffusion Coefficient")

st.markdown("""
In three dimensions, the **diffusion coefficient** $D$ is related to the long-time behavior of the MSD through the Einstein relation:
""")

st.latex(r"""
D = \lim_{t \to \infty} \frac{\langle r^2(t) \rangle}{6t}
""")

st.markdown("""
For motion in $d$ dimensions, the general form is:
""")

st.latex(r"""
D = \lim_{t \to \infty} \frac{\langle r^2(t) \rangle}{2 d t}
""")

st.markdown("""
This relation assumes purely diffusive motion, where ballistic effects are negligible at long times.
""")

st.info("💡 Tip: We can calculate the diffusion coefficient by fitting MSD vs. time data from molecular dynamics simulations.")

st.markdown("---")

st.subheader("Plotting MSD and Diffusion coefficient")

st.markdown("""
In this application, we analyze Mean Square Displacement (MSD) data as a function of time for three elements: Gold (Au), Platinum (Pt), and Copper (Cu).
By exploring these datasets, we can observe how the MSD and the corresponding diffusion coefficients vary with temperature and between different elements.
""")

st.markdown("""
Use the drop-down menus below to select an element and temperature, and the app will display the corresponding MSD vs. Time and Diffusion Coefficient vs. Temperature plots.
""")

# Element select dropdown
selected_elements = st.multiselect(
    'Select one or more elements',
    element_options,
    default=['Au']
)
if selected_elements:
    st.write(f'Selected elements: {", ".join(selected_elements)}')


# Temp select dropdown
selected_temps = st.multiselect(
    'Select one or more temperatures',
    temp_options,
    default=['3000']
)
if selected_temps:
    st.write(f'Selected temperatures: {", ".join(selected_temps)}')


st.subheader('MSD vs Time for Different Elements and Temperatures')

width=8/2.54
height=6/2.54
fig, ax = plt.subplots(figsize=(width, height))
fig2, ax2 = plt.subplots(figsize=(width, height))
for element in selected_elements:
    T = []
    D = []
    for temp in selected_temps:
        file_path=f'./{element}/{element}-{temp}K.log'
        log = lammps_logfile.File(file_path)
        x = log.get("Time", run_num=1)
        y = log.get("c_Msd[4]", run_num=1)
        coefficients = np.polyfit(x[-n:], y[-n:], 1)
        diff = coefficients[0]/6
        T.append(int(temp))
        D.append(diff)
        ax.plot(x, y - y[0], linestyle=style_map[element], color=color_map[temp], linewidth=0.5)
    T_vs_D = zip(T, D)
    T_vs_D_sorted = np.array(sorted(T_vs_D))
    ax2.plot(T_vs_D_sorted[:, 0], T_vs_D_sorted[:, 1], linestyle=style_map[element], marker=marker_map[element], linewidth=0.5)

style_legend_elements = [Line2D([0], [0], color='black', lw=0.5, linestyle=style_map[el], label=el)
                         for el in selected_elements]
color_legend_elements = [Line2D([0], [0], color=color_map[t], lw=0.5, label=f'{t} K')
                         for t in selected_temps]

legend1 = ax.legend(handles=style_legend_elements, title="Element", loc='upper left', fontsize=5, title_fontsize=6)
ax.add_artist(legend1)
ax.legend(handles=color_legend_elements, title="Temperature", loc='lower right', fontsize=5, title_fontsize=6)

ax.set_xlabel('Time ($ps$)', fontsize=10)
ax.set_ylabel('MSD ($A^{2}$)', fontsize=10)
ax.grid(False)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='minor', top=True, right=True, length=2, direction='out', labelsize=8, width=0.5)
ax.tick_params(which='major', length=4, top=True, right=True, direction='out', labelsize=8, width=0.8)
for spine in ax.spines.values():
    spine.set_linewidth(0.8)
st.pyplot(fig)


st.subheader('Diffusion Coefficient vs Temperaure for Different Elements')

ax2.set_xlabel('Temperature ($K$)', fontsize=16)
ax2.set_ylabel('Diffusion coefficient ($A^{2}/ps$)', fontsize=16)
ax2.grid(False)
ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())
ax2.tick_params(which='minor', top=True, right=True, length=2, direction='out', labelsize=14, width=1.0)
ax2.tick_params(which='major', length=4, top=True, right=True, direction='out', labelsize=14, width=1.5)
for spine in ax2.spines.values():
    spine.set_linewidth(2)
st.pyplot(fig2)


