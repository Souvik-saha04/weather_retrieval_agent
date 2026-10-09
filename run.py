import json
import streamlit as st
from model import get_weather, get_weather_response

st.set_page_config(page_title="Weather Assistant", page_icon="🌤️")

st.title("🌤️ Weather Assistant")

with st.form("weather_form"):
    city = st.text_input("Enter the name of the city", placeholder="e.g. Kolkata")
    submitted = st.form_submit_button("Get weather")

if submitted:
    city = city.strip()
    if not city:
        st.warning("Please enter a city name.")
        st.stop()

    # ---------- 1. get the data ----------
    with st.spinner(f"Fetching weather for {city}..."):
        data = get_weather(city)

    if "error" in data:
        st.error(data["error"]["message"])
        st.stop()

    loc = data["location"]
    cur = data["current"]

    # ---------- 2. BIG main card ----------
    with st.container(border=True):
        left, right = st.columns([2, 1])
        with left:
            st.subheader(f"📍 {loc['name']}, {loc['country']}")
            st.caption(f"Local time: {loc['localtime']}")
            st.markdown(
                f"<div style='font-size:96px; font-weight:300; line-height:1.1'>{cur['temp_c']}°C</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"### {cur['condition']['text']}")
            st.write(f"Feels like **{cur['feelslike_c']}°C**")
        with right:
            st.image("https:" + cur["condition"]["icon"].replace("64x64", "128x128"), width=150)

    # ---------- 3. MEDIUM cards ----------
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.metric("💨 Wind", f"{cur['wind_kph']} km/h")
        st.caption(f"Direction: {cur['wind_dir']}")
    with c2.container(border=True):
        st.metric("💧 Humidity", f"{cur['humidity']}%")
        st.progress(int(cur["humidity"]))
    with c3.container(border=True):
        st.metric("☀️ UV index", cur["uv"])
        st.caption("0 = low, 11+ = extreme")

    # ---------- 4. SMALL cards ----------
    small = [
        ("Pressure", f"{cur['pressure_mb']} mb"),
        ("Visibility", f"{cur['vis_km']} km"),
        ("Cloud cover", f"{cur['cloud']}%"),
        ("Precipitation", f"{cur['precip_mm']} mm"),
        ("Gust", f"{cur['gust_kph']} km/h"),
        ("Temperature (°F)", f"{cur['temp_f']}°F"),
    ]
    cols = st.columns(3)
    for i, (label, value) in enumerate(small):
        with cols[i % 3].container(border=True):
            st.caption(label)
            st.markdown(f"**{value}**")
    st.caption(f"Last updated: {cur['last_updated']}")

    # ---------- 5. AI explanation ----------
    st.divider()
    st.subheader("Assistant's take")
    try:
        with st.spinner("Asking the assistant..."):
            ai_text = get_weather_response(city)

        ai = json.loads(ai_text.replace("```json", "").replace("```", "").strip())

        for key, value in ai.items():
            with st.container(border=True):
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                if isinstance(value, dict):
                    for k, v in value.items():
                        st.write(f"{k.replace('_', ' ').title()}: {v}")
                elif isinstance(value, list):
                    for v in value:
                        st.write(f"- {v}")
                else:
                    st.write(value)
    except Exception as e:
        st.warning(f"The AI summary could not be shown: {e}")