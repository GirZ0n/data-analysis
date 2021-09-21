import streamlit as st

from src.tasks.task3.common.utils import filter_df_by_radius, get_all_stops, show_plots

METHODS_MAP = {
    'Single linkage method': 'single',
    'Average linkage method': 'average',
    'Complete linkage method': 'complete',
    'Centroid method': 'centroid',
    'Ward method': 'ward',
}

METRICS_MAP = {
    'Euclidean distance': 'euclidean',
    'Squared Euclidean distance': 'sqeuclidean',
    'City Block (Manhattan) distance': 'cityblock',
}

EUCLIDEAN_METHODS = {'ward', 'centroid'}


def show_analysis_page():
    all_stops = get_all_stops()
    filtered_stops = filter_df_by_radius(all_stops, st.session_state.stop_id, st.session_state.radius)

    methods = st.multiselect('Select methods:', options=METHODS_MAP.keys())
    for method in methods:
        st.header(method)

        method = METHODS_MAP[method]

        options = METRICS_MAP.keys()
        if method in EUCLIDEAN_METHODS:
            options = ['Euclidean distance']

        metrics = st.multiselect('Select metrics:', options=options, key=f'{method}_metric')
        for metric in metrics:
            st.subheader(metric)

            metric = METRICS_MAP[metric]

            threshold = st.number_input(
                'Threshold:',
                key=f'{method}_{metric}_threshold',
                value=0.0,
                format='%f',
                min_value=0.0,
            )

            if threshold == 0.0:
                threshold = None

            show_plots(filtered_stops, method=method, metric=metric, threshold=threshold)
