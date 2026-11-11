import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="PulsePoint Health", page_icon="✚", layout="wide")
st.set_option("client.toolbarMode", "viewer")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#F4F7FA;color:#183044}
.block-container{padding-top:2.5rem!important;max-width:1400px}
header[data-testid="stHeader"],div[data-testid="stToolbar"],#MainMenu,footer,.stDeployButton{display:none!important;visibility:hidden!important;height:0!important}
[data-testid="stDecoration"]{display:none!important}
[data-testid="stSidebar"]{background:#102B46}
[data-testid="stSidebar"] *{color:#F5FAFC}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:#102B46}
.brand{font-family:'Manrope';font-weight:800;font-size:24px;color:#102B46}
.brand span{color:#18A999}
.hero{padding:27px 30px;border-radius:18px;background:linear-gradient(115deg,#102B46,#174968 72%,#167C79);color:white;margin-bottom:20px}
.hero small{color:#80E0D2;letter-spacing:2px;font-weight:700}
.hero h1{color:white!important;font-size:30px;margin:7px 0}
.hero p{color:#D7E7EF;margin:0}
.metric{background:white;border:1px solid #E4EBF0;border-radius:15px;padding:17px;min-height:105px}
.metric label{font-size:11px;color:#718096;font-weight:700}
.metric strong{display:block;font-family:'Manrope';font-size:27px;color:#102B46;margin-top:5px}
.metric em{font-size:11px;color:#18A999;font-style:normal}
.panel{background:white;border:1px solid #E4EBF0;border-radius:15px;padding:19px;margin-bottom:15px}
.panel h3{font-size:17px;margin:0 0 12px}
div.stButton>button[kind="primary"]{background:#18A999;border:0;border-radius:9px;color:white;font-weight:700}
div.stButton>button{border-radius:9px}
.stTextInput input,.stTextArea textarea{border-radius:9px}
.login-card{background:white;border:1px solid #E4EBF0;border-radius:20px;padding:28px;box-shadow:0 12px 35px #102b4610}
.footer{text-align:center;color:#8A99A6;font-size:11px;padding:20px}
</style>
""", unsafe_allow_html=True)

# Demo-only data stored in Streamlit session; it resets when the session restarts.
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {"Reference":"PP-1001","Patient":"Aarav Mehta","Doctor":"Dr. Ananya Rao","Department":"Cardiology","Date":date.today()+timedelta(days=1),"Time":"10:30 AM","Status":"Confirmed"},
        {"Reference":"PP-1002","Patient":"Diya Sharma","Doctor":"Dr. Kabir Sen","Department":"Dermatology","Date":date.today()+timedelta(days=2),"Time":"12:00 PM","Status":"Pending"},
        {"Reference":"PP-1003","Patient":"Rohan Das","Doctor":"Dr. Ananya Rao","Department":"Cardiology","Date":date.today()-timedelta(days=3),"Time":"11:00 AM","Status":"Completed"},
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = [
        {"Patient":"Aarav Mehta","Feedback":"The doctor was attentive and explained everything clearly.","Sentiment":"Positive","Date":date.today()},
        {"Patient":"Diya Sharma","Feedback":"I waited for almost an hour. The process was frustrating.","Sentiment":"Negative","Date":date.today()},
        {"Patient":"Rohan Das","Feedback":"The appointment was fine overall.","Sentiment":"Neutral","Date":date.today()},
    ]
if "prescriptions" not in st.session_state:
    st.session_state.prescriptions = [
        {"Date":date.today()-timedelta(days=3),"Doctor":"Dr. Ananya Rao","Department":"Cardiology","Summary":"Follow-up consultation advised in two weeks."},
        {"Date":date.today()-timedelta(days=20),"Doctor":"Dr. Kabir Sen","Department":"Dermatology","Summary":"Review consultation completed."},
    ]

def sentiment(text):
    # Transparent keyword baseline for the MVP; upgrade to a trained NLP model later.
    positive = ["good","great","excellent","helpful","attentive","clear","clean","quick","friendly","satisfied","comfortable","smooth"]
    negative = ["bad","poor","wait","waiting","late","frustrat","rude","dirty","worst","slow","issue","problem","unhappy"]
    s = text.lower()
    p = sum(w in s for w in positive); n = sum(w in s for w in negative)
    return "Positive" if p > n else "Negative" if n > p else "Neutral"

def hero(kicker, title, subtitle):
    st.markdown(f'<div class="hero"><small>{kicker}</small><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def metric(label, value, note):
    st.markdown(f'<div class="metric"><label>{label}</label><strong>{value}</strong><em>{note}</em></div>', unsafe_allow_html=True)

def table(rows):
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# Login
if not st.session_state.logged_in:
    st.markdown('<div class="brand">✚ PulsePoint <span>HEALTH</span></div>', unsafe_allow_html=True)
    left,right=st.columns([1.05,1],gap="large")
    with left:
        st.markdown("""<div class="hero" style="min-height:360px;padding:34px">
        <small>CONNECTED CARE. SIMPLIFIED.</small>
        <h1 style="font-size:36px;margin-top:22px">Healthcare that<br>moves with you.</h1>
        <p style="font-size:15px;line-height:1.7;margin-top:16px">One connected experience for patients, clinicians and hospital teams — designed around better care and simpler operations.</p>
        <div style="margin-top:65px;color:#9DD8D5;font-size:12px;font-weight:700;letter-spacing:1.5px">SMARTER CARE. BETTER OUTCOMES.</div></div>""",unsafe_allow_html=True)
        st.caption("Smart Hospital Management Platform · Smarter Care. Better Outcomes.")
    with right:
        st.markdown('<div class="login-card">',unsafe_allow_html=True)
        st.subheader("Welcome to PulsePoint")
        st.caption("Choose your workspace to continue.")
        role=st.selectbox("Sign in as",["Patient","Doctor","Administrator"])
        defaults={"Patient":"aarav.mehta@pulsepointhealth.com","Doctor":"ananya.rao@pulsepointhealth.com","Administrator":"admin@pulsepointhealth.com"}
        email=st.text_input("Email address",value=defaults[role])
        st.text_input("Password",type="password",value="pulse123")
        st.caption("Select your workspace and enter your account details to continue.")
        if st.button("Sign in  →",type="primary",use_container_width=True):
            st.session_state.logged_in=True
            st.session_state.role=role
            st.session_state.name={"Patient":"Aarav Mehta","Doctor":"Dr. Ananya Rao","Administrator":"Hospital Admin"}[role]
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 PulsePoint Health · Smarter Care. Better Outcomes.</div>',unsafe_allow_html=True)
    st.stop()

role=st.session_state.role
name=st.session_state.name
with st.sidebar:
    st.markdown("## ✚ PulsePoint")
    st.markdown("<small style='color:#80E0D2;letter-spacing:2px'>HEALTH</small>",unsafe_allow_html=True)
    st.divider()
    st.caption(f"SIGNED IN AS · {role.upper()}")
    st.write(f"**{name}**")
    st.divider()
    menus={
        "Patient":["Overview","Book appointment","My appointments","Medical records","Billing","Feedback"],
        "Doctor":["Overview","My schedule","Patient records","Write prescription"],
        "Administrator":["Overview","Appointments","People","Feedback & insights","Operations"]
    }
    page=st.radio("NAVIGATION",menus[role],label_visibility="collapsed")
    st.divider()
    st.markdown("<small style='color:#B7C9D5'>Here for your health journey.</small>", unsafe_allow_html=True)
    if st.button("Sign out",use_container_width=True):
        st.session_state.logged_in=False
        st.rerun()

# Patient portal
if role=="Patient":
    if page=="Overview":
        hero("PATIENT PORTAL",f"Good day, {name.split()[0]}.","Your appointments, health records and care journey in one place.")
        own=[a for a in st.session_state.appointments if a["Patient"]==name and a["Date"]>=date.today() and a["Status"]!="Cancelled"]
        a,b,c,d=st.columns(4)
        with a: metric("UPCOMING APPOINTMENTS",len(own),"Your next care touchpoint")
        with b: metric("PRESCRIPTIONS",len(st.session_state.prescriptions),"Available in your records")
        with c: metric("PENDING BILLS","₹1,250","Outstanding invoices")
        with d: metric("LAB REPORTS","03","Reports available")
        x,y=st.columns([1.35,.8])
        with x:
            st.markdown('<div class="panel"><h3>Upcoming appointments</h3>',unsafe_allow_html=True)
            table(own if own else [{"Message":"No upcoming appointments"}])
            st.markdown('</div>',unsafe_allow_html=True)
        with y:
            st.markdown('<div class="panel"><h3>Quick actions</h3>',unsafe_allow_html=True)
            st.write("Use the navigation to book a consultation, review a prescription or share your experience.")
            st.markdown('</div>',unsafe_allow_html=True)
    elif page=="Book appointment":
        hero("CARE, ON YOUR SCHEDULE","Book an appointment","Choose a department, clinician and convenient time.")
        with st.form("booking"):
            c1,c2=st.columns(2)
            with c1:
                dept=st.selectbox("Department",["Cardiology","Dermatology","General Medicine","Orthopaedics","Paediatrics"])
                doctors={"Cardiology":["Dr. Ananya Rao","Dr. Vikram Iyer"],"Dermatology":["Dr. Kabir Sen","Dr. Meera Nair"],"General Medicine":["Dr. Riya Kapoor"],"Orthopaedics":["Dr. Arjun Bose"],"Paediatrics":["Dr. Neha Shah"]}
                doc=st.selectbox("Doctor",doctors[dept])
                appt_date=st.date_input("Preferred date",value=date.today()+timedelta(days=1),min_value=date.today())
            with c2:
                slot=st.selectbox("Available time",["09:30 AM","10:30 AM","11:30 AM","12:00 PM","02:00 PM","03:30 PM","04:30 PM"])
                reason=st.text_area("Reason for visit",placeholder="Briefly describe the reason for your consultation")
            if st.form_submit_button("Request appointment",type="primary",use_container_width=True):
                st.session_state.appointments.append({"Reference":f"PP-{1001+len(st.session_state.appointments)}","Patient":name,"Doctor":doc,"Department":dept,"Date":appt_date,"Time":slot,"Status":"Pending"})
                st.success("Your appointment request has been submitted successfully and is pending confirmation.")
    elif page=="My appointments":
        hero("YOUR CARE CALENDAR","My appointments","Track upcoming consultations and revisit past appointments.")
        own=[a for a in st.session_state.appointments if a["Patient"]==name]
        table(own if own else [{"Message":"No appointments found"}])
    elif page=="Medical records":
        hero("YOUR HEALTH, ORGANIZED","Medical records","A convenient view of prescriptions, reports and visit history.")
        t1,t2,t3=st.tabs(["Prescriptions","Lab reports","Visit history"])
        with t1: table(st.session_state.prescriptions)
        with t2:
            table([{"Report":"Complete Blood Count","Date":date.today()-timedelta(days=8),"Status":"Available"},{"Report":"Lipid Profile","Date":date.today()-timedelta(days=20),"Status":"Available"},{"Report":"Vitamin D","Date":date.today()-timedelta(days=20),"Status":"Available"}])

        with t3: table([{"Date":date.today()-timedelta(days=3),"Doctor":"Dr. Ananya Rao","Department":"Cardiology","Visit":"Consultation"}])
    elif page=="Billing":
        hero("TRANSPARENT & SIMPLE","Billing and payments","Review your hospital bills and payment status.")
        a,b=st.columns(2)
        with a: metric("OUTSTANDING BALANCE","₹1,250","Invoices awaiting payment")
        with b: metric("LAST PAYMENT","₹850","Most recent payment")
        table([{"Invoice":"INV-2041","Description":"Cardiology consultation","Amount":"₹850","Status":"Paid"},{"Invoice":"INV-2098","Description":"Diagnostic services","Amount":"₹1,250","Status":"Pending"}])

    elif page=="Feedback":
        hero("YOUR VOICE MATTERS","Share your experience","Your feedback helps improve every care interaction.")
        with st.form("feedback"):
            rating=st.select_slider("Rate your experience",["Poor","Fair","Good","Very good","Excellent"],value="Good")
            comment=st.text_area("Your feedback",placeholder="Tell us about your visit, staff, facilities or waiting time...")
            if st.form_submit_button("Submit feedback",type="primary"):
                if comment.strip():
                    label=sentiment(comment)
                    st.session_state.feedback.append({"Patient":name,"Feedback":comment,"Sentiment":label,"Date":date.today()})
                    st.success(f"Thank you for your feedback. We classified it as {label.lower()}.")
                else: st.warning("Please enter feedback before submitting.")

# Doctor portal
elif role=="Doctor":
    if page=="Overview":
        hero("CLINICIAN WORKSPACE","Good day, Dr. Rao.","A clear view of consultations and patient care activities.")
        schedule=[a for a in st.session_state.appointments if a["Doctor"]==name and a["Date"]>=date.today()]
        a,b,c=st.columns(3)
        with a: metric("UPCOMING CONSULTATIONS",len(schedule),"Assigned to your schedule")
        with b: metric("PATIENTS SEEN",sum(1 for item in st.session_state.appointments if item["Doctor"]==name and item["Status"]=="Completed"),"Completed consultations")
        with c: metric("PENDING NOTES",0,"No notes awaiting completion")
        st.markdown('<div class="panel"><h3>Upcoming schedule</h3>',unsafe_allow_html=True)
        table(schedule if schedule else [{"Message":"No upcoming consultations"}])
        st.markdown('</div>',unsafe_allow_html=True)
    elif page=="My schedule":
        hero("CLINICIAN WORKSPACE","My schedule","Review assigned patient consultations.")
        rows=[a for a in st.session_state.appointments if a["Doctor"]==name]
        table(rows if rows else [{"Message":"No appointments assigned"}])
    elif page=="Patient records":
        hero("PATIENT CONTEXT","Patient records","Review patient profiles and visit context.")
        patient=st.selectbox("Select patient",["Aarav Mehta","Diya Sharma","Rohan Das"])
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.subheader(patient)
        st.write("Patient ID: PP-P-1001  ·  Age: 42  ·  Blood group: O+")
        st.write("Allergies: Not recorded.")

        st.markdown('</div>',unsafe_allow_html=True)
    elif page=="Write prescription":
        hero("CLINICAL DOCUMENTATION","Consultation note","Document a consultation and prepare prescription instructions.")
        with st.form("rx"):
            patient=st.selectbox("Patient",["Aarav Mehta","Diya Sharma","Rohan Das"])
            summary=st.text_input("Consultation summary")
            instructions=st.text_area("Prescription instructions")
            if st.form_submit_button("Save draft",type="primary"):
                if summary.strip() and instructions.strip():
                    st.session_state.prescriptions.append({"Date":date.today(),"Doctor":name,"Department":"Consultation","Summary":f"{patient}: {summary}. {instructions}"})
                    st.success("Consultation note saved successfully.")
                else: st.warning("Complete both fields.")

# Administrator portal
else:
    if page=="Overview":
        hero("HOSPITAL COMMAND CENTRE","Operational overview","A consolidated view of appointments and patient experience.")
        fb=st.session_state.feedback; ap=st.session_state.appointments
        a,b,c,d=st.columns(4)
        with a: metric("TOTAL APPOINTMENTS",len(ap),"Appointments recorded")
        with b: metric("ACTIVE DOCTORS",7,"Across care departments")
        with c: metric("FEEDBACK RECEIVED",len(fb),"Feedback submissions")
        with d: metric("NEGATIVE FEEDBACK",sum(x["Sentiment"]=="Negative" for x in fb),"Flagged for review")
        x,y=st.columns(2)
        with x:
            st.markdown('<div class="panel"><h3>Appointment status</h3>',unsafe_allow_html=True)
            st.bar_chart(pd.Series([a["Status"] for a in ap]).value_counts())
            st.markdown('</div>',unsafe_allow_html=True)
        with y:
            st.markdown('<div class="panel"><h3>Feedback sentiment</h3>',unsafe_allow_html=True)
            st.bar_chart(pd.Series([f["Sentiment"] for f in fb]).value_counts())
            st.markdown('</div>',unsafe_allow_html=True)
    elif page=="Appointments":
        hero("SCHEDULING OPERATIONS","Appointment management","Review and update appointment requests.")
        table(st.session_state.appointments)
        refs=[a["Reference"] for a in st.session_state.appointments]
        chosen=st.selectbox("Select appointment reference",refs)
        status=st.selectbox("Update status",["Pending","Confirmed","Completed","Cancelled"])
        if st.button("Save status update",type="primary"):
            for a in st.session_state.appointments:
                if a["Reference"]==chosen: a["Status"]=status
            st.success("Appointment status updated successfully.")
    elif page=="People":
        hero("PEOPLE & ACCESS","Hospital directory","Manage patient and clinician directory information.")
        table([{"Name":"Aarav Mehta","Role":"Patient","Department":"—","Access":"Active"},{"Name":"Dr. Ananya Rao","Role":"Doctor","Department":"Cardiology","Access":"Active"},{"Name":"Dr. Kabir Sen","Role":"Doctor","Department":"Dermatology","Access":"Active"},{"Name":"Hospital Admin","Role":"Administrator","Department":"Operations","Access":"Active"}])

    elif page=="Feedback & insights":
        hero("VOICE OF THE PATIENT","Feedback & insights","Review patient sentiment and identify service recovery opportunities.")
        fb=st.session_state.feedback
        counts=pd.Series([f["Sentiment"] for f in fb]).value_counts()
        a,b,c=st.columns(3)
        with a: metric("POSITIVE",int(counts.get("Positive",0)),"Feedback entries")
        with b: metric("NEUTRAL",int(counts.get("Neutral",0)),"Feedback entries")
        with c: metric("NEGATIVE",int(counts.get("Negative",0)),"Review recommended")
        table(fb)

    elif page=="Operations":
        hero("HOSPITAL OPERATIONS","Operations snapshot","A lightweight view of service capacity and administrative indicators.")
        departments=["Cardiology","Dermatology","General Medicine","Orthopaedics","Paediatrics"]
        clinicians=["Dr. Ananya Rao","Dr. Vikram Iyer","Dr. Kabir Sen","Dr. Meera Nair","Dr. Riya Kapoor","Dr. Arjun Bose","Dr. Neha Shah"]
        a,b,c=st.columns(3)
        with a: metric("DEPARTMENTS",len(departments),"Care services")
        with b: metric("CLINICIANS",len(clinicians),"Across departments")
        with c: metric("APPOINTMENTS",len(st.session_state.appointments),"In the schedule")
        st.markdown('<div class="panel"><h3>Department directory</h3>',unsafe_allow_html=True)
        table([{"Department":department,"Service":"Available"} for department in departments])
        st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="footer">PulsePoint Health · Smarter Care. Better Outcomes.</div>',unsafe_allow_html=True)
