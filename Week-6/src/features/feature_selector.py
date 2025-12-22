from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestRegressor


def select_features(X, y):

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    selector = SelectFromModel(
        model,
        threshold="median"
    )

    selector.fit(X, y)
    return selector
