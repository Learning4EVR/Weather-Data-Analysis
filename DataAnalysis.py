import csv

# STEP 0: You will have a few file wide variables that make matching indexes to
# the csv file. You will want to figure out the column index of the date and temperature.
# We called our variables date_index and temp_index

date_index = 0
time_index = 1
temp_index = 2
wind_index = 3


# STEP 1: csv_reader(file)
# reads a file using csv.reader, and adds the rows into a list to return.
# as the csv file has a header, you will want to skip the first row or remove
# it somehow

def csv_reader(file, delim):
    contents = []
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        next(reader, None)

        for row in reader:
            contents.append(row)

    return contents


# STEP 2: client_input()
# Prompts the client for a date, the data can be a day, month or year or all combined. The prompt will be as follows:
# > Please enter a filter:
# you do not have to error check to see if it is valid.
# this can be a simple one line function that returns the answer to input(question)

def client_input():
    return input("Please enter a filter: ")


# Step 3: average_temperature(weather, filter)
# params: weather = list of weather values
#         filter - (day, month, or year, or other combinations)
# return: float
# using the provided filter (hint: use 'if date in (value in date index)') find the average temperature

def average_temperature(weather, filter):
    values = []
    for row in weather:
        if filter in row[date_index]:
            values.append(float(row[temp_index]))

    return sum(values) / len(values)


# Step 4: maximum_temperature(weather, filter)
# params: weather = list of weather values
#         filter - (day, month, or year, or other combinations)
# return: float
# Same as average, but instead returns the maximum temperature based on a filtered date value
# hint: start with a really low number for max temp (-99999)

def maximum_temperature(weather, filter):
    values = []
    for row in weather:
        if filter in row[date_index]:
            values.append(float(row[temp_index]))

    return max(values)


# Step 5: minimum_temperature(weather, filter)
# params: weather = list of weather values
#         filter - (day, month, or year, or other combinations)
# return: float
# Same as maximum, but instead returns the lowest/minimum temperature based on a filtered date value
# hint: if using a loop start with a really high number for min temp (99999)

def minimum_temperature(weather, filter):
    values = []
    for row in weather:
        if filter in row[date_index]:
            values.append(float(row[temp_index]))

    return min(values)


# Step 6: run()
# param: none
# return: none
# This function will be used to test all the functions you created above, and also so you have a working program
# you can use to perform an analysis on various dates. Don't forget to use .format() to format with the
# required number of decimal places.

def run():
    data = csv_reader("Temperatures.csv")
    date_filter = client_input()
    print(f"Average Temperature for {date_filter}: {average_temperature(data, date_filter):.2f}")
    print(f"Maximum Temperature for {date_filter}: {maximum_temperature(data, date_filter):.2f}")
    print(f"Minimum Temperature for {date_filter}: {minimum_temperature(data, date_filter):.2f}")


def tests():
    data = csv_reader("LovelandTemperatures", "\t")

    with open("LovelandTemps.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=",")

        for row in data:
            # print(row)
            writer.writerow(row)

    print(data[0])

    date_filter = client_input()

    print(f"{average_temperature(data, date_filter):.2f}")

    print(f"{maximum_temperature(data, date_filter):.2f}")

    print(f"{minimum_temperature(data, date_filter):.2f}")


# uncomment these lines of code after finishing your run() function, so it can autorun
if __name__ == '__main__':
    # run()
    tests()
