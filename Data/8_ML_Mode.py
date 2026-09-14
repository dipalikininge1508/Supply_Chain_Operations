import joblib
import streamlit as st
import pandas as pd
import gdown
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# 1. LOAD DATASET
# ============================================================

FILE_ID = "1WIncON4DKmSUIqdttb-MD0vAhvfQutbM"
CSV_PATH = "data/APL_Logistics.csv"
@st.cache_data
def load_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(
            url,
            CSV_PATH,
            quiet=False
        )
    return pd.read_csv(CSV_PATH)
    
df = load_data()

print("Dataset loaded successfully!")
print("Original Shape:", df.shape)


# ============================================================
# 2. REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates()

print(
    "Shape after removing duplicates:",
    df.shape
)


# ============================================================
# 3. TARGET VARIABLE
# ============================================================

target = "Late_delivery_risk"

print("\nLate Delivery Risk Distribution:")
print(
    df[target].value_counts()
)


# ============================================================
# 4. SELECT PREDICTION FEATURES
# ============================================================

# IMPORTANT:
# We DO NOT use "Days for shipping (real)"
# because it is known after shipment/delivery.
#
# We also do not use Delay_Gap because it is calculated
# using actual shipping days.

features = [

    "Days for shipment (scheduled)",

    "Shipping Mode",

    "Market",

    "Order Region",

    "Customer Segment",

    "Order Item Quantity",

    "Order Item Discount Rate",

    "Order Item Product Price",

    "Sales",

    "Product Price",

    "Order Item Profit Ratio"
]


# ============================================================
# 5. CREATE MODEL DATASET
# ============================================================

df_model = df[
    features + [target]
].copy()


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

df_model = df_model.dropna()

print(
    "\nShape after removing missing values:"
)

print(
    df_model.shape
)


# ============================================================
# 7. ENCODE CATEGORICAL VARIABLES
# ============================================================

categorical_columns = [

    "Shipping Mode",

    "Market",

    "Order Region",

    "Customer Segment"

]


label_encoders = {}


for column in categorical_columns:

    encoder = LabelEncoder()

    df_model[column] = encoder.fit_transform(
        df_model[column].astype(str)
    )

    label_encoders[column] = encoder


# ============================================================
# 8. SEPARATE FEATURES AND TARGET
# ============================================================

X = df_model[features]

y = df_model[target]


# ============================================================
# 9. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print(
    "\nTraining data:",
    X_train.shape
)

print(
    "Testing data:",
    X_test.shape
)


# ============================================================
# 10. LOGISTIC REGRESSION
# ============================================================

print("\n==============================")
print("LOGISTIC REGRESSION")
print("==============================")


logistic_model = LogisticRegression(
    max_iter=1000
)


logistic_model.fit(
    X_train,
    y_train
)


logistic_prediction = logistic_model.predict(
    X_test
)


logistic_accuracy = accuracy_score(
    y_test,
    logistic_prediction
)

logistic_precision = precision_score(
    y_test,
    logistic_prediction,
    zero_division=0
)

logistic_recall = recall_score(
    y_test,
    logistic_prediction,
    zero_division=0
)

logistic_f1 = f1_score(
    y_test,
    logistic_prediction,
    zero_division=0
)


print(
    "Accuracy :",
    logistic_accuracy
)

print(
    "Precision:",
    logistic_precision
)

print(
    "Recall   :",
    logistic_recall
)

print(
    "F1 Score :",
    logistic_f1
)


# ============================================================
# 11. DECISION TREE
# ============================================================

print("\n==============================")
print("DECISION TREE")
print("==============================")


decision_tree = DecisionTreeClassifier(

    random_state=42,

    max_depth=10

)


decision_tree.fit(
    X_train,
    y_train
)


tree_prediction = decision_tree.predict(
    X_test
)


tree_accuracy = accuracy_score(
    y_test,
    tree_prediction
)

tree_precision = precision_score(
    y_test,
    tree_prediction,
    zero_division=0
)

tree_recall = recall_score(
    y_test,
    tree_prediction,
    zero_division=0
)

tree_f1 = f1_score(
    y_test,
    tree_prediction,
    zero_division=0
)


print(
    "Accuracy :",
    tree_accuracy
)

print(
    "Precision:",
    tree_precision
)

print(
    "Recall   :",
    tree_recall
)

print(
    "F1 Score :",
    tree_f1
)


# ============================================================
# 12. RANDOM FOREST
# ============================================================

print("\n==============================")
print("RANDOM FOREST")
print("==============================")


random_forest = RandomForestClassifier(

    n_estimators=100,

    max_depth=12,

    random_state=42,

    n_jobs=-1

)


random_forest.fit(
    X_train,
    y_train
)


rf_prediction = random_forest.predict(
    X_test
)


rf_accuracy = accuracy_score(
    y_test,
    rf_prediction
)

rf_precision = precision_score(
    y_test,
    rf_prediction,
    zero_division=0
)

rf_recall = recall_score(
    y_test,
    rf_prediction,
    zero_division=0
)

rf_f1 = f1_score(
    y_test,
    rf_prediction,
    zero_division=0
)


print(
    "Accuracy :",
    rf_accuracy
)

print(
    "Precision:",
    rf_precision
)

print(
    "Recall   :",
    rf_recall
)

print(
    "F1 Score :",
    rf_f1
)


# ============================================================
# 13. MODEL COMPARISON
# ============================================================

results = pd.DataFrame({

    "Model": [

        "Logistic Regression",

        "Decision Tree",

        "Random Forest"

    ],

    "Accuracy": [

        logistic_accuracy,

        tree_accuracy,

        rf_accuracy

    ],

    "Precision": [

        logistic_precision,

        tree_precision,

        rf_precision

    ],

    "Recall": [

        logistic_recall,

        tree_recall,

        rf_recall

    ],

    "F1 Score": [

        logistic_f1,

        tree_f1,

        rf_f1

    ]

})


print("\n==============================")
print("MODEL COMPARISON")
print("==============================")


print(results)


# ============================================================
# 14. SELECT BEST MODEL
# ============================================================

best_model_name = results.loc[

    results["F1 Score"].idxmax(),

    "Model"

]


print("\nBest Model:")
print(
    best_model_name
)


if best_model_name == "Logistic Regression":

    best_model = logistic_model


elif best_model_name == "Decision Tree":

    best_model = decision_tree


else:

    best_model = random_forest


# ============================================================
# 15. CONFUSION MATRIX
# ============================================================

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")


best_prediction = best_model.predict(
    X_test
)


cm = confusion_matrix(

    y_test,

    best_prediction

)


print(cm)


# ============================================================
# 16. CLASSIFICATION REPORT
# ============================================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")


print(

    classification_report(

        y_test,

        best_prediction,

        zero_division=0

    )

)


# ============================================================
# 17. SAVE MODEL
# ============================================================

os.makedirs(
    "../Models",
    exist_ok=True
)


model_data = {

    "model": best_model,

    "features": features,

    "encoders": label_encoders

}


joblib.dump(

    model_data,

    "../Models/delivery_risk_model.pkl"

)


print("\nModel saved successfully!")

print(
    "Location: ../Models/delivery_risk_model.pkl"
)
