# Import python libraries
import streamlit as st
import plotly_express as px
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image
from collections import namedtuple
from math import radians, isclose, acos, asin, cos, sin, tan, atan, degrees, sqrt

# Insert icon of web app
icon = Image.open("resources/well.jpg")
# Page Layout
st.set_page_config(page_title="Drilling App", page_icon=icon)

# CSS code to improve the design of the web app
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
st.title("Drilling Engineering App :link:")

st.write("---")

st.markdown(
    """This App consists of plotting 3D wells trajectories as well as drilling
 basic calculations.
 - **Python Libraries:** streamlit, pandas, numpy, plotly, PIL
 """
)

# Fill in information about the project implemented in this app
expander_bar = st.expander("About")
expander_bar.write(
    "This project consists of plotting 3D well trajectories as well as drilling basic"
    " calculations."
)

# Insert image
image = Image.open("resources/dd.jpg")
st.image(image, width=100, use_column_width=True)

# Adding a mp4 video
st.markdown("**Drilling Fundamentals**")
video = open("resources/drilling.mp4", "rb")
st.video(video)
st.caption("Ulterra Drilling Techologies (2015). What is and Oil & Gas well?")

# Sidebar
st.sidebar.title(":arrow_down_small: **Navigation**")
uploaded_file = st.sidebar.file_uploader("Upload your csv file here")


# Pages
with st.sidebar:
    options = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data", "3D Wells", "Basic Calculations"],
        icons=["house", "clipboard-data", "tv", "calculator"],
    )


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


# Functions to calculate well profiles
Data = namedtuple("Input", "TVD KOP BUR DH")
Output = namedtuple("Output", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")


def well_J(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dh = data.DH
    if unit == "ingles":
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur
    if dh > R:
        dc = dh - R
    elif dh < R:
        dc = R - dh
    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc**2 + do**2)
    boc = degrees(acos(R / oc))
    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc**2 - R**2)
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_total = kop + (theta / bur) * 30 + tan_len
    output = Output(
        R=R,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_total=md_total,
    )
    names = ["R", "theta", "tvd_EOB", "MD_EOB", "DH_EOB", "Length_tan", "MD_Total"]
    for param, value in zip(names, output):
        if param == "theta":
            st.success(f"{param}: {value:.3f} degrees")
        else:
            st.success(f"{param}: {value:.3f} ft")


# Pozo S
# Functions to calculate well profiles
Data = namedtuple("Input", "TVD KOP BUR DOR DH")
Output = namedtuple(
    "Output",
    "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Lengh_tan Md_SOD TVD_SOD Dh_SOD Md_total",
)


def well_S(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dor = data.DOR
    dh = data.DH
    if unit == "ingles":
        R1 = 5729.58 / bur
    else:
        R1 = 1718.87 / bur
    if unit == "ingles":
        R2 = 5729.58 / dor
    else:
        R2 = 1718.87 / dor
    if dh > (R1 + R2):
        fe = dh - (R1 + R2)
    elif dh < (R1 + R2):
        fe = (R1 + R2) - dh
    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe**2 + eo**2)
    fg = R1 + R2
    fog = degrees(asin(fg / of))
    eog = fog - foe
    tvd_eob = kop + (R1 * sin(radians(eog)))
    md_eob = kop + ((eog / bur) * 100)
    d1 = R1 - R1 * cos(radians(eog))
    bc = sqrt(of**2 - fg**2)
    sod_md = kop + ((eog / bur) * 100) + bc
    sod_tvd = tvd_eob + (bc * cos(radians(eog)))
    d2 = d1 + (bc * sin(radians(eog)))
    md = kop + (((eog / bur) * 100) + bc) + ((eog / dor) * 100)
    TALLER = Output(
        R1=R1,
        R2=R2,
        Theta=eog,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=d1,
        Lengh_tan=bc,
        Md_SOD=sod_md,
        TVD_SOD=sod_tvd,
        Dh_SOD=d2,
        Md_total=md,
    )
    namesS = [
        "R1",
        "R2",
        "Theta",
        "TVD_EOB",
        "Md_EOB",
        "Dh_EOB",
        "Lengh_tan",
        "Md_SOD",
        "TVD_SOD",
        "Dh_SOD",
        "Md_total",
    ]
    for params, values in zip(namesS, TALLER):
        if params == "Theta":
            print(f"{params} -> {values:.3f} degrees")
        else:
            print(f"{params} -> {values:.3f} ft")


# Call file if exist
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# Call options of web app
if options == "Data":
    data(df)
elif options == "3D Wells":
    well_traj(df)
elif options == "Basic Calculations":
    if st.checkbox("J-Type Well"):
        st.subheader("**Enter input values**")
        tvd = st.number_input("Enter tvd value: ")
        kop = st.number_input("Enter kop value: ")
        bur = st.number_input("Enter bur value: ")
        dh = st.number_input("Enter dh value: ")
        st.subheader("**Show results**")
        well_J(Data(tvd, kop, bur, dh))

    elif st.checkbox("S-Type Well"):
        st.subheader("**Enter input values**")
        tvd = st.number_input("Enter tvd value: ")
        kop = st.number_input("Enter kop value: ")
        dh = st.number_input("Enter dh value: ")
        bur = st.number_input("Enter bur value: ")
        dor = st.number_input("Enter dor value: ")
        st.subheader("**Show results**")
        well_S(Data(tvd, kop, bur, dor, dh))
