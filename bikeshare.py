import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv' }

def get_city(): 
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input("\nHello! Let\'s explore some US bikeshare data!\n"
                     "Would you like to see data for Chicago, New York, or Washington? \n")
        if city.lower() in CITY_DATA.keys():
            return CITY_DATA[city.lower()]
        else:
            print("\nPlease enter a city only from Chicago, New York or Washington!\n")
        
def get_time():
    timefilter = input("\nWould you like to filter the data by month, day, or not at all? Type none for no time filter\n")
    if timefilter.lower() in ['month', 'day', 'none']:
        return timefilter 
    else:
        print("Please enter a valid time filter\n")       

def get_month():
    month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                   'May': 5, 'June': 6}
    month = input("\nWhich month? Enter a month: January, February, March, April, May, June: \n")
    if month.title() in month_dict.keys():
        return month_dict[month.title()]
    else:
        print("Please enter a month only from January to June\n")

def get_day():
    day_list =  ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? \n")
    if day.title() in day_list:
        return day.title()
    else: 
        print("Please enter a valid day\n")

def common_month(filterdf):
    
    most_pop_month = filterdf['Start Time'].dt.month.mode()[0]
    print("\nMost popular month: {}.".format(most_pop_month))

def common_day(filterdf):

    most_pop_day = filterdf['Start Time'].dt.weekday_name.mode()[0]
    print("\nMost popular day: {}.".format(most_pop_day))

def common_hour(filterdf):

    most_pop_hour = filterdf['Start Time'].dt.hour.mode()[0]
    if most_pop_hour == 0:
        newhour = 12
        apm = 'am'
    elif 1 <= most_pop_hour < 12:
        newhour = most_pop_hour
        apm = 'am'
    elif 13 <= most_pop_hour < 24:
        newhour = most_pop_hour - 12
        apm = 'pm'
    else:
        newhour = '12'
        apm = 'pm'
    print("\nMost popular hour of the day: {}{}.".format(newhour, apm))

def tripduration(filterdf):

    duration_sum = round(filterdf['Trip Duration'].sum())
    duration_average = round(filterdf['Trip Duration'].mean(),2)

    # Convert total minutes to hour
    hour, minute = divmod(duration_sum, 60)
    print("\nTotal trip duration: {} hours, {} minutes.".format(hour, minute))
    print("Average trip duration: {} minutes.".format(duration_average))

def station_stats(filterdf):

    pop_start_station = filterdf['Start Station'].mode()[0]
    pop_end_station = filterdf['End Station'].mode()[0]
    pop_trip = filterdf['bothstation'].mode()[0]
    print("\nPopular start station: {}.".format(pop_start_station))
    print("Popular end station: {}.".format(pop_end_station))
    print("Popular trip: {}.".format(pop_trip))

def user_stats(filterdf):
    
    user_type = filterdf['User Type'].value_counts()
    print("\nCount of each user type: \n{}.".format(user_type))

def gender_stats(filterdf):
    
    gender = filterdf['Gender'].value_counts()
    print("\nCount of each gender: \n{}.".format(gender))       
    
def birthyear_stats(filterdf):

    common_birthyear = filterdf['Birth Year'].mode()[0].astype('int')
    oldest_user = sorted(filterdf['Birth Year'])[0].astype('int')
    youngest_user = sorted(filterdf['Birth Year'])[-1].astype('int')
    print("\nMost common birth year: {}.".format(common_birthyear))
    print("Birth year of oldest user: {}.".format(oldest_user))
    print("Birth year of youngest user: {}.".format(youngest_user))

def display_data(filterdf, current_line):
    
    display = input("\nWould you like to view individual trip data?\n"
                    "Please enter yes or no\n")
    if display.lower() == 'yes':
        print(filterdf.iloc[current_line:current_line+5])
        current_line += 5
        return display_data(filterdf, current_line)
    if display.lower() == 'no':
        return
    else:
        print("I do not understand your input, please enter only 'yes' or 'no'")
            
def main():
    
    city = get_city()
    
    df = pd.read_csv(city)
    df = df.dropna()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # change duration to minutes.
    df['Trip Duration'] = df['Trip Duration']/60
    # concatenate start and end station 
    df['bothstation'] = df[['Start Station', 'End Station']].apply(lambda x: ' to '.join(x), axis = 1)
       
    timefilter = get_time()
    if timefilter == 'none':
        filterdf = df
    elif timefilter == 'month':
        month = get_month()
        filterdf = df[df['month'] == month]
    else:
        day = get_day()
        filterdf = df[df['day_of_week'] == day]

    # popular month
    if timefilter == 'none' or timefilter == 'day':
        start_time = time.time()
        common_month(filterdf)
        print("This took %s seconds." % (time.time() - start_time))
        print("Next statistics...")

    # popular day
    if timefilter == 'none' or timefilter == 'month':
        start_time = time.time()
        common_day(filterdf)
        print("This took %s seconds." % (time.time() - start_time))
        print("Next statistics...")

    # popular hour
    start_time = time.time()
    common_hour(filterdf)
    print("This took %s seconds." % (time.time() - start_time))
    print("Next statistics...")

    # trip duration stats:
    start_time = time.time()
    tripduration(filterdf)
    print("This took %s seconds." % (time.time() - start_time))
    print("Next statistics...")

    # station stats:
    start_time = time.time()
    station_stats(filterdf)
    print("This took %s seconds." % (time.time() - start_time))
    print("Next statistics...")

    # user type stats:
    start_time = time.time()
    user_stats(filterdf)
    print("This took %s seconds." % (time.time() - start_time))
    print("Next statistics...")

    # gender stats:
    if city in ["chicago.csv", "new_york_city.csv"]:
        start_time = time.time()
        gender_stats(filterdf)
        print("This took %s seconds." % (time.time() - start_time))
        print("Next statistics...")
        start_time = time.time()
        birthyear_stats(filterdf)
        print("This took %s seconds." % (time.time() - start_time))
        print("Next statistics...")

    # display data if user specifies they would like to
    display_data(filterdf, 0)
    
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() == 'yes':
        main()
    elif restart.lower() == 'no':
        return
    else:
        print("Pleas type only 'yes' or 'no'.")
        return restart
    
if __name__ == "__main__":
	main()
