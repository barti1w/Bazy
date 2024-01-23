import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()


class DataGenerator:
    def __init__(self):
        self.dietitian_user_ids = set()

    def create_data_user(self, num_records, file_name):
        insert_all_statements = []

        for i in range(1, num_records + 1):
            id_user = i
            apartment_number = fake.building_number()
            building_number = fake.building_number()
            city = fake.city()
            country = fake.country()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            login = fake.user_name()
            password = fake.password()
            phone_number = fake.phone_number()
            postal_code = fake.zipcode()
            role = random.choice(
                ['ADMIN', 'CLIENT', 'DIETITIAN'])
            street = fake.street_address()
            pesel = fake.random_int(min=10000000000, max=99999999999)
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime(
                '%Y-%m-%d')

            insert_statement = (
                f"   INTO \"USER\" (id_user, apartment_number, building_number, city, country, email, "
                f"first_name, last_name, login, password, phone_number, postal_code, role, street, pesel, date_of_birth) "
                f"VALUES ({id_user}, '{apartment_number}', '{building_number}', '{city}', '{country}', '{email}', "
                f"'{first_name}', '{last_name}', '{login}', '{password}', '{phone_number}', '{postal_code}', '{role}', "
                f"'{street}', '{pesel}', '{date_of_birth}')"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_ingredient(self, num_records, file_name):
        def calculate_calories(carbs, fat, protein):
            return round(4 * carbs + 9 * fat + 4 * protein, 2)

        insert_all_statements = []

        for i in range(1, num_records + 1):
            id_ingredient = i
            carbs = round(random.uniform(1, 50), 2)
            cost = round(random.uniform(0.5, 10), 2)
            fat = round(random.uniform(0.1, 20), 2)
            name = fake.word() + " Ingredient"
            protein = round(random.uniform(1, 30), 2)
            calories = calculate_calories(carbs, fat, protein)

            insert_statement = (
                f"   INTO ingredient (id_ingredient, carbs, cost, fat, name, protein, calories) "
                f"VALUES ({id_ingredient}, {carbs}, {cost}, {fat}, '{name}', {protein}, {calories})"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_product(self, num_records, file_name):
        insert_all_statements = []

        for i in range(1, num_records + 1):
            id_product = i
            meal = random.choice(['BREAKFAST', 'DINNER', 'SUPPER', 'SNACK'])
            name = fake.word() + " Product"
            prep_time = fake.time()
            rating = round(random.uniform(1, 5), 2)
            product_type = random.choice(['MEAT', 'VEGAN', 'KETOGENIC'])

            insert_statement = (
                f"   INTO product (id_product, meal, name, prep_time, rating, type) "
                f"VALUES ({id_product}, '{meal}', '{name}', '{prep_time}', {rating}, '{product_type}')"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_dietitian(self, num_records, file_name, max_user_id):
        num_records = min(num_records, max_user_id)

        dietitian_user_ids = random.sample(range(1, max_user_id + 1), num_records)
        self.dietitian_user_ids.update(dietitian_user_ids)

        insert_all_statements = []

        for i in range(1, num_records + 1):
            id_dietitian = i
            company_apartment_number = fake.building_number()
            company_building_number = fake.building_number()
            company_city = fake.city()
            company_country = fake.country()
            company_postal_code = fake.zipcode()
            company_street = fake.street_address()
            id_user = dietitian_user_ids[i - 1]

            insert_statement = (
                f"   INTO dietitian (id_dietitian, company_apartment_number, company_building_number, "
                f"company_city, company_country, company_postal_code, company_street, id_user) "
                f"VALUES ({id_dietitian}, '{company_apartment_number}', '{company_building_number}', "
                f"'{company_city}', '{company_country}', '{company_postal_code}', '{company_street}', {id_user})"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_client(self, num_records, file_name, max_user_id, max_dietitian_id):
        num_records = min(num_records, max_user_id, max_user_id - max_dietitian_id)

        user_ids_not_assigned = list(set(range(1, max_user_id + 1)) - self.dietitian_user_ids)
        user_ids = random.sample(user_ids_not_assigned, num_records)

        insert_all_statements = []

        for i in range(1, num_records + 1):
            id_client = i
            id_user = user_ids[i - 1]
            id_dietitian = random.randint(1, max_dietitian_id)

            insert_statement = (
                f"   INTO client (id_client, id_user, id_dietitian) "
                f"VALUES ({id_client}, {id_user}, {id_dietitian})"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_daily_schedule(self, num_records, file_name, max_client_id, max_product_id):
        end = datetime.strptime("25-01-2024", "%d-%m-%Y")
        start = end - timedelta(days=num_records)
        dates_of_diet = [start + timedelta(days=x) for x in range(0, (end - start).days)]

        id_client_id_product_date_of_diet = set()
        insert_all_statements = []

        for i in range(num_records):
            id_client = random.randint(1, max_client_id)
            id_product = random.randint(1, max_product_id)
            date_of_diet = dates_of_diet[i].strftime('%Y-%m-%d')
            comment = fake.text(max_nb_chars=255)
            opinion = random.choice(['1', '0', '-1'])

            while (id_client, id_product, date_of_diet) in id_client_id_product_date_of_diet:
                id_client = random.randint(1, max_client_id)
                id_product = random.randint(1, max_product_id)
                date_of_diet = dates_of_diet[i].strftime('%Y-%m-%d')

            insert_statement = (
                f"   INTO daily_schedule (id_client, id_product, \"comment\", date_of_diet, opinion) "
                f"VALUES ({id_client}, {id_product}, '{comment}', TO_DATE('{date_of_diet}', 'YYYY-MM-DD'), '{opinion}')"
            )

            id_client_id_product_date_of_diet.add((id_client, id_product, date_of_diet))

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)

    def create_data_product_ingredient(self, num_records, file_name, max_ingredient_id, max_product_id):
        num_records = min(num_records, max_ingredient_id * max_product_id)

        amounts = [fake.random_int(min=1, max=100) for _ in range(num_records)]

        id_ingredient_id_product = set()
        insert_all_statements = []

        for i in range(num_records):
            id_ingredient = random.randint(1, max_ingredient_id)
            id_product = random.randint(1, max_product_id)
            amount = amounts[i]

            while (id_ingredient, id_product) in id_ingredient_id_product:
                id_ingredient = random.randint(1, max_ingredient_id)
                id_product = random.randint(1, max_product_id)

            id_ingredient_id_product.add((id_ingredient, id_product))

            insert_statement = (
                f"   INTO product_ingredient (id_ingredient, id_product, amount) "
                f"VALUES ({id_ingredient}, {id_product}, '{amount}')"
            )

            insert_all_statements.append(insert_statement)

        insert_all_statement = "\n".join(insert_all_statements)
        final_statement = f"INSERT ALL\n{insert_all_statement}\nSELECT 1 FROM DUAL;"

        with open("sql/" + file_name, "w") as sql_file:
            sql_file.write(final_statement)
