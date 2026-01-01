import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ["january", "february", "march", "april", "may", "june"]
WEEK_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_input("Which city would you like to explore?", CITY_DATA.keys())
    month = get_input("Which month would you like to explore?", MONTHS, default='all')
    day = get_input("Which week day would you like to explore?", WEEK_DAYS, default='all')

    print('-'*40)

    return city, month, day

def show_raw_data(df):
    row_index = 0
    should_show_data = get_input("Would you like to see 5 rows of raw data?", ['yes', 'no'], default='no')
    while should_show_data == 'yes' and row_index < len(df):
        print(df.iloc[row_index:row_index + 5])
        row_index += 5
        should_show_data = get_input("Would you like to see 5 more rows of raw data?", ['yes', 'no'], default='no')

def get_input(prompt, valid_options, default=''):
    composed_prompt = f"{prompt} ({', '.join(valid_options)}"
    if default:
        valid_options = valid_options + ['']
        composed_prompt += f", default={default}): "
    else:
        composed_prompt += "): "

    user_input = input(composed_prompt).lower()
    while user_input not in valid_options:
        user_input = input(f"Invalid input.\n{composed_prompt}").lower()

    if user_input == '':
        user_input = default

    return user_input

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
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])

    # Extract date parts for filtering
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_number = MONTHS.index(month) + 1
        df = df[df['month'] == month_number]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f"The most common month is: {MONTHS[common_month - 1].title()}")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of week is: {common_day.title()}")

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most common start station is: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most common end station is: {common_end_station}")

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + " to " + df['End Station']
    common_station_combination = df['Station Combination'].mode()[0]
    print(f"The most common station combination is:\n{common_station_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types_counts.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts.to_string())
    else:
        print("\nNo gender data available for the selected city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\nNo birth data provided for the selected city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)
  
        restart = get_input('\nWould you like to restart? Enter yes or no.\n', ['yes', 'no'], default='no')
        if restart!= 'yes':
            break


if __name__ == "__main__":
	main()
