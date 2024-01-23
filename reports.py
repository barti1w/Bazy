import cx_Oracle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

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
        plt.xticks(rotation=45)
        plt.show()


cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")
connection = cx_Oracle.connect(user="wojciechowskib", password="bartosz",
                               dsn="213.184.8.44:1521/ORCL")
table_name = 'MONTHLY_REPORT'

cursor = connection.cursor()

cursor.execute(f"SELECT * FROM {table_name}")

rows = cursor.fetchall()

formatted_rows = [{'date': "-".join(str(row[0]).split(" ")[0].split("-")[:2]), 'revenue': row[1]} for row in rows]

cursor.close()
connection.close()

report = Report(formatted_rows, 'monthly')
report.plot()

x = range(0, len([row[0] for row in rows]))
y = [row[1] for row in rows]


slope, intercept, r_value, p_value, std_err = linregress(x, y)

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"R-squared: {r_value**2}")
print(f"P-value: {p_value}")
print(f"Standard Error: {std_err}")

plt.scatter(x, y, label='Data points')
plt.plot(x, intercept + slope * x, 'r', label='Regression line')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
