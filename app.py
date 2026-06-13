import streamlit as st
from pdf import PDF
from datetime import date
import pycountry
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Gillani AI Resume Studio Pro",
    page_icon="💼",
    layout="centered"
)

# ================= UI STYLE =================
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

.stButton>button {
    background-color: #22c55e;
    color: black !important;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("💼 Gillani AI Resume Studio Pro")
st.markdown("### Professional AI CV Builder (Stable Version)")
st.divider()

# ================= PHOTO =================
photo = st.file_uploader("📸 Upload Profile Photo", type=["jpg", "png"])

# ================= PERSONAL INFO =================
st.header("👤 Personal Information")

name = st.text_input("Complete Name")
job = st.text_input("Desired Job Position")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

countries = sorted([c.name for c in pycountry.countries])
nationality = st.selectbox("Nationality", countries)

gender = st.selectbox("Gender", ["Male", "Female", "Other"])
marital = st.selectbox("Marital Status", ["Single", "Married", "Other"])

dob = st.date_input("Date of Birth", min_value=date(1960,1,1))

st.divider()

# ================= EDUCATION =================
st.header("🎓 Education")

degree = st.selectbox(
    "Degree",
    ["Matric", "Intermediate", "Diploma", "Bachelor", "Master", "MPhil", "PhD", "Other"]
)

edu_school = st.text_input("Institute / University")
edu_start = st.date_input("Start Date (Education)", key="edu_start")
edu_end = st.date_input("End Date (Education)", key="edu_end")

st.divider()

# ================= EXPERIENCE =================
st.header("💼 Experience")

position = st.text_input("Position")
employer = st.text_input("Employer")
city = st.text_input("City")

exp_start = st.date_input("Start Date (Job)", key="exp_start")
exp_end = st.date_input("End Date (Job)", key="exp_end")

st.divider()

# ================= SKILLS =================
st.header("🛠 Skills")

skills = st.multiselect(
    "Select Skills",
    ["Communication", "Leadership", "Teamwork", "Problem Solving",
     "Python", "Excel", "Data Entry", "Marketing",
     "Sales", "Customer Service", "Design", "Writing"]
)

st.divider()

# ================= LANGUAGES =================
st.header("🌍 Languages")

languages = st.multiselect(
    "Select Languages",
    ["Urdu", "English", "Punjabi", "Hindi",
     "Arabic", "French", "German", "Spanish"]
)

st.divider()

# ================= SUMMARY =================
summary = f"{name} is a professional skilled in {', '.join(skills)} with experience in {position}. Strong background in {degree} education."

# ================= CV PREVIEW =================
if st.button("🚀 Generate CV Preview"):

    st.subheader("📄 CV Preview")

    st.markdown(f"""
# {name}
### {job}

📧 {email} | 📱 {phone}  
🌍 {nationality} | 🎂 {dob}  
👤 {gender} | {marital}

---

## 🎯 Summary
{summary}

---

## 🎓 Education
{degree} - {edu_school}  
{edu_start} to {edu_end}

---

## 💼 Experience
{position} - {employer} ({city})  
{exp_start} to {exp_end}

---

## 🛠 Skills
{", ".join(skills)}

---

## 🌍 Languages
{", ".join(languages)}
""")

    st.success("CV Generated Successfully 🚀")

# ================= PDF GENERATION (FIXED) =================
if st.button("📄 Download CV PDF"):

    pdf = PDF()
    pdf.add_page()

    # TITLE
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "GILLANI AI RESUME STUDIO PRO", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Professional AI Generated CV", ln=True)
    pdf.ln(5)

    # PHOTO
    if photo is not None:
        image_path = "temp.jpg"
        with open(image_path, "wb") as f:
            f.write(photo.read())
        pdf.image(image_path, x=160, y=10, w=40)

    # INFO
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "PERSONAL INFORMATION", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f"Name: {name}", ln=True)
    pdf.cell(200, 8, f"Job: {job}", ln=True)
    pdf.cell(200, 8, f"Email: {email}", ln=True)
    pdf.cell(200, 8, f"Phone: {phone}", ln=True)
    pdf.cell(200, 8, f"Nationality: {nationality}", ln=True)

    pdf.ln(3)

    # SUMMARY
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "SUMMARY", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, summary)

    pdf.ln(3)

    # EDUCATION
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "EDUCATION", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f"{degree} - {edu_school}", ln=True)
    pdf.cell(200, 8, f"{edu_start} to {edu_end}", ln=True)

    pdf.ln(3)

    # EXPERIENCE
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "EXPERIENCE", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f"{position} - {employer}", ln=True)
    pdf.cell(200, 8, f"{city}", ln=True)
    pdf.cell(200, 8, f"{exp_start} to {exp_end}", ln=True)

    pdf.ln(3)

    # SKILLS
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "SKILLS", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, ", ".join(skills))

    pdf.ln(3)

    # LANGUAGES
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "LANGUAGES", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, ", ".join(languages))

    pdf.output("cv.pdf")

    st.success("Professional CV PDF Generated Successfully 🚀")
