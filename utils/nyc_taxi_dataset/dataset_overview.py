import datetime as dt

import pandas as pd
import matplotlib.pyplot as plt
days_in_month = [31,29,31,
                 30,31,30,
                 31,31,30,
                 31,30,31]

def convertDate(d):
    return dt.datetime.fromisoformat(d)

def normalize_month_time(month, month_time):
    return month_time/days_in_month[month]

basedir = "../../_data/in/nyc_taxi/"
datafile = "test.csv"
datafile = "train.csv"

data_df = pd.read_csv(basedir+datafile);

time_data = pd.DataFrame()

time_data['spickup'] = data_df['pickup_datetime']
time_data['pickup'] = pd.to_datetime(time_data['spickup'].apply(convertDate))
time_data['day_time'] = [(x.hour+x.minute/60)/24 for x in time_data['pickup']]
time_data['week_time'] = [x.isoweekday()+(x.hour+x.minute/60)/24 -1 for x in time_data['pickup']]
time_data['month_time'] = [normalize_month_time(x.month-1,x.day+(x.hour+x.minute/60)/24 -1) for x in time_data['pickup']]
print(time_data['pickup'][0], time_data['day_time'][0])
print(time_data['pickup'][0], time_data['month_time'][0])
print(time_data['pickup'][0].isoweekday(), time_data['week_time'][0])
print("day_time max:",time_data['day_time'].max(), "min:",time_data['day_time'].min())
print("week_time max:",time_data['week_time'].max(), "min:",time_data['week_time'].min())
print("month_time max:",time_data['month_time'].max(), "min:",time_data['month_time'].min())
# t = convertDate("2021-03-16 01:02:20")
# print(t)
# print(t.day)
# print(t.hour)
# print(t.minute)
# print(t.isoweekday())

fig = plt.plot()
plt.hist(time_data['day_time'],bins=300)
plt.title('Day time')
plt.show()
plt.hist(time_data['week_time'],bins=300)
plt.title('Week time')
plt.show()
plt.hist(time_data['month_time'],bins=300)
plt.title('Month time')
plt.show()
time_data.to_csv(basedir+'train_norm_data.csv')

