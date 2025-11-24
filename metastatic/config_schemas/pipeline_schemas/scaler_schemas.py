from dataclasses import dataclass
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore
from metastatic.utils.utils import LoggableParamsMixin

@dataclass
class ScalerConfig(LoggableParamsMixin):
	_target_: str = MISSING
	def loggable_params(self) -> list[str]:
		return ['_target_']

@dataclass
class StandardScalerConfig(ScalerConfig):
	_target_: str = 'sklearn.preprocessing.StandardScaler'
	with_mean: bool = True
	with_std: bool = True


@dataclass
class MinMaxScalerConfig(ScalerConfig):
	_target_: str = 'sklearn.preprocessing.MinMaxScaler'
	feature_range: tuple[float, float] = (0, 1)



def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name='standard_scaler_schema',
		node=StandardScalerConfig,
		group='scalers'
	)

	cs.store(
		name='minmax_scaler_schema',
		node=MinMaxScalerConfig,
		group='scalers'
	)