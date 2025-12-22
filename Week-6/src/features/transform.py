import pandas as pd
import numpy as np

def transform_single_input(payload: dict, feature_columns: list):

    df = pd.DataFrame([payload])

    df = df.reindex(columns=feature_columns, fill_value=0)

    return df.values
