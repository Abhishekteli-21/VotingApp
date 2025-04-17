import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import random
import time
from datetime import datetime
# import os

# Set page configuration
st.set_page_config(
    page_title="Indian Style Voting System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'voter_id' not in st.session_state:
    st.session_state.voter_id = ""
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = {}  # Dict to track which voters have voted
if 'votes' not in st.session_state:
    st.session_state.votes = {}  # Dict to store votes by constituency
if 'voters_db' not in st.session_state:
    # Example voter database with voter ID, name, constituency, and password (in real scenario, this would be encrypted)
    st.session_state.voters_db = {
        "ABC1234567": {"name": "Raj Kumar", "constituency": "Mumbai North", "password": "1234", "has_voted": False},
        "DEF7654321": {"name": "Priya Singh", "constituency": "Mumbai South", "password": "5678", "has_voted": False},
        "GHI1122334": {"name": "Amit Patel", "constituency": "Delhi East", "password": "9012", "has_voted": False},
        "JKL5566778": {"name": "Sunita Sharma", "constituency": "Delhi West", "password": "3456", "has_voted": False},
        "MNO9900112": {"name": "Vikram Reddy", "constituency": "Bangalore Central", "password": "7890", "has_voted": False}
    }
if 'candidates' not in st.session_state:
    # Example candidates database with name, party, constituency, and symbol
    st.session_state.candidates = {
        "Mumbai North": [
            {"name": "Amitabh Joshi", "party": "National Democratic Alliance", "symbol": "🌷"},
            {"name": "Ravi Desai", "party": "United Progressive Alliance", "symbol": "✋"},
            {"name": "Meera Kulkarni", "party": "Regional People's Front", "symbol": "🚲"},
            {"name": "NOTA", "party": "None of the Above", "symbol": "❌"}
        ],
        "Mumbai South": [
            {"name": "Sanjay Patil", "party": "National Democratic Alliance", "symbol": "🌷"},
            {"name": "Lakshmi Iyer", "party": "United Progressive Alliance", "symbol": "✋"},
            {"name": "Farhan Ahmed", "party": "Progressive Democratic Party", "symbol": "🐘"},
            {"name": "NOTA", "party": "None of the Above", "symbol": "❌"}
        ],
        "Delhi East": [
            {"name": "Rakesh Verma", "party": "National Democratic Alliance", "symbol": "🌷"},
            {"name": "Zoya Khan", "party": "United Progressive Alliance", "symbol": "✋"},
            {"name": "Dinesh Gupta", "party": "People's Voice Party", "symbol": "🌟"},
            {"name": "NOTA", "party": "None of the Above", "symbol": "❌"}
        ],
        "Delhi West": [
            {"name": "Alok Nath", "party": "National Democratic Alliance", "symbol": "🌷"},
            {"name": "Preeti Tiwari", "party": "United Progressive Alliance", "symbol": "✋"},
            {"name": "Mohammed Salim", "party": "Democratic Workers Party", "symbol": "⚙️"},
            {"name": "NOTA", "party": "None of the Above", "symbol": "❌"}
        ],
        "Bangalore Central": [
            {"name": "Venkatesh Murthy", "party": "National Democratic Alliance", "symbol": "🌷"},
            {"name": "Divya Krishnan", "party": "United Progressive Alliance", "symbol": "✋"},
            {"name": "Robert D'Souza", "party": "Progressive People's Party", "symbol": "🚜"},
            {"name": "NOTA", "party": "None of the Above", "symbol": "❌"}
        ]
    }
if 'admin_credentials' not in st.session_state:
    st.session_state.admin_credentials = {"admin": "election2025"}
if 'election_status' not in st.session_state:
    st.session_state.election_status = "ongoing"  # Options: "ongoing", "completed"

# Initialize votes for each constituency and candidate if not already done
for constituency, candidates_list in st.session_state.candidates.items():
    if constituency not in st.session_state.votes:
        st.session_state.votes[constituency] = {candidate["name"]: 0 for candidate in candidates_list}

# Function to save votes to a CSV file
def save_votes_to_csv():
    votes_data = []
    for constituency, candidates_votes in st.session_state.votes.items():
        for candidate, vote_count in candidates_votes.items():
            votes_data.append({"Constituency": constituency, "Candidate": candidate, "Votes": vote_count})
    
    df = pd.DataFrame(votes_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"election_results_{timestamp}.csv"
    df.to_csv(filename, index=False)
    return filename

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .css-18e3th9 {
        padding: 2rem 1rem;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 16px;
        font-weight: bold;
    }
    .vote-btn {
        background-color: #FF9933;
        color: white;
    }
    .logout-btn {
        background-color: #FF5733;
        color: white;
    }
    .title-container {
        background-color: #138808;
        padding: 10px;
        border-radius: 5px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .candidate-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .symbol {
        font-size: 2em;
    }
</style>
""", unsafe_allow_html=True)

# Create header with Indian flag colors
st.markdown("""
<div style="background-color: #FF9933; height: 10px; width: 100%;"></div>
<div style="background-color: white; height: 10px; width: 100%;"></div>
<div style="background-color: #138808; height: 10px; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🗳️ Indian Electronic Voting System</h1>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Election_Commission_of_India_logo.svg/220px-Election_Commission_of_India_logo.svg.png", width=150)
    st.markdown("## Election Commission of India")
    st.markdown("---")
    
    # Show different options based on authentication status
    if st.session_state.admin_logged_in:
        st.markdown("### Admin Dashboard")
        admin_action = st.radio("Select Action", ["View Results", "Manage Election Status", "Download Results", "Logout"])
        
        if admin_action == "Logout":
            st.session_state.admin_logged_in = False
            st.rerun()
    
    elif st.session_state.authenticated:
        st.markdown(f"### Welcome, {st.session_state.voters_db[st.session_state.voter_id]['name']}")
        st.markdown(f"**Voter ID:** {st.session_state.voter_id}")
        st.markdown(f"**Constituency:** {st.session_state.voters_db[st.session_state.voter_id]['constituency']}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.voter_id = ""
            st.rerun()
    
    else:
        login_option = st.radio("Select Login Type", ["Voter", "Admin"])

# Main content area
if not st.session_state.authenticated and not st.session_state.admin_logged_in:
    # Login screen
    if 'login_option' in locals() and login_option == "Voter":
        st.markdown("<h2 style='text-align: center;'>Voter Login</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            voter_id = st.text_input("Enter Voter ID Card Number")
        
        with col2:
            password = st.text_input("Enter Password", type="password")
        
        if st.button("Login"):
            if voter_id in st.session_state.voters_db and st.session_state.voters_db[voter_id]["password"] == password:
                if not st.session_state.voters_db[voter_id]["has_voted"] and st.session_state.election_status == "ongoing":
                    st.session_state.authenticated = True
                    st.session_state.voter_id = voter_id
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                elif st.session_state.voters_db[voter_id]["has_voted"]:
                    st.error("You have already cast your vote.")
                else:
                    st.error("Elections are not currently ongoing.")
            else:
                st.error("Invalid Voter ID or Password. Please try again.")
    
    elif 'login_option' in locals() and login_option == "Admin":
        st.markdown("<h2 style='text-align: center;'>Election Commission Admin Login</h2>", unsafe_allow_html=True)
        
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        
        if st.button("Login as Admin"):
            if admin_username in st.session_state.admin_credentials and st.session_state.admin_credentials[admin_username] == admin_password:
                st.session_state.admin_logged_in = True
                st.success("Admin login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid admin credentials. Please try again.")

elif st.session_state.admin_logged_in:
    # Admin dashboard
    if admin_action == "View Results":
        st.markdown("<h2 style='text-align: center;'>Election Results Dashboard</h2>", unsafe_allow_html=True)
        
        # Summary statistics
        total_votes = sum(sum(candidates.values()) for candidates in st.session_state.votes.values())
        total_eligible = len(st.session_state.voters_db)
        turnout_percentage = (total_votes / total_eligible) * 100 if total_eligible > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Votes Cast", f"{total_votes}")
        with col2:
            st.metric("Eligible Voters", f"{total_eligible}")
        with col3:
            st.metric("Voter Turnout", f"{turnout_percentage:.2f}%")
        
        st.markdown("---")
        
        # Show results for each constituency
        for constituency, candidates_votes in st.session_state.votes.items():
            st.markdown(f"### {constituency} Results")
            
            # Create dataframe for the current constituency
            results_df = pd.DataFrame({
                "Candidate": list(candidates_votes.keys()),
                "Votes": list(candidates_votes.values())
            })
            
            # Add party information
            party_info = {candidate["name"]: candidate["party"] for candidate in st.session_state.candidates[constituency]}
            results_df["Party"] = results_df["Candidate"].map(party_info)
            
            # Sort by votes descending
            results_df = results_df.sort_values("Votes", ascending=False)
            
            # Display as table and chart
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.dataframe(results_df, hide_index=True)
            
            with col2:
                if results_df["Votes"].sum() > 0:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(results_df["Candidate"], results_df["Votes"], color=["#FF9933", "#FFFFFF", "#138808", "#000080"])
                    plt.xticks(rotation=45, ha="right")
                    plt.title(f"Vote Distribution in {constituency}")
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.info("No votes recorded for this constituency yet.")
            
            st.markdown("---")
    
    elif admin_action == "Manage Election Status":
        st.markdown("<h2 style='text-align: center;'>Manage Election Status</h2>", unsafe_allow_html=True)
        
        current_status = st.session_state.election_status
        st.info(f"Current election status: {current_status.upper()}")
        
        new_status = st.radio("Set Election Status", ["ongoing", "completed"], index=0 if current_status == "ongoing" else 1)
        
        if st.button("Update Status"):
            if new_status != current_status:
                st.session_state.election_status = new_status
                st.success(f"Election status updated to: {new_status.upper()}")
                time.sleep(1)
                st.rerun()
            else:
                st.info("No change in status.")
    
    elif admin_action == "Download Results":
        st.markdown("<h2 style='text-align: center;'>Download Election Results</h2>", unsafe_allow_html=True)
        
        if st.button("Generate Results CSV"):
            filename = save_votes_to_csv()
            # Create a download button for the generated file
            with open(filename, "rb") as file:
                st.download_button(
                    label="Download Results CSV",
                    data=file,
                    file_name=filename,
                    mime="text/csv"
                )
            st.success(f"Results saved to {filename}")

elif st.session_state.authenticated:
    # Voting screen
    constituency = st.session_state.voters_db[st.session_state.voter_id]["constituency"]
    
    st.markdown(f"<h2 style='text-align: center;'>Voting Ballot - {constituency}</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Please select one candidate and press the VOTE button to confirm your choice.</p>", unsafe_allow_html=True)
    
    # Display Indian election instructions
    st.info("""
    **Instructions:**
    1. You can select only ONE candidate.
    2. Your vote is confidential and secure.
    3. Verify your selection before confirming.
    4. Once your vote is cast, you cannot change it.
    5. If you don't want to vote for any candidate, you can select NOTA (None of the Above).
    """)
    
    # Display candidates for the voter's constituency
    candidate_selected = None
    
    candidates = st.session_state.candidates[constituency]
    
    # Create columns for candidates
    cols = st.columns(len(candidates))
    
    # Display candidate cards
    for i, candidate in enumerate(candidates):
        with cols[i]:
            st.markdown(f"""
            <div class="candidate-card">
                <div class="symbol">{candidate['symbol']}</div>
                <h3>{candidate['name']}</h3>
                <p>{candidate['party']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Radio button for selection
    candidate_selected = st.radio(
        "Select your candidate:",
        [f"{c['name']} ({c['party']}) {c['symbol']}" for c in candidates],
        index=None
    )
    
    # Vote button
    if st.button("CAST YOUR VOTE", type="primary"):
        if candidate_selected:
            # Extract candidate name from the selection
            selected_name = candidate_selected.split(" (")[0]
            
            # Show confirmation dialog
            confirm = st.warning(f"Are you sure you want to vote for {selected_name}?")
            confirm_cols = st.columns(2)
            
            with confirm_cols[0]:
                if st.button("Yes, Confirm My Vote"):
                    # Record the vote
                    st.session_state.votes[constituency][selected_name] += 1
                    st.session_state.voters_db[st.session_state.voter_id]["has_voted"] = True
                    
                    # Show success message with animation
                    st.balloons()
                    st.success("Your vote has been recorded successfully! Thank you for voting.")
                    
                    # Display a message indicating the voter will be logged out
                    st.info("You will be logged out in 5 seconds...")
                    time.sleep(5)
                    
                    # Log out the voter
                    st.session_state.authenticated = False
                    st.session_state.voter_id = ""
                    st.rerun()
            
            with confirm_cols[1]:
                if st.button("No, I Want to Change"):
                    st.rerun()
        else:
            st.error("Please select a candidate before casting your vote.")