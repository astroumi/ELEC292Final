from extraction import *
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

# ── assumes these are already populated from your feature extraction code ──
# features_train, labels_train, features_test, labels_test (all np.arrays)

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

    # # Predict
    # y_pred = pipeline.predict(features_test)
    # y_prob = pipeline.predict_proba(features_test)[:, 1]  # Probability(jumping)
    #
    # # ── Metrics ──────────────────────────────────────────────
    # acc     = accuracy_score(labels_test, y_pred)
    # recall  = recall_score(labels_test, y_pred)   # sensitivity / TPR
    # auc     = roc_auc_score(labels_test, y_prob)
    #
    # print(f"\n── {name} ──")
    # print(f"  Accuracy : {acc:.4f}")
    # print(f"  Recall   : {recall:.4f}")
    # print(f"  AUC      : {auc:.4f}")
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


# ── Run three classifiers ─────────────────────────────────────────────────────

# 1. Logistic Regression (shown directly in the slides) [file:240]
lr_model = train_classifier(
    LogisticRegression(max_iter=10000),
    "Logistic Regression",
    features_train, labels_train, features_test, labels_test
)

# print("Train shape:", features_train.shape)
# print(features_train)
# print("Test  shape:", features_test.shape)
# print(features_test)
#
# print("Train labels:", np.unique(labels_train, return_counts=True))
# print("Test  labels:", np.unique(labels_test, return_counts=True))

# # 2. K-Nearest Neighbours
# knn_model = train_classifier(
#     KNeighborsClassifier(n_neighbors=5),
#     "KNN k=5",
#     features_train, labels_train, features_test, labels_test
# )
#
# # 3. Decision Tree
# dt_model = train_classifier(
#     DecisionTreeClassifier(max_depth=5, random_state=42),
#     "Decision Tree",
#     features_train, labels_train, features_test, labels_test
# )