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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    cities = ['chicago', 'new york city', 'washington']
    while city.lower() not in CITY_DATA:
        city = input("Enter a city, Chicago, New York, or Washington: ")
        if city.lower() not in CITY_DATA:
            print("That city is invalid (typing DC is invalid and city is needed for new york)!")
            
    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month.lower() not in months:
        month = input("Please enter the month you would like to filter: ")
        if month.lower() not in months:
            print("That month is invalid! The data is only from the first 6 months of the year.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day.lower() not in days:
        day = input("Please enter a day of the week you want to filter on: ")
        if day.lower() not in days:
            print("That is an invalid, or incorrectly spelled, day of the week!")

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
    # Load the DataFrame based on the user input
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  
    
    # Month filtering
    if month.lower() != 'all':
        months = {
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6
        }
        month = month.lower()
        if month in months:  # Check if the month is in the dictionary
            month_index = months[month]
            df = df[df['month'] == month_index]
        else:
            print(f"'{month}' is not a valid month.")
    
    # Day filtering
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]  # Ensure day is capitalized correctly
    
    # Check if the DataFrame is empty after filtering
    if df.empty:
        print("No data available for the selected filters.")
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # The dataframe already has its own month column
    frequent_month = df['month'].mode()[0]
    print('The bikeshare is most commonly used in month:', frequent_month)

    # TO DO: display the most common day of week
    # The dataframe also has its own day column already
    frequent_day = df['day_of_week'].mode()[0]
    print('Bikeshare sees the most customers on:', frequent_day)

    # TO DO: display the most common start hour
    # Will need to follow steps from prior functions to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    frequent_hour = df['hour'].mode()[0]
    print('Bikeshare usage is most used during the {} hour'.format(frequent_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    frequent_start = df['Start Station'].mode()[0]
    print("The most frequent start station is:", frequent_start)

    # TO DO: display most commonly used end station
    frequent_end = df['End Station'].mode()[0]
    print('The most frequent end station is:', frequent_end)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print('Most common trip from start to end:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # The NumPy sum function will be used here for the columns
    total_time = df['Trip Duration'].sum(axis = 0)
    print('The Total Trip Duration based on your filters is {} seconds'.format(total_time))
    # the mean function will be used instead
    avg_time = df['Trip Duration'].mean(axis = 0)
    print('The Average Trip Duration based on your filters is {} seconds'.format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    city, month, day = get_filters()

    # Check if the DataFrame is empty
    if df.empty:
        print("No data available for the selected filters.")
        return

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('Here is the breakdown of the user types:\n', user_counts)

    # Display counts of gender only for Chicago and New York City
    if city in ['chicago', 'new york city']:
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            print('Here is the breakdown of the users by gender:\n', gender_counts)
        else:
            print('The dataset does not contain gender data.')
    else:
        print('The Washington dataset does not contain gender data.')

    # Display earliest, most recent, and most common year of birth only for Chicago and New York City
    if city in ['chicago', 'new york city']:
        if 'Birth Year' in df.columns:
            early_year = df['Birth Year'].min()
            last_year = df['Birth Year'].max()
            frequent_year = df['Birth Year'].mode()[0]
            
            print('The oldest users were born in:', early_year)
            print('The youngest users were born in:', last_year)
            print('The most frequent user birth year is:', frequent_year)
        else:
            print('The dataset does not contain Birth Year data.')
    else:
        print('The Washington dataset does not contain Birth Year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    """Displays raw data in increments of 5 rows based on user input."""
    start_loc = 0  # Initialize the starting location for displaying data
    while True:
        # Ask the user if they want to see the next 5 rows of data
        view_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()
        
        if view_data == 'yes':
            # Get the next 5 rows
            print(df.iloc[start_loc:start_loc + 5])  # Display the next 5 rows
            start_loc += 5  # Update the starting location
            
            # Check if we've reached the end of the DataFrame
            if start_loc >= len(df):
                print("No more data to display.")
                break
        elif view_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        print("Getting filters...")
        city, month, day = get_filters()
        print(f"Filters received: City={city}, Month={month}, Day={day}")

        print("Loading data...")
        df = load_data(city, month, day)
        print("Data loaded successfully.")

        print("Calculating time statistics...")
        time_stats(df)
        print("Time statistics calculated.")

        print("Calculating station statistics...")
        station_stats(df)
        print("Station statistics calculated.")

        print("Calculating trip duration statistics...")
        trip_duration_stats(df)
        print("Trip duration statistics calculated.")

        print("Calculating user statistics...")
        user_stats(df)
        print("User statistics calculated.")
        
        print("Prompting for displaying data...")
        display_data(df)
        print("Data displayed.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
