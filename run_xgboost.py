import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

def train_xgboost_multiclass(csv_path, test_size=0.2, n_splits=5, random_state=42):
    """
    Entraîne un XGBoost multi-classe sur un CSV contenant ID et LABEL (str).

    - LABEL : classes encodées en chaînes (ex: "A", "B", "C")
    - Ignorer la colonne ID
    - F1-score macro (adapté au multi-classe)
    """

    # Chargement
    df = pd.read_csv(csv_path)

    # Vérification
    if "LABEL" not in df.columns:
        raise ValueError("Le fichier CSV doit contenir une colonne LABEL.")

    # On retire ID si présent
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])

    X = df.drop(columns=["LABEL"])
    y = df["LABEL"]

    # Encodage multi-classe (string → int)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Split stratifié (multi-classe)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded
    )

    # Modèle XGBoost multi-classe
    model = XGBClassifier(
        objective="multi:softmax",
        num_class=len(encoder.classes_),
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=random_state,
        eval_metric="mlogloss"
    )

    # Entraînement
    model.fit(X_train, y_train)

    # Prédiction test
    y_pred = model.predict(X_test)

    # F1 macro (équilibre entre classes)
    f1 = f1_score(y_test, y_pred, average="macro")

    # Cross-validation stratifiée multi-classe
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    cv_scores = cross_val_score(
        model, X, y_encoded,
        cv=skf,
        scoring="f1_macro"
    )

    return {
        "model": model,
        "label_encoder": encoder,
        "f1_test_macro": f1,
        "cv_scores_macro": cv_scores,
        "cv_mean_macro": cv_scores.mean()
    }



if __name__ == "__main__":

    results = train_xgboost_multiclass("data/GSE83687/totalenergy_labeled.csv", test_size=0.3)
    print("F1 macro (test) :", results["f1_test_macro"])
    print("Cross-val :", results["cv_scores_macro"])
    print("Moyenne CV :", results["cv_mean_macro"])

    
