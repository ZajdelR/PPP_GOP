import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)

    periods = data['Interval'].unique()
    group = "group:"
    
    for systems in data['Systems'].unique():
        pppu.boxplot_interval_systems(data,'Hpe95','01D',systems,30, group=group)
        pppu.boxplot_interval_systems(data,'Hpe95','01H',systems,100, group=group)
        pppu.boxplot_interval_systems(data,'Hpe95','30S',systems,200, group=group)
        
        pppu.boxplot_interval_systems(data,'Vpe95','01D',systems,30, group=group)
        pppu.boxplot_interval_systems(data,'Vpe95','01H',systems,100, group=group)
        pppu.boxplot_interval_systems(data,'Vpe95','30S',systems,200, group=group)

