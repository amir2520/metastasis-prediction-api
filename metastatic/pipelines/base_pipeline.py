from typing import Union, Optional, Any
from collections.abc import Callable
# from collections import Counter
from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from metastatic.preprocess.gene_mutation_transformer import GeneMutProcess

from metastatic.utils.io_utils import open_file

from imblearn.base import BaseSampler



class BaseSklearnPipeline(ABC):
	def __init__(
		self,
		gene_mutation_preprocess_layer: GeneMutProcess,
		vectorizer_layer: Optional[TfidfVectorizer] = None,
		dim_reduction_layer: Optional[BaseEstimator] = None,
		resampler_layer: Optional[BaseSampler] = None,
		scaler_layer: Optional[BaseEstimator] = None
	) -> None:


		self.gene_mutation_layer = gene_mutation_preprocess_layer
		self.tfidf_vectorizer = vectorizer_layer
		self.dim_reduction_layer = dim_reduction_layer
		self.resampler_layer = resampler_layer
		self.scaler_layer = scaler_layer


	@abstractmethod
	def cross_validation(self, X: pd.DataFrame, y: pd.Series, cv: int = 5, scoring=None, n_jobs=-1) -> list[float]:
		...

	@abstractmethod
	def build_pipeline(self) -> Pipeline:
		...

	@abstractmethod
	def fit(self, X: pd.DataFrame, y: pd.Series) -> "BaseSklearnPipeline":
		...

	@abstractmethod
	def predict(self, X: pd.DataFrame) -> np.ndarray:
		...

	@abstractmethod
	def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
		...








