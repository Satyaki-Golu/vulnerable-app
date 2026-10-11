import streamlit as st
import sqlite3
import time
import os

# 1. Initialize the in-memory database and populate dummy Koala data
@st.cache_resource
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    # Create users table
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', '1234')")
    # Create koala names table
    cursor.execute("CREATE TABLE IF NOT EXISTS koalas (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cursor.execute("INSERT INTO koalas (name) VALUES ('Blinky'), ('Coco'), ('Nugget')")
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# Initialize session state for login tracking
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_hacked" not in st.session_state:
    st.session_state.is_hacked = False

# Public Interface: Main Koala Portal
st.title("🐨 The Koala Information Sanctuary")
st.write("Welcome to the community portal celebrating the world's finest marsupials!")

# Display current koalas
st.subheader("Our Sanctuary Resident Koalas")
try:
    current_koalas = cursor.execute("SELECT name FROM koalas").fetchall()
    for k in current_koalas:
        st.write(f"- {k[0]}")
except Exception as e:
    st.error(f"Database Error: {e}")

st.markdown("---")

# 2. Behind the scenes: Administrative Panel Login Drawer
with st.sidebar:
    st.header("🔒 Staff Control Panel")
    
    if not st.session_state.logged_in:
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        login_btn = st.button("Login")
        
        if login_btn:
            # 🚨 VULNERABILITY 1: RAW STRING CONCATENATION (SQL INJECTION)
            # This directly builds user inputs into the SQL query text.
            vuln_query = f"SELECT * FROM users WHERE username = '{user_input}' AND password = '{pass_input}'"
            
            st.caption(f"**Executed Query Preview:** `{vuln_query}`")
            
            try:
                cursor.execute(vuln_query)
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except Exception as err:
                st.error(f"SQL Execution Error: {err}")
    else:
        st.success("Logged in as Admin")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# 3. Admin Functionality & Resource Exhaustion (DoS)
if st.session_state.logged_in:
    st.header("🛠️ Admin Dashboard: Manage Database")
    
    # Normal Feature: Add Koala Name
    new_name = st.text_input("Register a New Koala Name:")
    if st.button("Add Koala"):
        if new_name:
            cursor.execute("INSERT INTO koalas (name) VALUES (?)", (new_name,))
            conn.commit()
            st.success(f"Added {new_name} successfully!")
            st.rerun()

    st.markdown("---")
    st.subheader("⚠️ Database Maintenance Tools")
    st.write("Warning: Running deep index padding may consume high server resources.")
    
    # 🚨 VULNERABILITY 2: UNRESTRICTED LOOPS / ALGORITHMIC COMPLEXITY DOS
    # This simulates a memory-leak / heavy database inflation vulnerability
    multiplier = st.number_input("Index Padding Multiplier (Default safe: 1)", min_value=1, value=1)
    
    if st.button("Run Vulnerable Index Function"):
        if multiplier > 500: # Threshold set to simulate severe impact
            st.session_state.is_hacked = True
            
            # Simulate artificial application lag freezing up the thread
            with st.spinner("Processing massive database payload... App lagging heavily..."):
                time.sleep(5) 
                
            st.error("🚨 WEBSITE HACKED: MEMORY EXHAUSTION DETECTED 🚨")
            st.write("Render container process terminating...")
            
            # Force a re-render so the UI updates for the user before the exit command executes
            time.sleep(2)
            
            # Automatically close the application process
            os._exit(1) #
            
            # Automatically close the application process gracefully
            os._exit(0) 
        else:
            # Safe branch: perform a minor loop simulation
            with st.spinner("Running optimization..."):
                time.sleep(0.5)
            st.success("Optimization finished smoothly.")

if st.session_state.is_hacked:
    st.error("🚨 WEBSITE HACKED 🚨")
