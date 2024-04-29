import streamlit as st
import os
import sys
import mysql.connector
from dotenv import load_dotenv

sys.path.append(os.path.abspath("pages"))

load_dotenv(override=True)
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=DB_PASSWORD,
    database="RecipeGenerator"
)
mycursor = mydb.cursor()

st.title("Community Recipes")
st.caption(
    "Need some inspiration for what to cook? View the most recent community recipes here!")


def load_gallery(most_recent_amount, pressed=False):
    mycursor.execute(
        f"SELECT * FROM Recipes ORDER BY created_at DESC LIMIT {most_recent_amount}")
    recipes = mycursor.fetchall()
    if not recipes:
        st.warning("No recipes found. Maybe make one?")
        return

    for recipe in recipes:
        food_name = recipe[1]
        meal = recipe[3]
        image_url = str(recipe[-1])
        if not image_url.startswith("https"):
            if not image_url.startswith("http"):
                st.warning(
                    f"Invalid URL for image of {food_name}. Skipping...")
                continue
        if not pressed:
            st.divider()
            st.header(food_name)
            st.image(image_url, width=300)
            with st.expander("Show more details"):
                st.write(meal)

        else:
            st.divider()
            st.header(food_name)
            st.image(image_url, width=300)


c1, c2 = st.columns(2)
show = c1.button("Show recipes")
hide = c1.button("Hide recipes")
clear = c1.button("Clear recipes")
if clear:
    mycursor.execute("DELETE FROM Recipes")
    mydb.commit()
    st.success("Recipes cleared!")

if show:
    load_gallery(30)
else:
    load_gallery(30, True)
