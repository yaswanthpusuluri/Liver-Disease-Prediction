import streamlit as st
from Util.util import Util

st.set_page_config(
    page_title="Liver Disease Prediction",
    page_icon="🩺",
    layout="wide"
)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > .main {
background-size: 500%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
right: 2rem;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

util = Util()

st.title("🩺 Liver Disease Prediction Application")

status = st.info("Loading trained model...")

model = util.load_model()

status.success("Application is ready for predictions.")
status.success("✅ Model loaded successfully. Ready for prediction.")
# ==========================================
# Sample Patient Data
# ==========================================

with st.sidebar:

    st.header("🧪 Sample Patient Data")
    st.caption("Click a button to automatically fill the patient details.")
    if st.button("🟢 Healthy Patient", use_container_width=True):
        util.load_sample_patient("healthy")
        st.rerun()

    if st.button("🔴 Liver Disease Patient", use_container_width=True):
        util.load_sample_patient("disease")
        st.rerun()

    if st.button("🎲 Random Patient", use_container_width=True):
        util.load_sample_patient("random")
        st.rerun()

    if st.button("🔄 Reset Form", use_container_width=True):
        st.session_state.patient_data = util.default_patient.copy()
        st.rerun()

st.subheader("Enter Patient Information")

st.info(
    "This prediction is generated using a trained Machine Learning model and is intended for educational purposes only."
)

util.form_functions(model)

st.markdown(util.page_footer(), unsafe_allow_html=True)