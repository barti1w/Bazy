import matplotlib.pyplot as plt


class ReportData:
    def __init__(self, date, revenue):
        self.date = date
        self.revenue = revenue


class Report:

    def __init__(self, values, type):
        self.type = type
        self.data = []
        for value in values:
            self.data.append(ReportData(value['date'], value['revenue']))

    def plot(self):
        plt.figure(figsize=(12, 8))
        dates = [data.date for data in self.data]
        revenues = [data.revenue for data in self.data]

        plt.bar(dates, revenues, color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Revenue')
        plt.title(f'{self.type} Revenue Bar Plot')
        plt.show()


# TODO read from DB
values = [
    {'date': '2024-01-01', 'revenue': 1500},
    {'date': '2024-02-01', 'revenue': 2523},
    {'date': '2024-03-01', 'revenue': 2000},
    {'date': '2024-04-01', 'revenue': 2680},

]
report = Report(values, 'monthly')
report.plot()
