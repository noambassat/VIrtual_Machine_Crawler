import pandas as pd
import numpy as np


def print_dataframe(df, desired_width, n_of_cols):

    np.set_printoptions(linewidth=desired_width)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 3)


    print(df)
