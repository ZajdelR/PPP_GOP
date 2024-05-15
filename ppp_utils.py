# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:35:06 2024

@author: UPWr
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and prepare your data
def load_apep_file(filename):
    data = pd.read_csv(filename)  # Make sure to replace 'your_data_file.csv' with your actual data file path
    data['HPE95'] = pd.to_numeric(data['HPE95'], errors='coerce')  # Assuming the data needs to be converted to numeric
    data['VPE95'] = pd.to_numeric(data['VPE95'], errors='coerce')
    
    return data

dirs = {'inp': 'INPUT',
        'plots': 'OUTPUT_PLOTS',
        'out': 'OUTPUT_DATA'}