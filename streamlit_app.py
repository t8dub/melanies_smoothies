# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
# Focus on the FRUIT_NAME Column

# To use a Snowpark COLUMN function named "col" we need to import it
# into our app. We'll place the import statement close to where we plan
# to use it. This will make more sense for beginners as they will be able
# to see why we imported it and how it is used. In a later lab, we'll
# move it up with other import statements in order to show good code
# organization.

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


# Adding a select box

# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
# )
# st.write("Your favorit fruit is:", option)


# Display the full Fruit Options List from loaded database
# add .select(col('FRUIT_NAME')) to bring in only the 1 column
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


# We are placing the multiselect entries into a variable called "ingredients."
# We can then write "ingredients" back out to the screen. Our ingredients variable
# is an object or data type called a LIST. So it's a list in the traditional sense
# of the word, but it is also a datatype or object called a LIST. A LIST is different
# than a DATAFRAME which is also different from a STRING!

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# Inserting order name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


# We can use the st.write() and st.text() methods to take a closer look at what is
# contained in our ingredients LIST. 
# top line really means 'if not null'; so we dont show empty brackets.

if ingredients_list:
 #  st.write(ingredients_list) # didn't need anymore
 #  st.text(ingredients_list) # didn't need anymore
    # indentations matter in python, indented lines here are part of the 'if' block
    ingredients_string = ''
    # line below = "for each fruit_chosen in ingredients_list multiselect box: do 
    # everything below this line that is indented". We never defined a variable 
    # named fruit_chosen, but Python understands that whatever is placed in that
    # position is a counter for items in the list. So we could just as easily say: 
    # "for x in ingredients_list:" The += operator means "add this to what is already
    # in the variable" so each time the FOR Loop is repeated, a new fruit name is 
    # appended to the existing string.
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    # Output the string. The st.write() command should be part of the IF block but
    # not part of the FOR Loop. You can try it as part of the FOR Loop and see an 
    # interesting result. In either case, you'll see that the result is going to need
    # some additional work. Don't worry, we'll make the string look a little better in
    # the next lab. 
    # st.write(ingredients_string) # didn't need anymore
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

