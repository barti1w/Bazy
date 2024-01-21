import warnings
warnings.filterwarnings("ignore")

import cx_Oracle
from data_generator import DataGenerator
import pandas as pd
import scipy.stats as stats
from scipy.stats import f_oneway

number_of_users, user_filename = 10, "user_data.sql"
number_of_ingredients, ingredient_filename = 100, "ingredient_data.sql"
number_of_products, product_filename = 30, "product_data.sql"
number_of_dietitians, dietitian_filename = 2, "dietitian_data.sql"
number_of_clients, client_filename = 8, "client_data.sql"
number_of_daily_schedule, daily_schedule_filename = 1000, "daily_schedule_data.sql"
number_of_product_ingredient, product_ingredient_filename = 200, "product_ingredient_data.sql"


def generate_insert_data():
    data_generator = DataGenerator()
    data_generator.create_data_user(number_of_users, user_filename)
    data_generator.create_data_ingredient(number_of_ingredients, ingredient_filename)
    data_generator.create_data_product(number_of_products, product_filename)
    data_generator.create_data_dietitian(number_of_dietitians, dietitian_filename, number_of_users)
    data_generator.create_data_client(number_of_clients, client_filename, number_of_users,
                                      min(number_of_dietitians, number_of_users))
    data_generator.create_data_daily_schedule(number_of_daily_schedule, daily_schedule_filename,
                                              min(number_of_clients, number_of_users,
                                                  number_of_users - number_of_dietitians), number_of_products)
    data_generator.create_data_product_ingredient(number_of_product_ingredient, product_ingredient_filename,
                                                  number_of_ingredients, number_of_products)


def run_sql_file(filename):
    fd = open("sql/" + filename, 'r')
    sql_file = fd.read()
    fd.close()

    sql_commands = sql_file.split(';')
    sql_commands.pop()

    for command in sql_commands:
        cursor.execute(command)


def create_database_with_data():
    run_sql_file('Create.sql')
    run_sql_file(user_filename)
    run_sql_file(ingredient_filename)
    run_sql_file(product_filename)
    run_sql_file(dietitian_filename)
    run_sql_file(client_filename)
    run_sql_file(daily_schedule_filename)
    run_sql_file(product_ingredient_filename)

def get_base_statistics(table_name, connection, columns):
    sql_select = "SELECT * FROM " + table_name
    df = pd.read_sql_query(sql_select, connection)
    print(table_name)
    print(df[columns].describe())

def normal(data):
    print("Badanie normalności rozkładu")
    stat, p_value = stats.shapiro(data)
    print(f'Statystyka: {stat}\nWartość p: {p_value}')

    if p_value < 0.05:
        print("Dane nie wykazują cech rozkładu normalnego.")
    else:
        print("Dane wykazują cechy rozkładu normalnego.")

def variance(data1, data2):
    stat, p_value = stats.levene(data1, data2)
    print(f'Statystyka: {stat}\nWartość p: {p_value}')

    if p_value < 0.05:
        print("Istnieje istotna różnica w wariancjach.")
    else:
        print("Brak istotnej różnicy w wariancjach.")

def dependent(data1, data2, variables_to_test):
    for variable in variables_to_test:
        data1_test = data1[variable]
        data2_test = data2[variable]
        t_statistic, p_value = stats.ttest_rel(data1_test, data2_test)
        print(f'{variable}: Statystyka testowa: {t_statistic}\nWartość p: {p_value}')

        if p_value < 0.05:
            print("Istnieją istotne różnice między zmiennymi.")
        else:
            print("Brak istotnych różnic między zmiennymi.")


def independent(data1, data2, variables_to_test):
    for variable in variables_to_test:
        data1_test = data1[variable]
        data2_test = data2[variable]
        t_statistic, p_value = stats.ttest_ind(data1_test, data2_test)
        print(f'{variable}: Statystyka testowa: {t_statistic}\nWartość p: {p_value}')

        if p_value < 0.05:
            print("Istnieją istotne różnice między zmiennymi.")
        else:
            print("Brak istotnych różnic między zmiennymi.")

def anova(data1, data2, data3):
    f_statistic, p_value = f_oneway(data1, data2, data3)
    print(f'F-Statistic: {f_statistic}\nP-Value: {p_value}')

    if p_value < 0.05:
        print("Istnieją istotne różnice między grupami.")
    else:
        print("Brak istotnych różnic między grupami.")

if __name__ == "__main__":
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")
    connection = cx_Oracle.connect(user="wojciechowskib", password="bartosz",
                                   dsn="213.184.8.44:1521/ORCL")
    cursor = connection.cursor()

    print("Generating insert data")
    generate_insert_data()

    try:
        print("Creating database")
        create_database_with_data()
    except:
        print("Something went wrong, dropping database and creating from scratch")
        try:
            run_sql_file('Drop.sql')
            create_database_with_data()
        except:
            print("Something went wrong, try again")
            run_sql_file('Drop.sql')
    connection.commit()

    print("\nStatystyka opisowa dla tabel")
    get_base_statistics("INGREDIENT", connection, ['CARBS', 'COST', 'FAT', 'PROTEIN', 'CALORIES'])
    get_base_statistics("\"USER\"", connection, ['DATE_OF_BIRTH'])
    get_base_statistics("PRODUCT", connection, ['RATING'])
    get_base_statistics("PRODUCT_INGREDIENT", connection, ['AMOUNT'])
    get_base_statistics("DAILY_SCHEDULE", connection, ['DATE_OF_DIET', 'OPINION'])

    print("\nStatystyka opisowa dla tabeli DAILY_SCHEDULE dla poszczególnych miesięcy [styczeń, luty]")
    sql_select = "SELECT * FROM DAILY_SCHEDULE INNER JOIN PRODUCT P on P.ID_PRODUCT = DAILY_SCHEDULE.ID_PRODUCT"
    df = pd.read_sql_query(sql_select, connection)
    desired_months = [1, 2]
    df['OPINION'] = df['OPINION'].astype(int)
    df['PREP_TIME'] = pd.to_timedelta(df['PREP_TIME'])
    df_january_february = df[df['DATE_OF_DIET'].dt.month.isin(desired_months)].copy()
    print(df_january_february[['RATING', 'OPINION', 'PREP_TIME']].describe())

    print("\nSkrypty testujące hipotezy na tabeli INGREDIENT")
    df_ingredient = pd.read_sql_query("SELECT * FROM INGREDIENT", connection)
    normal(df_ingredient['COST'])
    variance(df_ingredient['PROTEIN'], df_ingredient['COST'])

    print("\nTesty dla zmiennych zależnych, niezależnych")
    desired_months = [3, 4]
    df_november_december = df[df['DATE_OF_DIET'].dt.month.isin(desired_months)].copy()
    independent(df_january_february, df_november_december, ['OPINION', 'RATING'])

    # Pomiędzy rokiem 2022 a 2023 wprowadziliśmy poprawki w recepturach składników i chcemy sprawdzić czy pomogło
    dependent(df[df['DATE_OF_DIET'].dt.year.isin([2022])].copy(), df[df['DATE_OF_DIET'].dt.year.isin([2023])].copy(), ['OPINION', 'RATING', 'PREP_TIME'])

    print("\nTesty dla wielu średnich (analiza wariancji)")
    anova(df_ingredient['PROTEIN'], df_ingredient['FAT'], df_ingredient['CARBS'])

    cursor.close()
    connection.close()
