import altair.vegalite.v2 as alt
import numpy as np
import pandas as pd
from dfply import *
import calendar
alt.themes.enable('opaque')

df = pd.read_csv("data/Bike-Sharing-Dataset/day.csv")


weekday_dict = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    0: "Sunday"
}

month_dict= dict((k,v) for k,v in enumerate(calendar.month_abbr))


def get_weekday(n):
    return weekday_dict[n]

def get_month(n):
    return month_dict[n]


def plot_rental_by_time(df, time_unit = "weekday"):
    field_dict= {
        "weekday": "weekday_num",
        "month" : 'mnth'
    }

    sort_field  = field_dict[time_unit]
    casual_plt = alt.Chart(df).mark_bar().encode(y=alt.Y(time_unit, sort=alt.EncodingSortField(
        field=sort_field, order="ascending", op='sum')), x=alt.X('casual', title="Rental Count")).properties(title="Casual")


    registered_plt = alt.Chart(df).mark_bar().encode(y=alt.Y(time_unit, sort=alt.EncodingSortField(
        field=sort_field, order="ascending", op='sum')), x=alt.X('registered', title="Rental Count")).properties(title='Registered')


    total_plt = alt.Chart(df).mark_bar().encode(y=alt.Y(time_unit, sort=alt.EncodingSortField(
        field=sort_field, order="ascending", op='sum')), x=alt.X('cnt', title='Rental Count')).properties(title="Total")


    combined_plt = alt.vconcat(
        casual_plt, registered_plt, total_plt)
    combined_plt = combined_plt.resolve_scale(
        x='shared').properties(title="Rental Number by Weekday")
    return combined_plt

# convert weekday back to actual day


df['weekday_num'] = df.weekday
df['weekday'] = df.weekday.apply(get_weekday)

df['month'] = df.mnth.apply(get_month)


weekday_plt = plot_rental_by_time(df)

month_plt = plot_rental_by_time(df, time_unit= 'month')


alt.hconcat(weekday_plt, month_plt)
