import structlog

import numpy as np

from scipy.stats import norm


logger = structlog.get_logger('__name__')


def identify_outliers_z_score(data, threshold=3):
    mean, std = np.mean(data), np.std(data)
    z_score = np.abs((data - mean) / std)
    outliers_mask = z_score < threshold
    logger.info(f'z-score of {threshold} corresponds to a prob of'
                f' {100 * 2 * norm.sf(3):0.2f}%')
    logger.info(f'Rejection {(~outliers_mask).sum()} points')
    return outliers_mask


def filter_nan_lines(data):
    return ~data.isna().all(1) & ~data['price'].isna()


def remove_filtered_lines(data, filter_function):
    logger.info(f'Input data contains {data.shape[0]} rows.')
    _data = data[filter_function(data)]
    logger.info(f'Output data contains {_data.shape[0]} rows.')
    return _data


def flag_outliers(data, column, threshold):
    _data = data.copy()
    _data['is_outlier'] = ~identify_outliers_z_score(
        data[column], threshold=threshold)
    return _data


def clean_data(data):
    return data.pipe(
        remove_filtered_lines, filter_function=filter_nan_lines
    ).pipe(
        flag_outliers, column='price', threshold=1
    )
