from dataclasses import dataclass
from hydra.core.config_store import ConfigStore
from typing import Optional
from metastatic.utils.utils import LoggableParamsMixin

@dataclass
class SMOTEConfig(LoggableParamsMixin):
	_target_: str = 'imblearn.over_sampling.SMOTE'
	sampling_strategy: str = 'auto'
	k_neighbors: int = 5
	random_state: Optional[int] = None
	def loggable_params(self) -> list[str]:
		return ['_target_', 'sampling_strategy', 'k_neighbors']


def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name="SMOTE_schema",
		node=SMOTEConfig,
		group='imbalance'
	)