def func():
    # Implement your logic here
    def bin_numerical_features(df, bins, columns):
        import pandas as pd
        import math

        binning_info = {}
        for col, bin_size in zip(columns, bins):
            min_val = math.floor(df[col].min())
            max_val = math.ceil(df[col].max())
            num_bins = int((max_val - min_val) / bin_size) + 1
            bins_range = [
                (min_val + i * bin_size, min_val + (i + 1) * bin_size)
                for i in range(num_bins)
            ]
            bin_labels = [f"{start}-{end}" for start, end in bins_range]
            df[f"{col}_grouped_{bin_size}_bins"] = pd.cut(
                df[col],
                bins=[start for start, end in bins_range] + [max_val + 1],
                labels=bin_labels,
                include_lowest=True,
            )
            binning_info[col] = {
                "min": min_val,
                "max": max_val,
                "num_bins": num_bins,
                "bin_size": bin_size,
                "bin_ranges": bins_range,
            }
        return df, binning_info

    return bin_numerical_features


bin_numerical_features = func()
