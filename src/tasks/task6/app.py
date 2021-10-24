import datetime
from typing import List

import pandas as pd
import streamlit as st

from src.tasks.task6 import DATA_FOLDER
from src.tasks.task6.common import Column, PERIOD_MAP, Period, StateVar
from src.tasks.task6.fragments.data import show_data
from src.tasks.task6.fragments.results import show_results
from src.tasks.task6.fragments.sidebar import show_sidebar


@st.cache
def read_stats() -> pd.DataFrame:
    df = pd.read_csv(DATA_FOLDER / 'coronavirus_russia.csv')
    df[Column.DATE.value] = pd.to_datetime(df[Column.DATE.value], format='%d.%m.%Y').dt.date
    return df


def _get_columns(per_day: bool) -> List[str]:
    if per_day:
        return [Column.INFECTIONS_PER_DAY.value, Column.DEATHS_PER_DAY.value, Column.RECOVERED_PER_DAY.value]

    return [Column.INFECTIONS.value, Column.DEATHS.value, Column.RECOVERED.value]


def _get_stats_by_date(stats: pd.DataFrame, date: datetime.date, *, per_day: bool) -> pd.DataFrame:
    columns = _get_columns(per_day)

    return stats[
        (stats[Column.DATE.value] == date)
        & (stats[Column.REGION.value].isin([StateVar.REGION_A.get(), StateVar.REGION_B.get()]))
    ][
        [
            Column.REGION.value,
            *columns,
        ]
    ].set_index(
        Column.REGION.value
    )


def _get_filtered_stats(stats: pd.DataFrame) -> pd.DataFrame:
    if StateVar.PERIOD.get() == Period.PER_DAY:
        return _get_stats_by_date(stats, StateVar.DATE.get(), per_day=True)
    elif StateVar.PERIOD.get() == Period.PER_MONTH:
        curr_date = StateVar.DATE.get()
        prev_date = curr_date - datetime.timedelta(days=30)
        if prev_date in stats[Column.DATE.value].unique():
            curr_stats = _get_stats_by_date(stats, curr_date, per_day=False)
            prev_stats = _get_stats_by_date(stats, prev_date, per_day=False)
            return curr_stats - prev_stats
        else:
            return _get_stats_by_date(stats, curr_date, per_day=False)
    else:
        return _get_stats_by_date(stats, StateVar.DATE.get(), per_day=False)


def _get_success_column() -> str:
    if StateVar.PERIOD.get() == Period.PER_DAY:
        return Column.DEATHS_PER_DAY.value

    return Column.DEATHS.value


def main() -> None:
    st.title('A/B тестирование')

    stats = read_stats()
    show_sidebar(stats)

    if StateVar.REGION_A.get() == StateVar.REGION_B.get():
        st.error('Регионы не должны совпадать')
        st.stop()

    filtered_stats = _get_filtered_stats(stats)

    success_column = _get_success_column()
    d, n = show_data(filtered_stats, success_column)
    show_results(d, n)


if __name__ == '__main__':
    st.set_page_config(layout='wide', page_title='A/B тестирование')
    main()
