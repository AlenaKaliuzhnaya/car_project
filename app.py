import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
import urllib.request
from PIL import Image

data = pd.read_csv('vehicles_us.csv')

st.header('Choose your car!')
st.subheader('Use this app to select vehicle based on your preferences ')

urllib.request.urlretrieve(
    'https://machineswithsouls.com/wp-content/uploads/2021/06/bmw-m-cars.jpg',
    "machineswithsouls.jpg")

img = Image.open("machineswithsouls.jpg")

st.image(img)

st.caption(':red[Choose your parameters here]')
min_price = data['price'].min()
max_price = data['price'].max()

price_range = st.slider(
    "What is your price range?",
    min_value=int(min_price),
    max_value=int(max_price),
    value=(int(min_price), int(max_price)))


filtered_data = data[(data['price'] >= price_range[0]) & (data['price'] <= price_range[1])]

# car_models = st.multiselect(
#     'Choose models of vehicle that you prefer',
#     options=filtered_data['model'])


choose_new_car = st.checkbox('Show only new vehicles')

if choose_new_car:
    filtered_data = filtered_data[data.condition == 'new']

st.write('Here are your options with a split by price, condition and model of the vehicle')

fig = px.scatter(filtered_data, x="model_year", y="price", color="condition", hover_name="model",
                 log_x=True, size='price')
st.plotly_chart(fig, theme="streamlit")

st.write('Distribution of vehicles by fuel type')
fig2 = px.histogram(filtered_data, x="fuel", y="price")
st.plotly_chart(fig2)

st.write('Here are your options with a split by price, condition and model')

fig3 = px.bar(
   filtered_data, x="model", y="condition", color=["condition"]
)
st.plotly_chart(fig3)

st.write('Here is the list of recommended vehicles')
st.dataframe(filtered_data.sample(40))
