import streamlit as st
import os
import sys
from streamlit_star_rating import st_star_rating
sys.path.append(os.path.abspath("pages"))

st.title("Community Recipes")
st.caption(
    "Need some inspiration for what to cook? View the most recent community recipes here!")


def leave_thanks():
    st.write("Thank you for your review!")


def load_gallery(most_recent_amount, pressed=False):
    with open("pages/food.txt", "r") as f:
        recipes = f.read().split("]")
    for i in range(most_recent_amount):
        try:
            recipe = recipes[i]
            if len(recipe) == 0:
                continue
            if not pressed:
                food_name = recipe.split(" ||| ")[0]
                meal = recipe.split(" ||| ")[1]
                image = recipe.split(" ||| ")[2]

                st.divider()
                st.header(food_name)
                st.image(image, width=300)
                with st.expander("Show more details"):
                    st.write(meal)
                    stars = st_star_rating(label="Leave a review on the recipe!",
                                           maxValue=5, defaultValue=1, key=f"review{i}", dark_theme=True, size=20)
            else:
                image = recipe.split(" ||| ")[2]
                food_name = recipe.split(" ||| ")[0]

                st.divider()
                st.header(food_name)
                st.image(image, width=300)
        except IndexError:
            break


c1, c2 = st.columns(2)
show = c1.button("Show recipes")
hide = c1.button("Hide recipes")
if c1.button("Clear recipes"):
    with open("pages/food.txt", "w") as f:
        f.write("")
num = c2.number_input("Number of recipes to show",
                      min_value=1, max_value=30, value=10)
if show:
    load_gallery(num)
else:
    load_gallery(num, True)
