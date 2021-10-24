from typing import List

import statsmodels.api as sm
import streamlit as st

from src.tasks.task6.common import StateVar


def _check_p_value(p_value: float, alpha: float):
    if p_value < alpha:
        st.markdown(rf'p-value $$< \alpha = {alpha} \Rightarrow$$ доли статистически значимо различаются.')
    else:
        st.markdown(rf'p-value $$> \alpha = {alpha} \Rightarrow$$ доли статистически значимо не различаются.')


def show_results(d: List[int], n: List[int]):
    st.header('Результаты')

    z_stat, p_value = sm.stats.proportions_ztest(d, n)

    st.markdown(
        f"""
        z-метка $$= {z_stat}$$ </br>
        p-value $$= {p_value}$$
        """,
        unsafe_allow_html=True,
    )

    st.header('Вывод')
    _check_p_value(p_value, StateVar.SIGNIFICANCE_LEVEL.get())
