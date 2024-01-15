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

columns_to_replace = ['paint_color']

for column in columns_to_replace:
    print(column)
    data[column] = data[column].fillna('unknown')
    
column_to_replace = ['is_4wd']

for column in column_to_replace:
    print(column)
    data[column] = data[column].fillna('0')
    
    
data['model_year'] = data['model_year'].fillna(data.groupby(['model'])['model_year'].transform('median'))
data['odometer'] = data['odometer'].fillna(data.groupby(['model'])['odometer'].transform('median'))
data['odometer'] = data['odometer'].fillna(data.groupby(['model_year'])['odometer'].transform('median'))
data['cylinders'] = data['cylinders'].fillna(data.groupby(['model'])['cylinders'].transform('median'))


def replace_wrong_models(wrong_models, correct_models):
    for element in wrong_models:
        data['model'] = data['model'].replace(element, correct_models)    
        
replace_wrong_models(['ford f-250 sd', 'ford f250 super duty'], 'ford f-250 super duty')
replace_wrong_models(['ford f150', 'fford f-150'], 'ford f-150')
replace_wrong_models(['ford f250'], 'ford f-250')
replace_wrong_models(['ford f350 super duty', 'ford f-350 sd'], 'ford f-350 super duty')

st.caption('Choose your parameters here')
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

st.write('Here you can choose vehicle condition based on model year and price')

fig = px.scatter(filtered_data, x="model_year", y="price", color="condition", hover_name="model",
                 log_x=True, size='price')
st.plotly_chart(fig, theme="streamlit")

st.write('Distribution of vehicles by fuel type')
fig2 = px.histogram(filtered_data, x="fuel", y="price")
avg_price = filtered_data['price'].mean()
st.plotly_chart(fig2)

total_count_per_fuel = filtered_data['fuel'].value_counts()

filtered_data['count_percentage'] = (filtered_data.groupby('fuel')['fuel'].transform('count') / filtered_data['fuel']
                                     .count()) * 100

model_counts = filtered_data['model'].value_counts(normalize=True) * 100

# Create a bar chart using Plotly Express
fig2 = px.bar(x=model_counts.index, y=model_counts.values, labels={'x': 'Car Model', 'y': 'Percentage of Count'},
              title='Distribution of Car Models')

st.plotly_chart(fig2)

st.write('Here is the list of recommended vehicles')
st.dataframe(filtered_data.sample())
