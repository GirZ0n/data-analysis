from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans

from src.tasks.task3.common.utils import filter_df_by_radius, get_all_stops, show_map


def _get_model_config() -> Dict[str, Any]:
    st.header('KMeans model config')

    config = {}

    left_column, right_column = st.columns(2)

    with left_column:
        config['init'] = st.selectbox('Method for initialization:', options=['k-means++', 'random'])
        config['n_init'] = int(st.number_input('Number of runs:', value=10, min_value=1))
        config['tol'] = int(st.number_input('Tolerance:', value=1e-4, min_value=float(0), format='%f'))

    with right_column:
        config['algorithm'] = st.selectbox('K-means algorithm:', options=['elkan', 'full'])
        config['max_iter'] = int(st.number_input('Maximum iterations per run:', value=300, min_value=1))
        config['random_state'] = int(st.number_input('Random state:', value=42))

    return config


@st.cache
def _find_inertia(df: pd.DataFrame, max_number_of_clusters: int, config: Dict[str, Any]) -> List[float]:
    inertia = []
    for n_clusters in range(1, max_number_of_clusters + 1):
        model = KMeans(n_clusters=n_clusters, **config).fit(df)
        inertia.append(model.inertia_)

    return inertia


def _show_scree_plot(df: pd.DataFrame, config: Dict[str, Any]):
    st.header('Scree plot')

    filtered_df = df.drop(columns=['stop_name', 'stop_id'])

    max_number_of_clusters = int(st.number_input('Maximum number of clusters', min_value=1, value=20))

    inertia = _find_inertia(filtered_df, max_number_of_clusters, config)

    scree_plot = px.line(x=range(1, len(inertia) + 1), y=inertia, markers=True)
    scree_plot.update_layout(xaxis_title='Step', yaxis_title='Inertia')
    st.plotly_chart(scree_plot, use_container_width=True)


def _show_map(df: pd.DataFrame, config: Dict[str, Any]):
    st.header('Results')

    filtered_df = df.drop(columns=['stop_name', 'stop_id'])

    n_clusters = int(st.number_input('Number of clusters:', min_value=0, value=9))
    model = KMeans(n_clusters=n_clusters, **config)

    df['cluster'] = model.fit_predict(filtered_df)
    show_map(df, color='cluster')


def show_k_means_clustering_page():
    all_stops = get_all_stops()
    filtered_stops = filter_df_by_radius(all_stops, st.session_state.stop_id, st.session_state.radius).copy()

    config = _get_model_config()

    _show_scree_plot(filtered_stops, config)

    _show_map(filtered_stops, config)
