
import streamlit as st
import random
from collections import Counter

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_values = {r: i for i, r in enumerate(ranks, 2)}
reverse_suit_map = {'Hearts': 'h', 'Diamonds': 'd', 'Clubs': 'c', 'Spades': 's'}

blind_payouts = {
    "Royal Flush": 500,
    "Straight Flush": 50,
    "Four of a Kind": 10,
    "Full House": 3,
    "Flush": 1.5,
    "Straight": 1,
    "Less": 0  # PUSH
}

trips_payouts = {
    "Royal Flush": 50,
    "Straight Flush": 40,
    "Four of a Kind": 30,
    "Full House": 8,
    "Flush": 6,
    "Straight": 5,
    "Three of a Kind": 3
}

def create_deck():
    return [(r, s) for s in suits for r in ranks]

def str_to_code(card):
    r, s = card
    return r + reverse_suit_map[s]

def display_cards(cards, label="", size=90):
    if label:
        st.markdown(f"**{label}**")
    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        img = f"cards/{str_to_code(card)}.png"
        cols[i].image(img, width=size)

def evaluate_hand(cards):
    values = sorted([rank_values[r] for r, _ in cards], reverse=True)
    suits_in_hand = [s for _, s in cards]
    value_counts = Counter([r for r, _ in cards])
    is_flush = len(set(suits_in_hand)) == 1
    is_straight = all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))

    if is_flush and is_straight:
        if values[0] == 14:
            return "Royal Flush"
        return "Straight Flush"
    if 4 in value_counts.values():
        return "Four of a Kind"
    if sorted(value_counts.values()) == [2, 3]:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if 3 in value_counts.values():
        return "Three of a Kind"
    if list(value_counts.values()).count(2) == 2:
        return "Two Pair"
    if 2 in value_counts.values():
        return "One Pair"
    return "High Card"

def payout_blind(hand_type):
    if hand_type in blind_payouts:
        return blind_payouts[hand_type]
    return 0

def payout_trips(hand_type):
    return trips_payouts.get(hand_type, 0)

st.set_page_config(page_title="Ultimate Texas Hold'em", layout="wide")
st.title("♠️ Ultimate Texas Hold'em")

if "chips" not in st.session_state:
    st.session_state.chips = 1000
    st.session_state.game_started = False
    st.session_state.play_made = False

st.markdown(f"### 💰 Chips: ${st.session_state.chips}")

if not st.session_state.game_started:
    ante = st.number_input("Ante Bet", 10, 100, 25, step=5)
    trips = st.number_input("Trips Bet (optional)", 0, 100, 0, step=5)
    if st.button("🃏 Deal Cards"):
        deck = create_deck()
        random.shuffle(deck)
        st.session_state.ante = ante
        st.session_state.blind = ante
        st.session_state.trips = trips
        st.session_state.play_bet = 0
        st.session_state.player_hand = [deck.pop(), deck.pop()]
        st.session_state.dealer_hand = [deck.pop(), deck.pop()]
        st.session_state.community_cards = [deck.pop() for _ in range(5)]
        st.session_state.deck = deck
        st.session_state.game_started = True
        st.session_state.play_made = False

if st.session_state.game_started:
    display_cards(st.session_state.player_hand, label="Your Hand")
    display_cards(["back", "back"], label="Dealer Hand", size=90)

    if not st.session_state.play_made:
        st.write("### Choose Your Action")
        if st.button("Raise 4x"):
            st.session_state.play_bet = 4 * st.session_state.ante
            st.session_state.play_made = True
        elif st.button("Raise 2x"):
            st.session_state.play_bet = 2 * st.session_state.ante
            st.session_state.play_made = True
        elif st.button("Raise 1x"):
            st.session_state.play_bet = st.session_state.ante
            st.session_state.play_made = True
        elif st.button("Check"):
            st.session_state.play_bet = 0
            st.session_state.play_made = True

    if st.session_state.play_made:
        display_cards(st.session_state.community_cards, label="Community Cards")
        display_cards(st.session_state.dealer_hand, label="Dealer Hand")

        full_player = st.session_state.player_hand + st.session_state.community_cards
        full_dealer = st.session_state.dealer_hand + st.session_state.community_cards

        player_best = evaluate_hand(full_player)
        dealer_best = evaluate_hand(full_dealer)

        st.markdown(f"**Your Best Hand**: {player_best}")
        st.markdown(f"**Dealer Best Hand**: {dealer_best}")

        # Compare results
        player_score = ranks.index(player_best) if player_best in ranks else 0
        dealer_score = ranks.index(dealer_best) if dealer_best in ranks else 0

        win = player_score > dealer_score
        push = player_score == dealer_score
        lose = player_score < dealer_score

        if win:
            st.success("🏆 You Win!")
            st.session_state.chips += st.session_state.ante + st.session_state.play_bet
        elif push:
            st.info("🤝 It's a Push!")
        else:
            st.error("❌ You Lose")
            st.session_state.chips -= st.session_state.ante + st.session_state.play_bet

        # Apply trips
        if st.session_state.trips > 0:
            trips_payout = payout_trips(player_best)
            if trips_payout > 0:
                reward = trips_payout * st.session_state.trips
                st.success(f"💰 Trips Bonus! You win {trips_payout}x = ${reward}")
                st.session_state.chips += reward
            else:
                st.info("No Trips Bonus")

        st.session_state.game_started = False
