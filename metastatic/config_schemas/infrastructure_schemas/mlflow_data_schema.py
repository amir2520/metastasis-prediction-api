from dataclasses import dataclass
from omegaconf import SI, MISSING
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
	version: str = MISSING
	dvc_remote_repo: str = 'https://github.com/amir2520/metastasis-data-versioning.git'
	dvc_data_folder: str = 'data/raw'
	github_user_name: str = 'amir2520'
	gcp_project_id: str = SI("${oc.env:DATASET_GCP_PROJECT_ID}")
	github_access_token_secret_id: str = SI("${oc.env:GITHUB_ACCESS_TOKEN_SECRET_ID}")
	X_train_path: str = 'X_train_liver_all.csv'
	X_test_path: str = 'X_test_liver_all.csv'
	y_train_path: str = 'y_train_liver_all.csv'
	y_test_path: str = 'y_test_liver_all.csv'
	counter_path: str = 'metastatic/counter_dir/gene_mut_counter.pkl'


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