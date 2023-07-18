import os
import csv
import pandas as pd
import sys
import calendar


def readFiles(folder):
    """
     folder - it will contain the path from till the main weatherMan folder
     working - the function creates csv files from the sub-folders in weatherMan folder and 
                concats all the subFolder files into one csv for each subFolder
    """
    cities = []
    csv_names = []

    for SubFolder, dirs, SubFiles in os.walk(folder):

        csv_name = SubFolder.split("\\")

        folder_name = folder.split("\\")
        if csv_name[-1] != folder_name[-1]:

            df = pd.DataFrame()
            cities.append(csv_name[-1])
            for file_name in SubFiles:

                file_path = os.path.join(SubFolder, file_name)
                data = pd.read_csv(file_path)
                data = data.rename(
                    columns={data.columns[0]: 'Date'})
                df = pd.concat([df, data], axis=0)

            df.to_csv(csv_name[-1]+'.csv')
            csv_names.append(csv_name[-1]+'.csv')

    return cities, csv_names


def MaxTemp(cityCSV, year, rowName):
    """
     cityCSV - the csv file of the city whos data was required
     year - the mentioned year on the terminal
     rowName - the lable of the csv such as 'Max TemperatureC'
     working - the function finds the Max value from the lable that was given 
    """
    with open(cityCSV, 'r') as f:
        check = False
        file = csv.DictReader(f)
        max_temp = float('-inf')

        for row in file:
            col = row.keys()
            break

        col_list = list(col)

        for row in file:
            date = row[col_list[1]]
            ele = row[rowName]
            if ele != '' and date.startswith(year):
                check = True
                temp = float(ele)
                if temp > max_temp:
                    max_temp = temp
                    day = date

    if rowName == 'Max TemperatureC':
        if check == False:
            print(f'Highest: {year} year does not exist in {cityCSV}')
        else:
            day = day.split('-')
            month_name = calendar.month_name[int(day[1])]
            print(f'Highest: {int(max_temp)}C on {month_name} {day[2]}')
    else:
        if check == False:
            print(f'Humid: {year} year does not exist in {cityCSV}')
        else:
            day = day.split('-')
            month_name = calendar.month_name[int(day[1])]
            print(f'Humid: {int(max_temp)}% on {month_name} {day[2]}')


def MinTemp(cityCSV, year):
    """
     cityCSV - the csv file of the city whos data was required
     year - the mentioned year on the terminal
     working - the function finds the Min value from 'Min TemperatureC'
    """
    with open(cityCSV, 'r') as f:
        file = csv.DictReader(f)
        min_temp = float('inf')
        check = False

        for row in file:
            col = row.keys()
            break

        col_list = list(col)

        for row in file:
            date = row[col_list[1]]
            ele = row['Min TemperatureC']
            if ele != '' and date.startswith(year):
                check = True
                temp = float(ele)
                if temp < min_temp:
                    min_temp = temp
                    day = date

    if check == False:
        print(f'Lowest: {year} year does not exist in {cityCSV}')
    else:
        day = day.split('-')
        month_name = calendar.month_name[int(day[1])]
        print(f'Lowest: {int(min_temp)}C on {month_name} {day[2]}')


def AvgTemp(cityCSV, year, month, rowName):
    """
     cityCSV - the csv file of the city whos data was required
     year - the mentioned year on the terminal
     month - the mentioned month on the terminal
     rowName - the lable of the csv such as 'Max TemperatureC'
     working - the function finds the Average value from the given lable
    """
    with open(cityCSV, 'r') as f:
        file = csv.DictReader(f)
        sum = 0
        count = 0
        check = False

        for row in file:
            col = row.keys()
            break

        col_list = list(col)

        for row in file:
            date = row[col_list[1]]
            if date[0] != '<':
                ele = row[rowName]
                year_, month_, _ = date.split('-')
                if ele != '' and year == year_ and int(month) == int(month_):
                    check = True
                    temp = float(ele)
                    sum += temp
    _, count = calendar.monthrange(int(year), int(month))
    if check == False:
        return None

    return sum/count


def monthly_bar_chart(cityCSV, year, month):
    """
     cityCSV - the csv file of the city whos data was required
     year - the mentioned year on the terminal
     month - the mentioned month on the terminal
     working - the function finds the min temp and max temp 
                for each day of the given year and month and draws bar graph
    """
    dates = []
    min_temps = []
    max_temps = []

    with open(cityCSV, 'r') as f:
        file = csv.DictReader(f)

        for row in file:
            col = row.keys()
            break

        col_list = list(col)

        for row in file:
            date = row[col_list[1]]

            if date[0] != '<':
                min_ = row['Min TemperatureC']
                max_ = row['Max TemperatureC']
                year_, month_, day_ = date.split('-')
                if min_ != '' and max_ != '' and year == year_ and int(month) == int(month_):
                    dates.append(day_)
                    min_temps.append(float(min_))
                    max_temps.append(float(max_))

    print(calendar.month_name[int(month)], year)
    PrintBars(dates, min_temps, max_temps)
    print(calendar.month_name[int(month)], year)
    PrintBonusBars(dates, min_temps, max_temps)


