
import streamlit as st
import os
from data_fetcher import fetch_all_sources

st.title('UFC Predictor with Proxy Support')

proxy_url = st.text_input('Optional Proxy URL (http://user:pass@host:port)', '')
if proxy_url:
    os.environ['PROXY_URL'] = proxy_url

ufcstats_url = st.text_input('UFCStats Event URL')
tapology_slug = st.text_input('Tapology Slug')
sherdog_id = st.text_input('Sherdog Event ID')

if st.button('Fetch Fights'):
    fights = fetch_all_sources(ufcstats_url, tapology_slug, sherdog_id)
    if fights:
        st.success(f"Retrieved {len(fights)} fights")
        st.json(fights)
    else:
        st.error("No data fetched. Check URLs or proxy.")
