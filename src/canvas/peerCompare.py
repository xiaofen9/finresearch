import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


class Ploter():
    def __init__(self, filename, title='Data Change Overtime'):
        self.filename = filename
        self.title = title

    def downsample_data(self, dates, values, max_points=1000):
        # Calculate the step size based on the desired number of points
        step = max(1, int(len(dates) / max_points))
        # Select data points at regular intervals
        return dates[::step], values[::step]

    def plot(self, data_list, duration=None):
        # Initialize lists to determine the shortest date range
        min_dates = []
        max_dates = []

        # Process each element's data
        for data in data_list:
            dates = list(data['data'].keys())
            values = list(data['data'].values())
            
            # Convert string dates to datetime objects for comparison
            dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]
            dates, values = self.downsample_data(dates, values)

            
            # Append the min and max dates for this ticker to the lists
            min_dates.append(min(dates))
            max_dates.append(max(dates))
            
            # Plot each ticker's data
            plt.plot(dates, values, label=data['name'])

        # Find the shortest date range among all tickers
        global_start_date = max(min_dates)
        global_end_date = min(max_dates) if not duration else global_start_date + duration

        # Set the x-axis to this shortest date range
        plt.xlim(global_start_date, global_end_date)
        # Optionally format the dates on the x-axis for better readability
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Adjust interval as needed
        plt.gcf().autofmt_xdate()  # Auto-rotate date labels

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(self.title)
        plt.legend()
        plt.savefig(self.filename, bbox_inches='tight')
        plt.clf()

