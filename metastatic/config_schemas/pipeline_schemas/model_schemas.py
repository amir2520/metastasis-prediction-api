from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from typing import Optional, Union, Any
from metastatic.utils.utils import LoggableParamsMixin


@dataclass
class ModelConfig(LoggableParamsMixin):
	_target_: str = MISSING
	def loggable_params(self) -> list[str]:
		return ['_target_']


@dataclass
class LogisticRegressionConfig(ModelConfig):
    _target_: str = 'sklearn.linear_model.LogisticRegression'
    C: float = 10.0
    class_weight: Any = field(default=None)
    # solver: str = 'lbfgs'
    # penalty: str = 'l2'
    # max_iter: int = 1000

    def loggable_params(self) -> list[str]:
        return super().loggable_params() + ['C', 'class_weight']


@dataclass
class RandomForestClassifierConfig(ModelConfig):
	_target_: str = 'sklearn.ensemble.RandomForestClassifier'
	max_depth: int = 5
	class_weight: Any = field(default=None)
	# class_weight: dict = field(default_factory=lambda: {0: 1, 1: 1})
	def loggable_params(self) -> list[str]:
		return super().loggable_params() + ['max_depth', 'class_weight']


@dataclass
class LinearSVCConfig(ModelConfig):
	_target_: str = 'sklearn.svm.LinearSVC'
	max_iter: int = 1000
	class_weight: Any = field(default=None)
	# class_weight: dict = field(default_factory=lambda: {0: 1, 1: 1})
	def loggable_params(self) -> list[str]:
		return super().loggable_params() + ['max_iter', 'class_weight']

def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name="logistic_regression_model_schema",
		node=LogisticRegressionConfig,
		group="models"
	)
	cs.store(
		name="random_forest_model_schema",
		node=RandomForestClassifierConfig,
		group="models"
	)
	cs.store(
		name="linear_svc_model_schema",
		node=LinearSVCConfig,
		group="models"
	)
