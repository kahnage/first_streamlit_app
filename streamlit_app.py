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

def get_fruityvice_data(this_fruit_choice):
  # Get Fruityvice api data
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + str(fruit_choice))
  #streamlit.text(fruityvice_response.json()) # Just writes to the screen

  # take json data and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  
  return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')

try:
  # Get data from user
  fruit_choice = streamlit.text_input('What fruit would you like to check?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info")
  else:
    streamlit.write('The user entered', fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice)
    
    # output to screen as table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Select * from fruit_load_list")
    return my_cur.fetchall()
  # Connect to Snowflake
  
  my_cur = my_cnx.cursor()
  #my_cur.execute("Select current_user(), current_account(), current_region()")
  #my_data_row = my_cur.fetchone()
  #streamlit.text("Hello from Snowflake:")
  #streamlit.text(my_data_row)

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  #   my_cur.execute("Select * from fruit_load_list")
  #   my_data_row = my_cur.fetchall()
  #   streamlit.text("The fruit list contains:")

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(insert_row_snowflake)
  
# Get data from user
# fruit_choice = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
# streamlit.write('The user entered', fruit_choice)

# my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + fruit_choice + "')")


# STOP REFRESHING ENTIRE PAGE
streamlit.stop()
