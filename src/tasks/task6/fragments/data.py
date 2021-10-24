from typing import List, Tuple

import pandas as pd
import streamlit as st

from src.tasks.task6.common import StateVar


def _show_data_from_region(
    stats: pd.DataFrame,
    region: str,
    region_symbol: str,
    success_column_name: str,
) -> Tuple[int, int]:
    st.subheader(region)

    d = stats.loc[region, success_column_name]
    n = stats.loc[region].sum()

    st.markdown(
        f"""
          $$d_{region_symbol} = {d}$$ — смертей </br>
          $$n_{region_symbol} = {n}$$ — подтверждённых диагнозов
          """,
        unsafe_allow_html=True,
    )

    st.markdown(rf'$$\displaystyle\frac{{d_{region_symbol}}}{{n_{region_symbol}}} = {d / n}$$ — летальность')

    return d, n


def show_data(stats: pd.DataFrame, success_column_name: str) -> Tuple[List[int], List[int]]:
    st.header('Данные')
    left_column, right_column = st.columns(2)

    with left_column:
        d1, n1 = _show_data_from_region(stats, StateVar.REGION_A.get(), 'A', success_column_name)

    with right_column:
        d2, n2 = _show_data_from_region(stats, StateVar.REGION_B.get(), 'B', success_column_name)

    return [d1, d2], [n1, n2]
