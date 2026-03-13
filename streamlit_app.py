# Import python packages
import streamlit as st
import requests
import pandas as pd

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_the_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be', name_on_the_order)

# Connect to Snowflake
cnx = st.connection('snowflake')

# Get fruit options
my_dataframe = cnx.query("SELECT FRUIT_NAME,SEARCH_ON FROM smoothies.public.fruit_options")


# Ingredient selector
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'],
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string += i + ' '

        search_on = my_dataframe.loc[pd_df['FRUIT_NAME'] == i,'SEARCH_ON'].iloc[0]
        st.write('The Search value for ', i, ' is' , search_on, '.')
        st.subheader(i+'Nutrition Information')
        response = requests.get(f'https://my.smoothiefroot.com/api/fruit/{i}')
        sf_df = st.dataframe(data = response.json(), use_container_width = True)

        
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_the_order}')
    """

    submit_button = st.button('Submit Order')
    if submit_button:
        with cnx.cursor() as cur:
            cur.execute(my_insert_stmt)
        st.success(f'Your Smoothie is ordered, {name_on_the_order}!', icon="✅")

