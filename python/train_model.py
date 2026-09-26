from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR /
    "dataset" /
    "mpu6050_dataset.csv"
)

MODEL_DIR = (
    BASE_DIR /
    "model"
)

ARDUINO_DIR = (
    BASE_DIR /
    "arduino" /
    "embedded_ai"
)

MODEL_DIR.mkdir(
    exist_ok=True
)

ARDUINO_DIR.mkdir(
    exist_ok=True
)


MODEL_PATH = (
    MODEL_DIR /
    "mlp_model.pkl"
)

SCALER_PATH = (
    MODEL_DIR /
    "scaler.pkl"
)

HEADER_PATH = (
    ARDUINO_DIR /
    "model_data.h"
)


# ============================================================
# LOAD DATASET
# ============================================================

print("\n======================================")
print("        EMBEDDED AI TRAINING")
print("======================================")

print("\nLoading dataset...")

data = pd.read_csv(
    DATASET_PATH
)


print("\nDataset:")
print(data.head())


print("\nNumber of samples:")
print(len(data))


print("\nClass distribution:")
print(
    data["Label"].value_counts()
)


# ============================================================
# FEATURES AND LABELS
# ============================================================

X = data[
    [
        "Ax",
        "Ay",
        "Az"
    ]
].astype(float)


y = data["Label"].astype(str)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ============================================================
# FEATURE SCALING
# ============================================================

scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ============================================================
# CREATE NEURAL NETWORK
# ============================================================

model = MLPClassifier(

    hidden_layer_sizes=(8,),

    activation="relu",

    solver="lbfgs",

    alpha=0.0001,

    max_iter=2000,

    random_state=42
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining neural network...")

model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# TEST
# ============================================================

predictions = model.predict(
    X_test_scaled
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n======================================")
print("             RESULTS")
print("======================================")

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# ============================================================
# SAVE PYTHON MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    scaler,
    SCALER_PATH
)


print("\nPython model saved:")
print(MODEL_PATH)

print("\nScaler saved:")
print(SCALER_PATH)


# ============================================================
# GENERATE C HEADER
# ============================================================

weights_input_hidden = model.coefs_[0]
bias_hidden = model.intercepts_[0]

weights_hidden_output = model.coefs_[1]
bias_output = model.intercepts_[1]


classes = model.classes_


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------

def format_float(value):

    return f"{float(value):.9f}f"


def format_array(values):

    return ", ".join(
        format_float(value)
        for value in values
    )


# ============================================================
# CREATE HEADER
# ============================================================

with open(
    HEADER_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "#pragma once\n\n"
    )

    file.write(
        "// ==================================================\n"
    )

    file.write(
        "// AUTO-GENERATED MODEL FILE\n"
    )

    file.write(
        "// Do not edit manually.\n"
    )

    file.write(
        "// Generated by python/train_model.py\n"
    )

    file.write(
        "// ==================================================\n\n"
    )


    file.write(
        "#include <stddef.h>\n\n"
    )


    # --------------------------------------------------------
    # Model sizes
    # --------------------------------------------------------

    file.write(
        "constexpr int MODEL_INPUT_SIZE = 3;\n"
    )

    file.write(
        "constexpr int MODEL_HIDDEN_SIZE = 8;\n\n"
    )


    # --------------------------------------------------------
    # Class names
    # --------------------------------------------------------

    file.write(
        "static const char* CLASS_0 = "
        f"\"{classes[0]}\";\n"
    )

    file.write(
        "static const char* CLASS_1 = "
        f"\"{classes[1]}\";\n\n"
    )


    # --------------------------------------------------------
    # StandardScaler mean
    # --------------------------------------------------------

    file.write(
        "static const float INPUT_MEAN[3] = {\n"
    )

    file.write(
        "    " +
        format_array(
            scaler.mean_
        ) +
        "\n"
    )

    file.write(
        "};\n\n"
    )


    # --------------------------------------------------------
    # StandardScaler scale
    # --------------------------------------------------------

    file.write(
        "static const float INPUT_SCALE[3] = {\n"
    )

    file.write(
        "    " +
        format_array(
            scaler.scale_
        ) +
        "\n"
    )

    file.write(
        "};\n\n"
    )


    # --------------------------------------------------------
    # Input → Hidden weights
    # --------------------------------------------------------

    file.write(
        "static const float "
        "WEIGHTS_INPUT_HIDDEN[3][8] = {\n"
    )

    for row in weights_input_hidden:

        file.write(
            "    { " +
            format_array(row) +
            " },\n"
        )

    file.write(
        "};\n\n"
    )


    # --------------------------------------------------------
    # Hidden biases
    # --------------------------------------------------------

    file.write(
        "static const float "
        "BIAS_HIDDEN[8] = {\n"
    )

    file.write(
        "    " +
        format_array(
            bias_hidden
        ) +
        "\n"
    )

    file.write(
        "};\n\n"
    )


    # --------------------------------------------------------
    # Hidden → Output weights
    # --------------------------------------------------------

    file.write(
        "static const float "
        "WEIGHTS_HIDDEN_OUTPUT[8] = {\n"
    )

    file.write(
        "    " +
        format_array(
            weights_hidden_output.ravel()
        ) +
        "\n"
    )

    file.write(
        "};\n\n"
    )


    # --------------------------------------------------------
    # Output bias
    # --------------------------------------------------------

    file.write(
        "static const float "
        "BIAS_OUTPUT = " +
        format_float(
            bias_output[0]
        ) +
        ";\n"
    )


print("\nEmbedded model header generated:")
print(HEADER_PATH)


print("\n======================================")
print("        TRAINING COMPLETE")
print("======================================")