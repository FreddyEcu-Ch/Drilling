# Import python libraries
import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image

# Page Layout
st.set_page_config(page_title="Drilling App", page_icon='🛢')

# CSS cod🛢 to improve the design of the web app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
</style>""",
    unsafe_allow_html=True,
)

# Ttile of app
st.title("Drilling Engineering App")

st.write("---")

st.markdown("""This App consists of plotting 3D wells trajectories as well as drilling
 basic calculations.
 - **Python Libraries:** streamlit, pandas, numpy, plotly, PIL
 """)

# Fill in information about the project implemented in this app
expander_bar = st.expander("About")
expander_bar.write("This project consists of plotting 3D well trajectories as well as drilling basic calculations.")

# Insert image
image = Image.open("dd.jpg")
st.image(image, width=100, use_column_width=True)

# Adding a mp4 video
st.markdown("**Drilling Fundamentals**")
video = open("drilling.mp4", "rb")
st.video(video)
st.caption("Ulterra Drilling Techologies (2015). What is and Oil & Gas well?")

# Sidebar
st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload your csv file here")

# Pages
options = st.sidebar.radio("Pages", options=["Home", "Data", "3D Wells", "Basic Calculations"])


# Useful functions
def data(dataframe):
    st.header("Data Header")
    st.write(dataframe.head())
    st.header("Data Statistics")
    st.write(dataframe.describe())


def well_traj(dataframe):
    x_axis_val = st.selectbox("Select dispns", options=df.columns)
    y_axis_val = st.selectbox("Select dispew", options=df.columns)
    z_axis_val = st.selectbox("Select tvd", options=df.columns)
    fig = px.line_3d(dataframe, x_axis_val, y_axis_val, z_axis_val)
    st.plotly_chart(fig)


# Call file if exist
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# Call options of web app
if options == "Data":
    data(df)
elif options =="3D Wells":
    well_traj(df)

