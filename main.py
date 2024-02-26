import streamlit as st

st.set_page_config(page_title="Recipe Generator",
                   layout="wide", initial_sidebar_state="collapsed")

st.title("Recipe Generator")
st.text("Welcome to our innovative recipe finder tool, where culinary exploration meets convenience!")

st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

c1, c2 = st.columns(2)
c1.header("The UI")

c1.text("""All you need to do is enter the ingredients you have 
and we'll do the rest! Our simple and intuitive UI 
makes it easy to get started.
        
You can also choose to be surprised by our AI, who 
will generate a random recipe for you!""")

if c1.button("Make a recipe!"):
    st.switch_page("pages/recipe.py")

c2.image("https://i.imgur.com/UQkPzDi.png")
c2.image("https://i.imgur.com/Sr4NBL7.png")

st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

c1, c2 = st.columns(2)
c2.header("Community recipes")
c2.text("""Here you can view the community's most recent recipes!""")

if c2.button("View recent recipes"):
    st.switch_page("pages/view recents.py")

c1.image("https://i.imgur.com/uFGuVcE.png")
