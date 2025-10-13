import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import io
import time
import lammps-logfile

element_options = ['Au', 'Cu', 'Pt']
temp_options = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
 
st.title('Multiselect')

# Multi-select dropdown
selected_comps = st.multiselect(
    'Select one or more compositions',
    options,
    default=['Carbon']
)
if selected_comps:
    st.write(f'Selected compositions: {", ".join(selected_comps)}')
