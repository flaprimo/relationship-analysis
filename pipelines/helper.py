def df_tostring(df, rows=None):
    return f'  shape: {df.shape}\n' \
        f'  dataframe ({"first " + str(rows) if rows else "all"} rows):\n{df.head(rows).to_string()}\n'


def pass_results_pipeline(from_results, to_results, r_names):
    for name in r_names:
        to_results[0][name] = from_results[0][name]
        to_results[1][name] = from_results[1][name]

    return to_results


def remove_results_orchestrator(results):
    return {dataset_name: (None, dataset_result[1])
            for dataset_name, dataset_result in results.items()}
