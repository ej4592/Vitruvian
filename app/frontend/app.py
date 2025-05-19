import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import os

# API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

def login(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            return True
    except Exception as e:
        st.error(f"Error during login: {str(e)}")
    return False

def register(email: str, username: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/users/",
            json={"email": email, "username": username, "password": password}
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Error during registration: {str(e)}")
    return False

def get_groups():
    try:
        response = requests.get(
            f"{API_URL}/groups/",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching groups: {str(e)}")
    return []

def create_group(name: str, description: str):
    try:
        response = requests.post(
            f"{API_URL}/groups/",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            json={"name": name, "description": description}
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Error creating group: {str(e)}")
    return False

def get_exercises(group_id: int):
    try:
        response = requests.get(
            f"{API_URL}/exercises/",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            params={"group_id": group_id}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching exercises: {str(e)}")
    return []

def create_exercise(name: str, description: str, group_id: int):
    try:
        response = requests.post(
            f"{API_URL}/exercises/",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            json={"name": name, "description": description, "group_id": group_id}
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Error creating exercise: {str(e)}")
    return False

def submit_score(exercise_id: int, value: float):
    try:
        response = requests.post(
            f"{API_URL}/scores/",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            json={"exercise_id": exercise_id, "value": value}
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Error submitting score: {str(e)}")
    return False

def get_scores(exercise_id: int):
    try:
        response = requests.get(
            f"{API_URL}/scores/",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            params={"exercise_id": exercise_id}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching scores: {str(e)}")
    return []

def check_user_exists(email: str):
    try:
        response = requests.get(f"{API_URL}/users/check/{email}")
        if response.status_code == 200:
            return response.json()["exists"]
    except Exception as e:
        st.error(f"Error checking user: {str(e)}")
    return None

# Main app
st.title("Exercise Competition App")

# Authentication
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if login(email, password):
                st.success("Login successful!")
                st.rerun()
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Register")
            email = st.text_input("Email", key="register_email")
            first_name = st.text_input("First Name", key="register_first_name")
            last_name = st.text_input("Last Name", key="register_last_name")
            nickname = st.text_input("Nickname (Optional)", key="register_nickname")
            password = st.text_input("Password", type="password", key="register_password")
            submit = st.form_submit_button("Register")
            
            if submit:
                # Validate required fields
                if not all([email, first_name, last_name, password]):
                    st.error("Please fill in all required fields.")
                else:
                    try:
                        response = requests.post(
                            f"{API_URL}/users/",
                            json={
                                "email": email,
                                "first_name": first_name,
                                "last_name": last_name,
                                "nickname": nickname if nickname else None,
                                "password": password
                            }
                        )
                        if response.status_code == 200:
                            st.success("Registration successful! Please login.")
                            st.rerun()
                        else:
                            try:
                                error_detail = response.json().get('detail', 'Unknown error')
                                if "Email already registered" in error_detail:
                                    st.error("This email is already registered. Please use a different email address.")
                                else:
                                    st.error(f"Registration failed: {error_detail}")
                            except json.JSONDecodeError:
                                st.error(f"Registration failed: Server returned invalid response. Status code: {response.status_code}")
                                st.error(f"Response content: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Network error: {str(e)}")
                    except Exception as e:
                        st.error(f"Unexpected error: {str(e)}")

else:
    # Main app content
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Groups", "Exercises", "Leaderboard"])
    
    if page == "Groups":
        st.header("Groups")
        
        # Create new group
        with st.expander("Create New Group"):
            group_name = st.text_input("Group Name")
            group_description = st.text_area("Description")
            if st.button("Create Group"):
                if create_group(group_name, group_description):
                    st.success("Group created successfully!")
                    st.rerun()
        
        # Display groups
        groups = get_groups()
        if groups:
            for group in groups:
                with st.expander(f"{group['name']} - {group['description']}"):
                    st.write(f"Created: {group['created_at']}")
                    st.write(f"Members: {len(group['members'])}")
        else:
            st.info("No groups found. Create one to get started!")

    elif page == "Exercises":
        st.header("Exercises")
        
        # Select group
        groups = get_groups()
        if groups:
            selected_group = st.selectbox(
                "Select Group",
                options=groups,
                format_func=lambda x: x['name']
            )
            
            # Create new exercise
            with st.expander("Create New Exercise"):
                exercise_name = st.text_input("Exercise Name")
                exercise_description = st.text_area("Description")
                if st.button("Create Exercise"):
                    if create_exercise(exercise_name, exercise_description, selected_group['id']):
                        st.success("Exercise created successfully!")
                        st.rerun()
            
            # Display exercises
            exercises = get_exercises(selected_group['id'])
            if exercises:
                for exercise in exercises:
                    with st.expander(f"{exercise['name']} - {exercise['description']}"):
                        # Submit score
                        score = st.number_input("Your Score", min_value=0.0, step=0.1, key=f"score_{exercise['id']}")
                        if st.button("Submit Score", key=f"submit_{exercise['id']}"):
                            if submit_score(exercise['id'], score):
                                st.success("Score submitted successfully!")
                                st.rerun()
                        
                        # Display scores
                        scores = get_scores(exercise['id'])
                        if scores:
                            df = pd.DataFrame(scores)
                            df['recorded_at'] = pd.to_datetime(df['recorded_at'])
                            fig = px.line(df, x='recorded_at', y='value', title=f"Scores for {exercise['name']}")
                            st.plotly_chart(fig)
        else:
            st.info("No groups found. Create a group first!")

    elif page == "Leaderboard":
        st.header("Leaderboard")
        
        # Select group
        groups = get_groups()
        if groups:
            selected_group = st.selectbox(
                "Select Group",
                options=groups,
                format_func=lambda x: x['name']
            )
            
            # Get all exercises and scores
            exercises = get_exercises(selected_group['id'])
            if exercises:
                # Create a DataFrame for the leaderboard
                leaderboard_data = []
                for exercise in exercises:
                    scores = get_scores(exercise['id'])
                    for score in scores:
                        leaderboard_data.append({
                            'Exercise': exercise['name'],
                            'User': score['user_id'],  # In a real app, you'd want to show usernames
                            'Score': score['value'],
                            'Date': score['recorded_at']
                        })
                
                if leaderboard_data:
                    df = pd.DataFrame(leaderboard_data)
                    # Calculate rankings
                    df['Rank'] = df.groupby('Exercise')['Score'].rank(ascending=False)
                    st.dataframe(df.sort_values(['Exercise', 'Rank']))
                else:
                    st.info("No scores recorded yet!")
            else:
                st.info("No exercises found in this group!")
        else:
            st.info("No groups found. Create a group first!")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun() 