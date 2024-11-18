pip install matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# Load mood data:
try:
    mood = pd.read_csv("mood_data.csv")
except FileNotFoundError:
    mood = pd.DataFrame(columns=["Date", "Mood", "Note"])

# App title and intro:
st.title("Mood Tracker")
st.write("Track your mood and jot down a quick note.")

# Mood selection and note:
selected_mood = st.selectbox("How do you feel today?", ["Happy 😊", "Sad 😢", "Excited 😆", "Tired 😴", "Anxious 😟", "Relaxed 😌"])
note = st.text_input("Write a note (optional)")

# Log mood:
if st.button("Log Mood"):
    new_entry = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Mood": selected_mood, "Note": note}
    new_entry_df = pd.DataFrame([new_entry])
    mood = pd.concat([mood, new_entry_df], ignore_index=True)
    mood.to_csv("mood_data.csv", index=False)
    st.success("Mood logged successfully!")

# Display mood log:
st.write("### Your Mood Log")
st.write(mood)

# Plotting two bar charts:
st.write("### Mood Trends")

if not mood.empty:
    # Moods by date:
    mood['Date'] = pd.to_datetime(mood['Date'])
    mood_per_day = mood.groupby(mood['Date'].dt.date)['Mood'].count().reset_index()
    mood_per_day.columns = ['Date', 'Mood Count']

    # Mood Over Time:
    plt.figure(figsize=(12, 5))
    sns.barplot(x='Date', y='Mood Count', data=mood_per_day, palette="pastel")
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.title("Mood Count Over Time", fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=14, fontweight='bold')
    plt.ylabel("Mood Count", fontsize=14, fontweight='bold')
    st.pyplot(plt)

    # Mood Tracking bar chart:
    plt.figure(figsize=(12, 5))
    sns.countplot(x=mood['Mood'], palette="pastel")
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    max_count = mood['Mood'].value_counts().max()
    plt.yticks(range(1, max_count + 1, 1))
    plt.title("Mood Tracking", fontsize=16, fontweight='bold')
    plt.xlabel("Mood", fontsize=14, fontweight='bold')
    plt.ylabel("Mood Count", fontsize=14, fontweight='bold')
    st.pyplot(plt)
