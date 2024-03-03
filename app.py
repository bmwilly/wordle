import streamlit as st
import pandas as pd
import numpy as np

from wordle import play


st.title("Wordle")

# Add a text
st.write("Welcome to my app!")

play()
