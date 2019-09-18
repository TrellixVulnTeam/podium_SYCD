import pytest
import pytest_mock  # noqa

from takepod.models.impl.simple_trainers import SimpleTrainer
from takepod.models.model import AbstractSupervisedModel
from takepod.datasets.iterator import Iterator
from test.storage.conftest import (tabular_dataset, json_file_path)  # noqa


@pytest.fixture()
@pytest.mark.usefixtures("mocker")
def model(mocker):
    model = mocker.MagicMock(spec=AbstractSupervisedModel)
    return model

@pytest.mark.usefixtures("tabular_dataset", "model")  # noqa
def test_simple_trainer_no_num_epoch(tabular_dataset, model):
    iterator = Iterator(tabular_dataset, 1)
    with pytest.raises(ValueError):
        trainer = SimpleTrainer()
        trainer.train(model,
                      iterator=iterator,
                      feature_transform_fun=lambda x: x,
                      label_transform_fun=lambda y: y)


@pytest.mark.usefixtures("tabular_dataset", "model")  # noqa
def test_simple_trainer_num_epoch(tabular_dataset, model):
    tabular_dataset.finalize_fields()
    iterator = Iterator(tabular_dataset, batch_size=len(tabular_dataset))
    trainer = SimpleTrainer()
    trainer.train(model=model,
                  iterator=iterator,
                  feature_transform_fun=lambda x: x,
                  label_transform_fun=lambda y: y,
                  **{trainer.MAX_EPOCH_KEY: 10})
    assert model.fit.call_count == 10


def mock_feature_transform_fun(x):
    return x


def mock_label_transform_fun(y):
    y

@pytest.mark.usefixtures("tabular_dataset", "mocker", "model")  # noqa
def test_simple_trainer_batch_transform_call(tabular_dataset, mocker, model):
    tabular_dataset.finalize_fields()
    iterator = Iterator(tabular_dataset, batch_size=len(tabular_dataset))

    with mocker.patch(
            "test.models.test_simple_trainers.mock_feature_transform_fun",
            return_value=next(iterator.__iter__())[0]):
        with mocker.patch(
                "test.models.test_simple_trainers.mock_label_transform_fun",
                return_value=next(iterator.__iter__())[1]):
            trainer = SimpleTrainer()
            trainer.train(
                model=model,
                iterator=iterator,
                feature_transform_fun=mock_feature_transform_fun,
                label_transform_fun=mock_label_transform_fun,
                **{trainer.MAX_EPOCH_KEY: 10})
            assert mock_feature_transform_fun.call_count == 10  # pylint: disable=E1101
            assert mock_label_transform_fun.call_count == 10  # pylint: disable=E1101
