import pandas as pd
import numpy as np

# Define a dictionary mapping city codes to their respective CSV filenames
CITY_DATA = {
    'CH': 'chicago.csv',
    'NY': 'new_york_city.csv',
    'WS': 'washington.csv'
}

# Define the base path for accessing CSV files
PATH = '/Users/jessetownsend/Documents/Udacity/datascience_withpython/Mod3-Python/bikeshare-project/'

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # List of month names for readable output
    months_of_year = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Calculate and display the most common month of travel
    popular_month = df['Start Month'].mode()[0]
    print(f'The mode month: {months_of_year[popular_month-1]}')

    # Calculate and display the most common day of the week
    popular_day_week = df['Start Day'].mode()[0]
    print(f'The MODE day of the week: {popular_day_week}')

    # Calculate and display the most common start hour, formatted as HH:00
    popular_hour = df['Start Hour'].mode()[0]
    if popular_hour >= 10:
        print(f'The MODE hour: {popular_hour}h00')
    else:
        print(f'The MODE hour: 0{popular_hour}h00')
        
def station_stats(df):
    """Displays statistics on the most popular stations and trip combinations."""
    print('-' * 100)

    ride_count = df['Start Time'].count()

    # Most common start station
    if 'Start Station' in df.columns:
        popular_start = df['Start Station'].mode()[0]
        print(f'MODE Start Station for {ride_count} rides: {popular_start}')
    else:
        print('Start Station column not found.')

    # Most common end station
    if 'End Station' in df.columns:
        popular_end = df['End Station'].mode()[0]
        print(f'MODE End Station for {ride_count} rides: {popular_end}')
    else:
        print('End Station column not found.')

    # Most frequent start-to-end station combination
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        # Use a tuple for speed and avoid modifying the original DataFrame
        combo = df[['Start Station', 'End Station']].agg(tuple, axis=1)
        popular_combo = combo.mode()[0]
        print(f'MODE Trip Combo for {ride_count} rides: {popular_combo[0]} - {popular_combo[1]}')
    else:
        print('Cannot compute trip combo without both Start and End Station columns.')

    print('-' * 100)

def trip_duration_stats(df):
    """Displays statistics on total and average trip duration."""
    # Ensure 'Trip Duration' column exists and is numeric
    if 'Trip Duration' not in df.columns:
        print('Trip Duration column not found.')
        return

    # Drop NaN values for accurate stats
    trip_durations = pd.to_numeric(df['Trip Duration'], errors='coerce').dropna()
    ride_count = trip_durations.count()

    if ride_count == 0:
        print('No valid trip duration data available.')
        return

    # Calculate total travel time in hours (rounded to 2 decimals)
    total_duration_hrs = np.round(trip_durations.sum() / 3600, 2)
    # Calculate mean travel time in minutes (rounded to 2 decimals)
    avg_travel_min = np.round(trip_durations.mean() / 60, 2)

    # Pretty print with alignment and thousands separator
    print('-' * 100)
    print(f"{'Total Travel Time':<30}: {total_duration_hrs:>10,.2f} hrs ({ride_count:,} rides)")
    print(f"{'Mean Travel Time':<30}: {avg_travel_min:>10,.2f} min")
    print('-' * 100)

def user_stats(df):
    """Displays statistics on bikeshare users: user types, gender, and rider age."""
    print('-' * 100)

    # User Type counts
    if 'User Type' in df.columns:
        user_counts = df['User Type'].value_counts(dropna=False)
        print(f"{'User Type':<20} {'Count':>10}")
        print(user_counts.to_string())
        print('-' * 100)
    else:
        print("User Type column not found.")
        print('-' * 100)

    # Gender counts
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts(dropna=False)
        print(f"{'Gender':<20} {'Count':>10}")
        print(gender_counts.to_string())
        print('-' * 100)

    # Rider Age stats
    if 'Birth Year' in df.columns and 'Start Time' in df.columns:
        # Use numpy for speed, avoid chained assignment
        birth_years = pd.to_numeric(df['Birth Year'], errors='coerce')
        start_years = df['Start Time'].dt.year
        valid_mask = birth_years.notna() & start_years.notna()
        ages = (start_years[valid_mask] - birth_years[valid_mask]).astype(int)

        if not ages.empty:
            min_age = ages.min()
            mode_age = ages.mode().iloc[0]
            max_age = ages.max()
            print(f"{'MIN Rider Age':<20}: {min_age}")
            print(f"{'MODE Rider Age':<20}: {mode_age}")
            print(f"{'MAX Rider Age':<20}: {max_age}")
        else:
            print("No valid rider age data available.")
    else:
        print("Birth Year or Start Time column not found.")

