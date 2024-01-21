import cx_Oracle
from data_generator import DataGenerator
import pandas as pd

number_of_users, user_filename = 10, "user_data.sql"
number_of_ingredients, ingredient_filename = 100, "ingredient_data.sql"
number_of_products, product_filename = 30, "product_data.sql"
number_of_dietitians, dietitian_filename = 2, "dietitian_data.sql"
number_of_clients, client_filename = 8, "client_data.sql"
number_of_daily_schedule, daily_schedule_filename = 100, "daily_schedule_data.sql"
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

    print("Statystyka opisowa dla tabel")
    get_base_statistics("INGREDIENT", connection, ['CARBS', 'COST', 'FAT', 'PROTEIN', 'CALORIES'])
    get_base_statistics("\"USER\"", connection, ['DATE_OF_BIRTH'])
    get_base_statistics("PRODUCT", connection, ['RATING'])
    get_base_statistics("PRODUCT_INGREDIENT", connection, ['AMOUNT'])
    get_base_statistics("DAILY_SCHEDULE", connection, ['DATE_OF_DIET', 'OPINION'])

    print("Statystyka opisowa dla tabeli DAILY_SCHEDULE dla poszczególnych miesięcy")
    sql_select = "SELECT DATE_OF_DIET, RATING, OPINION, PREP_TIME FROM DAILY_SCHEDULE INNER JOIN PRODUCT P on P.ID_PRODUCT = DAILY_SCHEDULE.ID_PRODUCT"
    df = pd.read_sql_query(sql_select, connection)
    desired_months = [1, 2]
    filtered_df = df[df['DATE_OF_DIET'].dt.month.isin(desired_months)].copy()
    filtered_df['OPINION'] = filtered_df['OPINION'].astype(int)
    filtered_df['PREP_TIME'] = pd.to_timedelta(df['PREP_TIME'])
    print(filtered_df[['RATING', 'OPINION', 'PREP_TIME']].describe())


    connection.commit()
    cursor.close()
    connection.close()
