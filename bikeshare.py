import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('You can filter the data to focus on a specific month and day of the week.')

      
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = 0
    while city not in CITY_DATA.keys():
        print('\nWhich city would you like to look at? We have Chicago, New York City, and Washington.\n')
        city = input('  City Name >> ').lower()
        if city not in CITY_DATA.keys():
            print("\nI don't have data for that city, let's try again.")
    
    # get user input for month (all, january, february, ... , june)
    print('\nDo you want to look at data for a specific month? Type "Y" for Yes and "N" for No.\n')
    month_filter = 0
    while month_filter != 'Y' and month_filter != 'N':
        month_filter = input('  Y or N >> ').upper()
        if month_filter != 'Y' and month_filter != 'N':
            print('\nSorry, I do not understand.  Please type "Y" for Yes and "N" for No.')
    print('\nVery Good.')
    
    if month_filter == 'Y':
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6}
        month = 0
        while month not in months.keys():
            print('\nWhich month would you like to look at? We have data for January through June.\n')
            month = input('  Month Name >> ').title()
            if month not in months:
                print("\nI don't have data for that month, let's try again.\n")
        month = months[month]
    else:
        month = month_filter

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nDo you want to look at data for a specific day of the week? Type "Y" for Yes and "N" for No.\n')
    day_filter = 0
    while day_filter != 'Y' and day_filter != 'N':
        day_filter = input('  Y or N >> ').upper()
        if day_filter != 'Y' and day_filter != 'N':
            print('Sorry, I do not understand.  Please type "Y" for Yes and "N" for No.')
    print('\nGot it.')
    
    if day_filter == 'Y':
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = 0
        while day not in day_of_week:
            print('\nWhich day would you like to look at? We have data for Monday through Sunday.\n')
            day = input('  Day Name >> ').title()
            if day not in day_of_week:
                print("\nI don't have data for that day, let's try again.\n")
    else:
        day = day_filter
        
    print('\n')
    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter the dataframe
    if month != 'N':
        df = df[df['month'] == month]
    if day != 'N':
        df = df[df['day_of_week'] == day]
    df.reset_index(drop = True, inplace = True)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, unless a month filter was selected
    if len(df['month'].unique()) > 1:
        month_list = ['January', 'February', 'March', 'April', 'May', 'June']
        print("The most common month was {}.".format(month_list[df['month'].mode()[0] - 1]))

    # display the most common day of week, unless a day filter was selected
    if len(df['day_of_week'].unique()) > 1:
        print("The most common day of the week was {}.".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("The most common start hour was {}.".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station was {}.".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most common end station was {}.".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Start End Combination'] = df['Start Station'] + ' to ' + df['End Station']
    print("The most frequent combination of start station and end station trip was {}.".format(df['Start End Combination'].mode()[0]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was {}.".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("The average travel time was {}.".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber_count = df[df['User Type'] == "Subscriber"]['User Type'].count()
    customer_count = df[df['User Type'] == "Customer"]['User Type'].count()
    print("There were {} subscribers and {} customers.".format(subscriber_count, customer_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        male_count = df[df['Gender'] == "Male"]['Gender'].count()
        female_count = df[df['Gender'] == "Female"]['Gender'].count()
        print("There were {} males and {} females.".format(male_count, female_count))
    else:
        print("No gender data is available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("The earliest year of birth was {}.".format(earliest_birth_year))
        print("The most recent year of birth was {}.".format(latest_birth_year))
        print("The most common year of birth was {}.".format(most_common_birth_year))
    else:
        print("No birth year data is available.")


    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def raw_data_view(df):
    """Allows user to view the raw data from the DataFrame"""
    
    raw_data_flag = 'Y'
    
    while raw_data_flag == 'Y':
    
        # Prompt user if they want to review the raw data
        print('\nDo you want to look at 5 lines of the raw data? Type "Y" for Yes and "N" for No.\n')
        raw_data_flag = input('  Y or N >> ').upper()
    
        # Address bad user input
        while raw_data_flag != 'Y' and raw_data_flag != 'N':
            print('\nSorry, I do not understand.  Please type "Y" for Yes and "N" for No.\n')
            raw_data_flag = input('  Y or N >> ').upper()
    
        # Display data for the user, if they requested it
        if raw_data_flag == 'Y':
            print('\n')
            print(df.head())
            df.drop([0, 1, 2, 3, 4], inplace = True)
            df.reset_index(drop = True, inplace = True)
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
