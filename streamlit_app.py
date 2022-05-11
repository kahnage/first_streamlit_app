import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('This is a title')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Read in CSV
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Pick List for fruit
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the df on the page (as table)
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')

try:
  # Get data from user
  fruit_choice = streamlit.text_input('What fruit would you like to check?')
  if not fruit_choice:
    streamlit.erro("Please select a fruit to get info")
  else:
    streamlit.write('The user entered', fruit_choice)

    # Get Fruityvice api data
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + str(fruit_choice))
    #streamlit.text(fruityvice_response.json()) # Just writes to the screen

    # take json data and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # output to screen as table
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()


# STOP REFRESHING ENTIRE PAGE
streamlit.stop()

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("Select current_user(), current_account(), current_region()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("Select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit list contains:")
streamlit.dataframe(my_data_row)

# Get data from user
fruit_choice = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
streamlit.write('The user entered', fruit_choice)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
