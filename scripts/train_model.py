import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

# ==========================
# Load Dataset
# ==========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "indian_liver_patient.csv")

df = pd.read_csv(DATA_PATH)

# ==========================
# Preprocessing
# ==========================

df.rename(columns={"Dataset": "Diagnosis"}, inplace=True)

df["Diagnosis"] = df["Diagnosis"].apply(lambda x: 1 if x == 1 else 0)

df["Albumin_and_Globulin_Ratio"] = df["Albumin_and_Globulin_Ratio"].fillna(df["Albumin_and_Globulin_Ratio"].mean())

df["Gender"] = df["Gender"].map({
    "Male": 1,
    "Female": 0
})

# ==========================
# Features & Target
# ==========================

FEATURES = [
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

X = df[FEATURES]
y = df["Diagnosis"]

# ==========================
# Train Final Model
# ==========================

model = RandomForestClassifier(
    bootstrap=True,
    class_weight=None,
    criterion="entropy",
    max_depth=5,
    max_features="sqrt",
    min_samples_leaf=1,
    min_samples_split=2,
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# ==========================
# Save Model
# ==========================

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "model.pkl"))

import sklearn

print("Scikit-learn version:", sklearn.__version__)
print("Model saved successfully!")