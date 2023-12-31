import os
import pandas as pd
from fnmatch import fnmatch


def combineSamples(pattern, path='.', control_samples=None):
    result = {}

    # Get list of matching files
    files = [f for f in os.listdir(path) if fnmatch(f, pattern)]

    if not files:
        return result

    # Sort the files by the numerical part of the filename

    result['pattern'] = pattern
    result['path'] = path
    result['filenames'] = files
    result['files'] = len(files)

    # Read data from files into samples dataframe
    samples = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    # Check if DataFrame is not empty and the first column exists
    if not samples.empty and samples.columns[0]:
        samples.rename(columns={samples.columns[0]: 'sample'}, inplace=True)

    # Set 'sample' column as index, keeping the column in the dataframe
    samples.set_index('sample', drop=False, inplace=True)

    result['samples'] = samples

    # Determine control samples
    if control_samples is None:
        control_samples = int(len(files) * 0.6)
    control_samples = min(control_samples, len(samples))  # Ensure control_samples does not exceed total samples
    result['control_samples'] = control_samples

    # Split into control and test
    result['control'] = samples.iloc[:control_samples]
    result['test'] = samples.iloc[control_samples:]

    return result






















































































