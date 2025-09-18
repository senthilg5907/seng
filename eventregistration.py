import streamlit as st
import pandas as pd
import csv
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Event Registration System",
    page_icon="🎉",
    layout="wide"
)

# Initialize session state
if 'registrations' not in st.session_state:
    st.session_state.registrations = []

if 'registration_count' not in st.session_state:
    st.session_state.registration_count = 0

# CSV file path
CSV_FILE = "event_registrations.csv"

# Function to load existing registrations from CSV
@st.cache_data
def load_registrations_from_csv():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict('records')
        except:
            return []
    return []

# Function to save registration to CSV
def save_to_csv(registration):
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'email', 'event_choice', 'registration_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(registration)

# Function to validate email
def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Load existing registrations on app start
if not st.session_state.registrations:
    st.session_state.registrations = load_registrations_from_csv()
    st.session_state.registration_count = len(st.session_state.registrations)

# Main title and header
st.title("🎉 Event Registration System")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Registration", "Admin Dashboard"])

if page == "Registration":
    # Registration Form Section
    st.header("📝 Register for an Event")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="Enter your email")
        
        with col2:
            event_choices = [
                "Tech Conference 2024",
                "Marketing Workshop",
                "Data Science Summit",
                "Startup Networking Event",
                "Digital Marketing Bootcamp",
                "AI/ML Conference",
                "Business Strategy Workshop"
            ]
            event_choice = st.selectbox("Select Event *", [""] + event_choices)
            st.write("")  # Spacing
            
        submitted = st.form_submit_button("🎯 Register Now", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if not name.strip():
                errors.append("Name is required")
            
            if not email.strip():
                errors.append("Email is required")
            elif not is_valid_email(email.strip()):
                errors.append("Please enter a valid email address")
            
            if not event_choice:
                errors.append("Please select an event")
            
            # Check for duplicate email
            existing_emails = [reg['email'].lower() for reg in st.session_state.registrations]
            if email.strip().lower() in existing_emails:
                errors.append("This email is already registered")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Create registration record
                registration = {
                    'name': name.strip(),
                    'email': email.strip().lower(),
                    'event_choice': event_choice,
                    'registration_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Add to session state
                st.session_state.registrations.append(registration)
                st.session_state.registration_count += 1
                
                # Save to CSV
                save_to_csv(registration)
                
                # Success message
                st.success(f"🎉 Registration successful! Welcome {name}!")
                st.balloons()
                
                # Clear form by rerunning
                st.rerun()
    
    # Live registration count
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Registrations", st.session_state.registration_count)
    
    with col2:
        if st.session_state.registrations:
            latest_event = st.session_state.registrations[-1]['event_choice']
            st.metric("Latest Event", latest_event[:20] + "..." if len(latest_event) > 20 else latest_event)
    
    with col3:
        if st.session_state.registrations:
            today_count = sum(1 for reg in st.session_state.registrations 
                            if reg['registration_time'].startswith(datetime.now().strftime("%Y-%m-%d")))
            st.metric("Today's Registrations", today_count)

elif page == "Admin Dashboard":
    # Admin Dashboard
    st.header("🔧 Admin Dashboard")
    
    if st.session_state.registration_count == 0:
        st.info("No registrations yet.")
    else:
        # Display registrations table
        st.subheader("📊 Registration Overview")
        
        df = pd.DataFrame(st.session_state.registrations)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Registrations", len(df))
        
        with col2:
            unique_events = df['event_choice'].nunique()
            st.metric("Unique Events", unique_events)
        
        with col3:
            today = datetime.now().strftime("%Y-%m-%d")
            today_registrations = sum(1 for reg in st.session_state.registrations 
                                    if reg['registration_time'].startswith(today))
            st.metric("Today's Count", today_registrations)
        
        with col4:
            unique_emails = df['email'].nunique()
            st.metric("Unique Participants", unique_emails)
        
        st.markdown("---")
        
        # Event-wise breakdown
        st.subheader("📈 Event-wise Registration Count")
        event_counts = df['event_choice'].value_counts()
        st.bar_chart(event_counts)
        
        # Recent registrations
        st.subheader("🕒 Recent Registrations")
        recent_df = df.tail(10).sort_values('registration_time', ascending=False)
        st.dataframe(recent_df, use_container_width=True)
        
        # Full data table with search
        st.subheader("🗂️ All Registrations")
        
        # Search functionality
        search_term = st.text_input("🔍 Search registrations", placeholder="Search by name, email, or event...")
        
        if search_term:
            mask = (df['name'].str.contains(search_term, case=False, na=False) |
                   df['email'].str.contains(search_term, case=False, na=False) |
                   df['event_choice'].str.contains(search_term, case=False, na=False))
            filtered_df = df[mask]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
        
        # CSV Export functionality
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download full CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📊 Download Full CSV",
                data=csv_data,
                file_name=f"event_registrations_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Download filtered CSV if search is active
            if search_term and 'filtered_df' in locals():
                filtered_csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📋 Download Filtered CSV",
                    data=filtered_csv,
                    file_name=f"filtered_registrations_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Use search above to enable filtered export")
        
        # Clear all data (with confirmation)
        st.markdown("---")
        st.subheader("⚠️ Danger Zone")
        
        if st.button("🗑️ Clear All Registrations", type="secondary"):
            st.warning("Are you sure? This action cannot be undone!")
            if st.button("✅ Yes, Clear All Data", type="primary"):
                st.session_state.registrations = []
                st.session_state.registration_count = 0
                if os.path.exists(CSV_FILE):
                    os.remove(CSV_FILE)
                st.success("All registration data has been cleared!")
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎉 Event Registration System | Built with Streamlit</p>
        <p>💡 Live count updates automatically | Data persisted in CSV</p>
    </div>
    """, 
    unsafe_allow_html=True
)