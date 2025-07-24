import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate, hide_icons, hide_sidebar, remove_whitespaces
from connection import contract, w3

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()
load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")

def upload_to_pinata(file_path, api_key, api_secret):
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }
    
    with open(file_path, "rb") as file:
        file_data = file.read()
        file_name = os.path.basename(file_path)
    
    files = {
        "file": (file_name, file_data, "application/pdf")
    }
    
    response = requests.post(pinata_api_url, headers=headers, files=files)
    
    result = json.loads(response.text)
    if "IpfsHash" in result:
        ipfs_hash = result["IpfsHash"]
        print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
        return ipfs_hash
    else:
        print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
        return None

st.markdown("""
    <style>
    /* Global Reset */
    .stApp {
        background-color: #f0f2f5 !important;
        color: #212529 !important;
    }

    /* Container for better responsiveness */
    .content-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e2c4c;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    /* Subheading */
    .subheading {
        text-align: center;
        font-size: 1.2rem;
        color: #4a5568;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Form and Input Styles */
    .form-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 2.5rem;
        margin-bottom: 2rem;
        max-width: 650px;
        margin-left: auto;
        margin-right: auto;
    }

    .form-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e2c4c;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* ALL text content forced to visible color */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .stRadio, .stRadio label, .stRadio span, .stRadio div,
    .stCheckbox, .stCheckbox label, .stCheckbox span, .stCheckbox div,
    .stTextInput, .stTextInput label, .stTextInput span, .stTextInput div,
    .stButton, .stButton label, .stButton span, .stButton div,
    .stSubheader, label, p, span, div, h1, h2, h3, h4, h5, h6,
    .stSelectbox, .stSelectbox label, .stSelectbox span, .stSelectbox div {
        color: #1e2c4c !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 6px !important;
        border: 1px solid #cbd5e0 !important;
        background-color: #f8fafc !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #64748b !important;
        padding-bottom: 1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e40af !important;
        border-bottom: 2px solid #1e40af !important;
    }
    
    /* Exceptions for button text */
    .stButton > button {
        color: white !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e2c4c !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Input fields styling */
    .stTextInput > label {
        font-weight: 500 !important;
        color: #1e2c4c !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 6px !important;
        border: 1px solid #cbd5e0 !important;
        padding: 0.75rem 1rem !important;
        color: #1a202c !important;
        background-color: #f8fafc !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1e40af !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        border: none !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        background-color: #1e3a8a !important;
        transform: translateY(-1px) !important;
    }
    
    /* Success/error message styling */
    .stAlert {
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-top: 1rem !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        color: #4a5568;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ACADEMICS CERTIFICATE SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheading'>Secure management of academic certificates using blockchain</p>", unsafe_allow_html=True)

# Main form container
st.markdown("<div class='form-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='form-title'>Certificate Management Portal</h2>", unsafe_allow_html=True)

options = ("Generate Certificate", "View Certificates")
selected = st.selectbox("Select an action", options, label_visibility="collapsed")

if selected == options[0]:
    st.markdown("<div class='section-header'>Create New Certificate</div>", unsafe_allow_html=True)
    
    with st.form("Generate-Certificate"):
        uid = st.text_input(label="Student UID", placeholder="Enter unique student ID")
        candidate_name = st.text_input(label="Student Name", placeholder="Enter student full name")
        course_name = st.text_input(label="Course Name", placeholder="Enter course title")
        org_name = st.text_input(label="Institution Name", placeholder="Enter institution name")
        
        submit = st.form_submit_button("Generate Certificate")
        
        if submit:
            if not uid or not candidate_name or not course_name or not org_name:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Generating certificate and uploading to IPFS..."):
                    # Generate certificate file
                    pdf_file_path = "certificate.pdf"
                    institute_logo_path = "../assets/ins_logo.png"
                    generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)
                    
                    # Upload the PDF to Pinata
                    ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
                    
                    # Clean up temporary file
                    os.remove(pdf_file_path)
                    
                    if ipfs_hash:
                        # Create unique certificate ID
                        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
                        certificate_id = hashlib.sha256(data_to_hash).hexdigest()
                        
                        # Store on blockchain
                        contract.functions.generateCertificate(
                            certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash
                        ).transact({'from': w3.eth.accounts[0]})
                        
                        st.success(f"Certificate successfully generated!")
                        st.markdown(f"""
                        <div style="padding: 1rem; background-color: #f0f9ff; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #0369a1;">
                            <p style="margin-bottom: 0.5rem; font-weight: 600;">Certificate Details:</p>
                            <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                            <p style="margin-bottom: 0.25rem;"><strong>Student:</strong> {candidate_name}</p>
                            <p style="margin-bottom: 0.25rem;"><strong>Course:</strong> {course_name}</p>
                            <p style="margin-bottom: 0;"><strong>IPFS Hash:</strong> {ipfs_hash}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Failed to upload certificate to IPFS. Please try again.")
else:
    st.markdown("<div class='section-header'>Verify Certificate</div>", unsafe_allow_html=True)
    
    with st.form("View-Certificate"):
        certificate_id = st.text_input("Certificate ID", placeholder="Enter the certificate ID to verify")
        submit = st.form_submit_button("Verify Certificate")
        
        if submit:
            if not certificate_id:
                st.error("Please enter a certificate ID")
            else:
                try:
                    with st.spinner("Retrieving certificate from blockchain..."):
                        view_certificate(certificate_id)
                except Exception as e:
                    st.error("Invalid Certificate ID or certificate not found!")
                    st.markdown(f"""
                    <div style="padding: 1rem; background-color: #fff1f2; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #e11d48;">
                        <p style="margin-bottom: 0;">The certificate ID you entered could not be verified. Please check the ID and try again.</p>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer" style="color: #1e2c4c;">Academics Certificate System.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  
st.markdown('</div>', unsafe_allow_html=True)  