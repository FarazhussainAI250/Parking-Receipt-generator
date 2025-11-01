import streamlit as st
import sqlite3
from datetime import datetime
import io

# ---------- Configuration ----------
DB_PATH = "parking_entries.db"
DEPARTMENT_NAME = "Nadra Registration Office"
PARKING_FEE = 30

st.set_page_config(page_title="Nadra Registration Office", layout="centered")

# ----------- Custom CSS ------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://t3.ftcdn.net/jpg/03/22/22/56/360_F_322225640_9woTPc71vuaAapO8bGbNGKU5JbLgQUeQ.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
#top-header {
    position: fixed;
    top: 80px;
    right: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 8px 16px;
    border-radius: 8px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    z-index: 100;
}
#bottom-footer {
    position: fixed;
    bottom: 10px;
    left: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 6px 14px;
    border-radius: 6px;
    color: white;
    font-size: 14px;
    z-index: 100;
}
</style>

<div id="top-header">Respected Sir Shahzaib & Sir Ali Hamza</div>
<div id="bottom-footer">Developed by Faraz Hussain</div>
""", unsafe_allow_html=True)

# ---------- Database helpers ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            driver_name TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            amount INTEGER NOT NULL,
            payment_method TEXT,
            printed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_entry(vehicle_number, vehicle_type, driver_name, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO entries (vehicle_number, vehicle_type, driver_name, entry_time, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (vehicle_number.upper(), vehicle_type, driver_name, entry_time, amount))
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return rowid, entry_time

def fetch_recent(n=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, vehicle_number, vehicle_type, driver_name, entry_time, amount FROM entries ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- Utility ----------
def make_receipt_text(entry_id, vehicle_number, vehicle_type, driver_name, entry_time, amount):
    receipt_no = f"P-{datetime.now().strftime('%Y%m%d')}-{entry_id:04d}"
    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "----------------------------------------",
        f"{DEPARTMENT_NAME}",
        "Parking Receipt".center(40),
        "----------------------------------------",
        f"Receipt No: {receipt_no}",
        f"Date: {date_str}",
        f"Vehicle: {vehicle_number} ({vehicle_type})",
        f"Driver: {driver_name}",
        f"Entry Time: {entry_time}",
        f"Amount: Rs {amount}",
        "Paid: CASH",
        "----------------------------------------",
        "Thank you — Drive Safely",
        "----------------------------------------",
    ]
    return "\n".join(lines), receipt_no

# ---------- App UI ----------
init_db()

st.title("Nadra Registration Office — Parking Receipt")
st.write("Fill vehicle details and driver name, then click **Generate Receipt**. Fee is fixed at Rs 30.")

with st.form("entry_form"):
    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        vehicle = st.text_input("Vehicle Number (LEA1234)", max_chars=20)
    with col2:
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Rickshaw", "Other"])
    with col3:
        driver = st.text_input("Driver Name", max_chars=50)
    submitted = st.form_submit_button("Generate Receipt")

if submitted:
    if not vehicle.strip():
        st.error("Please enter Vehicle Number.")
    elif not driver.strip():
        st.error("Please enter Driver Name.")
    else:
        entry_id, entry_time = add_entry(vehicle.strip(), vehicle_type, driver.strip(), PARKING_FEE)
        receipt_text, receipt_no = make_receipt_text(entry_id, vehicle.strip().upper(), vehicle_type, driver.strip(), entry_time, PARKING_FEE)
        st.success(f"Receipt generated — {receipt_no}")
        st.code(receipt_text, language="text")
        b = receipt_text.encode("utf-8")
        st.download_button(label="Download Receipt (.txt)", data=b, file_name=f"{receipt_no}.txt", mime="text/plain")
        st.info("To get a hard copy: download and print, or use a paired thermal printer.")

st.markdown("---")
st.subheader("Recent Entries")
rows = fetch_recent(20)
if rows:
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID","Vehicle","Type","Driver","Entry Time","Amount Rs"])
    st.dataframe(df)
else:
    st.write("No entries yet.")

st.markdown("*Entries are stored locally in `parking_entries.db`. Extendable to printer or payment integration.*")
