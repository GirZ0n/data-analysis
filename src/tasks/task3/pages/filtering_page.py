import streamlit as st

from src.tasks.task3.common.utils import filter_df_by_radius, get_all_stops, show_map


def stop_id_callback():
    st.session_state.stop_id = int(st.session_state.stop_id_input)


def radius_callback():
    st.session_state.radius = int(st.session_state.radius_input)


def show_filter_page():
    st.header('All stops')

    all_stops = get_all_stops()
    show_map(all_stops, zoom=8)

    st.header(f'Surrounding area')

    left_column, right_column = st.columns(2)

    with left_column:
        stop_id = int(
            st.number_input(
                'Enter a stop id:',
                value=st.session_state.setdefault('stop_id', 100209),
                on_change=stop_id_callback,
                key='stop_id_input',
            )
        )

    with right_column:
        radius = int(
            st.number_input(
                'Enter a radius (m):',
                value=st.session_state.setdefault('radius', 1000),
                on_change=radius_callback,
                key='radius_input',
            )
        )

    filtered_stops = filter_df_by_radius(all_stops, stop_id, radius)
    show_map(filtered_stops)
