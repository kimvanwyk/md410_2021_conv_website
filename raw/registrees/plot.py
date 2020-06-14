import matplotlib
import matplotlib.pyplot as plt 
import pandas as pd

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

FILENAME = 'registrations_over_time.png'

def plot_registrations(dates, fn='plot.png'):

    df = pd.DataFrame({'xdata': dates, 'ydata': [n for (n,d) in enumerate(dates,1)]})
    plt.plot_date('xdata', 'ydata', data=df, xdate=True, ydate=False, marker='o', markerfacecolor='blue', markersize=8, color='skyblue', linewidth=3)

    plt.xlabel("Registration Date")
    plt.ylabel("Registration Number")

    yint = range(1, len(dates)+1, 10)
    plt.yticks(yint)

    plt.gcf().autofmt_xdate()

    plt.grid(True)

    plt.title('Registrations Over Time')

    plt.savefig(fn)

def plot_registration_dates(registration_dates, fn=FILENAME):
    dates = matplotlib.dates.date2num(registration_dates)
    plot_registrations(dates, fn)

