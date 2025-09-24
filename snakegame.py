import streamlit as st
import random
import time

# -----------------------------
# Config
# -----------------------------
GRID_SIZE = 20
SPEED = 0.15  # snake speed

# -----------------------------
# Initialize session state
# -----------------------------
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.run = False
    st.session_state.auto_play = False  # NEW: Auto mode toggle

# -----------------------------
# Helper Functions
# -----------------------------
def new_food():
    """Generate new food not colliding with snake."""
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in st.session_state.snake:
            return pos

def move_snake():
    """Move snake one step forward."""
    head = st.session_state.snake[0]
    x, y = head

    if st.session_state.direction == "UP":
        new_head = (x - 1, y)
    elif st.session_state.direction == "DOWN":
        new_head = (x + 1, y)
    elif st.session_state.direction == "LEFT":
        new_head = (x, y - 1)
    else:  # RIGHT
        new_head = (x, y + 1)

    # Check collisions
    if (
        new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    # Add new head
    st.session_state.snake.insert(0, new_head)

    # Check food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = new_food()
    else:
        st.session_state.snake.pop()

def reset_game():
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = new_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.run = True

def draw_board():
    """Draw the board with emojis."""
    board = [["⬛" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # food
    fx, fy = st.session_state.food
    board[fx][fy] = "🍎"

    # snake
    for i, (x, y) in enumerate(st.session_state.snake):
        board[x][y] = "🟩" if i > 0 else "🟥"

    return "<br>".join("".join(row) for row in board)

def auto_play_move():
    """Simple greedy AI: move snake towards food."""
    head = st.session_state.snake[0]
    fx, fy = st.session_state.food
    hx, hy = head

    if abs(fx - hx) > abs(fy - hy):  # Prioritize vertical/horizontal closeness
        if fx < hx and st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"
        elif fx > hx and st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"
    else:
        if fy < hy and st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"
        elif fy > hy and st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"

# -----------------------------
# UI Layout
# -----------------------------
st.title("🐍 Snake Game in Streamlit (Enhanced with Auto Play)")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.metric("Score", st.session_state.score)
with col3:
    if st.button("🔄 Restart"):
        reset_game()

# 🎮 Auto Play toggle
st.session_state.auto_play = st.checkbox("🤖 Auto Play", value=st.session_state.auto_play)

# 🎮 Colorful control pad
st.markdown("""
<style>
button[kind="secondary"] {
    width: 90px !important;
    height: 50px !important;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c2:
    if st.button("⬆️ Up", key="up"):
        if st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⬅️ Left", key="left"):
        if st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"
with c3:
    if st.button("➡️ Right", key="right"):
        if st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"
c1, c2, c3 = st.columns(3)
with c2:
    if st.button("⬇️ Down", key="down"):
        if st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"

# Game board placeholder
board_placeholder = st.empty()

# -----------------------------
# Game Loop
# -----------------------------
if st.session_state.run and not st.session_state.game_over:
    while st.session_state.run and not st.session_state.game_over:
        if st.session_state.auto_play:
            auto_play_move()
        move_snake()
        board_html = draw_board()
        board_placeholder.markdown(board_html, unsafe_allow_html=True)
        time.sleep(SPEED)
        st.rerun()

# -----------------------------
# Game Over Screen
# -----------------------------
if st.session_state.game_over:
    st.error(f"💀 Game Over! Final Score: {st.session_state.score}")
    if st.button("Play Again"):
        reset_game()
        st.rerun()

