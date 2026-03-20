import streamlit as st
import datetime

if "users" not in st.session_state:
    st.session_state["users"] = {}

if "announcements" not in st.session_state:
    st.session_state["announcements"] = []

if "comments" not in st.session_state:
    st.session_state["comments"] = {}

ALAs = [f"ALA {i}" for i in range(1, 11)]
sections = [f"{i}-Section" for i in range(7, 13)]

st.title("PSHS Announcement System")

menu = st.selectbox("Menu", ["Login", "Sign Up", "Check Account"])

# SIGN UP
if menu == "Sign Up":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "admin"])

    if role == "student":
        grade_section = st.selectbox("Grade & Section", sections)
        student_type = st.selectbox("Type", ["student", "batch officer-1", "batch officer-2"])
    else:
        advisor_sections = st.multiselect("Advisory Sections", sections)
        advises_ala = st.selectbox("Do you advise an ALA?", ["No", "Yes"])
        if advises_ala == "Yes":
            ala_choice_admin = st.selectbox("ALA", ALAs)
        else:
            ala_choice_admin = None

    ala = st.selectbox("Choose ALA", ALAs)
    position = st.selectbox("Position", ["Member", "President"])

    if st.button("Sign Up"):
        if email in st.session_state["users"]:
            st.error("User already exists")
        else:
            st.session_state["users"][email] = {
                "password": password,
                "role": role,
                "ala": ala,
                "position": position
            }
            st.session_state["user"] = email
            st.success("Account created and logged in!")

# LOGIN
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.session_state["users"]

        if email in users and users[email]["password"] == password:
            st.session_state["user"] = email
            st.success("Login successful")
        else:
            st.error("Invalid login")

# CHECK ACCOUNT
elif menu == "Check Account":
    st.subheader("Check Account")

    check_email = st.text_input("Enter email")

    if st.button("Check"):
        if check_email in st.session_state["users"]:
            user = st.session_state["users"][check_email]
            st.write("Role:", user["role"])
            st.write("ALA:", user["ala"])
            st.write("Position:", user["position"])
        else:
            st.error("Account not found")

# MAIN SYSTEM
if "user" in st.session_state:
    email = st.session_state["user"]
    user = st.session_state["users"][email]

    st.subheader(f"Welcome {email}")

    filter_org = st.selectbox("Filter by ALA", ["All"] + ALAs)
    filter_category = st.selectbox("Filter by Category", ["All", "Text", "QR", "Links"])

    if user["role"] == "admin" or user["position"] == "President":
        st.subheader("Create Announcement")

        title = st.text_input("Title")
        content = st.text_area("Content")
        category = st.selectbox("Category", ["Text", "QR", "Links", "All"])
        expiry = st.date_input("Expiry Date")

        if st.button("Post"):
            st.session_state["announcements"].append({
                "title": title,
                "content": content,
                "category": category,
                "ala": user["ala"],
                "date": datetime.date.today(),
                "expiry": expiry
            })
            st.success("Posted")

    st.subheader("Announcements")

    for i, ann in enumerate(st.session_state["announcements"]):

        if (filter_org == "All" or ann["ala"] == filter_org) and \
           (filter_category == "All" or ann["category"] == filter_category):

            st.write("###", ann["title"])
            st.write(ann["content"])
            st.write("ALA:", ann["ala"])
            st.write("Category:", ann["category"])

            if i not in st.session_state["comments"]:
                st.session_state["comments"][i] = []

            comment = st.text_input("Comment", key=str(i))

            if st.button("Submit", key="btn" + str(i)):
                st.session_state["comments"][i].append(comment)

            for c in st.session_state["comments"][i]:
                st.write("-", c)

            st.write("---")
