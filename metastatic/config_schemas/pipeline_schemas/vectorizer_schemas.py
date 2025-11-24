from dataclasses import dataclass, field
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore
from typing import Callable, Any
from collections.abc import Callable
from metastatic.utils.utils import LoggableParamsMixin


# @dataclass
# class TokenizerConfig:
# 	_target_: str = "metastatic.utils.utils.space_tokenizer"


@dataclass
class VectorizerConfig(LoggableParamsMixin):
	_target_: str = MISSING
	def loggable_params(self) -> list[str]:
		return ['_target_']

@dataclass
class TfidfVectorizerConfig(VectorizerConfig):
	_target_: str = 'sklearn.feature_extraction.text.TfidfVectorizer'
	# tokenizer: TokenizerConfig = TokenizerConfig()
	tokenizer: Any = "${get_method:metastatic.utils.utils.space_tokenizer}"



def setup_config():
	cs = ConfigStore.instance()
	cs.store(
		name="tfidf_vectorizer_schema",
		node=TfidfVectorizerConfig,
		group="vectorizers"
	)