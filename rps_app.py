# rps_app.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime
import io

st.set_page_config(
    page_title="Rock · Paper · Scissors 🎮",
    page_icon="✊✋✌️",
    layout="centered",
    initial_sidebar_state="expanded"
)

### ---------- helpers ----------
CHOICES = ["Rock", "Paper", "Scissors"]
EMOJI = {"Rock": "✊", "Paper": "✋", "Scissors": "✌️"}

def decide_winner(user, comp):
    if user == comp:
        return "Tie"
    wins = {
        ("Rock", "Scissors"),
        ("Paper", "Rock"),
        ("Scissors", "Paper")
    }
    return "User" if (user, comp) in wins else "Computer"

def ensure_session():
    if "user_score" not in st.session_state:
        st.session_state.user_score = 0
    if "comp_score" not in st.session_state:
        st.session_state.comp_score = 0
    if "rounds" not in st.session_state:
        st.session_state.rounds = 0
    if "history" not in st.session_state:
        # list of dicts: round, time, user, comp, result
        st.session_state.history = []

def add_round(user_choice, comp_choice, winner):
    st.session_state.rounds += 1
    if winner == "User":
        st.session_state.user_score += 1
    elif winner == "Computer":
        st.session_state.comp_score += 1
    st.session_state.history.append({
        "Round": st.session_state.rounds,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": f"{user_choice} {EMOJI[user_choice]}",
        "Computer": f"{comp_choice} {EMOJI[comp_choice]}",
        "Result": winner
    })

def reset_game():
    st.session_state.user_score = 0
    st.session_state.comp_score = 0
    st.session_state.rounds = 0
    st.session_state.history = []

def history_df():
    if st.session_state.history:
        return pd.DataFrame(st.session_state.history)
    return pd.DataFrame(columns=["Round","Time","User","Computer","Result"])

def csv_bytes_from_df(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

### ---------- UI ----------
ensure_session()

st.markdown(
    """
    <div style="background:linear-gradient(90deg,#6EE7B7,#3B82F6);
                padding:18px;border-radius:12px;color:#032B44;">
      <h1 style="margin:0;padding:0;">Rock · Paper · Scissors</h1>
      <div style="font-size:14px;opacity:0.95;">User vs Computer — keep score, track history, download results</div>
    </div>
    """, unsafe_allow_html=True
)

st.write("")  # spacing

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Make your move")
    # Big buttons for choices
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"Rock {EMOJI['Rock']}", key="b_rock"):
            user_choice = "Rock"
            comp_choice = random.choice(CHOICES)
            winner = decide_winner(user_choice, comp_choice)
            add_round(user_choice, comp_choice, winner)
            st.session_state.last_action = (user_choice, comp_choice, winner)
    with c2:
        if st.button(f"Paper {EMOJI['Paper']}", key="b_paper"):
            user_choice = "Paper"
            comp_choice = random.choice(CHOICES)
            winner = decide_winner(user_choice, comp_choice)
            add_round(user_choice, comp_choice, winner)
            st.session_state.last_action = (user_choice, comp_choice, winner)
    with c3:
        if st.button(f"Scissors {EMOJI['Scissors']}", key="b_scissors"):
            user_choice = "Scissors"
            comp_choice = random.choice(CHOICES)
            winner = decide_winner(user_choice, comp_choice)
            add_round(user_choice, comp_choice, winner)
            st.session_state.last_action = (user_choice, comp_choice, winner)

    st.write("")
    if "last_action" in st.session_state:
        u, c, w = st.session_state.last_action
        if w == "Tie":
            st.info(f"Round {st.session_state.rounds}: It's a tie — {EMOJI[u]} vs {EMOJI[c]}")
        elif w == "User":
            st.success(f"Round {st.session_state.rounds}: You win! {EMOJI[u]} beats {EMOJI[c]}")
        else:
            st.error(f"Round {st.session_state.rounds}: Computer wins — {EMOJI[c]} beats {EMOJI[u]}")

with col2:
    st.subheader("Scoreboard")
    st.markdown("##")
    # visually appealing metrics
    score_col1, score_col2, score_col3 = st.columns([1,1,1])
    score_col1.metric(label="Your Score", value=st.session_state.user_score, delta=f"+{st.session_state.user_score}" if st.session_state.user_score>0 else "0")
    score_col2.metric(label="Computer Score", value=st.session_state.comp_score, delta=f"+{st.session_state.comp_score}" if st.session_state.comp_score>0 else "0")
    score_col3.metric(label="Rounds Played", value=st.session_state.rounds)

    st.write("")
    # Progress bar toward "best of" style (optional)
    target = st.sidebar.selectbox("Game type", ["Unlimited", "Best of 3", "Best of 5", "Best of 7"], index=0)
    if target != "Unlimited":
        best_n = int(target.split()[-1])
        needed = (best_n // 2) + 1
        prog = 0
        if (st.session_state.user_score + st.session_state.comp_score) > 0:
            prog = (st.session_state.user_score / max(1, st.session_state.user_score + st.session_state.comp_score))
        st.progress(prog)
        if st.session_state.user_score >= needed:
            st.balloons()
            st.success(f"You've won the {target}!")
        elif st.session_state.comp_score >= needed:
            st.warning(f"Computer has won the {target}.")

st.write("---")

# History & download
st.subheader("Round History")
df_hist = history_df()
if df_hist.empty:
    st.info("No rounds yet — pick Rock, Paper, or Scissors to start playing!")
else:
    # color-coding results inline using dataframe style for display
    def color_result(val):
        if val == "User":
            return "color: green; font-weight:600"
        elif val == "Computer":
            return "color: red; font-weight:600"
        else:
            return "color: gray; font-weight:600"

    st.dataframe(df_hist.style.applymap(lambda v: "font-weight:600" if isinstance(v, str) else "", subset=["User","Computer"])
                         .applymap(lambda v: color_result(v) if v in ["User","Computer","Tie"] else "", subset=["Result"]),
                 use_container_width=True)

    # Download CSV
    csv_bytes = csv_bytes_from_df(df_hist)
    st.download_button(
        label="Download history as CSV",
        data=csv_bytes,
        file_name=f"rps_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

st.write("---")

# Controls
controls_left, controls_right = st.columns([1,1])
with controls_left:
    if st.button("Reset game", key="reset"):
        reset_game()
        st.success("Game reset — scores and history cleared.")

with controls_right:
    st.write(" ")
    st.write(" ")
    st.caption("Tip: use keyboard and click the big buttons to play fast!")

# Footer stats
st.markdown(
    """
    <div style="margin-top:8px;padding:12px;border-radius:10px;background:#f8fafc;">
      <small style="color:#475569;">This small app keeps state across interactions during the session. Close the browser tab or press Reset to clear scores.</small>
    </div>
    """, unsafe_allow_html=True
)
