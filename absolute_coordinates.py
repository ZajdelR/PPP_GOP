# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:13:49 2024

@author: UPWr
"""

import pandas as pd
import re
from geodezyx.reffram.geometry import helmert_trans_estim_minimisation, helmert_trans_estim
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def parse_filename(filename):
    # Regex to extract components from the filename
    pattern = r'(.+?)_(.+?)_(.+?)_(.+?)/(.+?)-\2-\4-\3.dat.1h:#'
    match = re.match(pattern, filename)
    if match:
        return match.groups()
    return [filename] + [None]*7  # Return the filename and None for other fields if no match

def read_and_process_file(filepath):
    # Initialize a list to hold the data
    data = []
    
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()  # Split line by whitespace
            if parts:  # Check if there are any parts
                filename = parts[0]  # The first part is the complex filename
                other_columns = parts[1:]  # Remaining parts are the other columns
                
                # Parse the filename
                campaign, ac, systems, interval, station = parse_filename(filename)
                
                # Extract additional components from the rest
                # station, ac2, interval2, systems2, suffix = rest.split('-')
                # suffix, _ = suffix.split('.dat')
                
                # Append to data list including other columns
                data.append([campaign, ac, systems, interval] + other_columns)
    
    # Create DataFrame from the data
    columns = ['campaign', 'ac', 'systems', 'interval', 'col0','col1','station','X','Y','Z','date','time','col2']
    df = pd.DataFrame(data, columns=columns)
    
    df = df[df.ac != 'REF']
    return df

def filter_solution_df(df, interval, systems, ac):
    ref_df = df[(df.interval == interval) &
                (df.systems == systems) &
                (df.ac == ac)].set_index('station')[['X','Y','Z']]
    return ref_df

def helmert_parameters(df):
    # Extract reference and solution coordinates
    X_ref = df['X_ref'].values
    Y_ref = df['Y_ref'].values
    Z_ref = df['Z_ref'].values
    X_sol = df['X_sol'].values
    Y_sol = df['Y_sol'].values
    Z_sol = df['Z_sol'].values

    # Compute means
    mean_X_ref = np.mean(X_ref)
    mean_Y_ref = np.mean(Y_ref)
    mean_Z_ref = np.mean(Z_ref)
    mean_X_sol = np.mean(X_sol)
    mean_Y_sol = np.mean(Y_sol)
    mean_Z_sol = np.mean(Z_sol)

    # Compute scale factor
    scale_factor = np.sqrt(np.mean((X_sol - mean_X_sol)**2 + (Y_sol - mean_Y_sol)**2 + (Z_sol - mean_Z_sol)**2) / np.mean((X_ref - mean_X_ref)**2 + (Y_ref - mean_Y_ref)**2 + (Z_ref - mean_Z_ref)**2))

    # Compute rotation matrix
    A = np.vstack((X_ref - mean_X_ref, Y_ref - mean_Y_ref, Z_ref - mean_Z_ref)).T
    B = np.vstack((X_sol - mean_X_sol, Y_sol - mean_Y_sol, Z_sol - mean_Z_sol)).T
    H = np.dot(B.T, A)
    U, _, Vt = np.linalg.svd(H)
    R = np.dot(U, Vt)

    # Compute translation vector
    T = np.array([mean_X_sol, mean_Y_sol, mean_Z_sol]) - scale_factor * np.dot(R, np.array([mean_X_ref, mean_Y_ref, mean_Z_ref]))
    
    parameters = {
        'S': 6371000000*(scale_factor-1),
        'RX': R[0,1]*6371000000,
        'RY': R[0,2]*6371000000,
        'RZ': R[1,2]*6371000000,
        'TX': T[0]*1e3,
        'TY': T[1]*1e3,
        'TZ': T[2]*1e3,
        'STA': len(X_ref)
    }
    
    return parameters, scale_factor, R, T


from scipy.optimize import least_squares

def helmert_transform(x, coords_ref):
    """Apply the Helmert transformation to the reference coordinates."""
    tx, ty, tz, s, rx, ry, rz = x
    sin_rx, cos_rx = np.sin(rx), np.cos(rx)
    sin_ry, cos_ry = np.sin(ry), np.cos(ry)
    sin_rz, cos_rz = np.sin(rz), np.cos(rz)

    Rx = np.array([[1, 0, 0], [0, cos_rx, -sin_rx], [0, sin_rx, cos_rx]])
    Ry = np.array([[cos_ry, 0, sin_ry], [0, 1, 0], [-sin_ry, 0, cos_ry]])
    Rz = np.array([[cos_rz, -sin_rz, 0], [sin_rz, cos_rz, 0], [0, 0, 1]])
    R = Rx @ Ry @ Rz
    scale_matrix = (1 + s) * np.eye(3)

    return coords_ref @ scale_matrix @ R + np.array([tx, ty, tz])

def objective_function(x, coords_ref, coords_sol):
    """Objective function to minimize: difference between transformed ref and solution coordinates."""
    transformed_coords = helmert_transform(x, coords_ref)
    return np.ravel(transformed_coords - coords_sol)

def estimate_helmert_parameters(df):
    coords_ref = df[['X_ref', 'Y_ref', 'Z_ref']].to_numpy()
    coords_sol = df[['X_sol', 'Y_sol', 'Z_sol']].to_numpy()

    # Initial guess: [TX, TY, TZ, scale, RX, RY, RZ]
    x0 = np.zeros(7)

    # Minimize the objective function
    result = least_squares(objective_function, x0, args=(coords_ref, coords_sol))

    parameters = {
        'TX': result.x[0]*1e3,
        'TY': result.x[1]*1e3,
        'TZ': result.x[2]*1e3,
        'S': result.x[3]*6371000000,
        'RX': result.x[4]*6371000000,
        'RY': result.x[5]*6371000000,
        'RZ': result.x[6]*6371000000
    }

    return parameters, result

# Example usage
file_path = './INPUT/ABSOLUTE_XYZ_REF'  # Specify your file path here
df = read_and_process_file(file_path)
acs = df.ac.unique()
ints = df.interval.unique()

interval= '30S'
ref_ac = 'IGS'

helmert = {}
helmert2 = {}

for systems in ['Gxxx','GRxx','GREx']:
    X1in = filter_solution_df(df, interval, 'Gxxx', ref_ac).astype(float)
    
    for ac in acs:
        if ac == ref_ac:
            continue
        X2in = filter_solution_df(df, interval, systems, ac).astype(float)
        helmert_df = pd.merge(X1in,X2in,left_index=True,right_index=True,suffixes=("_ref","_sol"))
        # helmert2[f"{ac}_{systems}_{interval}"] = helmert_trans_estim(X1in.values,X2in.values)
         
        
        # helmert[f"{ac}_{systems}_{interval}"], *x = helmert_parameters(helmert_df)
        
        helmert2[f"{ac}_{systems}_{interval}"], *x = estimate_helmert_parameters(helmert_df)
        
df_helmert = pd.DataFrame(helmert2).T

df_helmert[['ac', 'systems', 'interval']] = df_helmert.index.to_series().str.split('_', expand=True)
df_helmert.set_index(['ac', 'systems', 'interval'],inplace=True)

f,a = plt.subplots(3,1,figsize=(17.3/2.54, 16/2.54),sharex=True)
for systems,ax in zip(['Gxxx','GRxx','GREx'],a):
    
    df_h1 = df_helmert.xs(systems, level='systems')
    sns.heatmap(df_h1, annot=True, fmt=".1f", 
                cmap=f"RdYlBu", linewidths=.5, 
                cbar=False, vmin=-3,vmax=3,
                ax=ax)
    ax.set_ylabel(systems)
    plt.tight_layout(pad=0.01)
    # Check if directories provided and save the plot to file

plt.savefig(f'./OUTPUT_PLOTS/HELMERT_HEATMAP_{interval}.png',dpi=600)
    

    
    