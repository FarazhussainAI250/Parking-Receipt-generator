import streamlit as st
import sqlite3
from datetime import datetime
import io

# ---------- Configuration ----------
DB_PATH = "parking_entries.db"
DEPARTMENT_NAME = "Nadra Registration Office"
PARKING_FEE = 30

st.set_page_config(page_title="Nadra Registration Office", layout="wide")

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
/* Mobile Responsive CSS */
@media (max-width: 768px) {
    #top-header {
        position: relative !important;
        top: 0 !important;
        right: 0 !important;
        margin: 10px 0 !important;
        text-align: center !important;
        font-size: 16px !important;
    }
    #bottom-footer {
        position: relative !important;
        bottom: 0 !important;
        left: 0 !important;
        margin: 10px 0 !important;
        text-align: center !important;
        font-size: 12px !important;
    }
    .main .block-container {
        padding: 1rem !important;
    }
    .stDataFrame {
        font-size: 12px !important;
    }
}

/* Print-friendly CSS */
@media print {
    .stApp { background: none !important; }
    #top-header, #bottom-footer { display: none !important; }
    .main .block-container { max-width: none !important; padding: 0 !important; }
    .stCode { 
        text-align: center !important;
        margin: 0 auto !important;
        max-width: 300px !important;
        font-family: monospace !important;
        font-size: 12px !important;
        line-height: 1.2 !important;
    }
}
</style>


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

def fetch_recent(n=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, vehicle_number, vehicle_type, driver_name, entry_time, amount FROM entries ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_by_date(date_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, vehicle_number, vehicle_type, driver_name, entry_time, amount FROM entries WHERE DATE(entry_time) = ? ORDER BY id DESC", (date_str,))
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_all_entries():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, vehicle_number, vehicle_type, driver_name, entry_time, amount FROM entries ORDER BY id DESC")
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

# Initialize session state for form clearing
if 'clear_form' not in st.session_state:
    st.session_state.clear_form = False

st.title("Nadra Registration Office — Parking Receipt")
st.write("Fill vehicle details and driver name, then click **Generate Receipt**. Fee is fixed at Rs 30.")

with st.form("entry_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        vehicle = st.text_input("Vehicle Number (LEA1234)", max_chars=20, value="" if st.session_state.clear_form else st.session_state.get('vehicle', ''))
    with col2:
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Rickshaw", "Other"], index=0 if st.session_state.clear_form else st.session_state.get('vehicle_type_idx', 0))
    with col3:
        driver = st.text_input("Driver Name", max_chars=50, value="" if st.session_state.clear_form else st.session_state.get('driver', ''))
    submitted = st.form_submit_button("Generate Receipt")

if submitted:
    if not vehicle.strip():
        st.error("Please enter Vehicle Number.")
        st.session_state.clear_form = False
    elif not driver.strip():
        st.error("Please enter Driver Name.")
        st.session_state.clear_form = False
    else:
        entry_id, entry_time = add_entry(vehicle.strip(), vehicle_type, driver.strip(), PARKING_FEE)
        receipt_text, receipt_no = make_receipt_text(entry_id, vehicle.strip().upper(), vehicle_type, driver.strip(), entry_time, PARKING_FEE)
        st.success(f"Receipt generated — {receipt_no}")
        st.code(receipt_text, language="text")
        b = receipt_text.encode("utf-8")
        st.download_button(label="Download Receipt (.txt)", data=b, file_name=f"{receipt_no}.txt", mime="text/plain")
        st.info("To print: Use browser's print option (Ctrl+P) or download and print.")
        if st.button("🖨️ Print Receipt", key=f"print_{entry_id}"):
            st.markdown("""
            <script>
            window.print();
            </script>
            """, unsafe_allow_html=True)
            # Clear form after printing
            st.session_state.clear_form = True
            st.success("✅ Print dialog opened! Form cleared for next entry.")
            st.rerun()

# Reset clear_form flag after rerun
if st.session_state.clear_form:
    st.session_state.clear_form = False

# Sidebar for viewing options
with st.sidebar:
    st.header("📅 View Entries")
    view_option = st.radio("Select View:", ["Recent (5)", "Today's Entries", "Select Date", "All Entries"])
    
    if view_option == "Select Date":
        selected_date = st.date_input("Select Date:", datetime.now().date())
        date_str = selected_date.strftime("%Y-%m-%d")
    elif view_option == "Today's Entries":
        date_str = datetime.now().strftime("%Y-%m-%d")

st.markdown("---")

# Display entries based on selection
if view_option == "Recent (5)":
    st.subheader("Recent Entries (Last 5)")
    rows = fetch_recent(5)
elif view_option == "Today's Entries":
    st.subheader(f"Today's Entries ({datetime.now().strftime('%Y-%m-%d')})")
    rows = fetch_by_date(date_str)
elif view_option == "Select Date":
    st.subheader(f"Entries for {selected_date.strftime('%Y-%m-%d')}")
    rows = fetch_by_date(date_str)
else:  # All Entries
    st.subheader("All Entries")
    rows = fetch_all_entries()

if rows:
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID","Vehicle","Type","Driver","Entry Time","Amount Rs"])
    st.dataframe(df, use_container_width=True)
    
    # Show summary
    total_amount = sum(row[5] for row in rows)
    st.info(f"📊 Total Entries: {len(rows)} | Total Amount: Rs {total_amount}")
else:
    st.write("No entries found for selected criteria.")

st.markdown("*Use sidebar to filter entries by date • Fullscreen icon (⛶) available in table*")

