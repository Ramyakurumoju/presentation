import streamlit as st
import os

# Initialize session state for storing student data
if "students" not in st.session_state:
    st.session_state.students = []

# Function to add a student and their video
def add_student(name, roll_number, video_path):
    # Check if the student is already added
    for student in st.session_state.students:
        if student['roll_number'] == roll_number:
            st.warning(f"Roll Number {roll_number} is already added.")
            return
    # Add the student
    st.session_state.students.append({'name': name, 'roll_number': roll_number, 'video': video_path})
    # Sort students by roll number
    st.session_state.students.sort(key=lambda x: x['roll_number'])

# Function to predict the next student
def predict_next_student(current_roll):
    for student in st.session_state.students:
        if student['roll_number'] > current_roll:
            return student
    return None  # If no student is left

# Streamlit App
def main():
    st.title("Student Introduction and Video Prediction App")

    # Upload student information
    st.subheader("Upload Student Introduction Video")
    student_name = st.text_input("Enter Student's Name")
    student_roll = st.number_input("Enter Student's Roll Number", min_value=1, step=1)
    uploaded_video = st.file_uploader("Upload Introduction Video", type=["mp4", "mov"])

    if uploaded_video and student_name and student_roll:
        # Ensure uploads folder exists
        os.makedirs("uploads", exist_ok=True)

        # Save the uploaded video
        video_path = os.path.join("uploads", f"{student_roll}_{student_name}_{uploaded_video.name}")
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        # Add the student to the list
        add_student(student_name, student_roll, video_path)

        # Confirm addition
        st.success(f"Student '{student_name}' (Roll: {student_roll}) has been added with their video.")

    # Display list of students
    st.subheader("Students and Their Videos")
    if st.session_state.students:
        for student in st.session_state.students:
            st.write(f"Roll Number: {student['roll_number']}, Name: {student['name']}")
            st.video(student['video'])

    # Predict the next student based on roll number
    st.subheader("Predict the Next Student")
    current_roll = st.number_input("Enter Current Roll Number", min_value=0, step=1)

    if st.button("Predict Next Student"):
        next_student = predict_next_student(current_roll)
        if next_student:
            st.success(f"The next student to present is: {next_student['name']} (Roll: {next_student['roll_number']})")
            st.video(next_student['video'])
        else:
            st.warning("No students are left to present.")


if __name__ == "__main__":
    main()
