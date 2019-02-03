def df_tostring(df, rows=None):
    return f'  shape: {df.shape}\n' \
        f'  dataframe ({"first " + str(rows) if rows else "all"} rows):\n{df.head(rows).to_string()}\n'
