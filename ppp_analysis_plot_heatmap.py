import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v1'
    data = pppu.load_and_prepare_data(filepath)
        
    data1 = pppu.heatmap_mean_rate(data,'30S','GREx')
    data2 = pppu.heatmap_mean_rate(data,'30S','Gxxx')
    
    xx = data1-data2
