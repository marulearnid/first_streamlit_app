import pandas
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError

streamlit.title('My new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
    fruityvice_res = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
    fruityvice_normalized = pandas.json_normalize(fruityvice_res.json())
    return fruityvice_normalized


streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
    if not fruit_choice:
        streamlit.error('Please enter fruit name to get information.')
    else:
        fruityvice_data = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_data)

except URLError as e:
    streamlit.error()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

streamlit.header("Our Fruit List:")
if streamlit.button('Get Fruit List'):
    fruit_list = get_fruit_list()
    streamlit.dataframe(fruit_list)

def add_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
        return f'Thanks for adding {new_fruit}'

new_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add your Favorite'):
    streamlit.text(add_fruit(new_fruit))


