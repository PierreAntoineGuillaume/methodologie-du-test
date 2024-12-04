import logging
from cleaner import Cleaner
from data import TupleSale, TuplePropre, BienType
from model_comparator import ModelComparator, InMemoryModelComparator
from pipeline import Pipeline
from provider import Provider
from trainer import ScikitLearnTrainer, ModelSaver, Model

logger = logging.getLogger()


class MockProvider(Provider):
    def get(self) -> list[TupleSale]:
        return []


class MockCleaner(Cleaner):
    def clean(self, input_data: list[TupleSale]) -> list[TuplePropre]:
        return [
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
            TuplePropre(prix=100000, surface=100, type_bien=BienType.Maison, pieces=4),
        ]


class MockSaver(ModelSaver):
    def save(self, model: Model) -> None:
        pass


def make_pipeline(
    provider: Provider | None = None,
    cleaner: Cleaner | None = None,
    saver: ModelSaver | None = None,
    model_comparator: ModelComparator | None = None,
) -> Pipeline:
    if provider is None:
        provider = MockProvider()
    if cleaner is None:
        cleaner = MockCleaner()
    if saver is None:
        saver = MockSaver()
    if model_comparator is None:
        model_comparator = InMemoryModelComparator()
    return Pipeline(
        provider, cleaner, ScikitLearnTrainer(0.2, 2, logger), saver, model_comparator
    )


def test_comparator_gets_something_from_real_model() -> None:
    comparator = InMemoryModelComparator()
    pipeline = make_pipeline(model_comparator=comparator)
    pipeline.get_data_and_train_model()
    assert comparator.metadata_list[0] is not None
