import re

import streamlit as st 
import json 
from datetime import datetime 
 
# ---------------- DATA ---------------- 
version_float = 1.1 
 
questions = [
    {"q": "How often do you complete tasks before the deadline?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you start assignments early?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you delay tasks even when they are important?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How frequently do you work intensely right before deadlines?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you plan your work schedule in advance?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How well do you manage your time?",
     "opts": [("Very well",0),("Well",1),("Average",2),("Poorly",3),("Very poorly",4)]},

    {"q": "How often do you create to-do lists or schedules?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you underestimate how long tasks will take?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do distractions prevent you from completing tasks on time?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you feel overwhelmed by your responsibilities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How well do you sleep at night?",
     "opts": [("Very well",0),("Fairly well",1),("Occasionally restless",2),("Often restless",3),("Very poorly",4)]},

    {"q": "How do you usually feel when a deadline is approaching?",
     "opts": [("Calm",0),("Slightly stressed",1),("Moderately stressed",2),("Very stressed",3),("Extremely stressed",4)]},

    {"q": "How often do you feel guilty when you delay tasks?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Do you feel more productive under pressure?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you avoid tasks that seem difficult?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you lose motivation while working on tasks?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you complete tasks at the last minute?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you submit work late?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Do you prefer working steadily or in last-minute bursts?",
     "opts": [("Steadily",0),("Mostly steadily",1),("Mixed",2),("Mostly last-minute",3),("Always last-minute",4)]},

    {"q": "How satisfied are you with your productivity?",
     "opts": [("Very satisfied",0),("Satisfied",1),("Neutral",2),("Dissatisfied",3),("Very dissatisfied",4)]}
]

psych_states = {
    "Highly Organized & Low Stress": (0, 19),
    "Generally Stable": (20, 39),
    "Moderate Stress / Occasional Procrastination": (40, 59),
    "High Stress / Deadline Pressure": (60, 79),
    "Chronic Procrastination & Overwhelmed": (80, 100)
}
 
# ---------------- HELPERS ---------------- 
def validate_name(name: str) -> bool: 
    return len(name.strip()) > 0  
    
    import re

def validate_name(name):
    return bool(re.match(r"^[A-Za-z\s'-]+$", name)) 
 
def validate_dob(dob: str) -> bool: 
    try: 
        datetime.strptime(dob, "%Y-%m-%d") 
        return True 
    except: 
        return False 
 
def interpret_score(score: int) -> str: 
    for state, (low, high) in psych_states.items(): 
        if low <= score <= high: 
            return state 
    return "Unknown" 
 
def save_json(filename: str, data: dict): 
    with open(filename, "w", encoding="utf-8") as f: 
        json.dump(data, f, indent=2) 
 
# ---------------- STREAMLIT APP ---------------- 
st.set_page_config(page_title="Student Psychological Survey")

# 🎨 DESIGN (INSERT HERE)
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.stButton>button {
    background-color: #667eea;
    color: white;
    border-radius: 8px;
    padding: 10px;
}

.stButton>button:hover {
    background-color: #5a67d8;
}

h1, h2, h3 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("📙 Student Psychological Survey")
# Initialize session flag
if "survey_started" not in st.session_state:
    st.session_state.survey_started = False
# ----------------- START PAGE -----------------
st.info("Please fill out your details and answer all questions honestly.")
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")
 
# --- Start Survey --- 
if st.button("Start Survey"): 
 
    # Validate inputs 
    errors = [] 
    if not (len(name.strip()) > 0 and not any(c.isdigit() for c in name)):
        errors.append("Invalid given name.")
    if not (len(surname.strip()) > 0 and not any(c.isdigit() for c in surname)):
        errors.append("Invalid surname.")
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except:
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")
    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")
        # ✅ Set flag to True so next rerun knows we're inside the survey
        st.session_state.survey_started = True
        # Save user info in session
        st.session_state.user_info = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "sid": sid
        }
# ----------------- SURVEY PAGE -----------------
if st.session_state.survey_started:
    total_score = 0
    answers = []
    for idx, q in enumerate(questions):
        opt_labels = [opt[0] for opt in q["opts"]]
        choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
        score = next(score for label, score in q["opts"] if label == choice)
        total_score += score
        answers.append({
            "question": q["q"],
            "selected_option": choice,
            "score": score
        })
    if st.button("Submit Answers"):

      status = interpret_score(total_score)

    st.markdown(f"## ✅ Your Result: {status}")
    st.markdown(f"**Total Score:** {total_score}")

    record = {
        **st.session_state.user_info,
        "total_score": total_score,
        "result": status,
        "answers": answers,
        "version": version_float
    }

    json_filename = f"{st.session_state.user_info['sid']}_result.json"
    save_json(json_filename, record)

    st.success(f"Your results are saved as {json_filename}")

    st.download_button(
        "Download your result JSON",
        json.dumps(record, indent=2),
        file_name=json_filename
    )