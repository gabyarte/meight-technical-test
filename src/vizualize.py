import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_data(data, label='Price'):
    fig = plt.figure(figsize=(12, 10))

    plt.subplot(2, 2, 1)
    data.hist(bins=50, label=label, alpha=0.6)
    plt.axvline(np.mean(data), ls='--', c='r', label='Mean')
    plt.axvline(np.median(data), ls=':', c='g', label='Median')
    plt.ylabel('Counts')
    plt.title(f'{label} Distribution')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.scatter(data,
                np.random.normal(7, 0.2, size=data.shape[0]),
                alpha=0.5)
    plt.title(f'{label} Distribution')

    plt.subplot(2, 2, 3)
    sns.boxplot(y=data)

    plt.subplot(2, 2, 4)
    sns.violinplot(y=data, inner='quartile', bw_method=0.2)
    return fig


def plot_outliers(data, outliers_mask, threshold):
    visual_scatter = np.random.normal(size=data.shape[0])
    fig, ax = plt.subplots()
    ax.scatter(data[outliers_mask],
                visual_scatter[outliers_mask],
                s=10,
                label='Good',
                color='#4CAF50')
    ax.scatter(data[~outliers_mask],
                visual_scatter[~outliers_mask],
                s=10,
                label='Bad',
                color='#F44336')
    ax.legend()
    plt.title(f'Outliers ({threshold=})')
    return fig
