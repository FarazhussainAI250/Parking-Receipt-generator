# Parking-Receipt-generator
<img width="1579" height="719" alt="PARKING" src="https://github.com/user-attachments/assets/d2cc909a-d730-4297-9fad-6edb6ddeedc0" />




 Parking Receipt Web App

## 📖 Overview

This is a simple **Streamlit-based web app** for generating parking receipts at Hospital.  
It allows the parking attendant to enter a **vehicle number** and **driver name**, automatically records the **entry time, date, and receipt number**, and generates a downloadable **receipt** in text format.

---

## 🚀 Features

✅ Input vehicle number and driver name  
✅ Auto-generate current date and time  
✅ Auto-generate unique receipt number  
✅ Fixed parking fee (Rs 30)  
✅ Downloadable text receipt  
✅ View recent parking entries in a table  
✅ Local SQLite database for storage  
✅ Easy to extend for printer integration or payments

---

## 🧰 Requirements

- Python 3.8 or newer
- Streamlit
- SQLite (comes pre-installed with Python)
- Pandas (for displaying recent entries)

You can install the required packages using:

```bash
pip install streamlit pandas
```

---

## ▶️ How to Run

1. Download the file **`parking_streamlit_app.py`**.
2. Open a terminal (Command Prompt / PowerShell / VS Code Terminal).
3. Navigate to the folder where the file is located.
4. Run the following command:

```bash
streamlit run parking_streamlit_app.py
```

5. The app will open automatically in your default web browser.

---

## 🧾 Usage Instructions

1. In the input form, enter the **Vehicle Number** (e.g., `LEA-1234`) and **Driver Name**.
2. Click **Generate Receipt**.
3. The app will show the receipt details and allow you to **download** the receipt as a `.txt` file.
4. Recent parking entries will be displayed in the table below.

---

## 💾 Database Info

- The app automatically creates a local SQLite database file: `parking_entries.db`.
- Each entry includes:
  - Vehicle number
  - Driver name
  - Entry time
  - Parking amount (Rs 30)
  - Auto-generated receipt ID

---

## 🖨️ Printing the Receipt

Currently, receipts are generated as downloadable text files.  
You can print them using:

- Your computer’s printer, or
- A Bluetooth thermal printer (ESC/POS supported).

In future versions, you can easily integrate **Bluetooth or Wi-Fi thermal printer support** using libraries like:

- `python-escpos`
- `qz-tray`

---

## 🧩 Future Enhancements

- Bluetooth thermal printer integration
- QR code / barcode on receipt
- Online payment options (JazzCash, Easypaisa)
- PDF receipt format
- Admin dashboard for daily reports

---

## 🏗️ Project Structure

```
parking_streamlit_app.py   # Main app
parking_entries.db          # Local SQLite DB (auto-created)
README.md                   # This file
```

---

## 👨‍💻 Author

**Developer:** Faraz Hussain  
**Project:** Parking Receipt Generator  
**Framework:** Streamlit  
**Language:** Python 3  
**Version:** 1.0.0

---




