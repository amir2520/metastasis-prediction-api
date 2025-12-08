from typing import Optional, Union, Any, Iterable, TYPE_CHECKING, Generator
import dataclasses
from dataclasses import asdict
import importlib
import numpy as np
import scipy.sparse as sp
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from contextlib import contextmanager
from mlflow.tracking.fluent import ActiveRun
import mlflow
from mlflow.pyfunc import PythonModel
from omegaconf import DictConfig, OmegaConf, MISSING
from metastatic.config_schemas.infrastructure_schemas.mlflow_data_schema import MLflowConfig
import logging
import subprocess
import socket
import os
import metastatic

# metastatic_path = os.path.dirname(os.path.dirname(__file__))

MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')

if TYPE_CHECKING:
    from metastatic.config_schemas.config_schema import SingleModelConfig


def run_shell_command(cmd: str) -> str:
    return subprocess.run(cmd, text = True, shell = True, check = True, capture_output = True).stdout


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f'[{socket.gethostname()}] {name}')


def space_tokenizer(s: str) -> list[str]:
	return s.split()


class LoggableParamsMixin:
    def loggable_params(self) -> list[str]:
        return []


class SparseToArray(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass
    
    def fit(self, X: Union[np.ndarray, sp.spmatrix], y: Optional[Union[np.ndarray, pd.Series]] = None) -> "SparseToArray":
        return self
    
    def transform(self, X: Union[np.ndarray, sp.spmatrix]) -> np.ndarray:
        return X.toarray() if sp.issparse(X) else X


@contextmanager
def activate_mlflow(
    experiment_name: Optional[str] = None,
    run_name: Optional[str] = None,
    run_id: Optional[str] = None
) -> Iterable[mlflow.ActiveRun]:
    set_experiment(experiment_name)
    run: ActiveRun
    with mlflow.start_run(run_name=run_name, run_id=run_id) as run:
        yield run


def set_experiment(experiment_name: Optional[str] = None) -> None:
    if experiment_name is None:
        experiment_name = 'Default'
    try:
        mlflow.create_experiment(experiment_name)
    except mlflow.exceptions.RestException:
        pass
    mlflow.set_experiment(experiment_name)


def log_training_hparams_single_model(config: "SingleModelConfig") -> None:
    structured_config = OmegaConf.to_object(config.single_model)
    logged_nodes = set()
    def loggable_params(node: Any, path: list[str]) -> Generator[tuple[str, Any], None, None]:
        current_path = ".".join(path) if path else "root"       
        if isinstance(node, LoggableParamsMixin) and id(node) not in logged_nodes:
            for param_name in node.loggable_params():
                param_value = getattr(node, param_name)
                full_key = ".".join(path + [param_name])
                yield full_key, param_value
            logged_nodes.add(id(node))
        
        children = None
        if isinstance(node, (dict, DictConfig)):
            try:
                children = node.items()
            except Exception as e:
                return
        elif dataclasses.is_dataclass(node):
            children = ((f.name, getattr(node, f.name)) for f in dataclasses.fields(node))
        if children is None:
            return
        
        for key, val in children:
            if isinstance(val, type(MISSING)):
                continue
            try:
                for item in loggable_params(val, path + [key]):
                    yield item
            except Exception as e:
                continue
    
    params = dict(loggable_params(structured_config, []))
    mlflow.log_params(params)



def get_client() -> mlflow.tracking.MlflowClient:
    return mlflow.tracking.MlflowClient(MLFLOW_TRACKING_URI)


def get_all_experiment_ids() -> list[str]:
    return [exp.experiment_id for exp in mlflow.search_experiments()]


def get_best_run() -> dict[str, Any]:
    best_runs = mlflow.search_runs(get_all_experiment_ids(), filter_string="tag.best_run LIKE 'v%'")
    if len(best_runs) == 0:
        return {}

    indices = best_runs["tags.best_run"].str.split("v").str[-1].astype(int).sort_values()
    best_runs = best_runs.reindex(index=indices.index)
    best_runs_dict: dict[str, Any] = best_runs.iloc[-1].to_dict()
    return best_runs_dict


def log_model(
    mlflow_config: MLflowConfig, 
    new_best_run_tag: str, 
    registered_model_name: str,
    trained_pipeline: Any  
) -> None:
    experiment_name = mlflow_config.experiment_name
    run_id = mlflow_config.run_id
    run_name = mlflow_config.run_name
    
    with activate_mlflow(experiment_name=experiment_name, run_id=run_id, run_name=run_name) as _:
        # Log the actual sklearn pipeline
        mlflow.sklearn.log_model(
            sk_model=trained_pipeline,
            artifact_path="model",
            registered_model_name=registered_model_name,
            # code_path=[metastatic_path]
        )
        mlflow.set_tag("best_run", new_best_run_tag)


def custom_instantiate(config: Any) -> Any:
    if isinstance(config, DictConfig):
        config_as_dict = OmegaConf.to_container(config, resolve=True)
    else:
        config_as_dict = asdict(config)
    # config_as_dict = asdict(config)
    if "_target_" not in config_as_dict:
        raise ValueError("config does not have _target_ key")

    _target_ = config_as_dict['_target_']
    _partial_ = config_as_dict.get('_partial_', False)

    config_as_dict.pop('_target_', None)
    config_as_dict.pop('_partial_', None)
    splitted_target = _target_.split('.')
    module_name, class_name = '.'.join(splitted_target[:-1]), splitted_target[-1]

    module = importlib.import_module(module_name)
    _class = getattr(module, class_name)
    if _partial_:
        return partial(_class, **config_as_dict)
    return _class(**config_as_dict)