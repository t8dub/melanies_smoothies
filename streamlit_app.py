# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Display the full Fruit Options List from loaded database
# add .select(col('FRUIT_NAME')) to bring in only the 1 column
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop() # diagnostic

# Convert the Snowpark dataframe to a Pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop() # diagnostic

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# Inserting order name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        # to get the "Search On" Value
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    # Output the string. 
    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    # st.write(my_insert_stmt) # diagnostic - didn't need anymore
    # st.stop() # diagnostic - didn't need anymore

    # Add a Submit Button
    time_to_insert = st.button('Submit Order')

    # Insert the order into snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")




