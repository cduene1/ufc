import streamlit as st
import pandas as pd
import json
from scraper import fetch_event_data
from ufc_model import predict_ufc_fights

st.set_page_config(page_title="UFC Predictor", layout="wide")
st.title("🥋 UFC Real-Time Predictor")

# JSON upload fallback
uploaded = st.file_uploader("Upload event JSON (fallback)", type="json")
event = None
if uploaded:
    try:
        event = json.load(uploaded)
    except Exception as e:
        st.error(f"Error reading JSON: {e}")

if event is None:
    event_url = st.text_input("Event URL (leave blank for upcoming event)", "")
    if st.button("🔄 Refresh Data"):
        st.experimental_rerun()
    event = fetch_event_data(event_url or None)

if event.get('error'):
    st.error(f"Error fetching data: {event['error']}")

st.subheader(event.get("event_name", "Upcoming UFC Event"))
if event.get("location") and event.get("date"):
    st.caption(f"{event.get('location')} — {event.get('date')}")

fights = event.get("fights", [])
if not fights:
    st.info("No fights to display. Provide a valid Event URL or upload JSON.")
else:
    results = predict_ufc_fights(fights)
    for r in results:
        st.markdown(f"### 🥊 {r['matchup']}")
        st.metric("Predicted Winner", r["winner"], f"{r['confidence']}%")
        st.markdown(f"Method: {r['method']} | Go Distance: {r['go_distance']}")
        if r.get("upset_alert"):
            st.warning("⚠️ Potential Upset!")
        st.info(r["explanation"])
        st.markdown("---")

    df = pd.DataFrame(results)
    st.download_button("📥 Download All Predictions", df.to_csv(index=False), "ufc_predictions.csv", mime="text/csv")
