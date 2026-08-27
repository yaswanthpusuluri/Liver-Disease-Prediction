import os
import joblib
import pandas as pd
import streamlit as st


class Util:

    def __init__(self):
        # Sample Patients

        self.default_patient = {
            "Age": 17,
            "Gender": 1,
            "Total_Bilirubin": 0.9,
            "Direct_Bilirubin": 0.3,
            "Alkaline_Phosphotase": 202,
            "Alanine_Aminotransferase": 22,
            "Aspartate_Aminotransferase": 19,
            "Total_Proteins": 7.4,
            "Albumin": 4.1,
            "Albumin_and_Globulin_Ratio": 1.2
        }

        self.healthy_patient = {
            "Age": 26,
            "Gender": 0,
            "Total_Bilirubin": 0.7,
            "Direct_Bilirubin": 0.2,
            "Alkaline_Phosphotase": 180,
            "Alanine_Aminotransferase": 24,
            "Aspartate_Aminotransferase": 22,
            "Total_Proteins": 7.2,
            "Albumin": 4.5,
            "Albumin_and_Globulin_Ratio": 1.4
        }

        self.disease_patient = {
            "Age": 58,
            "Gender": 1,
            "Total_Bilirubin": 5.6,
            "Direct_Bilirubin": 2.9,
            "Alkaline_Phosphotase": 310,
            "Alanine_Aminotransferase": 118,
            "Aspartate_Aminotransferase": 132,
            "Total_Proteins": 6.0,
            "Albumin": 2.9,
            "Albumin_and_Globulin_Ratio": 0.7
        }

        self.features = [
                    "Age",
                    "Gender",
                    "Total_Bilirubin",
                    "Direct_Bilirubin",
                    "Alkaline_Phosphotase",
                    "Alanine_Aminotransferase",
                    "Aspartate_Aminotransferase",
                    "Total_Proteins",
                    "Albumin",
                    "Albumin_and_Globulin_Ratio"
                ]

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.model_path = os.path.join(BASE_DIR, "models", "model.pkl")
        self.data_path = os.path.join(BASE_DIR, "data", "indian_liver_patient.csv")

        self.dataset = pd.read_csv(self.data_path)

        # Same preprocessing used during training
        self.dataset["Gender"] = self.dataset["Gender"].map({
            "Male": 1,
            "Female": 0
        })

        self.dataset["Albumin_and_Globulin_Ratio"] = (
            self.dataset["Albumin_and_Globulin_Ratio"]
            .fillna(self.dataset["Albumin_and_Globulin_Ratio"].median())
        )
        if "patient_data" not in st.session_state:
            st.session_state.patient_data = self.default_patient.copy()
           

    @st.cache_resource
    def load_model(_self):

            model = joblib.load(_self.model_path)
                

            return model

    def input_data_fields(self):

        default_vals = st.session_state.patient_data

        col1, col2 = st.columns(2)

        age = col1.number_input(
            "Age",
            value=int(default_vals["Age"]),
            step=1
        )

        gender = col2.selectbox(
                "Gender",
            ("Male", "Female"),
            index=0 if default_vals["Gender"] == 1 else 1
        )

        total_bilirubin = col1.number_input(
            "Total Bilirubin (mg/dL)",
            value=float(default_vals["Total_Bilirubin"]),
            step=0.1
        )

        direct_bilirubin = col2.number_input(
            "Direct Bilirubin (mg/dL)",
            value=float(default_vals["Direct_Bilirubin"]),
            step=0.1
        )

        alkaline_phosphotase = col1.number_input(
            "Alkaline Phosphotase (IU/L)",
            value=int(default_vals["Alkaline_Phosphotase"]),
            step=1
        )           

        alanine_aminotransferase = col2.number_input(
            "Alanine Aminotransferase (U/L)",
            value=int(default_vals["Alanine_Aminotransferase"]),
            step=1
        )

        aspartate_aminotransferase = col1.number_input(
            "Aspartate Aminotransferase (U/L)",
            value=int(default_vals["Aspartate_Aminotransferase"]),
            step=1
        )

        total_proteins = col2.number_input(
            "Total Proteins (g/dL)",
            value=float(default_vals["Total_Proteins"]),
            step=0.1
        )

        albumin = col1.number_input(
            "Albumin (g/dL)",
            value=float(default_vals["Albumin"]),
            step=0.1
        )

        albumin_globulin_ratio = col2.number_input(
            "Albumin / Globulin Ratio",
            value=float(default_vals["Albumin_and_Globulin_Ratio"]),
            step=0.1
        )

        gender = 1 if gender == "Male" else 0

        return pd.DataFrame([{
            "Age": age,
            "Gender": gender,
            "Total_Bilirubin": total_bilirubin,
            "Direct_Bilirubin": direct_bilirubin,
            "Alkaline_Phosphotase": alkaline_phosphotase,
            "Alanine_Aminotransferase": alanine_aminotransferase,
            "Aspartate_Aminotransferase": aspartate_aminotransferase,
            "Total_Proteins": total_proteins,
            "Albumin": albumin,
            "Albumin_and_Globulin_Ratio": albumin_globulin_ratio
        }])

    def form_functions(self, model):

        with st.form("prediction_form"):

            input_df = self.input_data_fields()

            submitted = st.form_submit_button(
                "Predict",
                type="primary"
            )

            if submitted:

                with st.spinner("Predicting..."):

                    prediction = model.predict(input_df)[0]

                    probability = model.predict_proba(input_df)[0]

                    no_disease_confidence = probability[0] * 100
                    disease_confidence = probability[1] * 100

                st.subheader("Prediction Result")

                if prediction == 1:

                    st.error(
                        "⚠️ High Risk of Liver Disease Detected. Please consult a healthcare professional for further diagnosis."
                    )

                    st.metric(
                        "Prediction Confidence",
                        f"{disease_confidence:.2f}%"
                    )

                else:

                    st.success(
                        "✅ Low Risk of Liver Disease Detected. No significant indication of liver disease was found."
                    )

                    st.metric(
                        "Prediction Confidence",
                        f"{no_disease_confidence:.2f}%"
                    )

    def load_sample_patient(self, patient_type):

        if patient_type == "healthy":
            sample = self.dataset[self.dataset["Dataset"] == 2].sample(1)

        elif patient_type == "disease":
            sample = self.dataset[self.dataset["Dataset"] == 1].sample(1)

        else:
            sample = self.dataset.sample(1)

        sample = sample.drop(columns=["Dataset"])

        st.session_state.patient_data = (
            sample.iloc[0]
            .to_dict()
        )                

    def page_footer(self):

        return """
        <style>
        footer {visibility:hidden;}
        </style>

        <hr>

        <center>
            <h4>Liver Disease Prediction using Machine Learning</h4>
            <p>Final Year Project</p>
        </center>
        """