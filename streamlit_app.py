# Streamlit smoothie order form with fruit selection from Snowflake
# Co-authored with CoCo
# Import python packages
import streamlit as st
import requests  
import pandas as pd
from snowflake.snowpark.functions import col #when_matched
#get_active_session

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)



name_on_order = st.text_input("Name on Smoothie")
st.write("Name on your Smoothie is", name_on_order)

#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
'Choose up to 5 fruits'
, my_dataframe
)
if ingredients_list:
    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write("Your ingredients:", ingredients_string)

    time_to_order = st.button("Submit Order")
    if time_to_order:
        my_insert_stmt = "INSERT INTO smoothies.public.orders(ingredients, NAME_ON_ORDER) VALUES (?, ?)"
        session.sql(my_insert_stmt, params=[ingredients_string, name_on_order]).collect()
        st.success("Your smoothie order has been submitted!", icon="✅")




# Always show current orders table
#st.subheader("Orders in Table:")
##st.dataframe(data=orders_df, use_container_width=True)
