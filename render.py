import base64
import streamlit as st
from datetime import timedelta, time, date


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<center><img src="data:image/svg+xml;base64,%s"/></center>' % b64
    st.image(svg)  # , unsafe_allow_html=True)


def rotate_svg(svg, angle, angle_vis):
    offset = int(887.04 / 2)

    return svg.replace(
        '<g id="rete">',
        '<g id="rete" transform="rotate('
        + str(angle + int(360 * 11 / 365) + angle_vis / 360)
        + ", "
        + str(offset)
        + ", "
        + str(offset)
        + ')">',
    ).replace(
        '<g id="reticule">',
        '<g id="reticule" transform="rotate('
        + str(angle_vis)
        + ", "
        + str(offset)
        + ", "
        + str(offset)
        + ')">',
    )


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    with st.spinner("..."):

        if "date_numeric" not in st.session_state:
            st.session_state["date_numeric"] = date.today()
        if "date_slider" not in st.session_state:
            st.session_state["date_slider"] = (
                st.session_state.date_numeric
                - date(st.session_state.date_numeric.year, 1, 1)
            ).days
        if "time_numeric" not in st.session_state:
            st.session_state["time_numeric"] = time()
        if "time_slider" not in st.session_state:
            st.session_state["time_slider"] = time()

        def update_date_slider():
            st.session_state.date_slider = (
                st.session_state.date_numeric
                - date(st.session_state.date_numeric.year, 1, 1)
            ).days

        def update_date_numeric():
            st.session_state.date_numeric = date(
                st.session_state.date_numeric.year, 1, 1
            ) + timedelta(days=st.session_state.date_slider)

        def update_time_slider():
            st.session_state.time_slider = st.session_state.time_numeric

        def update_time_numeric():
            st.session_state.time_numeric = st.session_state.time_slider

        f = open("figures/combined.svg")
        svg = f.read()
        f.close()

        with st.sidebar:
            with st.container(border=True):
                date_numeric = st.date_input(
                    "Date", key="date_numeric", on_change=update_date_slider
                )
                date_slider = st.slider(
                    "Day of Year",
                    # value=(date_numeric - date(date_numeric.year, 1, 1)).days,
                    min_value=0,
                    max_value=365,
                    key="date_slider",
                    on_change=update_date_numeric,
                )
                angle_rete = int(
                    360 * (date_numeric - date(date_numeric.year, 1, 1)).days / (365)
                )
                st.text(f"Mere rotation : {angle_rete}°")

            with st.container(border=True):
                time_numeric = st.time_input(
                    "Time", key="time_numeric", on_change=update_time_slider
                )
                time_slider = st.slider(
                    "Time",
                    min_value=time(0, 0),
                    max_value=time(23, 59),
                    key="time_slider",
                    on_change=update_time_numeric,
                )
                angle_vis = int(
                    360 * (time_numeric.hour + time_numeric.minute / 60) / 24
                )
                st.text(f"Day rotation : {angle_vis}°")

            st.download_button(
                label="⬇ Download SVG",
                data=rotate_svg(svg, angle_rete, angle_vis),
                file_name="astrolabe.svg",
            )

        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            st.write(" ")
        with col2:
            with st.container(border=True):
                st.write(date_numeric)
                st.write(time_slider)
                render_svg(rotate_svg(svg, angle_rete, angle_vis))
        with col3:
            st.write(" ")
