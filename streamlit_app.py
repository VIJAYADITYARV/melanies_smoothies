# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Get the Snowflake session
session = get_active_session()

# Get the name for the smoothie order
name_on_order = st.text_input('Name on smoothie order:')

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")

st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Keep this commented out to keep the app tidy
# st.dataframe(data=my_dataframe, use_container_width=True)

# Allow users to select multiple ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen

    st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""



    st.write(my_insert_stmt)

    if st.button('Submit'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
