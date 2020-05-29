import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_city():
    """
    Asks for a city from the data to analyse.
    Returns:
    city - name of the city to analyse.
    """
    while True:
        city = input('\nWhich city would you like to analyse?\n1. Chicago\n2. New York\n3. Washington?\n\n')
        if city.lower == ('chicago') or city == ('1'):
            return 'chicago'
        elif city.lower == ('new york') or city == ('2'):
            return 'new york city'
        elif city.lower == ('washington') or city == ('3'):
            return 'washington'
            break
        else:
            print("\nI'm sorry, your city is not in this list.")
            continue
    return city

def get_month():
    """
    Asks the user which months they would like to filter with.
    Returns:
    month - name of the month to analyse.
    """
    while True:
        month = input('\nWhich month would you like to analyse?\nEnter an integer between 1 and 6, where January = 1 and June = 6 or all\n\n')
        if month == 'all':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            month = MONTHS[int(month) - 1]
            break
        else:
            print("I'm sorry, the month you picked is not in this list.")
            continue
    return month

def get_day():
    """
    Asks the user which day they would like to filter with.
    Returns:
    day - name of the day to analyse.
    """
    while True:
        day = input('\nWhich day would you like to analyse?\nEnter an integer between 1 and 7, where Monday = 1 and Sunday = 7, or all\n\n')
        if day == 'all':
            day = 'all'
            break
        elif day in {'1','2','3','4','5','6','7'}:
            day = DAYS[int(day) - 1]
            break
        else:
            print("I'm sorry, the day you picked is not in this list.")
            continue
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington).
    #  HINT: Use a while loop to handle invalid inputs
    print ('='*90)
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    return city, month, day

def question_divider(start_time):
    """
    Function to print out the processing time.
    """
    time_str = "\n[This took %s seconds]" % round((time.time() - start_time),2)
    print(time_str)
    print ('-'*90)

def summary (city, month, day, df):
    """"
    Displays the choices made for city, month and day by the user
    """
    start_time = time.time()

    print('\nYou have selected the following:')
    print('City:    ', city.title())
    print('Month:   ', month.title())
    print('Day:     ', day.title())

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()

    #load data onto DataFrame
    df = pd.read_csv(CITY_DATA[city])

    #convert the Start Time column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    #apply the filter for month
    if month != 'all':
        month_i = MONTHS.index(month) + 1
        df = df[df.month == month_i]
        month = month.title()

    #apply the filter for day
    if day != 'all':
        day_i = DAYS.index(day)
        df = df[df.day_of_week == day_i]
        day = day.title()

    summary(city.title(), month, day, df)

    question_divider(start_time)

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nPopular time of travel:\n')
    start_time = time.time()

    # display the most common month; convert to string
    common_month = MONTHS[df['month'].mode()[0] - 1].title()
    print('Most Common Month:        ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day = DAYS[common_day].title()
    print('Most Common Day:          ', common_day)

    # display the most common start hour in 12 hour format with AM or PM
    common_hour = df['hour'].mode()[0]
    if common_hour == 0:
        meridiem = 'am'
        common_hour_read = 12
    elif 1 <= common_hour < 13:
        meridiem = 'am'
        common_hour_read = common_hour
    elif 13 <= common_hour < 24:
        meridiem = 'pm'
        common_hour_read = common_hour - 12
    print('Most Common Starting hour:   {}{}'.format(common_hour_read, meridiem))

    question_divider(start_time)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nPopular Stations and Trips:\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station:   ' ,start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:     ', end_station)

    # display most frequent combination of start station and end station trip
    start_end_comb = df.groupby(['Start Station', 'End Station'])
    freq_comb = start_end_comb['Trip Duration'].value_counts().idxmax()
    print('Most Frequent trip:           {}, {}'.format(freq_comb[0], freq_comb[1]))

    question_divider(start_time)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Total travel time is shown in years, days, hours, minutes and seconds
    Average trip duration is given in hours, minutes and seconds
    """
    print('\nTrip Duration\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    print('The total travel time is:    ', total_travel_time, 'seconds')
    print('                                approx. {} days {} hours {} minutes'.format(days, hours, minutes))

    # display mean travel time
    average_travel = df['Trip Duration'].mean()
    min, sec = divmod(average_travel, 60)
    hr, min = divmod(min, 60)
    print('The average travel time is:  ', average_travel, 'seconds')
    print('                                approx. {} hours, {} minutes'.format(hours,minutes))

    question_divider(start_time)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nUser Information\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n',user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender:\n',gender)
    except KeyError:
        print("Gender: No data available")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nYear of Birth:')
        print('Earliest:    ', int(df['Birth Year'].min()))
        print('Most Recent: ', int(df['Birth Year'].max()))
        print('Most Common: ', int(df['Birth Year'].value_counts().idxmax()))
    else:
        print("\nYear of Birth: No data available")

    question_divider(start_time)

def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    row_index=0
    see_data = input('\nWould you like to see some raw data from the current dataset?\n(y or n)\n')
    while True:
        if see_data == 'n':
            return
        if see_data == 'y':
            print('\n', df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input('\nWould you like to see some more raw data from the current dataset?\n(y or n)\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart?\n(y or n)\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
