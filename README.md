NASA Asteroid Data Analysis

Overview

This project analyzes asteroid data from a CSV file (nasa.csv) containing information about near-Earth asteroids. The analysis includes data cleaning, processing, statistical insights, and visualizations to explore key characteristics of these asteroids.

Features

Data Preparation

**Loading Data** (load_data)

Reads the CSV file and returns a NumPy ndarray containing the data.

Handles file-related exceptions (e.g., invalid file name, missing file).

**Column Filtering** (scoping_data)

Removes specified columns from the dataset.

**Filtering by Date** (mask_data)

Keeps only asteroids with a close approach date from the year 2000 onward using a boolean mask.

**Data Summary** (data_details)

Cleans the dataset by removing columns Neo Reference ID, Orbiting Body, and Equinox.

Displays the number of rows, columns, and table headers.

**Data Analysis**

**Largest Absolute Magnitude** (max_absolute_magnitude)

Finds the asteroid with the highest absolute magnitude.

**Closest Asteroid to Earth** (closest_to_earth)

Identifies the asteroid with the smallest miss distance in kilometers.

**Most Common Orbits** (common_orbit)

Creates a dictionary with orbit IDs as keys and asteroid counts as values.

**Asteroid Diameter Statistics** (min_max_diameter)

Computes the average of minimum and maximum estimated diameters for all asteroids.

**Data Visualization**

**Histogram of Asteroid Diameters** (plt_hist_diameter)

Plots a histogram of asteroid counts by their average diameter (km) with 10 bins.

**Histogram of Common Orbits** (plt_hist_common_orbit)

Displays a histogram of asteroid distribution across orbit ranges.

**Hazardous Asteroids Pie Chart** (plt_pie_hazard)

Visualizes the percentage of hazardous vs. non-hazardous asteroids.

**Main Function**

The main function executes all tasks in sequence and handles exceptions where necessary.

**Requirements**

Python 3.x

NumPy

Pandas

Matplotlib

Any other necessary dependencies
