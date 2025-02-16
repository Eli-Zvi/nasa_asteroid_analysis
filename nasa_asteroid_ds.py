# Ilay Zvi_324125657
"""
@Project: Mamman15
nasa_asteroid_ds.py - defines functions for analyzing asteroid data
@Author : Ilay Zvi
@semester : 24b
"""
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_name):
    """
    loads data from a given file
    @param file_name - the name of the file, assumes that the file is in the same folder as the project
    @return - a numpy array with the loaded data
    """
    try:
        data = np.genfromtxt(file_name, dtype=None, delimiter=',')
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_name} file not found")
    except OSError:
        raise OSError("Unable to open file", file_name)

    return data


def scoping_data(data, names):
    """
    removes the given columns given in the array names from the given data
    @param data - data to be parsed
    @param names - columns to be removed
    @return - data without the given columns
    """
    if isinstance(names, str):  # if we get a string on accident we can just make it into a list with one item
        names = [names]

    indices = []

    # I could've used np.where, but I didn't want to change it since it works, and it couldn't be anymore "optimized"
    # finds the indices of the columns that we want to remove
    for i in range(len(data[0])):
        temp = data[0][i].lower()
        for j in range(len(names)):
            if temp == names[j].lower():
                indices.append(i)
                break

    new_data = np.delete(data, indices, axis=1)  # axis = 1 to delete the columns

    return new_data


def mask_data(data):
    """
    Remove all asteroids that their close approach date is under 2000 and returns the new data numpy array
    @param data - data to be parsed
    @return - data with their Close Approach Date's year over 1999
    """
    header = data[0]  # store headers

    try:
        column = np.where(data[0] == "Close Approach Date")[0][0]  # find index of "Close Approach Date"
    except IndexError:
        raise IndexError("Column Close Approach Date does not exist")

    column_data = data[1:, column:column + 1]  # get the dates
    years = []  # initialize a list for all the years

    for i in range(len(column_data)):
        years.append(int(column_data[i][0].split('-')[0]))  # split and store the years from each row

    years = np.array(years)  # convert list to numpy array
    mask = years > 1999  # mask for years
    masked_data = np.vstack((header, data[1:][mask]))  # add the header after applying mask to data

    return masked_data


def data_details(data):
    """
    Removes the columns Equinox, Orbiting Body, Neo Reference ID from data and displays its shape
    @param data - data to be parsed
    """
    modified_data = scoping_data(data, ["Neo Reference ID", "Orbiting Body", "Equinox"])
    size = modified_data.shape  # get the shape of the array

    print(f"Number of rows: {size[0]} \nNumber of columns: {size[1]}\nHeaders: {modified_data[0]}")


def max_absolute_magnitude(data):
    """
    Finds the asteroid with the highest Absolute Magnitude and returns its name and its magnitude as a tuple
    @param data - data to be parsed
    @return - a tuple containing the name and magnitude of the asteroid with the highest absolute magnitude
    """
    max_magnitude_index = 1  # start from 1 cus 0 is the header row

    try:
        am_column_index = np.where(data[0] == "Absolute Magnitude")[0][0]  # find index of "Absolute Magnitude"
        name_index = np.where(data[0] == "Name")[0][0]  # find index of "Name"
    except IndexError:
        raise IndexError("Column Absolute Magnitude or Name does not exist")

    # compare all asteroid's absolute magnitude
    for i in range(2, len(data)):
        if float(data[i][am_column_index]) > float(data[max_magnitude_index][am_column_index]):
            max_magnitude_index = i

    return int(data[max_magnitude_index][name_index]), float(data[max_magnitude_index][am_column_index])


def closest_to_earth(data):
    """
    Finds the asteroid closest to earth based on the column Miss Dist.(kilometers) and returns its name
    @param data - data to be parsed
    @return - the name of the asteroid closest to earth
    """
    closest = 1

    try:
        md_column = np.where(data[0] == "Miss Dist.(kilometers)")[0][0]
        name_column = np.where(data[0] == "Name")[0][0]
    except IndexError:
        raise IndexError("Column Miss Dist.(kilometers) or Name does not exist")

    # compare all asteroid's distance
    for i in range(2, len(data)):
        if float(data[i][md_column]) > float(data[closest][md_column]):
            closest = i

    return int(data[closest][name_column])


def common_orbit(data):
    """
    Returns a dictionary of the Orbit ID and the number of asteroids that correlate with the ID
    @param data - data to be parsed
    @return - dictionary
    """
    try:
        orbit_column = np.where(data[0] == "Orbit ID")[0][0]
    except IndexError:
        raise IndexError("Column Orbit ID does not exist")

    orbit_dict = {}

    for i in range(1, len(data)):
        try:  # if the ID exists in the dictionary increment the number of found asteroids
            orbit_dict[data[i][orbit_column]] += 1
        except KeyError:  # if ID does not exist in the dictionary add a new ID
            orbit_dict.update({str(data[i][orbit_column]): 1})

    return orbit_dict


def min_max_diameter(data):
    """
    Calculates and returns the min and max average diameter in KM of all the asteroids as a tuple
    @param data - data to be parsed
    @return - tuple containing the min and max average diameter of all the asteroids
    """
    try:
        min_col = np.where(data[0] == "Est Dia in KM(min)")[0][0]
        max_col = np.where(data[0] == "Est Dia in KM(max)")[0][0]
    except IndexError:
        raise IndexError("Column Est Dia in KM(min) or Est Dia in KM(max) does not exist")

    # calculate sum and average of the min and max diameter of asteroids
    min_data = data[1:, min_col].astype(float).sum()
    max_data = data[1:, max_col].astype(float).sum()
    min_avg = min_data / (len(data) - 1)
    max_avg = max_data / (len(data) - 1)

    return float(min_avg), float(max_avg)


