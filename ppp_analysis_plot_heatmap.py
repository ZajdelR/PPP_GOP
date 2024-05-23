import ppp_utils as pppu

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)
    systems = data.Systems.unique()

    vlim = (80,100)
    rat = {system:pppu.create_heatmap_station_specific(data,'30S',system,'Rat',scalar=1) for system in systems}

    for system, df in rat.items():
        pppu.plot_heatmap(df, '30S', system, 'Rat',
                          vmin=vlim[0], vmax=vlim[1],
                          cbar='RdYlGn')