from provider import Provider


def test_pipeline_gets() -> None:
    assert Provider().get() != []
