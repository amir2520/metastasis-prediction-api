from dataclasses import dataclass
from omegaconf import SI
from typing import Optional
from hydra.core.config_store import ConfigStore


@dataclass
class MLflowConfig:
	mlflow_internal_tracking_uri: str = SI("${oc.env:MLFLOW_INTERNAL_TRACKING_URI,localhost:6101}")
	experiment_name: str = "MetasExperiments"
	run_name: Optional[str] = None
	run_id: Optional[str] = None
	experiment_id: Optional[str] = None


@dataclass 
class DataConfig:
	X_train_path: str = 'metastatic/datasets/X_train_liver_all.csv'
	X_test_path: str = 'metastatic/datasets/X_test_liver_all.csv'
	y_train_path: str = 'metastatic/datasets/y_train_liver_all.csv'
	y_test_path: str = 'metastatic/datasets/y_test_liver_all.csv'
	counter_path: str = 'metastatic/datasets/gene_mut_counter.pkl'


@dataclass
class InfrastructureConfig:
	mlflow: MLflowConfig = MLflowConfig()
	data: DataConfig = DataConfig()


def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name='infrastructure_schema',
		node=InfrastructureConfig,
		group='infrastructure'
	)