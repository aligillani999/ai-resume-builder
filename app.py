import reportlab
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date
import pycountry

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Gillani AI Resume Studio Pro",
    page_icon="💼",
    layout="centered"
)

# ================= UI STYLE FIX =================
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

/* Buttons text fix (IMPORTANT) */
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
st.markdown("### Professional AI CV Builder (Fixed Version)")
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

# ================= PDF GENERATION =================
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def write_line(c, text, x, y, max_width=90):
    """
    Safe text writer (prevents overflow)
    """
    lines = []
    words = text.split(" ")
    current = ""

    for word in words:
        if len(current + " " + word) < max_width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)

    for line in lines:
        c.drawString(x, y, line.strip())
        y -= 15

    return y


if st.button("📄 Download CV PDF"):

    c = canvas.Canvas("cv.pdf", pagesize=A4)
    width, height = A4

    x = 50
    y = height - 50

    # ================= HEADER =================
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "GILLANI AI RESUME STUDIO PRO")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(x, y, "Professional AI Generated CV")
    y -= 40

    # ================= PHOTO =================
    if photo is not None:
        with open("temp.jpg", "wb") as f:
            f.write(photo.read())
        c.drawImage("temp.jpg", 420, height - 150, width=120, height=120)

    # ================= PERSONAL INFO =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "PERSONAL INFORMATION")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, f"Name: {name}", x, y)
    y = write_line(c, f"Job: {job}", x, y)
    y = write_line(c, f"Email: {email}", x, y)
    y = write_line(c, f"Phone: {phone}", x, y)
    y = write_line(c, f"Nationality: {nationality}", x, y)

    y -= 10

    # ================= SUMMARY =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "PROFESSIONAL SUMMARY")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, summary, x, y)

    y -= 10

    # ================= EDUCATION =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "EDUCATION")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, f"{degree} - {edu_school}", x, y)
    y = write_line(c, f"{edu_start} to {edu_end}", x, y)

    y -= 10

    # ================= EXPERIENCE =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "EXPERIENCE")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, f"{position} - {employer} ({city})", x, y)
    y = write_line(c, f"{exp_start} to {exp_end}", x, y)

    y -= 10

    # ================= SKILLS =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "SKILLS")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, ", ".join(skills), x, y)

    y -= 10

    # ================= LANGUAGES =================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "LANGUAGES")
    y -= 20

    c.setFont("Helvetica", 10)
    y = write_line(c, ", ".join(languages), x, y)

    c.save()

    st.success("Professional CV PDF Generated Successfully 🚀")