def plt_hist_diameter(data):
    """
    displays a histogram of the average diameter of the asteroids in data
    @param data - data to be parsed
    """
    try:
        min_col = np.where(data[0] == "Est Dia in KM(min)")[0][0]
        max_col = np.where(data[0] == "Est Dia in KM(max)")[0][0]
    except IndexError:
        raise IndexError("Column Est Dia in KM(min) or Est Dia in KM(max) does not exist")

    # convert min and max diameter columns into floats and sort them after calculating their average
    min_data = data[1:, min_col:min_col + 1].astype(float)
    max_data = data[1:, max_col:max_col + 1].astype(float)
    avg_data = np.sort((min_data + max_data) / 2, axis=0)

    plt.title("Histogram of Average Diameters of Asteroids")
    plt.xlabel("Average Diameter (km)")
    plt.ylabel("Number of Asteroids")
    plt.grid(True)
    # the edges of the graph will be the average min and max distance, we will create an x-axis that fits those values
    edges = min_max_diameter(data)
    bin_x_axis = np.linspace(edges[0], edges[1], 11)

    # plot histogram with the data and bins we've calculated
    plt.hist(avg_data, bins=bin_x_axis, color='steelblue', edgecolor='black')
    plt.show()


def plt_hist_common_orbit(data):
    """
    displays a histogram of the number of asteroids according to their ID (with each bin having a range of 100 IDs)
    @param data - data to be parsed
    """
    orbit_dic = common_orbit(data)
    id_count = [0]  # used to store the number of asteroids in each bin, index 0 is bin 0-99 and so on

    for key in orbit_dic:
        temp = int(key) // 100

        if temp >= len(id_count):  # if we find a new range of keys, we need to add more bins
            for i in range((temp - len(id_count)) + 1):  # adds the number of missing bins
                id_count.append(0)

        id_count[temp] += orbit_dic[key]  # increment the number of asteroids correlating with the range of the ID

    # create bins according to the number of different bins in id_count
    bin_x_axis = np.linspace(0, (len(id_count) - 1) * 100, len(id_count))
    plt.xlabel("Minimum Orbit Intersection")
    plt.ylabel("Number of Asteroids")
    plt.title("Histogram of Asteroids by Minimum Orbit Intersection")
    plt.grid(True)

    # plot histogram with the data and bins we've calculated
    plt.hist(bin_x_axis, weights=id_count, bins=bin_x_axis, color='steelblue', edgecolor='black')
    plt.show()


def plt_pie_hazard(data):
    """
    display a pie chart with 2 different classifiers, hazardous and non-hazardous and their percentages
    @param data - data to be parsed
    """
    try:
        hazard_col = np.where(data[0] == "Hazardous")[0][0]
    except IndexError:
        raise IndexError("Column Hazardous does not exist")

    classifiers = ["Hazardous", "Non-Hazardous"]  # define classifiers
    cols = ['red', 'green']  # define colors for each classifier

    hazard_list = [10000, 0]  # initialize counter for each classifier

    # count the number of asteroids correlating with each classifier
    for i in range(len(data)):
        if data[i][hazard_col] == "True":
            hazard_list[0] += 1
        else:
            hazard_list[1] += 1

    # plot pie using the data we've found - add formatting to the percentages and rotate the starting angle of the chart
    plt.pie(hazard_list, labels=classifiers, colors=cols, autopct='%1.1f%%', startangle=150)
    plt.title("Percentage of Hazardous and Non-Hazardous Asteroids")
    plt.show()


def main():
    # I hope this main is done as requested - Thank you for the course :)

    while True:
        file_name = input("Please enter the name of the csv file you want to load\n"
                          "Do not add the file type after the name of the csv file\n")
        try:
            data = load_data(file_name + ".csv")
            break
        except (OSError, FileNotFoundError) as e:
            print(e)

    # There were no errors to take care of in this section once the data was properly loaded

    print("****************************** scoping_data ******************************")
    print(scoping_data(data, ["Neo Reference ID"]))  # remove Neo Reference ID column

    print("****************************** mask_data ******************************")
    # remove all asteroids with Close Approach Date that is less than 2000
    print(mask_data(data)[:, np.where(data[0] == "Close Approach Date")[0]])

    print("****************************** data_details ******************************")
    data_details(scoping_data(data, 'Name'))  # will remove column Name first and then test data_details

    print("****************************** max_absolute_magnitude ******************************")
    max_absolute_result = max_absolute_magnitude(data)
    print(f"ID: {max_absolute_result[0]}\nMagnitude: {max_absolute_result[1]}")

    print("****************************** closest_to_earth ******************************")
    print(f"ID: {closest_to_earth(data)}")

    print("****************************** common_orbit ******************************")
    orbit_dic = common_orbit(data)
    for key in orbit_dic:
        print(f"Orbit ID: {key}, Number of Asteroids: {orbit_dic[key]}")

    print("****************************** min_max_diameter ******************************")
    min_max_tuple = min_max_diameter(data)
    print(f"Average Minimum Estimated Diameter in KM: {min_max_tuple[0]}\n"
          f"Average Maximal Estimated Diameter in KM: {min_max_tuple[1]}")

    print("****************************** plt_hist_diameter ******************************")
    plt_hist_diameter(data)

    print("****************************** plt_hist_common_orbit ******************************")
    plt_hist_common_orbit(data)

    print("****************************** plt_hist_pie_hazard ******************************")
    plt_pie_hazard(data)


main()
