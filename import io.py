import io
import os
import matplotlib.pyplot as plt
import pandas as pd


def clean_and_load_data(csv_content):
    """Loads CSV content dynamically, applies data validation rules,

    prints row-skipping reasons, and returns a clean DataFrame.
    """
    lines = csv_content.strip().split("\n")
    valid_rows = []

    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            print(f"Row {idx + 1} skipped: incomplete data.")
            continue

        name, classes_held, classes_attended, marks = parts

        # Validate numeric types
        try:
            held = int(classes_held)
            attended = int(classes_attended)
        except ValueError:
            print(
                f"Row {idx + 1} skipped: invalid attendance values '{classes_held}', '{classes_attended}'."
            )
            continue

        try:
            marks_val = float(marks)
        except ValueError:
            print(f"Row {idx + 1} skipped: invalid Marks '{marks}'.")
            continue

        # Validate logic: attended cannot exceed held
        if attended > held:
            print(
                f"Row {idx + 1} skipped: attended ({attended}) cannot exceed held ({held})."
            )
            continue

        valid_rows.append([name, held, attended, marks_val])

    if not valid_rows:
        return None

    # Create DataFrame
    df = pd.DataFrame(
        valid_rows,
        columns=["Name", "Classes_Held", "Classes_Attended", "Marks"],
    )
    return df


def process_students(df):
    """Calculates attendance percentage and flags 'At Risk' status using boolean filtering."""
    # Calculate attendance percentage
    df["Attendance_Pct"] = (df["Classes_Attended"] / df["Classes_Held"]) * 100

    # Determine risk status using boolean masks
    low_attendance = df["Attendance_Pct"] < 75
    low_marks = df["Marks"] < 40

    df["Status"] = "OK"
    df.loc[low_attendance, "Status"] = "At Risk (attendance below 75%)"
    df.loc[low_marks, "Status"] = "At Risk (marks below 40%)"

    # If a student fails both, choose a representative flag or combined info
    df.loc[low_attendance & low_marks, "Status"] = (
        "At Risk (attendance below 75% & marks below 40%)"
    )

    return df


def generate_report(df):
    """Prints the descriptive text report matching Menu Option 1 expected outputs."""
    if df is None or df.empty:
        print("No valid data to analyse.")
        return

    for _, row in df.iterrows():
        print(
            f"{row['Name']}: {row['Attendance_Pct']:.2f}% | Marks {int(row['Marks'])} | {row['Status']}"
        )


def generate_summary_and_charts(df):
    """Prints averages and displays data visualizations matching Menu Option 2."""
    if df is None or df.empty:
        print("No valid data to analyse.")
        return

    # 1. Print Text Summary
    avg_attendance = df["Attendance_Pct"].mean()
    avg_marks = df["Marks"].mean()

    # Identify At Risk students using boolean filtering
    at_risk_df = df[df["Status"].str.startswith("At Risk")]
    at_risk_count = len(at_risk_df)
    at_risk_names = ", ".join(at_risk_df["Name"].tolist())

    print(
        f"Average attendance: {avg_attendance:.2f}% | Average marks: {avg_marks:.2f}"
    )
    print(f"At Risk students: {at_risk_count} ({at_risk_names})")
    print("Bar chart and scatter chart 'Attendance vs Marks' displayed")

    # 2. Render Charts using Matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar Chart: Attendance per student
    ax1.bar(df["Name"], df["Attendance_Pct"], color="skyblue", edgecolor="black")
    ax1.axhline(
        75, color="red", linestyle="--", label="75% Attendance Threshold"
    )
    ax1.set_title("Student Attendance Percentage")
    ax1.set_xlabel("Student Name")
    ax1.set_ylabel("Attendance (%)")
    ax1.set_ylim(0, 105)
    ax1.legend()

    # Scatter Chart: Attendance vs Marks
    ax2.scatter(
        df["Attendance_Pct"],
        df["Marks"],
        color="purple",
        s=100,
        edgecolors="black",
    )
    ax2.axvline(75, color="red", linestyle="--", label="75% Attendance")
    ax2.axhline(40, color="orange", linestyle="--", label="40 Marks Pass")
    ax2.set_title("Attendance vs Marks")
    ax2.set_xlabel("Attendance (%)")
    ax2.set_ylabel("Marks (out of 100)")
    ax2.set_xlim(0, 105)
    ax2.set_ylim(0, 105)
    ax2.legend()

    plt.tight_layout()
    plt.show()


# ==========================================
# TEST RUNNERS (Simulating the 4 Test Cases)
# ==========================================

# Test Data Definitions
data_tc1 = "Aman,40,36,80\nRiya,40,28,65\nKaran,40,30,35"
data_tc2 = "Neha,40,30,40"
data_tc3 = "Aman,40,45,80\nRiya,40,30,abc"

print("=" * 50)
print("TEST CASE 1: Normal Input (Menu Option 1)")
print("=" * 50)
df1 = clean_and_load_data(data_tc1)
df1 = process_students(df1)
generate_report(df1)

print("\n" + "=" * 50)
print("TEST CASE 2: Boundary / Minimum Input (Menu Option 1)")
print("=" * 50)
df2 = clean_and_load_data(data_tc2)
df2 = process_students(df2)
generate_report(df2)

print("\n" + "=" * 50)
print("TEST CASE 3: Invalid Input")
print("=" * 50)
df3 = clean_and_load_data(data_tc3)
if df3 is not None:
    df3 = process_students(df3)
    generate_report(df3)
else:
    print("No valid data to analyse.")

print("\n" + "=" * 50)
print("TEST CASE 4: Different Valid Scenario (Menu Option 2)")
print("=" * 50)
# Uses clean data from Test Case 1 as specified
generate_summary_and_charts(df1)
