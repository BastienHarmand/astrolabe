import streamlit as st
import base64
from datetime import timedelta, time, date
import textwrap


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<center><img src="data:image/svg+xml;base64,%s"/></center>' % b64
    st.write(html, unsafe_allow_html=True)


def rotate_svg(svg, angle):
    offset = int(887.04 / 2)

    return svg.replace(
        '<g id="rete">',
        '<g id="rete" transform="rotate('
        + str(angle + int(360 * 11 / 365))
        + ", "
        + str(offset)
        + ", "
        + str(offset)
        + ')">',
    )


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    if "date_numeric" not in st.session_state:
        st.session_state["date_numeric"] = date.today()
    if "date_slider" not in st.session_state:
        st.session_state["date_slider"] = (
            st.session_state.date_numeric
            - date(st.session_state.date_numeric.year, 1, 1)
        ).days

    def update_date_slider():
        st.session_state.date_slider = (
            st.session_state.date_numeric
            - date(st.session_state.date_numeric.year, 1, 1)
        ).days

    def update_date_numeric():
        st.session_state.date_numeric = date(
            st.session_state.date_numeric.year, 1, 1
        ) + timedelta(days=st.session_state.date_slider)

    f = open("figures/combined.svg")
    svg = f.read()
    f.close()

    with st.sidebar:
        with st.container(border=True):
            date_select = st.date_input(
                "Date", date.today(), key="date_numeric", on_change=update_date_slider
            )
            time_select = st.slider(
                "Day of Year",
                value=(date_select - date(date_select.year, 1, 1)).days,
                min_value=0,
                max_value=365,
                key="date_slider",
                on_change=update_date_numeric,
            )
            angle = int(360 * (date_select - date(date_select.year, 1, 1)).days / (365))
            st.text(f"Mere rotation : {angle}°")

        st.download_button(
            label="⬇ Download SVG",
            data=rotate_svg(svg, angle),
            file_name="astrolabe.svg",
        )

    col1, col2, col3 = st.columns([1, 10, 1])

    with col1:
        st.write(" ")

    with col2:
        with st.container(border=True):
            st.write(date_select)
            render_svg(rotate_svg(svg, angle))

    with col3:
        st.write(" ")
