import streamlit as st
import requests
import pandas as pd

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_the_order = st.text_input("Name on Smoothie:")

if name_on_the_order:
    st.write("The name on your smoothie will be", name_on_the_order)

# Connect to Snowflake
cnx = st.connection("snowflake")

# Get fruit options
my_dataframe = cnx.query(
    "SELECT FRUIT_NAME, SEARCH_ON FROM smoothies.public.fruit_options",
    ttl=600
)

st.dataframe(my_dataframe, use_container_width=True)

# Ingredient selector
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    for fruit in ingredients_list:
        search_on = my_dataframe.loc[
            my_dataframe["FRUIT_NAME"] == fruit, "SEARCH_ON"
        ].iloc[0]

        st.subheader(f"{fruit} Nutrition Information")

        try:
            response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{search_on}",
                timeout=10
            )
            response.raise_for_status()
            fruit_data = pd.DataFrame(response.json())
            st.dataframe(fruit_data, use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Could not fetch nutrition info for {fruit}: {e}")

    submit_button = st.button("Submit Order")

    if submit_button:
        if not name_on_the_order.strip():
            st.warning("Please enter a name for your smoothie order.")
        else:
            try:
                cur = cnx.cursor()
                cur.execute(
                    """
                    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                    VALUES (?, ?)
                    """,
                    (ingredients_string, name_on_the_order.strip())
                )
                st.success(
                    f"Your Smoothie is ordered, {name_on_the_order.strip()}!",
                    icon="✅"
                )
            except Exception as e:
                st.error(f"Order could not be submitted: {e}")
