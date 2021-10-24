from enum import Enum, unique
from typing import Any, Optional

import streamlit as st


@unique
class StateVar(Enum):
    DATE = 'date'
    PERIOD = 'period'
    REGION_A = 'region_a'
    REGION_B = 'region_b'
    SIGNIFICANCE_LEVEL = 'significance_level'

    def get(self, *, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self.value, default)

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value


@unique
class Column(Enum):
    DATE = 'Дата'
    REGION = 'Регион'
    RECOVERED_PER_DAY = 'Выздоровлений за день'
    INFECTIONS_PER_DAY = 'Заражений за день'
    DEATHS_PER_DAY = 'Смертей за день'
    RECOVERED = 'Выздоровлений'
    INFECTIONS = 'Заражений'
    DEATHS = 'Смертей'


@unique
class Period(Enum):
    PER_DAY = 'per_day'
    PER_MONTH = 'per_month'
    ALL = 'all'


PERIOD_MAP = {
    'За день': Period.PER_DAY,
    'За месяц': Period.PER_MONTH,
    'За всё время': Period.ALL,
}
