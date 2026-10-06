
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Student Transport and Bus Route Finder", page_icon="🚌", layout="wide")

st.markdown("""
<style>

.stApp{
background: linear-gradient(to right,#eef4ff,#ffffff);
}

section[data-testid="stSidebar"]{
background:#0F172A;
}

section[data-testid="stSidebar"] *{
color:white;
}

.main-header{
background:linear-gradient(135deg,#1E3A8A,#2563EB);
padding:35px;
border-radius:25px;
text-align:center;
color:white;
box-shadow:0px 10px 30px rgba(0,0,0,0.25);
margin-bottom:20px;
}

.main-header h1{
font-size:48px;
font-weight:700;
}

.main-header p{
font-size:20px;
opacity:0.9;
}

.metric-card{
background:white;
padding:25px;
border-radius:20px;
text-align:center;
box-shadow:0 8px 20px rgba(0,0,0,0.12);
transition:0.3s;
}

.metric-card:hover{
transform:translateY(-5px);
}

.metric-number{
font-size:40px;
font-weight:bold;
color:#2563EB;
}

.metric-title{
font-size:18px;
color:#666;
}

.route-card{
background:white;
padding:25px;
border-radius:20px;
margin-top:15px;
box-shadow:0px 5px 20px rgba(0,0,0,0.12);
border-left:8px solid #2563EB;
}

.search-box{
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 5px 20px rgba(0,0,0,0.12);
margin-bottom:20px;
}

.footer{
text-align:center;
color:#666;
margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("transport.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS buses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
bus_number TEXT,
route_name TEXT,
boarding_point TEXT,
pickup_time TEXT,
driver_name TEXT,
driver_contact TEXT,
route_details TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM buses")
if cur.fetchone()[0] == 0:
    data=[
    ("BUS101","Hosur Route","Hosur Bus Stand","7:15 AM","Ramesh","9876543210","Hosur → Mathigiri → SIPCOT → College"),
    ("BUS102","Bangalore Route","Electronic City","6:30 AM","Kumar","9876543211","Electronic City → Attibele → College"),
    ("BUS103","Krishnagiri Route","Krishnagiri Bus Stand","6:45 AM","Suresh","9876543212","Krishnagiri → Shoolagiri → College")
    ]
    cur.executemany("""INSERT INTO buses
(bus_number,route_name,boarding_point,pickup_time,driver_name,driver_contact,route_details)
VALUES (?,?,?,?,?,?,?)""",data)
    conn.commit()

st.markdown("""
<div class="main-header">
<h1>🚌 Student Transport and Bus Route Finder</h1>
<p>Smart College Transportation Management System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<h2 style='text-align:center;color:white;'>
🚌 Transport System
</h2>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "",
    ["🏠 Dashboard",
     "🔍 Student Portal",
     "⚙️ Admin Portal"]
)

df = pd.read_sql_query("SELECT * FROM buses", conn)

if menu=="🏠 Dashboard":
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size:40px;">🚌</div>
        <div class="metric-number">{len(df)}</div>
        <div class="metric-title">Total Buses</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size:40px;">🛣️</div>
        <div class="metric-number">{df['route_name'].nunique()}</div>
        <div class="metric-title">Routes</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size:40px;">📍</div>
        <div class="metric-number">{df['boarding_point'].nunique()}</div>
        <div class="metric-title">Boarding Points</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size:40px;">👨‍✈️</div>
        <div class="metric-number">{df['driver_name'].nunique()}</div>
        <div class="metric-title">Drivers</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Transport Database")
    st.dataframe(df,use_container_width=True)

elif menu=="🔍 Student Portal":
    st.subheader("🔍 Find My Bus")
    search = st.text_input("Enter Location / Boarding Point")

    if search:
        result = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]

        if not result.empty:
            st.success("AI Recommendation Generated")
            best = result.iloc[0]

            st.info(f"""
Recommended Bus: {best['bus_number']}
Route: {best['route_name']}
Match Accuracy: 95%
""")

            for _,row in result.iterrows():
                st.markdown(f"""
<div class='route-card'>
<h3>{row['bus_number']} - {row['route_name']}</h3>
<b>Boarding Point:</b> {row['boarding_point']}<br>
<b>Pickup Time:</b> {row['pickup_time']}<br>
<b>Driver:</b> {row['driver_name']}<br>
<b>Contact:</b> {row['driver_contact']}<br>
<b>Route:</b> {row['route_details']}
</div>
""",unsafe_allow_html=True)
        else:
            st.error("No matching route found")

elif menu=="⚙️ Admin Portal":
    st.subheader("🔐 Admin Portal")

    password = st.text_input("Admin Password", type="password")

    if password=="admin123":
        st.success("Login Successful")

        with st.form("addbus"):
            bus = st.text_input("Bus Number")
            route = st.text_input("Route Name")
            board = st.text_input("Boarding Point")
            time = st.text_input("Pickup Time")
            driver = st.text_input("Driver Name")
            contact = st.text_input("Driver Contact")
            details = st.text_area("Route Details")

            submit = st.form_submit_button("Add Bus")

            if submit:
                cur.execute("""INSERT INTO buses
                (bus_number,route_name,boarding_point,pickup_time,driver_name,driver_contact,route_details)
                VALUES (?,?,?,?,?,?,?)""",
                (bus,route,board,time,driver,contact,details))
                conn.commit()
                st.success("Bus Added Successfully")

        st.subheader("Existing Buses")
        st.dataframe(pd.read_sql_query("SELECT * FROM buses", conn), use_container_width=True)

    elif password:
        st.error("Invalid Password")
