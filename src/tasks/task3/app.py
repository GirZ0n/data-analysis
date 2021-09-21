import sys

import streamlit as st

sys.path.append('')
sys.path.append('../../..')

from src.tasks.task3.pages import PAGE_MAP


def main():
    st.set_page_config(layout='wide')

    with st.sidebar:
        page_name = st.radio('Choose page:', options=PAGE_MAP.keys())

    PAGE_MAP[page_name]()


if __name__ == '__main__':
    main()
