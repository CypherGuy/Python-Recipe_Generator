import streamlit as st
import os
import mysql.connector
from dotenv import load_dotenv
from streamlit_extras.switch_page_button import switch_page
import time


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

# Create a page for the user to sign up.


def signup():
    st.title("Sign Up")
    st.caption("Create your account.")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        mycursor.execute(
            "INSERT INTO logins (username, password) VALUES (%s, %s)", (new_username, new_password))
        mydb.commit()
        st.success("Account created successfully! Redirecting to login..")
        time.sleep(1)
        switch_page("login")

    if st.button("Already have an account? Login"):
        switch_page("login")


signup()
