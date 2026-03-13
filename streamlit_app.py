# Import python packages
import streamlit as st

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_the_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be', name_on_the_order)

# Connect to Snowflake
cnx = st.connection('snowflake')

# Get fruit options
my_dataframe = cnx.query("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")

# Ingredient selector
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME']
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_the_order}')
    """

    submit_button = st.button('Submit Order')
    if submit_button:
        with cnx.cursor() as cur:
            cur.execute(my_insert_stmt)
        st.success(f'Your Smoothie is ordered, {name_on_the_order}!', icon="✅")
