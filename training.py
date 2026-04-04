# from extraction import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    accuracy_score, recall_score, confusion_matrix,
    ConfusionMatrixDisplay, roc_curve, RocCurveDisplay, roc_auc_score
)
import joblib
from hdf import appdata_dir, features_path, model_path


def train_classifier(classifier, name, features_train, labels_train, features_test, labels_test):
    """
    Wraps any sklearn classifier in a StandardScaler pipeline,
    trains it, and prints all evaluation metrics from the slides.
    """

    # Build pipeline: scaler + classifier
    # Scaler is fit ONLY on training data — avoids data leakage
    pipeline = make_pipeline(StandardScaler(), classifier) #sets up pipeline to train using classifier input

    # Train
    pipeline.fit(features_train, labels_train) #normalizes data then trains model

    # Predict
    y_pred = pipeline.predict(features_test)
    y_prob = pipeline.predict_proba(features_test)[:, 1]  # Probability(jumping)

    # ── Metrics ──────────────────────────────────────────────
    acc     = accuracy_score(labels_test, y_pred)
    recall  = recall_score(labels_test, y_pred)   # sensitivity / TPR
    auc     = roc_auc_score(labels_test, y_prob)

    print(f"\n── Model Trianing: {name} ──")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Recall   : {recall:.4f}")
    print(f"  AUC      : {auc:.4f}")
    #
    # # ── Confusion Matrix ─────────────────────────────────────
    # cm = confusion_matrix(labels_test, y_pred)
    # disp = ConfusionMatrixDisplay(cm, display_labels=["walking", "jumping"])
    # disp.plot()
    # plt.title(f"Confusion Matrix — {name}")
    # plt.tight_layout()
    # plt.savefig(f"confusion_{name.replace(' ', '_')}.png")
    # plt.show()
    #
    # # ── ROC Curve ────────────────────────────────────────────
    # fpr, tpr, _ = roc_curve(labels_test, y_prob)
    # RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc, estimator_name=name).plot()
    # plt.title(f"ROC Curve — {name}")
    # plt.tight_layout()
    # plt.savefig(f"roc_{name.replace(' ', '_')}.png")
    # plt.show()

    return pipeline  # return trained model in case you want to reuse it

def run_training(model_type):
    # Check if features exist using pathlib
    if not features_path.exists():
        print(f"ERROR: Run extraction first! Extraction file not found.")
        return

    # Load the extracted features
    data = np.load(features_path)
    features_train = data['X_train']
    labels_train = data['y_train']
    features_test = data['X_test']
    labels_test = data['y_test']

    print(f"INFO: Training {model_type} on {features_train.shape[0]} x {features_train.shape[1]} samples...")

    if model_type == 'lr':
        model = LogisticRegression(max_iter=10000)
        name = "Logistic Regression"
    elif model_type == 'knn':
        model = KNeighborsClassifier(n_neighbors=5)
        name = "KNN k=5"
    else:
        print(f"ERROR: Unknown model type '{model_type}'")
        return

    # Train and get the pipeline
    trained_pipeline = train_classifier(
        model, name,
        features_train, labels_train, features_test, labels_test
    )

    # Save the trained model to disk!
    joblib.dump(trained_pipeline, model_path)
    print(f"INFO: Model traing successful, saved to disk. (Type: {model_type})")