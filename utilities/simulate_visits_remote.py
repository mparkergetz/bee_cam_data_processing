import pandas as pd
from multiprocessing import Pool
import numpy as np
from concurrent.futures import ThreadPoolExecutor


treatment_times = pd.read_csv('treatment_times.csv', index_col=False)
treatment_times['datetime'] = pd.to_datetime(treatment_times['datetime'], format= "%Y-%m-%d %H:%M:%S")
treatment_times = treatment_times.drop(columns='date')

camera_timeline = pd.read_csv('camera_timeline.csv')
camera_timeline['datetime'] = pd.to_datetime(camera_timeline['datetime'])

bombus_df = pd.read_csv('bombus_df.csv')
bombus_df['datetime'] = pd.to_datetime(bombus_df['datetime'])
bombus_df = pd.merge(bombus_df, treatment_times[['pi', 'datetime', 'color']], on=['pi', 'datetime'], how='left')
bombus_df['new_visit'] = (bombus_df['time_diff'] > 4) | (bombus_df['time_diff'].isna())
bombus_df['visit_id'] = bombus_df.groupby(['species'])['new_visit'].cumsum()

visit_durations = (
    bombus_df.groupby(['species', 'visit_id', 'pi', 'color'])['datetime']
    .agg(visit_start='min', visit_end='max')
    .reset_index()
)
visit_durations['duration'] = (
    (visit_durations['visit_end'] - visit_durations['visit_start']).dt.total_seconds()
)

visit_times = visit_durations[['visit_start', 'visit_end']]

def simulate_single_shuffle(unique_pis, visit_times):
    visit_times_pi = visit_times.copy()
    selected_pis = np.random.choice(unique_pis, size=len(visit_times))
    visit_times_pi['pi'] = pd.Categorical(selected_pis, categories=unique_pis)
    
    total_color_counts = {}
    for index, visit in visit_times_pi.iterrows():
        pi_visit = visit['pi']
        visit_start = visit['visit_start']
        visit_end = visit['visit_end']

        matching_entries = camera_timeline[
            (camera_timeline['pi'] == pi_visit) &
            (camera_timeline['datetime'] >= visit_start) &
            (camera_timeline['datetime'] <= visit_end)
        ]

        if not matching_entries.empty:
            unique_colors = matching_entries['color'].drop_duplicates()
            for color in unique_colors:
                if color in total_color_counts:
                    total_color_counts[color] += 1
                else:
                    total_color_counts[color] = 1
    return total_color_counts

def simulate_shuffles(num_iterations):
    unique_pis = np.arange(1,11).tolist()
    
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(simulate_single_shuffle, unique_pis, visit_times) for _ in range(num_iterations)]
        for future in futures:
            results.append(future.result())

    return results

simulation_results = simulate_shuffles(10000)