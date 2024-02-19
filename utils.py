import os
import textwrap

def glimpse(df, col_width=None, type_width=None, num_examples=None):
    """
    Prints a summary of the given pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to summarize.
    col_width : int, optional
        The width of the column names in characters. Defaults to None.
    type_width : int, optional
        The width of the column data types in characters. Defaults to None.
    num_examples : int, optional
        The number of rows to include in the preview of the data. Defaults to None, which shows the first 5 rows.

    Returns
    -------
    None

    Notes
    -----
    This function prints the number of rows and columns in the DataFrame, and a preview of the data.
    The preview includes the column names, data types, and a few rows of data.
    The data values are colored based on their data type: strings are purple, and other data types are blue.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
    >>> glimpse(df)
    Rows: 3
    Columns: 2

    A  int64  [1 2 3]
    B  object ['a' 'b' 'c']
    """
    terminal_width = os.get_terminal_size().columns
    if col_width is None:
        col_width = max([len(col) for col in df.columns])
    if type_width is None:
        type_width = max([len(str(df[col].dtype)) for col in df.columns])
    print(f"")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"")
    for col in df.columns:
        if df[col].dtype == "object":
            color = "\033[35m"
        else:
            color = "\033[96m"
        if num_examples is None:
            values = df[col].head().values
        else:
            values = df[col].head(num_examples).values
        line = f"\033[34m{col:<{col_width}}\033[0m \033[38;5;94m{str(df[col].dtype):<{type_width}}\033[0m {color}{values}\033[0m"
        if len(line) > terminal_width:
            wrapper = textwrap.TextWrapper(width=terminal_width, subsequent_indent=" " * (col_width + type_width + 3))
            line = wrapper.fill(line)
        print(line)
    print(f"")
