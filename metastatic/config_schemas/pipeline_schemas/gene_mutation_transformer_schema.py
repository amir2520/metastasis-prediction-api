from dataclasses import dataclass
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from metastatic.utils.utils import LoggableParamsMixin


@dataclass
class GeneMutProcessConfig(LoggableParamsMixin):
	_target_: str = 'metastatic.preprocess.gene_mutation_transformer.GeneMutProcess'
	# _partial_: bool = True
	gene_counter_path: str = SI("${single_model.infrastructure.data.counter_path}") # 'metastatic/datasts/gene_mut_counter.pkl'
	include_rare: bool = True
	rare_threshold: int = 20
	gene_col: str = 'gene_mut'

	def loggable_params(self) -> list[str]:
		return ['_target_', 'include_rare', 'rare_threshold']


def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name='gene_mutation_precessor_schema',
		node=GeneMutProcessConfig,
		group='preprocessing'
	)