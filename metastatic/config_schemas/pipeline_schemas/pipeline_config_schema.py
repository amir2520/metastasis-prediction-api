from dataclasses import dataclass, field
from omegaconf import MISSING
from collections import Counter
from typing import Optional, Any
from collections.abc import Callable
from metastatic.config_schemas.pipeline_schemas import dimension_reduction_schemas
from metastatic.config_schemas.pipeline_schemas import gene_mutation_transformer_schema
from metastatic.config_schemas.pipeline_schemas import model_schemas
from metastatic.config_schemas.pipeline_schemas import vectorizer_schemas
from metastatic.config_schemas.pipeline_schemas import scaler_schemas
from metastatic.config_schemas.pipeline_schemas import resampler_schema
from hydra.core.config_store import ConfigStore


@dataclass
class PipelineConfig:
	gene_mutation_preprocess_layer: gene_mutation_transformer_schema.GeneMutProcessConfig = gene_mutation_transformer_schema.GeneMutProcessConfig()
	vectorizer_layer: Optional[vectorizer_schemas.VectorizerConfig] = vectorizer_schemas.TfidfVectorizerConfig()
	dim_reduction_layer: Optional[dimension_reduction_schemas.DimensionalityReductionConfig] = dimension_reduction_schemas.NMFConfig()
	resampler_layer: Optional[resampler_schema.SMOTEConfig] = None # resampler_schema.SMOTEConfig() 
	scaler_layer: Optional[scaler_schemas.ScalerConfig] = scaler_schemas.StandardScalerConfig()


@dataclass
class SingleModelPipelineConfig(PipelineConfig):
	_target_: str = 'metastatic.pipelines.single_model_pipeline.SingleModelPipeline'
	model_layer: model_schemas.ModelConfig = model_schemas.LogisticRegressionConfig()


@dataclass
class VotingEnsemblePipelineConfig(PipelineConfig):
	_target_: str = MISSING
	model_layers: list[model_schemas.ModelConfig] = MISSING #field(default_factory=lambda: [])


def setup_config():
	resampler_schema.setup_config()
	dimension_reduction_schemas.setup_config()
	gene_mutation_transformer_schema.setup_config()
	model_schemas.setup_config()
	scaler_schemas.setup_config()
	vectorizer_schemas.setup_config()

	cs = ConfigStore.instance()
	cs.store(name = 'single_model_pipeline_schema', node = SingleModelPipelineConfig, group='pipeline')