from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from geopy.distance import great_circle
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from src.tasks.task3 import DATA_FOLDER


@st.cache
def get_all_stops() -> pd.DataFrame:
    all_stops = pd.read_csv(DATA_FOLDER / 'ALL_SPB_STOPS.csv', sep=';', encoding='cp1251')
    all_stops.rename(
        columns={'ID_STOP': 'stop_id', 'STOP_NAME': 'stop_name', 'LATITUDE': 'lat', 'LONGITUDE': 'lon'},
        inplace=True,
    )
    return all_stops


@st.cache
def filter_df_by_radius(df: pd.DataFrame, stop_id: int, radius: int = 1000) -> pd.DataFrame:
    init_lat = df[df['stop_id'] == stop_id]['lat'].values[0]
    init_lon = df[df['stop_id'] == stop_id]['lon'].values[0]

    def filter_row_function(row) -> bool:
        if great_circle((init_lat, init_lon), (row['lat'], row['lon'])).m <= radius:
            return True
        return False

    mask = df.apply(filter_row_function, axis=1)
    return df[mask]


def show_map(df, color: str = None, zoom: int = 12):
    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lon',
        hover_name='stop_name',
        hover_data=['stop_id'],
        color=color,
        zoom=zoom,
        mapbox_style='carto-positron',
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def show_plots(
    df: pd.DataFrame,
    method: str,
    metric: str,
    threshold: Optional[int] = None,
    criterion: str = 'distance',
):
    dendrogram = ff.create_dendrogram(
        df[['lat', 'lon']],
        distfun=lambda x: pdist(x, metric=metric),
        linkagefun=lambda x: linkage(x, method=method),
        color_threshold=threshold,
    )

    if threshold is not None:
        dendrogram.add_hline(y=threshold, opacity=0.5)

    dendrogram.update_layout(xaxis_title='Object number', yaxis_title='Distance')

    st.plotly_chart(dendrogram, use_container_width=True)

    link = linkage(df[['lat', 'lon']], method=method, metric=metric)
    reverse_distance = link[:, 2][::-1]

    scree_plot = px.line(x=range(1, len(reverse_distance) + 1), y=reverse_distance, markers=True)
    if threshold is not None:
        scree_plot.add_hline(y=threshold, opacity=0.5)
    scree_plot.update_layout(xaxis_title='Step', yaxis_title='Distance')
    st.plotly_chart(scree_plot, use_container_width=True)

    if threshold is not None:
        df_with_cluster_number = df.copy()
        df_with_cluster_number['cluster'] = fcluster(link, threshold, criterion=criterion)
        show_map(df_with_cluster_number, color='cluster')
