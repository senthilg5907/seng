import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Smart Tic-Tac-Toe ❌⭕",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state variables
if 'board' not in st.session_state:
    st.session_state.board = [None] * 9
if 'current_player' not in st.session_state:
    st.session_state.current_player = '❌'  # X goes first
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = None
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Play vs Computer"
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'score' not in st.session_state:
    st.session_state.score = {'❌': 0, '⭕': 0, 'Draws': 0}

def check_winner(board):
    """Check if there's a winner and return the winner and winning line"""
    # Winning combinations
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], line
    return None, None

def is_board_full(board):
    """Check if the board is full"""
    return all(cell is not None for cell in board)

def computer_move():
    """Make a random move for the computer"""
    empty_cells = [i for i, cell in enumerate(st.session_state.board) if cell is None]
    if empty_cells and not st.session_state.winner:
        time.sleep(0.5)  # Add a small delay for better UX
        return random.choice(empty_cells)
    return None

def reset_game():
    """Reset the game state"""
    st.session_state.board = [None] * 9
    st.session_state.current_player = '❌'
    st.session_state.winner = None
    st.session_state.winning_line = None
    st.session_state.game_over = False

def reset_score():
    """Reset the score"""
    st.session_state.score = {'❌': 0, '⭕': 0, 'Draws': 0}

