import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import io
import time
import lammps_logfile

element_options = ['Au', 'Cu', 'Pt']
temp_options = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
 
st.title('Element select')

# Multi-select dropdown
selected_comps = st.multiselect(
    'Select one or more elements',
    element_options,
    default=['Au']
)
if selected_comps:
    st.write(f'Selected elements: {", ".join(selected_comps)}')
