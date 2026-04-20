import streamlit as st
import datetime

if "users" not in st.session_state:
    st.session_state["users"] = {}

if "announcements" not in st.session_state:
    st.session_state["announcements"] = []

if "comments" not in st.session_state:
    st.session_state["comments"] = {}

if "user" not in st.session_state:
    st.session_state["user"] = None

ALAs = [
    "chemyun", "Suga", "Pisay math circle", "Sikatala", "Pisayaw", 
    "Debate", "Musikanta", "Rondalla", "Hobbyists", "Echo"
]

sections = [
    "7-EMERALD", "7-RUBY", "7-DIAMOND",
    "8-CAMIA", "8-SAMPAGUITA", "8-JASMINE",
    "9-SODIUM", "9-RUBIDIUM", "9-POTASSIUM",
    "10-PROTON", "10-NEUTRON", "10-ELECTRON",
    "11-A", "11-B", "11-C",
    "12-A", "12-B", "12-C"
]

batch_officers = [
    "Student", "President", "Vice President", "Secretary", 
    "Treasurer", "Auditor", "Peace Officers"
]
# -----------------------------

st.title("PSHS Announcement System")

menu = st.selectbox("Menu", ["Login", "Sign Up", "Check Account"])

if menu == "Sign Up":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "admin"])

    grade_section = None
    advisor_sections = []
    ala_choice_admin = None

    if role == "student":
        grade_section = st.selectbox("Grade & Section", sections)
        student_type = st.selectbox("Type", batch_officers)
    else:
        advisor_sections = st.multiselect("Advisory Sections", sections)
        advises_ala = st.selectbox("Do you advise an ALA?", ["No", "Yes"])
        if advises_ala == "Yes":
            ala_choice_admin = st.selectbox("ALA", ALAs)

    ala = st.selectbox("Choose ALA", ALAs)
    position = st.selectbox("Position", ["Member", "President"])

    if st.button("Sign Up"):
        if not email.strip():
            st.error("Email cannot be empty.")
        elif not password.strip():
            st.error("Password cannot be empty.")
        elif email in st.session_state["users"]:
            st.error("User already exists.")
        else:
            st.session_state["users"][email] = {
                "password": password,
                "role": role,
                "ala": ala,
                "position": position,
                "grade_section": grade_section,
                "advisory_sections": advisor_sections,
                "ala_advised": ala_choice_admin
            }
            st.session_state["user"] = email
            st.success("Account created and logged in!")

elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email.strip() or not password.strip():
            st.error("Please fill in all fields.")
        elif email in st.session_state["users"] and st.session_state["users"][email]["password"] == password:
            st.session_state["user"] = email
            st.success("Login successful")
        else:
            st.error("Invalid login")

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

if st.session_state["user"]:
    email = st.session_state["user"]
    user = st.session_state["users"][email]

    st.subheader(f"Welcome {email}")

    st.subheader("User Profiles")

    all_users = list(st.session_state["users"].keys())
    if all_users:
        selected_user = st.selectbox("View Profile", all_users)
        profile = st.session_state["users"][selected_user]

        st.write("Email:", selected_user)
        st.write("Role:", profile["role"])
        st.write("ALA:", profile["ala"])
        st.write("Position:", profile["position"])

        if profile["role"] == "student":
            st.write("Section:", profile["grade_section"])
        else:
            st.write("Advisory Sections:", profile["advisory_sections"])
            st.write("ALA Advised:", profile["ala_advised"])

    today = datetime.date.today()

    st.session_state["announcements"] = [
        ann for ann in st.session_state["announcements"]
        if ann["expiry"] >= today
    ]

    st.subheader("Announcements")

    view_mode = st.selectbox(
        "View announcements from",
        ["All Users"] + list(st.session_state["users"].keys())
    )

    filter_org = st.selectbox("Filter by ALA", ["All"] + ALAs)
    filter_category = st.selectbox("Filter by Category", ["All", "Text", "QR", "Links"])

    if user["role"] == "admin" or user["position"] == "President":
        st.subheader("Create Announcement")

        title = st.text_input("Title")
        content = st.text_area("Content")
        category = st.selectbox("Category", ["Text", "QR", "Links"])
        expiry = st.date_input("Expiry Date")

        if st.button("Post"):
            if not title.strip():
                st.error("Title cannot be empty.")
            elif not content.strip():
                st.error("Content cannot be empty.")
            elif expiry < today:
                st.error("Expiry date cannot be in the past.")
            else:
                st.session_state["announcements"].append({
                    "title": title,
                    "content": content,
                    "category": category,
                    "ala": user["ala"],
                    "date": today,
                    "expiry": expiry,
                    "author": email
                })
                st.success("Posted successfully!")
                st.rerun()

    for i, ann in enumerate(st.session_state["announcements"]):

        if view_mode != "All Users" and ann.get("author") != view_mode:
            continue

        if (filter_org == "All" or ann["ala"] == filter_org) and \
           (filter_category == "All" or ann["category"] == filter_category):

            st.write(f"### {ann['title']}")
            st.write(ann["content"])
            st.write("Posted by:", ann.get("author", "Unknown"))
            st.write("ALA:", ann["ala"])
            st.write("Category:", ann["category"])
            st.write("Expires on:", ann["expiry"])

            if i not in st.session_state["comments"]:
                st.session_state["comments"][i] = []

            comment = st.text_input("Add comment", key=f"comment_{i}")

            if st.button("Submit", key=f"btn_{i}"):
                if comment.strip():
                    st.session_state["comments"][i].append(comment)
                    st.rerun()
                else:
                    st.warning("Comment cannot be empty.")

            for c in st.session_state["comments"][i]:
                st.write(f"- {c}")

            st.write("---")
