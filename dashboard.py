import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import altair as alt

# Hide Streamlit default menu, header, and footer
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Force light (white) theme
st.set_page_config(
    page_title="Task Graph",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/api/tasks/"
response = requests.get(API_URL)
tasks = response.json()

if isinstance(tasks, dict):
    tasks = [tasks]

df = pd.DataFrame(tasks)

if "due_date" not in df.columns:
    df["due_date"] = pd.NaT
else:
    df["due_date"] = pd.to_datetime(df["due_date"], errors="coerce")

if "completed" not in df.columns:
    df["completed"] = False

now = datetime.now()
df["status"] = df.apply(
    lambda row: "Completed" if row["completed"] else (
        "Overdue" if pd.notna(row["due_date"]) and row["due_date"] < now else (
            "Approaching" if pd.notna(row["due_date"]) and row["due_date"] <= now + pd.Timedelta(days=1) else "On time"
        )
    ),
    axis=1
)

# Count tasks by status
status_counts = df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]

# Custom colors
status_colors = {
    "Completed": "green",
    "Overdue": "red",
    "Approaching": "orange",
    "On time": "blue"
}

print(df)
# Altair bar chart
chart = alt.Chart(status_counts).mark_bar().encode(
    x=alt.X("status:N", sort=list(status_colors.keys()), title="Task Status"),
    y=alt.Y("count:Q", title="Number of Tasks"),
    color=alt.Color("status:N", scale=alt.Scale(domain=list(status_colors.keys()),
                                               range=list(status_colors.values())),
                                               legend=None)
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)
