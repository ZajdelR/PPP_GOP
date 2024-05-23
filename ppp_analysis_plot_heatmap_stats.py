import ppp_utils
import ppp_utils as pppu

# Main execution
if __name__ == "__main__":
    filepath = './INPUT/STATISTICS_v3'
    data = pppu.load_and_prepare_data(filepath)
    systems = data.Systems.unique()
    intervals = ['01D', '30S']
    intervals = ['30S']

    vlims = {'01D': (0, 30),
             '30S': (0, 200)}

    results = {}
    stat: str = 'Vpe95'

    for interval in intervals:
        # STATION_AC PIVOT
        results[interval] = {system: pppu.create_heatmap_station_specific(data, interval, system, stat) for system in
                             systems}

        # STATION_AC PLOT
        for system, df in results[interval].items():
            pppu.plot_heatmap(df, interval, system, stat,
                              vmin=vlims[interval][0], vmax=vlims[interval][1],
                              cbar='RdYlGn_r')

        # STATION_AC PIVOT REL TO CST
        results[interval + '_rel'] = {system: pppu.calculate_ratio(df, 'SPOCC') for
                                      system, df in
                                      results[interval].items()}
        # STATION_AC PIVOT REL TO GPS
        results[interval + '_sysrel'] = {system: -pppu.calculate_ratio_toref(results[interval]['Gxxx'], df) for
                                         system, df in
                                         results[interval].items()}

        # RELATIVE PLOTS
        relative_settings = dict(vmin=-30,
                                 vmax=30,
                                 perc=True,
                                 cbar='RdYlGn',
                                 stat=stat)

        for system, df in results[interval + '_rel'].items():
            pppu.plot_heatmap(df, interval, system, **relative_settings,
                              save_suffix='_SPOCCREF',
                              append_title="Change wrt. SPOCC")

        for system, df in results[interval + '_sysrel'].items():
            pppu.plot_heatmap(df, interval, system, **relative_settings,
                              save_suffix='_GPSREF',
                              append_title="Change wrt. GPS-only")
