from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel, validator
from typing import Dict, Any
import numpy as np
import mlflow
import os


app = FastAPI()

class DataFrameInput(BaseModel):
    dataframe: Dict[str, Any]  # DataFrame converted to dict
    
    @validator('dataframe')
    def validate_gene_mut_column(cls, v):
        # If using 'columns' orient, check columns list
        if 'gene_mut' not in v:
            raise ValueError("DataFrame must contain 'gene_mut' column")
        return v


tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
if not tracking_uri:
    raise ValueError("MLFLOW_TRACKING_URI environment variable is not set")
mlflow.set_tracking_uri(tracking_uri)

client = mlflow.MlflowClient()
experiment = client.get_experiment_by_name('MetasExperiments')
best_runs = client.search_runs(experiment_ids=[experiment.experiment_id],
							   filter_string="tags.best_run LIKE '%'",
							   order_by=["start_time DESC"]
)
run_id = best_runs[0].info.run_id

model = mlflow.sklearn.load_model(f'runs:/{run_id}/model')



@app.post('/predict_data')
def predict_data(input: DataFrameInput):
    try:
        # Try normal DataFrame creation first (works for lists)
        df = pd.DataFrame(input.dataframe)
    except ValueError:
        # Fall back to single-row if scalar values
        df = pd.DataFrame([input.dataframe])
    
    predictions = model.predict_proba(df)
    return {
        'predicted_probability': predictions.tolist(),
        'num_samples': len(predictions)
    }