def city_filter(PATH):
    """Prompts the user to select a city dataset and loads the corresponding CSV file."""
    # Define valid city codes and their full names
    CITIES = ['CH', 'NY', 'WS']
    CITY_NAMES = {'CH': 'Chicago', 'NY': 'New York', 'WS': 'Washington'}
    user_input = True

    # Loop until a valid city code is provided
    while user_input:
        user_city = input('CH - Chicago\n'
                          'NY - New York\n'
                          'WS - Washington DC\n'
                          'Which dataset do you want to use [CH, NY, WS]: ').upper()
        
        if user_city in CITIES:
            user_input = False
        else:
            print("*** Invalid Input - only [CH, NY, WS] ***")
    
    # Attempt to load the CSV file for the selected city
    try: 
        df = pd.read_csv(PATH + CITY_DATA[user_city])
    except: 
        print('*** CSV Import Failed ***')
    else:
        print(f'--- Imported {CITY_NAMES[user_city]} City Data ---')
        return df

def filter_by_month(df):
    """Filters the dataset by a user-specified month."""
    # List of month names for readable output
    months_of_year = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    while True:
        try:
            month_input = input('Choose by which month you wish to filter the dataset [1-12]: ').strip()
            monthNum = int(month_input)
            if 1 <= monthNum <= 12:
                break
            else:
                print("\n*** Invalid Input ***\nInsert an integer [1 <= month <= 12]")
        except ValueError:
            print("\n*** Invalid Input ***\nInsert an integer [1 <= month <= 12]")

    filtered_df = df[df['Start Month'] == monthNum]
    print(f'--- Month Selected: {months_of_year[monthNum-1]} ---')
    return filtered_df

def filter_by_day_of_week(df):
    """Filters the dataset by a user-specified day of the week."""
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_map = {
        "1": "Monday", "Mon": "Monday", "Monday": "Monday",
        "2": "Tuesday", "Tue": "Tuesday", "Tuesday": "Tuesday",
        "3": "Wednesday", "Wed": "Wednesday", "Wednesday": "Wednesday",
        "4": "Thursday", "Thu": "Thursday", "Thursday": "Thursday",
        "5": "Friday", "Fri": "Friday", "Friday": "Friday",
        "6": "Saturday", "Sat": "Saturday", "Saturday": "Saturday",
        "7": "Sunday", "Sun": "Sunday", "Sunday": "Sunday"
    }

    while True:
        user_input = input(
            "1 - MON - Monday\n"
            "2 - TUE - Tuesday\n"
            "3 - WED - Wednesday\n"
            "4 - THU - Thursday\n"
            "5 - FRI - Friday\n"
            "6 - SAT - Saturday\n"
            "7 - SUN - Sunday\n"
            "Choose by which day of the week you wish to filter the dataset: "
        ).strip().capitalize()
        day = day_map.get(user_input, None)
        if day:
            break
        print("\n*** Invalid input ***")

    print(f'--- Selected Filter: {day}')
    # Use vectorized comparison for speed
    filtered_df = df[df['Start Day'] == day]
    return filtered_df

