# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests  
import pandas as pd



# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw:")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Customer name on Smoothie will be: ", name_on_order)

st.write(
  """ choose your fruits you want in your custom smoothie!
  """
)

# option = st.selectbox(
#     "what is your favourit fruit ?",
#     ("Banana", "Strawberries", "peaches"),
# )

# st.write("You selected:", option)

cnx= st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("Fruit_name"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#converting the snowpark DataFrame to a Pandas Dataframe so we can use the LOC function
pd_df= my_dataframe.to_pandas()
st.dataframe(pd_df)


selected_value = st.multiselect("Choose up to 5 ingredients:",my_dataframe,max_selections=5)
#st.write("You selected:", selected_value)


if selected_value:
    st.write("You selected:")
    #st.text(selected_value)
    ingredient_list = ''

    for fruit_selected in selected_value:
        ingredient_list += fruit_selected + ' '
    #added as part of lesson 12
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_selected, 'SEARCH_ON'].iloc[0]
        if search_on is None:
            search_on=fruit_selected
        st.write('The search value for ', fruit_selected,' is ', search_on, '.')
        st.subheader(fruit_selected + 'Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
        df = smoothiefroot_response.json()
        st.dataframe(data=df,use_container_width=True)

    st.write(ingredient_list)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
                    values ('""" + ingredient_list +"""','"""+ name_on_order +"""')"""

    #st.write(my_insert_stmt)
    
    is_clicked = st.button("Submit order")
    if is_clicked:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        #st.write(my_insert_stmt)


