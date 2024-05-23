import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)
    systems = data.Systems.unique()

    vlim = (80,100)    
    ratGRE = pppu.create_heatmap_station_specific(data,'30S','GREx','Rat',scalar=1)
    ratGR = pppu.create_heatmap_station_specific(data,'30S','GRxx','Rat',scalar=1)
    ratG = pppu.create_heatmap_station_specific(data,'30S','Gxxx','Rat',scalar=1)
    
    stat = 'Vpe95'
    
    vlim = (10,100)
    pppu.create_heatmap_station_specific(data,'30S','GREx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.create_heatmap_station_specific(data,'30S','GRxx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.create_heatmap_station_specific(data,'30S','Gxxx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    
    vlim = (-30,30)
    pppu.create_heatmap_station_specific(data,'30S','GREx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.create_heatmap_station_specific(data,'30S','GRxx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.create_heatmap_station_specific(data,'30S','Gxxx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
    # 
    vlim = (0,30)
    pppu.create_heatmap_station_specific(data,'01D','GREx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.create_heatmap_station_specific(data,'01D','GRxx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    pppu.create_heatmap_station_specific(data,'01D','Gxxx',stat,rev='_r',vmin=vlim[0],vmax=vlim[1])
    
    vlim = (-30,30)
    pppu.create_heatmap_station_specific(data,'01D','GREx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.create_heatmap_station_specific(data,'01D','GRxx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
    pppu.create_heatmap_station_specific(data,'01D','Gxxx',stat,vmin=vlim[0],vmax=vlim[1],perc=True)
