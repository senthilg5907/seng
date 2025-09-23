import streamlit as st
import time
import datetime

# Page configuration
st.set_page_config(
    page_title="Enhanced Stopwatch",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E86C1;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .timer-display {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        margin: 2rem 0;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .running {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .stopped {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .reset {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .stButton > button {
        height: 4rem;
        width: 10rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .start-btn {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
    }
    
    .stop-btn {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .reset-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .lap-time {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .status-indicator {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .status-running {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
    }
    
    .status-stopped {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .status-ready {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'lap_times' not in st.session_state:
    st.session_state.lap_times = []

def format_time(seconds):
    """Format seconds into MM:SS.ms format"""
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:06.3f}"

def get_current_time():
    """Calculate current elapsed time"""
    if st.session_state.is_running and st.session_state.start_time:
        return st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed_time

# Main title
st.markdown('<h1 class="main-title">⏱️ Enhanced Stopwatch ⏱️</h1>', unsafe_allow_html=True)

# Get current time for display
current_time = get_current_time()

# Timer display with dynamic styling
if st.session_state.is_running:
    timer_class = "timer-display running"
    status_text = "🟢 RUNNING"
    status_class = "status-indicator status-running"
elif current_time > 0:
    timer_class = "timer-display stopped"
    status_text = "🔴 STOPPED"
    status_class = "status-indicator status-stopped"
else:
    timer_class = "timer-display reset"
    status_text = "⚪ READY"
    status_class = "status-indicator status-ready"

# Status indicator
st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)

# Timer display
st.markdown(f'<div class="{timer_class}">{format_time(current_time)}</div>', unsafe_allow_html=True)

# Button controls
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("🚀 START", key="start", help="Start the stopwatch"):
        if not st.session_state.is_running:
            st.session_state.start_time = time.time()
            st.session_state.is_running = True
            st.rerun()

with col2:
    if st.button("⏸️ STOP", key="stop", help="Stop the stopwatch"):
        if st.session_state.is_running:
            st.session_state.elapsed_time = get_current_time()
            st.session_state.is_running = False
            st.session_state.start_time = None
            st.rerun()

with col3:
    if st.button("🔄 RESET", key="reset", help="Reset the stopwatch to zero"):
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0.0
        st.session_state.is_running = False
        st.session_state.lap_times = []
        st.rerun()

with col4:
    if st.button("📍 LAP", key="lap", help="Record a lap time"):
        if st.session_state.is_running or current_time > 0:
            lap_time = get_current_time()
            st.session_state.lap_times.append(lap_time)
            st.rerun()

# Statistics section
if current_time > 0 or st.session_state.lap_times:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Statistics")
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("⏰ Current Time", format_time(current_time))
        if st.session_state.lap_times:
            st.metric("🏁 Total Laps", len(st.session_state.lap_times))
    
    with col_stats2:
        if st.session_state.lap_times:
            avg_lap = sum(st.session_state.lap_times) / len(st.session_state.lap_times)
            st.metric("📈 Average Lap", format_time(avg_lap))
            st.metric("🏆 Best Lap", format_time(min(st.session_state.lap_times)))
    
    st.markdown('</div>', unsafe_allow_html=True)

# Lap times section
if st.session_state.lap_times:
    st.markdown("### 🏃‍♂️ Lap Times")
    for i, lap_time in enumerate(reversed(st.session_state.lap_times), 1):
        lap_number = len(st.session_state.lap_times) - i + 1
        st.markdown(f'<div class="lap-time">Lap {lap_number}: {format_time(lap_time)}</div>', 
                   unsafe_allow_html=True)

# Auto-refresh when running
if st.session_state.is_running:
    time.sleep(0.1)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">'
    '💡 Tips: Use START to begin timing, STOP to pause, LAP to record splits, and RESET to clear all data'
    '</div>', 
    unsafe_allow_html=True
)