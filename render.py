import streamlit as st
import base64
import textwrap


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

def rotate_svg(svg, angle):
    offset = int(887.04/2)

    return svg.replace('<g id="rete">', '<g id="rete" transform="rotate('+str(angle)+', '+str(offset) + ', '+ str(offset) + ')">')

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    from datetime import timedelta, time, date
    time_select = st.slider(
        "Date", min_value=date(2025, 1,1), max_value=date(2025, 12, 30)
    )

    

    t = int(360*(time_select-date(2025, 1,1)).days/(365))
    st.write((time_select-date(2025, 1,1)).days)
    print(type(time_select-date(2025, 1,1)))

    f = open("figures/combined.svg")
    svg = f.read()
    f.close()

    with st.container(border=True):
        st.write("### SVG Output")
        render_svg(rotate_svg(svg, t))
