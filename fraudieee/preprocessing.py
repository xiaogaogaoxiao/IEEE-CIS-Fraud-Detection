from sklearn.base import BaseEstimator, TransformerMixin

from .utils import find_and_replace


class Nan2CatConverter(BaseEstimator, TransformerMixin):
    """Converts NaN to separate category.

    Parameters
    ----------
    columns : list-like, optional (default=None)
        Columns where NaNs are converted to separate category. If not
        specified takes all of the DataFrame columns.
    nan_category : str, optional (default="NaN")
        Name of the newly created category if the column is of the
        `category` data type.
    """
    def __init__(self, columns=None, nan_category="NaN"):
        self.columns = columns
        self.nan_category = nan_category

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        columns = X_new.columns if self.columns is None else self.columns
        cat_columns = set(columns).intersection(
            X_new.columns[X_new.dtypes == "category"]
        )
        for col in cat_columns:
            X_new[col] = X_new[col].cat.add_categories(self.nan_category)
        X_new[columns] = X_new[columns].fillna(self.nan_category)

        return X_new


class ManualColumnGrouper(BaseEstimator, TransformerMixin):
    """Groups columns in accordance with the guidelines provided.

    Parameters
    ----------
    column : str
        Name of the column to group.
    replace_pairs : dict-like
        Dictionary-like object where key is the value that will be imputed
        to the selected values. Values' selection is defined in the values
        assigned to key, which should also be a dictionary containing two
        keys. First key: `regex` with regex sentence assigned as string,
        second key: `case` is the boolean value mentioning whether regex
        should be case-sensitive. Alternatively you can pass a string
        instead of dictionary-like object but then automatically regex will
        be case-insensitive.
    group_others : bool, optional (default=False)
        Flag indicating whether not matched records should be group into
        a separate group.
    other_name : str, optional (default="Other")
        Name of the group for unselected records. Valid only if
        `group_others` is set to `True`.
    """
    def __init__(self, column, replace_pairs, group_others=False,
                 other_name="Other"):
        self.column = column
        self.replace_pairs = replace_pairs
        self.group_others = group_others
        self.other_name = other_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        for name, command in self.replace_pairs.items():
            try:
                regex = command["regex"]
                case = command["case"]
            except TypeError:
                regex = command
                case = False
            find_and_replace(
                df=X_new,
                column=self.column,
                regex_sentence=regex,
                replace_value=name,
                case=case,
                inplace=True
            )
        if self.group_others:
            other_sentence = (
                "^("
                + "|".join(list(self.replace_pairs.keys()))
                + ")$"
            )
            X_new.loc[
                ~X_new[self.column].str.contains(
                    other_sentence, case=True, na=False
                ),
                self.column
            ] = self.other_name

        return X_new
