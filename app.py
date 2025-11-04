import streamlit as st
import json
from firebase_admin import credentials, firestore, initialize_app
import pyrebase

# ✅ STREAMLIT CONFIG
st.set_page_config(page_title="Instagram Secure Login", page_icon="📸")

# ✅ LOAD FIREBASE WEB CONFIG
firebase_web_config = {
    "apiKey": st.secrets["firebase"]["api_key"],
    "authDomain": st.secrets["firebase"]["auth_domain"],
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": st.secrets["firebase"]["storage_bucket"],
    "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
    "appId": st.secrets["firebase"]["app_id"],
}

firebase = pyrebase.initialize_app(firebase_web_config)
auth = firebase.auth()

# ✅ LOAD FIRESTORE ADMIN SDK SERVICE ACCOUNT
firebase_service = json.loads(st.secrets["firebase"]["service_account"])
cred = credentials.Certificate(firebase_service)
initialize_app(cred)
db = firestore.client()

st.title("📸 Instagram Secure App")

menu = st.radio("Select Option:", ["Login", "Signup"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")


if menu == "Signup":
    if st.button("Create Account"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("✅ Account created successfully!")
        except Exception as e:
            st.error(f"❌ Failed: {e}")


elif menu == "Login":
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("✅ Login Successful!")

            # Example Firestore write action
            db.collection("logins").add({"email": email})

        except Exception as e:
            st.error(f"❌ Login Failed: {e}")
