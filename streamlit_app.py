# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col




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

cnx= st.connect("snoflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("Fruit_name"))
#st.dataframe(data=my_dataframe, use_container_width=True)



selected_value = st.multiselect("Choose up to 5 ingredients:",my_dataframe,max_selections=5)
#st.write("You selected:", selected_value)


if selected_value:
    st.write("You selected:")
    #st.text(selected_value)
    ingredient_list = ''

    for fruit_selected in selected_value:
        ingredient_list += fruit_selected + ' '

    st.write(ingredient_list)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
                    values ('""" + ingredient_list +"""','"""+ name_on_order +"""')"""

    st.write(my_insert_stmt)
    
    is_clicked = st.button("Submit order")
    if is_clicked:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        #st.write(my_insert_stmt)