# Custom CSS for modern 3D design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 20px;
        border-radius: 20px;
    }
    .title {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }
    .status {
        text-align: center;
        font-size: 1.8rem;
        margin: 1.5rem 0;
        padding: 1.2rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
    }
    .score-board {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .score-item {
        text-align: center;
        color: white;
        font-weight: 600;
    }
    .score-value {
        font-size: 1.5rem;
        font-weight: 800;
    }
    .reset-btn {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        border-radius: 12px;
        padding: 0.8rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        margin: 5px;
    }
    .reset-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .mode-selector {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .game-board {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.8rem;
        border-radius: 22px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        perspective: 1000px;
    }
    .cell {
        height: 90px;
        width: 90px;
        border-radius: 12px;
        font-size: 42px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 6px;
        transition: all 0.3s ease;
        transform-style: preserve-3d;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border: none;
        cursor: pointer;
    }
    .cell-x {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        box-shadow: 0 6px 12px rgba(255,75,75,0.4), 
                    inset 0 -4px 8px rgba(160,0,0,0.5),
                    inset 0 4px 8px rgba(255,150,150,0.5);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        transform: translateZ(10px) rotateX(5deg);
    }
    .cell-o {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        box-shadow: 0 6px 12px rgba(78,205,196,0.4),
                    inset 0 -4px 8px rgba(0,100,90,0.5),
                    inset 0 4px 8px rgba(150,255,240,0.5);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        transform: translateZ(10px) rotateX(5deg);
    }
    .cell-empty {
        background: rgba(255, 255, 255, 0.08);
        color: rgba(255,255,255,0.7);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2),
                    inset 0 -4px 8px rgba(0,0,0,0.1),
                    inset 0 4px 8px rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.1);
        transform: translateZ(5px);
    }
    .cell-empty:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateZ(15px) scale(1.05) rotateX(5deg);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3),
                    inset 0 -4px 8px rgba(0,0,0,0.1),
                    inset 0 4px 8px rgba(255,255,255,0.1);
    }
    .cell-winning {
        background: linear-gradient(135deg, #f9d423, #ff4e50);
        color: white;
        box-shadow: 0 8px 16px rgba(249,212,35,0.5),
                    inset 0 -4px 8px rgba(180,100,0,0.5),
                    inset 0 4px 8px rgba(255,230,150,0.5);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: pulse 1.5s infinite, glow 2s infinite;
        transform: translateZ(20px) scale(1.1) rotateX(5deg);
    }
    @keyframes pulse {
        0% { transform: translateZ(20px) scale(1.1) rotateX(5deg); }
        50% { transform: translateZ(25px) scale(1.15) rotateX(5deg); }
        100% { transform: translateZ(20px) scale(1.1) rotateX(5deg); }
    }
    @keyframes glow {
        0% { box-shadow: 0 8px 16px rgba(249,212,35,0.5), 
                        inset 0 -4px 8px rgba(180,100,0,0.5),
                        inset 0 4px 8px rgba(255,230,150,0.5); }
        50% { box-shadow: 0 12px 24px rgba(249,212,35,0.7), 
                        inset 0 -4px 8px rgba(180,100,0,0.5),
                        inset 0 4px 8px rgba(255,230,150,0.5); }
        100% { box-shadow: 0 8px 16px rgba(249,212,35,0.5), 
                        inset 0 -4px 8px rgba(180,100,0,0.5),
                        inset 0 4px 8px rgba(255,230,150,0.5); }
    }
    .instructions {
        background: rgba(255, 255, 255, 0.08);
        padding: 1.2rem;
        border-radius: 18px;
        margin-top: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 15px;
    }
    .stRadio > div [role="radiogroup"] {
        flex-direction: row;
        gap: 15px;
    }
    .stRadio label {
        color: white;
        background: rgba(255,255,255,0.1);
        padding: 8px 16px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    .stRadio label:hover {
        background: rgba(255,255,255,0.2);
    }
    .stRadio input:checked + label {
        background: rgba(255,255,255,0.3);
        font-weight: bold;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# UI Components
st.markdown('<h1 class="title">Smart Tic-Tac-Toe ❌⭕</h1>', unsafe_allow_html=True)

# Score board
st.markdown('<div class="score-board">', unsafe_allow_html=True)
st.markdown(f'<div class="score-item">❌<br><span class="score-value">{st.session_state.score["❌"]}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="score-item">Draws<br><span class="score-value">{st.session_state.score["Draws"]}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="score-item">⭕<br><span class="score-value">{st.session_state.score["⭕"]}</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Game mode selection
with st.container():
    st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
    st.markdown("### Select Game Mode:")
    mode = st.radio("", 
                    ["Two Players", "Play vs Computer"], 
                    index=1 if st.session_state.game_mode == "Play vs Computer" else 0,
                    horizontal=True,
                    label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if mode != st.session_state.game_mode:
        st.session_state.game_mode = mode
        reset_game()

# Display current player or winner
with st.container():
    if st.session_state.winner:
        if st.session_state.winner == "Draw":
            st.markdown('<div class="status">It\'s a Draw! 🤝</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status">Player {st.session_state.winner} Wins! 🎉</div>', unsafe_allow_html=True)
    elif not st.session_state.game_over:
        st.markdown(f'<div class="status">Current Player: {st.session_state.current_player}</div>', unsafe_allow_html=True)

# Create the game board
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    
    # Create 3x3 grid
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            with cols[col]:
                # Determine cell style based on state
                cell_class = "cell-empty"
                if st.session_state.board[idx] == '❌':
                    cell_class = "cell-x"
                elif st.session_state.board[idx] == '⭕':
                    cell_class = "cell-o"
                
                # Add winning class if part of winning line
                if st.session_state.winning_line and idx in st.session_state.winning_line:
                    cell_class = "cell-winning"
                
                # Display the cell content
                cell_content = st.session_state.board[idx] or " "
                
                # Create a button for each cell
                disabled = st.session_state.board[idx] is not None or st.session_state.winner or (st.session_state.game_mode == "Play vs Computer" and st.session_state.current_player == '⭕')
                
                if st.button(cell_content, 
                             key=f"btn_{idx}", 
                             use_container_width=True,
                             disabled=disabled):
                    # Handle player move
                    if st.session_state.board[idx] is None and not st.session_state.winner:
                        st.session_state.board[idx] = st.session_state.current_player
                        
                        # Check for winner or draw
                        st.session_state.winner, st.session_state.winning_line = check_winner(st.session_state.board)
                        if st.session_state.winner:
                            st.session_state.game_over = True
                            if st.session_state.winner != "Draw":
                                st.session_state.score[st.session_state.winner] += 1
                            else:
                                st.session_state.score["Draws"] += 1
                        elif is_board_full(st.session_state.board):
                            st.session_state.winner = "Draw"
                            st.session_state.game_over = True
                            st.session_state.score["Draws"] += 1
                        else:
                            # Switch player
                            st.session_state.current_player = '⭕' if st.session_state.current_player == '❌' else '❌'
                            
                            # Computer's turn if in vs computer mode
                            if st.session_state.game_mode == "Play vs Computer" and st.session_state.current_player == '⭕' and not st.session_state.winner:
                                move = computer_move()
                                if move is not None:
                                    st.session_state.board[move] = '⭕'
                                    st.session_state.winner, st.session_state.winning_line = check_winner(st.session_state.board)
                                    if st.session_state.winner:
                                        st.session_state.game_over = True
                                        if st.session_state.winner != "Draw":
                                            st.session_state.score[st.session_state.winner] += 1
                                        else:
                                            st.session_state.score["Draws"] += 1
                                    elif is_board_full(st.session_state.board):
                                        st.session_state.winner = "Draw"
                                        st.session_state.game_over = True
                                        st.session_state.score["Draws"] += 1
                                    else:
                                        st.session_state.current_player = '❌'
                        
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 New Game", use_container_width=True, type="primary"):
        reset_game()
        st.rerun()
with col2:
    if st.button("📊 Reset Score", use_container_width=True):
        reset_score()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Play", expanded=False):
    st.markdown("""
    **Tic-Tac-Toe Rules:**
    - The game is played on a 3x3 grid
    - Player ❌ goes first
    - Players take turns placing their marks in empty squares
    - The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
    - If all 9 squares are full and no player has 3 in a row, the game ends in a draw
    
    **Tips:**
    - Try to create opportunities where you have two ways to win
    - Block your opponent when they have two in a row
    - The center square is the most valuable position
    """)
    
# Add some fun emojis
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: white;'>🎮 ❌ ⭕ 🎯 🏆</div>", unsafe_allow_html=True)