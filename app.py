
import streamlit as st
import os

st.set_page_config(page_title="Ultimate Texas Hold'em", layout="wide")
st.title("♠️ Ultimate Texas Hold'em")

# Example: Displaying a few cards
card_dir = "images"
example_cards = ["ace_of_spades.png", "10_of_hearts.png", "jack_of_hearts.png"]

st.subheader("Your Hole Cards:")
cols = st.columns(len(example_cards))
for i, card in enumerate(example_cards[:2]):
    cols[i].image(os.path.join(card_dir, card), width=100)

st.subheader("Community Cards:")
cols = st.columns(len(example_cards))
for i, card in enumerate(example_cards):
    cols[i].image(os.path.join(card_dir, card), width=100)
