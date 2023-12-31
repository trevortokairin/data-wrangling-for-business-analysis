import pandas as pd

def reformatSamples(samples):
    # Check if all samples have the same number of observations
    if samples.groupby('sample').size().nunique() > 1:
        return None

    # Add an observation number within each sample
    samples['observation'] = samples.groupby('sample').cumcount() + 1

    # Pivot the dataframe
    samples_reformat = samples.pivot(index='sample', columns='observation', values='diameter')

    # Rename the columns
    samples_reformat.columns = ['obs.' + str(col) for col in samples_reformat.columns]

    # Reset the index and add 1 to make it start from 1
    samples_reformat.reset_index(inplace=True)
    samples_reformat.index = samples_reformat.index + 1

    return samples_reformat



































