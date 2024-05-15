import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v1'
    data = pppu.load_and_prepare_data(filepath)
    analysis_results = pppu.analyze_by_ac_and_site(data)
    pppu.save_results_to_excel(analysis_results,filepath.split('/')[-1])