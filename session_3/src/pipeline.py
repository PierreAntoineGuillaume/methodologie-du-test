import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, FunctionTransformer


class Cleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(
            labels=["date", "transaction_id", "client_id"], axis=1
        )
        valid_values = ["legit", "fraud", "high_risk", "low_risk"]
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df[df["amount"].notna() & (df["amount"] >= 1)]
        df = df[df["label"].isin(valid_values)]
        return df.dropna(axis=0)


class PandasCsvProvider:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def get(self) -> pd.DataFrame:
        return pd.read_csv(self.path)


class Metadata:
    def __init__(self, accuracy: float):
        self.accuracy: float = accuracy
    def __str__(self) -> str:
        return f"Metadata({self.accuracy})"

class Model:
    def __init__(self, pipeline: Pipeline, metadata: Metadata):
        self.pipeline: Pipeline = pipeline
        self.metadata: Metadata = metadata


class Trainer:
    def train(self, df: pd.DataFrame) -> Model:
        # Separate features and target
        X = df[["product_id", "amount"]]
        y = df["label"]

        # Label encode the target variable
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        # Preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                # For product_id: hash it or apply custom logic (ensure it's treated as DataFrame here)
                ("product_id", FunctionTransformer(lambda x: x.map(hash)), ["product_id"]),
                # Scale amount
                ("amount", StandardScaler(), ["amount"])
            ],
            remainder="drop"
        )

        # Define the model
        model = RandomForestClassifier(random_state=42)

        # Create the pipeline
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ])

        # Split data for training and evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

        # Train the pipeline
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        return Model(
            pipeline=pipeline,
            metadata=Metadata(accuracy)
        )