def main():
    """Main function to run the bikeshare statistics terminal interface."""
    # Define valid menu options
    answers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
    menu = 0
    df = None
    activeTerminal = True
    print('-'*100)
    print('--- Welcome to the Bikeshare Stats Terminal ---')

    # Main loop to keep the terminal active
    while activeTerminal:
        # Load the dataset for the selected city
        no_filter_df = city_filter(PATH)

        if no_filter_df is not None:
            # Convert Start Time and End Time to datetime format
            no_filter_df['Start Time'] = pd.to_datetime(no_filter_df['Start Time'])
            no_filter_df['End Time'] = pd.to_datetime(no_filter_df['End Time'])

            # Add derived columns for analysis
            no_filter_df['Start Day'] = no_filter_df['Start Time'].dt.day_name()
            no_filter_df['Start Month'] = no_filter_df['Start Time'].dt.month
            no_filter_df['Start Hour'] = no_filter_df['Start Time'].dt.hour

            # Reset menu option to match answers
            menu = '0'
            
            # Create a deep copy of the unfiltered dataframe
            df = no_filter_df.copy(deep=True)

        # Inner loop for menu options
        while menu in answers:
            print('-'*100)
            print('--- Bikeshare Main Menu ---\n'
                  '1  - Filter By Month\n'
                  '2  - Filter By Day of Week\n'
                  '3  - Filter By Both\n'
                  '4  - Remove all Filters\n'
                  '5  - View DataFrame Info\n'
                  '6  - View First 10 Rows\n'
                  '7  - View Stacks of 5 Rows\n'
                  '8  - Describe Stats for a Column\n'
                  '9  - Most Frequent Travel Times\n' 
                  '10 - Most Popular Stations & Trips\n'
                  '11 - Trip Duration Stats\n'
                  '12 - Bikeshare User Stats\n'
                  'c  - Go back to the City Menu\n'
                  'x  - Terminate Program')
            
            try:
                menu = input('Insert your command:').strip()
            except KeyboardInterrupt:
                print('*** Terminating Program ***')
                menu = 'x'
                activeTerminal = False
            else:
                if not menu.isdigit():
                    if menu.lower() == 'c':
                        print('--- Reselect City Dataset ---')
                    elif menu.lower() == 'x':
                        activeTerminal = False
                        print('*** Cancelling Program ***')
                    else:
                        print('*** Invalid Input only [1-10] ***')
                        menu = '0'
                elif menu == '1':
                    # Apply month filter
                    try:
                        df = filter_by_month(no_filter_df)
                    except:
                        print('*** Failed to Apply Filter ***')
                    else:
                        print('--- Month Filter Applied ---')
                elif menu == '2':
                    # Apply day of week filter
                    try:
                        df = filter_by_day_of_week(no_filter_df)
                    except:
                        print('*** Failed to Apply Filter ***')
                    else:
                        print('--- Day of Week Filter Applied ---')
                elif menu == '3':
                    # Apply both month and day of week filters
                    try:
                        df = filter_by_month(no_filter_df)
                        df = filter_by_day_of_week(df)
                    except:
                        print('*** Failed to Apply Filters ***')
                    else:
                        print('--- Month Filter Applied ---')
                        print('--- Day of Week Filter Applied ---')
                elif menu == '4':
                    # Remove all filters and restore original dataframe
                    print('-'*100)
                    print('--- All Filters Removed ---') 
                    df = no_filter_df.copy(deep=True)
                elif menu == '5':
                    # Display dataframe info
                    print('-'*100)
                    print(df.info())
                    print('-'*100)
                elif menu == '6':
                    # Display the first 10 rows of the dataframe
                    print(df.head(10))
                elif menu == '7':
                    # Display rows in stacks of 5, with option to continue
                    print(' --- Viewing 5 Row Stacks ---')
                    one_more_row = True
                    rowStart = 0
                    while one_more_row:
                        for rowIndex in range(rowStart, rowStart+5):
                            print('-'*100)
                            print(df.iloc[rowIndex])
                        
                        ask_for_more = input('Do you want to view the next 5 rows? [yY / nN]: ').strip()[0]
                        if ask_for_more == 'N' or ask_for_more == 'n':
                            one_more_row = False
                        elif ask_for_more == 'Y' or ask_for_more == 'y':
                            rowStart += 5
                        else:
                            print('*** Invalid Input ***\nPrinting the Next Row by Default')
                elif menu == '8':
                    # Display descriptive statistics for a user-selected column
                    un_selected = True
                    print('-'*120)
                    for col in df.columns:
                        print(col, end='|')
                    print('\n' + '-'*120)
                    
                    while un_selected:
                        col_option = input('Choose a column from the list above: ').strip().title()
                        if col_option in df.columns:
                            print(df[col_option].describe())
                            un_selected = False
                        else:
                            print('*** Invalid Column Name - Type the column name correctly')
                    print('-'*100)
                elif menu == '9':
                    # Display most frequent travel times
                    print('-'*100)
                    print('--- Viewing the Most Frequent Travel Times ---')
                    time_stats(df)
                elif menu == '10':
                    # Display most popular stations and trips
                    station_stats(df)
                elif menu == '11':
                    # Display trip duration statistics
                    trip_duration_stats(df)
                elif menu == '12':
                    # Display bikeshare user statistics
                    user_stats(df)

    # Print a final separator when the terminal is closed
    print('*'*100)            

# Entry point for the script
if __name__ == "__main__":
    main()