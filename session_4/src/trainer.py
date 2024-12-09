import pickle
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd
from hrid import HRID
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from data import TuplePropre, TuplePropreSansPrix


class Metadata:
    name: str

    def __init__(
        self,
        name: str,
    ):
        self.name = name


class Model:
    pipeline: Pipeline
    metadata: Metadata

    def __init__(self, pipeline: Pipeline, metadata: Metadata):
        self.pipeline = pipeline
        self.metadata = metadata

    def predict(self, data: list[TuplePropreSansPrix]) -> Any:
        X = [
            {
                "type": item.type_bien.name.lower(),
                "surface": item.surface,
                "pieces": item.pieces,
            }
            for item in data
        ]
        return self.pipeline.predict(pd.DataFrame(X))

    def get_metadata(self) -> Metadata:
        return self.metadata


class Trainer:
    def train(self, data: list[TuplePropre]) -> Model:
        raise NotImplementedError

    def save(self, model: Model) -> None:
        raise NotImplementedError

    def load(self, name: str) -> Model:
        raise NotImplementedError


class ModelSaver:
    def save(self, model: Model) -> None:
        raise NotImplementedError

    def get_model_from_metadata(self, best_models_metadata: Metadata) -> Model:
        raise NotImplementedError


class ScikitModelSaver(ModelSaver):
    save_path: str
    logger: Logger

    def __init__(self, save_path: str, logger: Logger):
        self.save_path = save_path
        self.logger = logger

    def save(self, model: Model) -> None:
        Path(self.save_path).mkdir(exist_ok=True, parents=True)
        with open(self.save_path + "/" + model.metadata.name + ".pkl", "wb") as file:
            pickle.dump({"pipeline": model.pipeline, "metadata": model.metadata}, file)

    def get_model_from_metadata(self, best_models_metadata: Metadata) -> Model:
        model_path = self.save_path + "/" + best_models_metadata.name + ".pkl"
        with open(model_path, "rb") as file:
            load = pickle.load(file)
            return Model(load["pipeline"], load["metadata"])


class ScikitLearnTrainer(Trainer):
    test_size: float
    random_state: int
    save_path: str
    logger: Logger

    def __init__(self, test_size: float, random_state: int, logger: Logger):
        self.logger = logger
        self.test_size = test_size
        self.random_state = random_state

    def train(self, data: list[TuplePropre]) -> Model:
        training_id = HRID().generate()
        self.logger.info(f"training model {training_id}")

        X = [
            {
                "type": item.type_bien.name.lower(),
                "surface": item.surface,
                "pieces": item.pieces,
            }
            for item in data
        ]
        y = [item.prix for item in data]
        y_train = y

        x_train = pd.DataFrame(X)

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    ColumnTransformer(
                        transformers=[("type", OneHotEncoder(), ["type"])],
                        remainder="passthrough",
                    ),
                ),
                ("regressor", LinearRegression()),
            ]
        )

        pipeline.fit(x_train, y_train)

        return Model(pipeline=pipeline, metadata=Metadata(name=training_id))
