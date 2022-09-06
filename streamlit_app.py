import pandas
import requests
import snowflake.connector
import streamlit as st
from urllib.error import URLError


st.markdown("# Main page")
st.sidebar.markdown("# Main page")

st.title('My new healthy diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
    fruityvice_res = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
    fruityvice_normalized = pandas.json_normalize(fruityvice_res.json())
    return fruityvice_normalized


st.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
    if not fruit_choice:
        st.error('Please enter fruit name to get information.')
    else:
        fruityvice_data = get_fruityvice_data(fruit_choice)
        st.dataframe(fruityvice_data)

except URLError as e:
    st.error()



def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

st.header("Our Fruit List:")
if st.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    fruit_list = get_fruit_list()
    my_cnx.close()
    st.dataframe(fruit_list)

def add_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
        return f'Thanks for adding {new_fruit}'

new_fruit = st.text_input('What fruit would you like add?')
if st.button('Add your Favorite'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    st.text(add_fruit(new_fruit))
    my_cnx.close()


