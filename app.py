import urllib.request
import pandas as pd
import plotly.express as px
import streamlit as st
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
min_price = int(data['price'].min())
max_price = int(data['price'].max())

price_range = st.slider(
    "What is your price range?",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price))

filtered_data = data[(data['price'] >= price_range[0]) & (data['price'] <= price_range[1])]

choose_new_car = st.checkbox('Show only new vehicles')

if choose_new_car:
    filtered_data = filtered_data[data.condition == 'new']

st.write('Here are your options with a split by price, condition and model of the vehicle')

fig = px.scatter(filtered_data, x="model_year", y="price", color="condition", hover_name="model",
                 log_x=True, size='price')
st.plotly_chart(fig, theme="streamlit")

st.write('Distribution of vehicles by fuel type')

total_count_per_fuel = filtered_data['fuel'].value_counts()

filtered_data['count_percentage'] = (filtered_data.groupby('fuel')['fuel'].transform('count') / filtered_data['fuel']
                                     .count()) * 100

model_counts = filtered_data['model'].value_counts(normalize=True) * 100

# Create a bar chart using Plotly Express
fig2 = px.bar(x=model_counts.index, y=model_counts.values, labels={'x': 'Car Model', 'y': 'Percentage of Count'},
              title='Distribution of Car Models')

st.plotly_chart(fig2)

st.write('Here is the list of recommended vehicles')
st.dataframe(filtered_data.sample(40))
