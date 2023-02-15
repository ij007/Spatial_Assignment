# -*- coding: utf-8 -*-
"""Spatic asssignment.ipynb

Original file is located at
    https://colab.research.google.com/drive/1KCeMg41amwj6lDrO_q1T2GrYpqwKAGfY
"""

# Install geopy package
#!pip install geopy

import pandas as pd
from geopy import distance

def Distance(d1, d2):
    '''
    Parameters:
    d1 = (latitude, longitude)
    d2 = (latitude, longitude)

    Returns: Distance between two coords in kilometers.
    '''
    return distance.distance(d1, d2).km

def levenshtein_distance(s1, s2):
    """
    Parameters:
    s1 = string 1
    s2 = string 2
    
    Returns:
    Levenshtein distance between two strings
    """
    # If the first string is shorter than the second, recursively swap the strings
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    # If the second string is empty, return the length of the first string
    if len(s2) == 0:
        return len(s1)
    # Initialize the first row with incremental values from 0 to the length of the second string
    previous_row = range(len(s2) + 1)
    # Loop through each character in the first string
    for i, c1 in enumerate(s1):
        # Initialize the current row with the incremental index and the first value set to i+1
        current_row = [i + 1]
        # Loop through each character in the second string
        for j, c2 in enumerate(s2):
            # Calculate the minimum edit distance from three possible operations: insertion, deletion, and substitution
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        # Set the current row as the previous row for the next iteration
        previous_row = current_row
    # Return the last element in the final row, which represents the minimum edit distance between the two strings
    return previous_row[-1]

def is_similar_name(name1, name2, threshold=5):
    """
    Check if two names are similar using the Levenshtein distance algorithm.
    """
    # Calculate the Levenshtein distance between two lowercase strings
    distance = levenshtein_distance(name1.lower(), name2.lower())
    # If the distance is less than or equal to the threshold, the names are considered similar
    return distance <= threshold

# Read the CSV file into a pandas dataframe
df = pd.read_csv('assignment_data.csv')
# Create a new column called 'is_similar' initialized with zeros and concatenate it with the original dataframe
is_similar = pd.DataFrame([0]*len(df), columns=['is_similar'])
df = pd.concat([df, (is_similar)], axis=1)

# Write the modified dataframe to a new CSV file
df.to_csv('output.csv')
