import ppp_utils as pppu
import pandas as pd
import os

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)
    analysis_results = pppu.analyze_by_ac_and_site(data)
    
    results = {}
    groups = analysis_results.groupby('int')
    for idx, group in groups:
        for column in group.columns[3:]:
            x = pd.pivot_table(group,column,'sol','sys')*1e3
            results[f"{column}_{idx}"] = x
            x.to_excel(os.path.join(pppu.dirs['out'],f"{column}_{idx}.xlsx"))
    # pppu.save_results_to_excel(analysis_results,filepath.split('/')[-1])