# %%
# import package
import datetime
import altair.vegalite.v2 as alt
alt.themes.enable('opaque')
import numpy as np
import pandas as pd
from dfply import *

# %%
# read dataframe

data = pd.read_csv("data/Bike-Sharing-Dataset/day.csv")
data['dates'] = pd.to_datetime(data['dteday'])
data.set_index("dates")
# extract date for visualization


# %%
# load chart for altair
chart = alt.Chart(data)

(chart.mark_line().encode(x='dates:T', y='casual').properties(
    title="Causal Rental over time"))

(chart.mark_line().encode(x='dates:T', y='registered').properties(
    title="Registered Rental over time"))

(chart.mark_line().encode(x='dates:T', y='cnt').properties(title="Total Rental over time"
                                                           ))

data['year'] = pd.DatetimeIndex(data['dates']).year

data_monthly = (data >> group_by(X.year, X.mnth)
                >> summarize(mnth_casual = X.casual.sum(),
                          mnth_registered= X.registered.sum(),
                          mnth_total = X.cnt.sum()))

data_monthly >>= unite('year_mnth', 'year', 'mnth', sep="-")
casual_mnth_plot = alt.Chart(data_monthly).mark_line(color='orange').encode(
    x='year_mnth:T', y='mnth_casual:Q').properties(title="Casual Rental")

registered_mnth_plot = alt.Chart(data_monthly).mark_line(color='blue').encode(
    x='year_mnth:T', y='mnth_registered:Q').properties(title="Registered Rental")

total_mnth_plot = alt.Chart(data_monthly).mark_line(color = 'red').encode(
    x=alt.X('year_mnth:T', title="Time in Year Month"), y= alt.Y('mnth_total:Q', title='Rental Count')).properties(title="Total Rental")

combined_plot = alt.vconcat(casual_mnth_plot, registered_mnth_plot,
                            total_mnth_plot).properties(title="Combined Rental Plots")

data_monthly >>= rename(registered='mnth_registered', casual='mnth_casual', total='mnth_total') >> gather(
    "rental_type", "count", ['registered', 'total', 'casual'])


data_rentals = (data_monthly >> mask(
    (X.rental_type == 'registered') | (X.rental_type == 'casual')))


rental_type_plot = alt.Chart(data_rentals).mark_line().encode(
    x=alt.X("year_mnth:T", title='Time in Year Month'),
    y=alt.Y('count', title='Rental Count'),
    color=alt.Color('rental_type', title='Rental Type')).properties(title="Registered and Casual Rentals Over Time")

# %%
combined_plot =  total_mnth_plot | rental_type_plot

combined_plot
# %%
combined_plot = combined_plot.resolve_scale(y='shared')
combined_plot
