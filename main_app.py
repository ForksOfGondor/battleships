import streamlit as st
import numpy as np
import random

GRID_SIZE = 5
NUM_SHIPS = 3

def create_board():
    return np.full((GRID_SIZE, GRID_SIZE), "~")  # "~" represents water

# Place ships randomly
def place_ships(board):
    ships = set()
    while len(ships) < NUM_SHIPS:
        ship = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        ships.add(ship)
    return ships

# Check if a guess is adjacent to a ship
def is_hurt(guess, ships):
    row, col = guess
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr == 0 and dc == 0):
                continue
            if (row + dr, col + dc) in ships:
                return True
    return False

# Initialize session state
if "player_board" not in st.session_state:
    st.session_state.player_board = create_board()
    st.session_state.computer_board = create_board()
    st.session_state.computer_ships = place_ships(st.session_state.computer_board)
    st.session_state.player_ships = place_ships(st.session_state.player_board)
    st.session_state.computer_guesses = set()
    st.session_state.player_guesses = set()
    st.session_state.game_over = False
    st.session_state.message = ""

def computer_turn():
    while True:
        guess = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if guess not in st.session_state.computer_guesses:
            st.session_state.computer_guesses.add(guess)
            if guess in st.session_state.player_ships:
                st.session_state.player_board[guess] = "💥"
                st.session_state.player_ships.remove(guess)
            elif is_hurt(guess, st.session_state.player_ships):
                st.session_state.player_board[guess] = "⚠️"  # Hurt indicator
            else:
                st.session_state.player_board[guess] = "❌"
            break

# Display the game boards
def display_board(board, hide_ships=False):
    display = np.copy(board)
    if hide_ships:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in st.session_state.computer_ships and display[r][c] == "~":
                    display[r][c] = "~"  # Hide ships
    return display

st.title("🚢 Battleship: Player vs. Computer")

if st.session_state.game_over:
    st.write(st.session_state.message)
    if st.button("Play Again"):
        st.session_state.clear()
        st.rerun()
else:
    st.subheader("Your Board")
    st.table(display_board(st.session_state.player_board))
    
    st.subheader("Computer's Board")
    st.table(display_board(st.session_state.computer_board, hide_ships=True))
    
    row = st.number_input("Enter row (0-4):", min_value=0, max_value=4, step=1)
    col = st.number_input("Enter column (0-4):", min_value=0, max_value=4, step=1)
    
    if st.button("Fire!"):
        guess = (row, col)
        if guess in st.session_state.player_guesses:
            st.warning("You've already fired at this location!")
        else:
            st.session_state.player_guesses.add(guess)
            if guess in st.session_state.computer_ships:
                st.session_state.computer_board[guess] = "💥"
                st.session_state.computer_ships.remove(guess)
                st.success("Hit!")
            elif is_hurt(guess, st.session_state.computer_ships):
                st.session_state.computer_board[guess] = "⚠️"  # Hurt indicator
                st.info("Hurt! A ship is nearby.")
            else:
                st.session_state.computer_board[guess] = "❌"
                st.info("Miss!")
            
            # Check for win condition
            if not st.session_state.computer_ships:
                st.session_state.game_over = True
                st.session_state.message = "🎉 You Win! All enemy ships are destroyed!"
            else:
                computer_turn()
                if not st.session_state.player_ships:
                    st.session_state.game_over = True
                    st.session_state.message = "💥 Game Over! The computer sank all your ships!"


# Refresh button
if st.button("Refresh Game Board"):
    st.rerun()
# done
