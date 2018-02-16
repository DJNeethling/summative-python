import random  # used to generate data entries
import datetime  # used to log time of errors
import time  # time is used to create delay in data input loop

def generate_sensor():  # this function generates the sensor dataset
    w, h = 16, 32 # defines 32 sensors with 16 entries
    matrix = [[random.random() for x in range(w)] for y in range(h)] # populates sensor entries with random values between 0 and 1
    return matrix  # return sensor readings


def generate_error(readings=[[]]):  # this function generates errors, it is assumed sensors are on unique circuits otherwise problem 3 cannot be more than 1 error
    sensor_error_likelihood = random.random()  # determines the likelihood of errors for current timestamp
    for x in range(0, 32): # cycle through all sensors
        error_in_message = random.random()  # Checks the odds of error in specific sensor instance
        if error_in_message > sensor_error_likelihood: # If the odds of a error in the sensor is larger than the likelihood determined above a error occurs
            position_of_error = int(random.random() * 15)   # Checks at which position the error occurs
            readings[x][position_of_error] = 'err' # adds error message into sensor readings
            if position_of_error < 15:  # checks if error occurred at last sensor entry
                for y in range(position_of_error+1, 16):  # if not last sensor entry cycle through remaining sensor entries
                    readings[x][y] = ''  # removes data from sensor entries after error
    return readings  # return dataset


def check_error(readings=[[]]):  # This function checks for errors in the data set and changes them to int
    output = [[]]  # generate output variable
    incorrect_sensors = []  # this field stores the positions of the errors
    for i in range(0, 32):  # cycle through each sensor
        added = False  # set added field to false so that the same sensor isn't added twice
        for j in range(0, 16):  # cycle through all sensor entries
            if isinstance(readings[i][j], basestring):  # checks if the entry is a string
                if added == False:  # checks if sensor has been added yet
                    output.append(readings[i])  # add sensor to error output set
                    output[len(output)-1][j] = -1  # set the 'err' text to -1
                    incorrect_sensors.append(i+1)  # remember the sensor where the error occurred
                    added = True  # sensor has been added
    del output[0]  # remove initial value from 2d list
    return output, incorrect_sensors  # return the error fields


def sensor_input_instance():  # loops through a full iteration of sensor feedback
    readings = generate_sensor()  # generate sensor readings
    sensor_date = datetime.datetime.now()  # check the date the readings were generated
    generate_error(readings)  # generate errors in the data

    with open('somefile.txt', 'a') as the_file:  # open file to write data
        for i in range(0, 32):  # write data for each sensor
            the_file.write("Sensor {} at {} values: {}\n".format(i+1, sensor_date, readings[i]))  # write sensor number, time and values
        the_file.write('\n')  # add line in text file for readability

    errors, error_positions = check_error(readings)  # check for errors in the dataset
    with open('somefile.txt', 'a') as the_file:  # open file to write data
        for i in range(0, len(error_positions)):  # loop through all error entries
            the_file.write("Sensor {} at {} has error in following readings: {}\n".format(error_positions[i], sensor_date, errors[i]))  # write sensor, date and error data where errors occurred
        the_file.write('\n\n\n')  # write multiple lines to indicate closeout of this timestamp of data


for counter in range(0, 5):  # creates cycles where sensor data is received
    sensor_input_instance()  # generate cycle of errors and check for errors
    time.sleep(5)  # wait for 5 seconds before next cycle