from dotenv import load_dotenv
import os
import streamlit as st
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from streamlit_extras.stylable_container import stylable_container
from streamlit.components.v1 import html


st.set_page_config(page_title="Make a recipe!", layout="wide",
                   initial_sidebar_state="collapsed")


def make_meals(mealcount, user_prompt, dontwant, preferred_language, recipeNames, recipeList, meal_chain, max_time, calories, cuisine):
    for i in range(mealcount):
        with st.spinner(f"Generating meal {i+1} of {mealcount}..."):
            output = meal_chain.invoke(
                {"ingredients": user_prompt, "recipeNames": [i for i in recipeNames], "dontwant": dontwant, "language": preferred_language, "max_time": max_time, "calories": calories, "cuisine": cuisine})
            food_name = output["recipe"].strip().split("\n")[0]
            print(output["recipe"])
            recipeNames.append(food_name)
            search = GoogleSerperAPIWrapper(type="images")
            results = search.results(food_name)
            recipe_string = output["recipe"]
            image = results["images"][0]["imageUrl"]
            start_index = recipe_string.find(
                'Food name: ') + len('Food name: ')

            # Concatenate the food name, recipe string, and image URL
            output_string = f'{food_name} ||| {recipe_string} ||| {image}]'

            # This puts the most recent images on top
            with open('pages/food.txt', 'r+') as file:
                original_content = file.read()
                file.seek(0)
                file.write(output_string + original_content)

            # Assign each food to it's image
            recipeList[output["recipe"]] = image
            lorem = (f"""
<img src="{list(recipeList.values())[i]}" width="300">
<p><em>Please note these images should be to show how you could plate the food and may not be the exact recipe.</em></p>
<p>{recipe_string.split("Instructions:")[0]}</p>
<p>Instructions: {recipe_string.split("Instructions:")[1]}</p>
"""
            )

            html(lorem, height=800, scrolling=True)

            # a1.image(list(recipeList.values())[i], width=300)
            # a1.caption(
            #     "Please note these images should be to show how you could plate the food and may not be the exact recipe.")
            # a1.write(recipe_string.split("Instructions:")[0])
            # a1.write(f"""Instructions: {
            #          recipe_string.split("Instructions:")[1]}""")

    st.divider()
    st.caption("By Kabir Ghai, made in 2024")


load_dotenv(override=True)
SERPER = os.environ["SERPER_API_KEY"]
API_KEY = os.environ["OPENAI_API_KEY"]

llm = OpenAI(api_key=API_KEY, temperature=0.9)

recipe_prompt_template = PromptTemplate(
    template="""Provide a recipe of the following cuisine: {cuisine} that takes under {max_time} minutes to cook, with every word in {language}, using some or all of these ingredients if given: {ingredients}. 
    DON'T PICK ANYTHING CLOSE TO ANYTHING IN THIS LIST: {recipeNames}. 
    DO NOT INCLUDE ANY OF THESE UNDER ANY CIRCUMSTANCES: {dontwant}.
    The amount of calories in this recipe must be between the two numbers in these brackets: {calories}.
    
    You must stick to this format WITHOUT THE BRACKETS:
    FOLLOW THE FORMAT BELOW:
    FOLLOW THE FORMAT BELOW:
    FOLLOW THE FORMAT BELOW:
    
    Put the food name here

    Ingredients: (Put the ingredients here. Do not include the same ingredient more than once. Separate each ingredient with a newline and bullet points.)

    Instructions: (Put the instructions here. Separate each step with a newline and bullet points. PROVIDE THE FULL RECIPE, DO NOT STOP HALFWAY THROUGH.)

    YOUR RECIPE MUST END WITH HOW YOU PUT THE FOOD ON THE PLATE. DO NOT STOP BEFORE THAT.
    DO NOT MIX sweet and savoury or make "weird" food combinations (like chicken and meringues)
    DO NOT MENTION THE TIME IT TAKES TO COOK THE FOOD IN THE RECIPE. I WILL DO THAT FOR YOU.
    """,
    input_variables=["ingredients", "recipeNames",
                     "dontwant", "language", "max_time", "calories", "cuisine"]
)

meal_chain = LLMChain(llm=llm, prompt=recipe_prompt_template,
                      verbose=True, output_key="recipe")

recipeList = {}
recipeNames = []
st.title("Make a recipe!")
user_prompt = st.text_input(
    "Enter ingredients separated by commas or press 'Surprise me!'")

a1, a2 = st.columns(2)
b1, b2, b3 = a1.columns(3)
s1, s2 = a1.columns(2)
b1.text("")
b2.text("")
generate_button = b1.button(
    "Generate", type="primary", use_container_width=True)
surprise_button = b2.button("Surprise me!", use_container_width=True)
a2.header("Options")

c1, c2 = a2.columns(2)
d1, d2 = st.columns(2)

mealcount = a2.slider(
    "How many recipes do you want?",
    1, 10, 3)

dontwant = a2.text_input(
    "Anything you don't want in the recipe? (separate by commas)", max_chars=150)
preferred_language_options = ["English",
                              "Punjabi", "Spanish", "French", "German"]

cuisine_options = ["Anything", "Indian", "Italian", "Chinese", "Japanese",
                   "Mexican", "American", "British", "French", "German", "Spanish"]
cuisine = a2.selectbox(
    "Select Cuisine", cuisine_options, index=0)
a2.caption("More coming soon")

max_time = a2.slider(
    'The meal should take less then this amount of minutes to make', 15, 120, 25, 5)

calories = a2.slider(
    'The meal should aim to have between this many calories', 300, 1500, (500, 1000), 10)

preferred_language = a2.selectbox(
    "What language should the recipe be in?", preferred_language_options)

if generate_button:
    if user_prompt:
        make_meals(mealcount, user_prompt, dontwant,
                   preferred_language, recipeNames, recipeList, meal_chain, max_time, calories, cuisine)
    else:
        st.warning("Please enter ingredients or press 'Surprise me!'")

if surprise_button:
    make_meals(1, user_prompt, "", "English",
               recipeNames, recipeList, meal_chain, max_time, calories, "Any that you want.")
    # st.stop()