def PrintBars(dates, min_temps, max_temps):
    """
     dates - the dates of the with min and max temps 
     min_temps - the list of all the min temps index acc to dates
     max_temps - the list of all the max temps index acc to dates
     working - prints the bar with + sign 
    """
    for i in range(len(dates)):

        print(dates[i], end=' ')
        for j in range(int(max_temps[i])):
            print('\033[31m+\033[0m', end='')
        try:
            print(f" {int(max_temps[i])}C")
        except Exception as e:
            print(e)

        print(dates[i], end=' ')
        for k in range(int(min_temps[i])):
            print('\033[34m+\033[0m', end='')
        try:
            print(f" {int(min_temps[i])}C")
        except Exception as e:
            print(e)


def PrintBonusBars(dates, min_temps, max_temps):
    """
     dates - the dates of the with min and max temps 
     min_temps - the list of all the min temps index acc to dates
     max_temps - the list of all the max temps index acc to dates
     working - prints the bar with + sign and concats the min and max
                temps together as one bar but different color
    """
    for i in range(len(dates)):

        print(dates[i], end=' ')
        for j in range(int(min_temps[i])):
            print('\033[34m+\033[0m', end='')

        for j in range(int(max_temps[i])):
            print('\033[31m+\033[0m', end='')

        try:
            print(f" {int(min_temps[i])}C - {int(max_temps[i])}C")
        except Exception as e:
            print(e)


def FindFile(folder, file_name):
    """
     folder - it will contain the path from till the main weatherMan folder
     file_name - name of file which needs to be checked
     working - searches if the file exists in the folder
    """
    check = False
    for _, _, SubFiles in os.walk(folder):
        # for name in SubFiles:
        #     if name == file_name:
        #         return True
        if file_name in SubFiles:
            return True
    return check


try:
    flag = sys.argv[1]

    if flag == '-e':

        check = False
        year = sys.argv[2]
        folder = os.path.normpath(sys.argv[3])
        folder = folder.split('\\')
        file = folder[-1]
        folder = '\\'.join(folder[:len(folder)-1])

        cities, csv_names = readFiles(folder)
        for i in range(len(cities)):
            if cities[i].lower() == file.lower():
                check = True
                MaxTemp(csv_names[i], year, 'Max TemperatureC')
                MinTemp(csv_names[i], year)
                MaxTemp(csv_names[i], year, 'Max Humidity')
                break
        if check == False:
            print('Folder does not exist')

    elif flag == '-a':

        check = False
        date = sys.argv[2]
        date = date.split('/')
        year = date[0]
        month = date[1]
        folder = os.path.normpath(sys.argv[3])
        folder = folder.split('\\')
        file_name = folder[-1]
        file = folder[-2]
        folder = '\\'.join(folder[:len(folder)-2])

        cities, csv_names = readFiles(folder)

        if FindFile(folder, file_name):

            for i in range(len(cities)):
                if cities[i].lower() == file.lower():

                    check = True
                    max_avg_temp = AvgTemp(
                        csv_names[i], year, month, 'Max TemperatureC')
                    min_avg_temp = AvgTemp(
                        csv_names[i], year, month, 'Min TemperatureC')
                    max_avg_humid = AvgTemp(
                        csv_names[i], year, month, 'Max Humidity')

                    if max_avg_temp:
                        try:
                            print(f'Highest Average: {int(max_avg_temp)}C')
                        except:
                            print('could not convert float to string')
                    else:
                        print(f'Highest Average: {max_avg_temp}')

                    if min_avg_temp:
                        try:
                            print(f'Lowest Average: {int(min_avg_temp)}C')
                        except:
                            print('could not convert float to string')
                    else:
                        print(f'Lowest Average: {min_avg_temp}')

                    if max_avg_humid:
                        try:
                            print(f'Average Humidity: {int(max_avg_humid)}%')
                        except:
                            print('could not convert float to string')

                    else:
                        print(f'Average Humidity: {max_avg_humid}')

                    break
            if check == False:
                print('Folder does not exist')
        else:
            print('File not found')

    elif flag == '-c':

        check = False
        date = sys.argv[2]
        date = date.split('/')
        year = date[0]
        month = date[1]
        folder = os.path.normpath(sys.argv[3])
        folder = folder.split('\\')
        file_name = folder[-1]
        file = folder[-2]
        folder = '\\'.join(folder[:len(folder)-2])

        cities, csv_names = readFiles(folder)
        if FindFile(folder, file_name):
            for i in range(len(cities)):
                if cities[i].lower() == file.lower():
                    check = True
                    monthly_bar_chart(csv_names[i], year, month)
                    break

            if check == False:
                print('Folder does not exist')

        else:
            print('File not found')

    else:
        print('Invalid Flag!')
except:
    print('No values entered')
