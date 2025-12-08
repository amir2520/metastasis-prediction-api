from typing import Optional
from dataclasses import dataclass
from hydra.core.config_store import ConfigStore
from metastatic.config_schemas.infrastructure_schemas import mlflow_data_schema
from metastatic.config_schemas.pipeline_schemas import pipeline_config_schema
from metastatic.config_schemas import model_selector_schemas
from metastatic.config_schemas.dask_schemas import gcp_cluster_schema



@dataclass
class BaseConfig:
	infrastructure: mlflow_data_schema.InfrastructureConfig = mlflow_data_schema.InfrastructureConfig()
	cluster: gcp_cluster_schema.DaskGCPClusterConfig = gcp_cluster_schema.DaskGCPClusterConfig()
	registered_model_name: Optional[str] = "metastatic_model"


@dataclass
class SingleModelConfig(BaseConfig):
	pipeline: pipeline_config_schema.SingleModelPipelineConfig = pipeline_config_schema.SingleModelPipelineConfig()
	model_selector: Optional[model_selector_schemas.MetastaticDetectionModelSelectorConfig] = model_selector_schemas.MetastaticDetectionModelSelectorConfig()



def setup_config():
	mlflow_data_schema.setup_config()
	pipeline_config_schema.setup_config()
	model_selector_schemas.setup_config()
	gcp_cluster_schema.setup_config()

	cs = ConfigStore.instance()
	cs.store(
		name='single_model_config_schema',
		node=SingleModelConfig,
		group='single_model'
	)

