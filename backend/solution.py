import pandas as pd


class DataIssueSolver:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def solve_missing_values(self) -> pd.DataFrame:
        for col in self.df.columns:
            if self.df[col].isnull().any():
                if str(self.df[col].dtype).startswith(('float', 'int')):
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                else:
                    mode_vals = self.df[col].mode()
                    fill = mode_vals.iloc[0] if not mode_vals.empty else ""
                    self.df[col].fillna(fill, inplace=True)
        return self.df

    def solve_duplicates(self) -> pd.DataFrame:
        return self.df.drop_duplicates()

