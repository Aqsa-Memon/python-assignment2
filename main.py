import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #f5f5f5, #e0f7fa);
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #00796B;
            margin-bottom: 20px;
        }
        .convert-btn {
            display: block;
            margin: auto;
            background-color: #00796B !important;
            color: white !important;
            font-size: 20px !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
            text-align: center;
            transition: background 0.3s;
        }
        .convert-btn:hover {
            background-color: #004D40 !important;
        }
        .result-text {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin-top: 20px;
        }
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #00796B;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Header
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2099/2099238.png", width=80)
st.sidebar.markdown("<h2 class='sidebar-title'>🔄 Unit Converter</h2>", unsafe_allow_html=True)

# Conversion Categories
data = {
    "Length": {'Kilometers': 1000, 'Meters': 1, 'Centimeters': 0.01, 'Millimeters': 0.001,
               'Miles': 1609.34, 'Yards': 0.9144, 'Feet': 0.3048, 'Inches': 0.0254},
    "Weight": {'Kilograms': 1, 'Grams': 0.001, 'Milligrams': 0.000001, 'Pounds': 0.453592, 'Ounces': 0.0283495},
    "Temperature": None,
    "Volume": {'Liters': 1, 'Milliliters': 0.001, 'Cubic Meters': 1000, 'Gallons': 3.78541},
    "Time": {'Seconds': 1, 'Minutes': 60, 'Hours': 3600, 'Days': 86400},
}

conversion_type = st.sidebar.selectbox('Select Conversion Type', list( data.keys()))

# Header
st.markdown("<h1 class='title'>📏 Universal Unit Converter</h1>", unsafe_allow_html=True)

# Conversion Function
def convert_units(value, from_unit, to_unit, conversion_dict):
    if from_unit == to_unit:
        return value  
    try:
        base_value = value * conversion_dict[from_unit]
        return base_value / conversion_dict[to_unit]
    except (KeyError, ZeroDivisionError):
        return None 

def temperature_conversion(value, from_unit, to_unit):
    conversions = {
        ("Celsius", "Fahrenheit"): lambda x: x * 9/5 + 32,
        ("Celsius", "Kelvin"): lambda x: x + 273.15,
        ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
        ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
        ("Kelvin", "Celsius"): lambda x: x - 273.15,
        ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32
    }
    return conversions.get((from_unit, to_unit), lambda x: None)(value)

# User Input
st.write("### 🔢 Enter Value:")
value = st.number_input("", value=0.0, min_value=0.0 if conversion_type != "Temperature" else None)

st.write("### 🔄 Select Units:")
if conversion_type == "Temperature":
    units = ['Celsius', 'Fahrenheit', 'Kelvin']
else:
    units = list(data[conversion_type].keys())

col1, col2 = st.columns(2)
from_unit = col1.selectbox('From Unit', units, key="from_unit")
to_unit = col2.selectbox('To Unit', units, key="to_unit")

# Convert Button
if st.button('🔄 Convert', key="convert", help="Click to Convert", use_container_width=True):
    if conversion_type == "Temperature":
        result = temperature_conversion(value, from_unit, to_unit)
    else:
        result = convert_units(value, from_unit, to_unit, data[conversion_type])
    
    if result is not None:
        st.markdown(f"<p class='result-text'>✅ {value:,.2f} {from_unit} = {result:,.6f} {to_unit}</p>", unsafe_allow_html=True)
    else:
        st.error("⚠ Invalid conversion! Please check the selected units.")

# Sidebar Guide
st.sidebar.markdown("""
---
### 📌 How to Use:
1. Select a **conversion type** from the sidebar.
2. Enter a **value** in the input box.
3. Choose **From** and **To** units.
4. Click **Convert** and see the result! 🎉
---
""")
