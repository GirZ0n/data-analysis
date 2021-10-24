import pandas as pd
import streamlit as st

from src.tasks.task6.common import Column, PERIOD_MAP, StateVar


def show_sidebar(stats: pd.DataFrame) -> None:
    with st.sidebar:
        date = st.date_input(
            label='Дата:',
            min_value=stats[Column.DATE.value].min(),
            max_value=stats[Column.DATE.value].max(),
            value=stats[Column.DATE.value].max(),
        )
        StateVar.DATE.set(date)

        period = st.radio('Период:', options=PERIOD_MAP.keys())
        StateVar.PERIOD.set(PERIOD_MAP[period])

        regions = sorted(stats[Column.REGION.value].unique())

        region_a = st.selectbox('Регион А:', options=regions, index=regions.index('Москва'))
        StateVar.REGION_A.set(region_a)

        region_b = st.selectbox('Регион B:', options=regions, index=regions.index('Санкт-Петербург'))
        StateVar.REGION_B.set(region_b)

        significance_level = st.number_input(
            r'Уровень значимости:',
            min_value=float(0),
            max_value=float(1),
            value=0.01,
            step=0.1,
        )
        StateVar.SIGNIFICANCE_LEVEL.set(significance_level)
