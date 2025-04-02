
import streamlit as st
from PIL import Image
import os

st.set_page_config(layout="wide")
st.title("♠️ Ultimate Texas Hold'em")

def display_cards(card_names, label):
    st.markdown(f"**{label}:**")
    cols = st.columns(len(card_names))
    for col, card in zip(cols, card_names):
        image_path = os.path.join("cards", card)
        if os.path.exists(image_path):
            col.image(image_path, width=100)
        else:
            col.write(f"Missing image: {card}")

# Example hand rendering
player_cards = ["ace_of_spades.png", "king_of_hearts.png"]
community_cards = ["10_of_hearts.png", "jack_of_hearts.png", "queen_of_hearts.png", "2_of_clubs.png", "7_of_spades.png"]

display_cards(player_cards, "Your Hole Cards")
display_cards(community_cards, "Community Cards")
