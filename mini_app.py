import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date

# Define the scopes
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Get credentials from Streamlit secrets
credentials_dict = st.secrets["gcp_service_account"]

# Create credentials from the dict
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

# Authorize gspread client
client = gspread.authorize(creds)

# Open your Google Sheet by name
sheet = client.open("mini-app-logger").sheet1  

st.title("My mini health log app 😊")

# Mood options
moods = {
    "😊": "Happy",
    "😠": "Angry",
    "😕": "Confused",
    "🎉": "Excited"
}

st.subheader("1. Log your mood")

# Dropdown menu for mood selection
selected_mood = st.selectbox("How are you feeling?", list(moods.keys()))
note = st.text_input("Optional note")              
submit = st.button("Submit Mood")

if submit:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, selected_mood, moods[selected_mood], note]
    sheet.append_row(row)
    st.success("Mood logged successfully.")

# Mood graph
today = date.today()
st.subheader(f"2. Mood Overview ({today})")

# Load data from Google Sheets
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Strip extra spaces from column names
df.columns = df.columns.str.strip()

# Debug: show columns and first few rows
st.write("Columns in dataframe:", df.columns.tolist())
st.write(df.head())

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Filter today's entries
df_today = df[df["timestamp"].dt.date == today]

# Check if 'mood' column exists before counting
if "mood" in df_today.columns:
    mood_counts = df_today["mood"].value_counts()
    st.bar_chart(mood_counts)
else:
    st.error("Column 'mood' not found in today's data!")
