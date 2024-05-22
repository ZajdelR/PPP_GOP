import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)
    
    vlim = (80,100)    
    ratGRE = pppu.heatmap_station_specific(data,'30S','GREx','Rat',scalar=1)
    ratGR = pppu.heatmap_station_specific(data,'30S','GRxx','Rat',scalar=1)
    ratG = pppu.heatmap_station_specific(data,'30S','Gxxx','Rat',scalar=1)
    
    exit()
    vlim = (10,100)
    pppu.heatmap_station_specific(data,'30S','GREx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.heatmap_station_specific(data,'30S','GRxx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.heatmap_station_specific(data,'30S','Gxxx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    
    vlim = (-30,30)
    pppu.heatmap_station_specific(data,'30S','GREx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.heatmap_station_specific(data,'30S','GRxx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.heatmap_station_specific(data,'30S','Gxxx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
    # 
    vlim = (0,30)
    pppu.heatmap_station_specific(data,'01D','GREx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.heatmap_station_specific(data,'01D','GRxx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.heatmap_station_specific(data,'01D','Gxxx','Vpe95',rev='_r',vmin=vlim[0],vmax=vlim[1])
    
    vlim = (-30,30)
    pppu.heatmap_station_specific(data,'01D','GREx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.heatmap_station_specific(data,'01D','GRxx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.heatmap_station_specific(data,'01D','Gxxx','Vpe95',vmin=vlim[0],vmax=vlim[1],perc=True)
