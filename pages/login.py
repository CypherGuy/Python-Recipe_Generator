import streamlit as st
import os
import mysql.connector
from dotenv import load_dotenv
from streamlit_extras.switch_page_button import switch_page

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

# Create a page for the user to login. Use MySQL to verify the user's credentials.


def login():
    st.title("Login")
    st.caption("Enter your credentials to login.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    mycursor.execute(
        "SELECT * FROM logins WHERE username = %s AND password = %s", (username, password))

    correctCredentials = mycursor.fetchall()

    if st.button("Login"):
        if correctCredentials.__len__() > 0:
            st.success(f"Logged in as {username}!")
        else:
            st.error("Invalid credentials. Please try again.")

    if st.button("Don't have an account? Sign Up"):
        switch_page("signup")


login()
