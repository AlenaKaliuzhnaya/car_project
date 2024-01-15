import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

data = pd.read_csv('vehicles_us.csv')

st.header('Choose your car!')
st.subheader('Use this app to select vehicle based on your preferences ')

import urllib.request
from PIL import Image

urllib.request.urlretrieve(
    'https://machineswithsouls.com/wp-content/uploads/2021/06/bmw-m-cars.jpg',
    "machineswithsouls.jpg")

img = Image.open("machineswithsouls.jpg")

st.image(img)

st.caption(':red[Choose your parameters here]')

price_range = st.slider(
    "What is your price range?",
    min_value=1.000000,
    max_value=375000.000000,
    value=(1.000000, 375000.000000)
)

actual_range = list(range(int(price_range[0]), int(price_range[1]) + 1))

car_models = st.multiselect(
    'Choose models of vehicles that you prefer',
    options=data['model']
)

choose_new_car = st.checkbox('Show only new vehicles')

if choose_new_car:
    filtered_data = data[(data['price'].isin(actual_range)) & (data['condition'] == 'new') & (data['model'].isin(car_models))]
else:
    filtered_data = data[data['price'].isin(actual_range)]

st.write('Here are your options with a split by price, condition, and model of the vehicle')

fig = px.scatter(filtered_data, x="model", y="price", color="condition", hover_name="model", log_x=True, size_max=60)
st.plotly_chart(fig)

st.write('Distribution of vehicles by fuel type')
fig2 = px.histogram(filtered_data, x="fuel", y="price")
st.plotly_chart(fig2)

st.write('Here is the list of recommended vehicles')
st.dataframe(filtered_data.sample(40))