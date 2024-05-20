import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io
import time
import base64
from datetime import datetime, timedelta

# Initialize DataFrame
if 'attendance_df' not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(columns=['ID', 'Name', 'Phone', 'Timestamp'])

# Generate QR Code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Get current QR data
def get_current_qr_data():
    return base64.b64encode(str(time.time()).encode()).decode()

# Display QR Code
def display_qr_code(img):
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    st.image(f"data:image/png;base64,{img_str}")

# Form for user input
def user_form():
    st.write("Please enter your details:")
    with st.form("attendance_form"):
        id_input = st.text_input("Student ID")
        name_input = st.text_input("Name")
        phone_input = st.text_input("Phone Number")
        qr_data = st.text_input("QR Data")
        submitted = st.form_submit_button("Submit")

        if submitted:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.attendance_df = st.session_state.attendance_df.append({
                'ID': id_input,
                'Name': name_input,
                'Phone': phone_input,
                'Timestamp': current_time,
                'QR Data': qr_data
            }, ignore_index=True)
            st.success("Attendance recorded!")

# Save DataFrame to CSV
def save_to_csv():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"attendance_{current_time}.csv"
    st.session_state.attendance_df.to_csv(filename, index=False)
    st.session_state.attendance_df = pd.DataFrame(columns=['ID', 'Name', 'Phone', 'Timestamp'])
    st.success(f"Attendance data saved as {filename}")

# Main app logic
st.title("Seminar Attendance System")

# Display QR Code every 2 minutes
if 'last_qr_update' not in st.session_state or datetime.now() - st.session_state.last_qr_update > timedelta(minutes=2):
    st.session_state.qr_data = get_current_qr_data()
    st.session_state.qr_image = generate_qr_code(st.session_state.qr_data)
    st.session_state.last_qr_update = datetime.now()

display_qr_code(st.session_state.qr_image)

# Show user form
user_form()

# Save CSV every hour
if 'last_save' not in st.session_state:
    st.session_state.last_save = datetime.now()

if datetime.now() - st.session_state.last_save > timedelta(hours=1):
    save_to_csv()
    st.session_state.last_save = datetime.now()
