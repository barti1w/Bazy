CREATE TABLE "USER" (
    id_user INT NOT NULL,
    apartment_number VARCHAR(255) DEFAULT NULL,
    building_number VARCHAR(255) DEFAULT NULL,
    city VARCHAR(255) DEFAULT NULL,
    country VARCHAR(255) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    first_name VARCHAR(255) DEFAULT NULL,
    last_name VARCHAR(255) DEFAULT NULL,
    login VARCHAR(255) DEFAULT NULL,
    password VARCHAR(255) DEFAULT NULL,
    phone_number VARCHAR(255) DEFAULT NULL,
    postal_code VARCHAR(255) DEFAULT NULL,
    role VARCHAR2(10) CHECK( role IN ('ADMIN','CLIENT','DIETITIAN')),
    street VARCHAR(255) DEFAULT NULL,
    pesel VARCHAR(11) DEFAULT NULL,
    date_of_birth DATE DEFAULT NULL,
    PRIMARY KEY (id_user));

CREATE TABLE ingredient (
    id_ingredient INT NOT NULL,
    carbs FLOAT NOT NULL,
    cost FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    name VARCHAR(255) NOT NULL,
    protein FLOAT NOT NULL,
    calories FLOAT NOT NULL,
    PRIMARY KEY (id_ingredient));

CREATE TABLE product (
    id_product INT NOT NULL,
    meal VARCHAR2(10) CHECK( meal IN ('BREAKFAST', 'DINNER', 'SUPPER', 'SNACK')),
    name VARCHAR(255) DEFAULT NULL,
    prep_time VARCHAR(255) DEFAULT NULL,
    rating float DEFAULT NULL,
    type VARCHAR2(10) CHECK( type IN ('MEAT', 'VEGAN', 'KETOGENIC')),
    PRIMARY KEY (id_product));

CREATE TABLE dietitian (
    id_dietitian INT NOT NULL,
    company_apartment_number VARCHAR(255) DEFAULT NULL,
    company_building_number VARCHAR(255) DEFAULT NULL,
    company_city VARCHAR(255) DEFAULT NULL,
    company_country VARCHAR(255) DEFAULT NULL,
    company_postal_code VARCHAR(255) DEFAULT NULL,
    company_street VARCHAR(255) DEFAULT NULL,
    id_user INT DEFAULT NULL,
    PRIMARY KEY (id_dietitian),
    FOREIGN KEY (id_user) REFERENCES "USER" (id_user));

CREATE TABLE client (
    id_client INT NOT NULL,
    id_dietitian INT NOT NULL,
    id_user INT DEFAULT NULL,
    PRIMARY KEY (id_client),
    FOREIGN KEY (id_user) REFERENCES "USER" (id_user),
    FOREIGN KEY (id_dietitian) REFERENCES dietitian (id_dietitian));

CREATE TABLE daily_schedule (
    id_client INT NOT NULL,
    id_product INT NOT NULL,
    "comment" VARCHAR(255) DEFAULT NULL,
    date_of_diet date NOT NULL,
    opinion CHAR(2) CHECK (opinion IN ('1','0', '-1')),
    PRIMARY KEY (id_client,id_product, date_of_diet),
    FOREIGN KEY (id_product) REFERENCES product (id_product),
    FOREIGN KEY (id_client) REFERENCES client (id_client));

CREATE TABLE product_ingredient (
    id_ingredient INT NOT NULL,
    id_product INT NOT NULL,
    amount VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_ingredient,id_product),
    FOREIGN KEY (id_product) REFERENCES product (id_product),
    FOREIGN KEY (id_ingredient) REFERENCES ingredient (id_ingredient));