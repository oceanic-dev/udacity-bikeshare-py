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
    print(f'The MODE day of the week: {df['Start Day'].mode()[0]}')

    # Calculate and display the most common start hour, formatted as HH:00
    popular_hour = df['Start Hour'].mode()[0]
    if popular_hour >= 12:
        print(f'The MODE hour: {popular_hour}h00')
    else:
        print(f'The MODE hour: 0{popular_hour}h00')

def station_stats(no_filter_df):
    """Displays statistics on the most popular stations and trip combinations."""
    # Print a separator line for readability
    print('-'*100)

    # Calculate the total number of rides
    ride_count = no_filter_df['Start Time'].count()

    # Display the most commonly used start station
    print(f'MODE Start Station for {ride_count} rides: {no_filter_df['Start Station'].mode()[0]}')

    # Display the most commonly used end station
    print(f'MODE End Station for {ride_count} rides: {no_filter_df['End Station'].mode()[0]}')
    
    # Create a column for start-to-end station combinations
    no_filter_df['Station Combo'] = no_filter_df['Start Station'] + ' - ' + no_filter_df['End Station']

    # Display the most frequent start-to-end station combination
    print(f'MODE Trip Combo for {ride_count} rides: {no_filter_df['Station Combo'].mode()[0]}')

    no_filter_df.drop(columns=['Station Combo'], inplace = True)

    # Print a separator line for readability
    print('-'*100)

def trip_duration_stats(df):
    """Displays statistics on total and average trip duration."""
    # Print a separator line for readability
    print('-'*100)

    # Calculate and display total travel time in hours
    print(f'Total Travel Time of {df['Start Time'].count()} rides: {(df['Trip Duration'].sum()/3600).round(2)} hrs')

    # Calculate and display mean travel time in minutes
    print(f'MEAN travel time across {df['Start Time'].count()} rides: {(df['Trip Duration'].mean()/60).round(2)} min')

    # Print a separator line for readability
    print('-'*100)

def user_stats(df):
    """Displays statistics on bikeshare users, including user types, gender, and age."""
    # Print a separator line for readability
    print('-'*100)

    # Display counts of different user types
    print(df['User Type'].value_counts())
    print('-'*100)

    # Display counts of gender, if the column exists in the dataset
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
        print('-'*100)

    # Calculate and display rider age statistics, if Birth Year column exists
    if 'Birth Year' in df.columns:
        # Create a copy of the dataframe, filtering out rows with missing Birth Year
        df_filter_nan = df[df['Birth Year'].notna()].copy()

        # Calculate rider age based on the year of the Start Time
        df_filter_nan['Rider Age'] = df_filter_nan['Start Time'].dt.year - df_filter_nan['Birth Year'].astype(int)

        # Display minimum, mode, and maximum rider ages
        print(f'MIN Rider Age: {int(df_filter_nan["Rider Age"].min())}')
        print(f"MODE Rider Age: {int(df_filter_nan['Rider Age'].mode().iloc[0])}")
        print(f"MAX Rider Age: {int(df_filter_nan['Rider Age'].max())}")

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
    monthNum = 0
    # List of month names for readable output
    months_of_year = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Loop until a valid month number (1-12) is provided
    while monthNum < 1 or monthNum > 12:
        try: 
            monthNum = input('Choose by which month you wish to filter the dataset [1-12]: ').strip()
            monthNum = int(monthNum)
        except KeyboardInterrupt:
            print('\n*** Terminating Script ***')
            sys.exit()
        except:
            print("\n*** Invalid Input ***\n"
                  "Insert an integer [1 <= month <= 12]")
            monthNum = 0
        else:
            filtered_df = df[df['Start Month'] == monthNum]
    
    print(f'--- Month Selected: {months_of_year[monthNum-1]} ---')   
    return filtered_df

def filter_by_day_of_week(df):
    """Filters the dataset by a user-specified day of the week."""
    # List of valid days of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = 'Day'

    # Loop until a valid day is provided
    while day not in days_of_week:
        try:
            day = input(
                "1 - MON - Monday\n"
                "2 - TUE - Tuesday\n"
                "3 - WED - Wednesday\n"
                "4 - THU - Thursday\n"
                "5 - FRI - Friday\n"
                "6 - SAT - Saturday\n"
                "7 - SUN - Sunday\n"
                "Choose by which day of the week you wish to filter the dataset: ").strip()
        except KeyboardInterrupt:
            print('\n*** Terminating Script ***')
            sys.exit()
        else:
            day = day.capitalize()  # Standardize input to title case
            # Map numeric or abbreviated inputs to full day names
            if day in ["1", "Mon"]: 
                day = "Monday"
            elif day in ["2", "Tue"]: 
                day = "Tuesday"
            elif day in ["3", "Wed"]: 
                day = "Wednesday"
            elif day in ["4", "Thu"]: 
                day = "Thursday"
            elif day in ["5", "Fri"]: 
                day = "Friday"
            elif day in ["6", "Sat"]: 
                day = "Saturday"
            elif day in ["7", "Sun"]: 
                day = "Sunday"
            if day not in days_of_week:
                print("\n*** Invalid input ***")

    print(f'--- Selected Filter: {day}')        
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