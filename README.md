# PulsePoint Health

A role-based smart hospital management platform built with Python and Streamlit.

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Install dependencies: `python -m pip install -r requirements.txt`
4. Start the application: `python -m streamlit run app.py`

## Included capabilities
- Separate Patient, Doctor, and Administrator workspaces
- Appointment request, schedule viewing, and status management
- Patient prescription, lab report, and billing views
- Doctor patient-record view and consultation-note entry
- Patient feedback capture with sentiment categorization
- Administrator appointment, directory, and feedback analytics
- Custom PulsePoint Health branding and a simplified application toolbar

## Technical notes
This is an early-stage portfolio project. The current version uses fictional sample records and Streamlit session state; records are not persisted to a database. Sign-in is a role-based interface flow and is not backed by production authentication. The feedback sentiment feature uses a simple keyword baseline and should not be represented as a trained or clinically validated model. Appointment and billing workflows are not connected to hospital systems or payment services.

The application is for software demonstration and learning, not for clinical use or handling real patient data.
