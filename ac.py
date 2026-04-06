import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# Page Config
# =========================
st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("🎓 Student Performance Dashboard 🎓")

# =========================
# Load & Preprocess Data (WITH TERMINAL LOGS)
# =========================
print("📥 Loading CSV file...")
df = pd.read_csv("Student Data-1.csv")
print(f"Original shape: {df.shape}")

print("🧹 Removing empty rows...")
df = df.dropna(how='all')
print(f"After removing empty rows: {df.shape}")

print("🗑️ Removing rows with missing names...")
df = df[df["Name"].notna()]
print(f"After removing missing names: {df.shape}")

print("🔧 Fixing column names...")
df.columns = df.columns.str.replace("&", "_")

print("🔢 Converting numeric columns...")
numeric_cols = ["Python", "AI_DS", "Mathematics", "OS", "IoT", "CN", "Total", "Attendance_Percentage"]
print(f"Columns: {numeric_cols}")

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
print("Conversion done.")

print("📊 Filling missing numeric values with mean...")
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("Filling done.")

print("🔁 Removing duplicate rows...")
df = df.drop_duplicates()
print(f"After removing duplicates: {df.shape}")

print("✅ Preprocessing completed!")

# =========================
# Filters
# =========================
st.sidebar.header("Filters")
city = st.sidebar.multiselect("City", df["City"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique())
name_filter = st.sidebar.multiselect("Student Name", df["Name"].unique())

filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]
if gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]
if name_filter:
    filtered_df = filtered_df[filtered_df["Name"].isin(name_filter)]

# =========================
# Key Metrics
# =========================
st.subheader("📌 Key Metrics 📌")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average Score", round(filtered_df["Total"].mean(), 2))
col3.metric("Average Attendance", round(filtered_df["Attendance_Percentage"].mean(), 2))

# =========================
# Top 3 Students & Subject Insights
# =========================
st.subheader("🏆 Top 3 Students")

subjects = ["Python", "AI_DS", "Mathematics", "OS", "IoT", "CN"]

top_3_df = filtered_df.sort_values(by="Total", ascending=False).head(3)

subject_avg = filtered_df[subjects].mean()
overall_highest_subject = subject_avg.idxmax()
overall_lowest_subject = subject_avg.idxmin()

col1, col2, col3 = st.columns(3)

col1.markdown("🥇 **Top 3 Students:**")
for i, name in enumerate(top_3_df["Name"], start=1):
    col1.write(f"{i}. {name}")

col2.metric("📈 Highest Subject", f"{overall_highest_subject} ({round(subject_avg.max(),2)})")
col3.metric("📉 Lowest Subject", f"{overall_lowest_subject} ({round(subject_avg.min(),2)})")

# =========================
# Chart Helper
# =========================
def chart_box_bigger(chart, width=800, height=500):
    st.plotly_chart(chart.update_layout(width=width, height=height), use_container_width=False)

# =========================
# Row 1: Grade & City
# =========================
col1, col2 = st.columns(2)

fig_grade = px.histogram(filtered_df, x="Grade", color="Grade", title="Grade Distribution")
with col1:
    chart_box_bigger(fig_grade)

city_counts = filtered_df["City"].value_counts().reset_index()
city_counts.columns = ["City", "Count"]
fig_city = px.bar(city_counts, x="City", y="Count", color="City", title="City-wise Student Count")
with col2:
    chart_box_bigger(fig_city)

# =========================
# Row 2: Subject & Attendance
# =========================
col1, col2 = st.columns(2)

fig_subject = px.box(filtered_df, y=subjects, title="Subject Score Distribution")
with col1:
    chart_box_bigger(fig_subject)

fig_attendance = px.scatter(
    filtered_df,
    x="Attendance_Percentage",
    y="Total",
    color="Grade",
    hover_data=["Name"],
    title="Attendance vs Total Score"
)
with col2:
    chart_box_bigger(fig_attendance)

# =========================
# Row 3: Activity & Top Scores
# =========================
col1, col2 = st.columns(2)

fig_activity = px.pie(filtered_df, names="Activity_Performed", title="Activity Participation")
with col1:
    chart_box_bigger(fig_activity)

top_scores = filtered_df.sort_values(by="Total", ascending=False).head(10)
fig_top = px.bar(top_scores, x="Name", y="Total", color="Grade", title="Top 10 Total Scores")
with col2:
    chart_box_bigger(fig_top)