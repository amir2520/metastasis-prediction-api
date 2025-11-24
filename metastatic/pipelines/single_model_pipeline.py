from metastatic.pipelines.base_pipeline import BaseSklearnPipeline
from sklearn.pipeline import Pipeline
from sklearn.base import ClassifierMixin
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np
from metastatic.utils.utils import SparseToArray
from imblearn import pipeline


class SingleModelPipeline(BaseSklearnPipeline):
	def __init__(self, model_layer: ClassifierMixin, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model_layer = model_layer
		self.pipeline = self.build_pipeline()

	def build_pipeline(self) -> Pipeline:
		layers = []
		layers.append(('gene_mutation_processor', self.gene_mutation_layer))

		if self.tfidf_vectorizer:
			layers.append(('tfidf', self.tfidf_vectorizer))
		
		if self.dim_reduction_layer:
			layers.append(('dim_reduction', self.dim_reduction_layer))

		if self.resampler_layer:
			layers.append(('resampler', self.resampler_layer))
			layers.append(('sparse_to_array', SparseToArray()))

		if self.scaler_layer:
			layers.append(('scaler', self.scaler_layer))

		layers.append((f'{self.model_layer.__class__.__name__}', self.model_layer))

		model_pipeline = pipeline.Pipeline(layers)
		return model_pipeline

	def cross_validation(self, X: pd.DataFrame, y: pd.Series, cv: int = 5, scoring=None, n_jobs=-1, **kwargs) -> dict:
		pipeline = self.build_pipeline()
		scores = cross_val_score(pipeline, X, y, scoring=scoring, n_jobs=n_jobs, cv=cv, **kwargs)
		return {'scores': scores, 'mean': scores.mean(), 'std': scores.std()}

	def fit(self, X:pd.DataFrame, y: pd.Series) -> "SingleModelPipeline":
		self.pipeline.fit(X, y)
		return self

	def predict(self, X: pd.DataFrame) -> np.ndarray:
		return self.pipeline.predict(X)

	def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
		if hasattr(self.pipeline, 'predict_proba'):
			return self.pipeline.predict_proba(X)
		raise AttributeError(f'{self.model_layer.__class__.__name__} does not support predict_proba')
