import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

def train_logistic_regression(df):
    
    # Séparer features et label
    X = df.iloc[:, :-1]
    y = df["LABEL"]
    
    # Split train / test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    
    # Pipeline : Standardisation + Logistic Regression
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression())
    ])
    
    # Entraînement
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Évaluation
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("\nClassification report:\n")
    print(classification_report(y_test, y_pred))
    
    return model


if __name__ == "__main__":

    df = pd.read_csv("data/toy/test_shuffled.csv")
    train_logistic_regression(df)

    
