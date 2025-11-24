from sklearn.base import TransformerMixin, BaseEstimator
from collections import Counter
import pandas as pd
from typing import Optional
from metastatic.utils.io_utils import open_file
import pickle


class GeneMutProcess(BaseEstimator, TransformerMixin):
    def __init__(self, gene_counter_path: str, include_rare: bool, rare_threshold: int, gene_col: str) -> None:
        self.include_rare = include_rare
        self.rare_threshold = rare_threshold
        self.gene_counter_path = gene_counter_path

        gene_counter_file = open_file(path=self.gene_counter_path, mode='rb')
        gene_counter = pickle.load(gene_counter_file)
        
        self.gene_counter = gene_counter
        self.non_rare_list = [key for key, val in self.gene_counter.items() if val >= self.rare_threshold]
        self.gene_col = gene_col

        
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "GeneMutProcess":
        return self
    
    def mut_process(self, row) -> str:
        mut = row[self.gene_col]
        final_result = ''
        try:
            for each_gene in mut.split(', '):
                for each_mut in each_gene.split(' - '):
                    each_mut = each_mut.replace(' ', '_')
                    #final_result += (each_mut + ' ')
                    if each_mut in self.non_rare_list:
                        final_result += (each_mut+ ' ')
                    if self.include_rare:
                        gene = each_mut.split('_')[0]
                        if gene != '':
                            final_result += (gene + '_rare ')
        except:
            pass
        final_result = final_result.strip()
        return final_result   
    
    def transform(self, X: pd.DataFrame) -> pd.Series:
        X = X.copy()
        X = X.apply(self.mut_process, axis = 1)
        return X