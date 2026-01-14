from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier


def select_features(X, y):

    model = RandomForestClassifier(
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
