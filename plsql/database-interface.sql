-- Dla przykładu możliwość dodawania/usuwania/aktualizowania rekordów w bazie za pomocą procedur i funkcji została wykonana tylko na jednej tabeli
CREATE
    OR REPLACE PACKAGE USER_INTERFACE AS
    PROCEDURE insert_user(
        p_apartment_number VARCHAR2 DEFAULT NULL,
        p_building_number VARCHAR2 DEFAULT NULL,
        p_city VARCHAR2 DEFAULT NULL,
        p_country VARCHAR2 DEFAULT NULL,
        p_email VARCHAR2 DEFAULT NULL,
        p_first_name VARCHAR2 DEFAULT NULL,
        p_last_name VARCHAR2 DEFAULT NULL,
        p_login VARCHAR2 DEFAULT NULL,
        p_password VARCHAR2 DEFAULT NULL,
        p_phone_number VARCHAR2 DEFAULT NULL,
        p_postal_code VARCHAR2 DEFAULT NULL,
        p_role VARCHAR2 DEFAULT NULL,
        p_street VARCHAR2 DEFAULT NULL,
        p_pesel VARCHAR2 DEFAULT NULL,
        p_date_of_birth DATE DEFAULT NULL
    );

    PROCEDURE delete_user(p_user_id NUMBER);

    PROCEDURE update_user(
        p_user_id NUMBER,
        p_apartment_number VARCHAR2 DEFAULT NULL,
        p_building_number VARCHAR2 DEFAULT NULL,
        p_city VARCHAR2 DEFAULT NULL,
        p_country VARCHAR2 DEFAULT NULL,
        p_email VARCHAR2 DEFAULT NULL,
        p_first_name VARCHAR2 DEFAULT NULL,
        p_last_name VARCHAR2 DEFAULT NULL,
        p_login VARCHAR2 DEFAULT NULL,
        p_password VARCHAR2 DEFAULT NULL,
        p_phone_number VARCHAR2 DEFAULT NULL,
        p_postal_code VARCHAR2 DEFAULT NULL,
        p_role VARCHAR2 DEFAULT NULL,
        p_street VARCHAR2 DEFAULT NULL,
        p_pesel VARCHAR2 DEFAULT NULL,
        p_date_of_birth DATE DEFAULT NULL
    );

END USER_INTERFACE;
/

CREATE
    OR REPLACE PACKAGE BODY USER_INTERFACE AS
    PROCEDURE insert_user(
        p_apartment_number VARCHAR2 DEFAULT NULL,
        p_building_number VARCHAR2 DEFAULT NULL,
        p_city VARCHAR2 DEFAULT NULL,
        p_country VARCHAR2 DEFAULT NULL,
        p_email VARCHAR2 DEFAULT NULL,
        p_first_name VARCHAR2 DEFAULT NULL,
        p_last_name VARCHAR2 DEFAULT NULL,
        p_login VARCHAR2 DEFAULT NULL,
        p_password VARCHAR2 DEFAULT NULL,
        p_phone_number VARCHAR2 DEFAULT NULL,
        p_postal_code VARCHAR2 DEFAULT NULL,
        p_role VARCHAR2 DEFAULT NULL,
        p_street VARCHAR2 DEFAULT NULL,
        p_pesel VARCHAR2 DEFAULT NULL,
        p_date_of_birth DATE DEFAULT NULL
    ) IS
        numer_max NUMBER(4);
    BEGIN
        IF
            p_first_name IS NULL OR p_last_name IS NULL OR p_role IS NULL THEN
            RAISE_APPLICATION_ERROR(-20001, 'First Name, Last Name, and Role cannot be null.');
        END IF;

        SELECT ID_USER
        INTO numer_max
        FROM "USER"
        ORDER BY ID_USER DESC FETCH NEXT 1 ROWS ONLY;


        INSERT INTO "USER" (ID_USER,
                            APARTMENT_NUMBER,
                            BUILDING_NUMBER,
                            CITY,
                            COUNTRY,
                            EMAIL,
                            FIRST_NAME,
                            LAST_NAME,
                            LOGIN,
                            PASSWORD,
                            PHONE_NUMBER,
                            POSTAL_CODE,
                            ROLE,
                            STREET,
                            PESEL,
                            DATE_OF_BIRTH)
        VALUES (numer_max + 1,
                p_apartment_number,
                p_building_number,
                p_city,
                p_country,
                p_email,
                p_first_name,
                p_last_name,
                p_login,
                p_password,
                p_phone_number,
                p_postal_code,
                p_role,
                p_street,
                p_pesel,
                p_date_of_birth);
    END;

    PROCEDURE delete_user(p_user_id NUMBER) IS
        v_user_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_user_count FROM "USER" WHERE ID_USER = p_user_id;

        IF v_user_count = 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'User with ID ' || p_user_id || ' does not exist.');
        ELSE
            DELETE FROM "USER" WHERE ID_USER = p_user_id;
        END IF;
    END;

    PROCEDURE update_user(
        p_user_id NUMBER,
        p_apartment_number VARCHAR2 DEFAULT NULL,
        p_building_number VARCHAR2 DEFAULT NULL,
        p_city VARCHAR2 DEFAULT NULL,
        p_country VARCHAR2 DEFAULT NULL,
        p_email VARCHAR2 DEFAULT NULL,
        p_first_name VARCHAR2 DEFAULT NULL,
        p_last_name VARCHAR2 DEFAULT NULL,
        p_login VARCHAR2 DEFAULT NULL,
        p_password VARCHAR2 DEFAULT NULL,
        p_phone_number VARCHAR2 DEFAULT NULL,
        p_postal_code VARCHAR2 DEFAULT NULL,
        p_role VARCHAR2 DEFAULT NULL,
        p_street VARCHAR2 DEFAULT NULL,
        p_pesel VARCHAR2 DEFAULT NULL,
        p_date_of_birth DATE DEFAULT NULL
    ) IS
        v_user_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_user_count FROM "USER" WHERE ID_USER = p_user_id;

        IF v_user_count = 0 THEN
            RAISE_APPLICATION_ERROR(-20003, 'User with ID ' || p_user_id || ' does not exist.');
        ELSE
            UPDATE "USER"
            SET APARTMENT_NUMBER = NVL(p_apartment_number, APARTMENT_NUMBER),
                BUILDING_NUMBER  = NVL(p_building_number, BUILDING_NUMBER),
                CITY             = NVL(p_city, CITY),
                COUNTRY          = NVL(p_country, COUNTRY),
                EMAIL            = NVL(p_email, EMAIL),
                FIRST_NAME       = NVL(p_first_name, FIRST_NAME),
                LAST_NAME        = NVL(p_last_name, LAST_NAME),
                LOGIN            = NVL(p_login, LOGIN),
                PASSWORD         = NVL(p_password, PASSWORD),
                PHONE_NUMBER     = NVL(p_phone_number, PHONE_NUMBER),
                POSTAL_CODE      = NVL(p_postal_code, POSTAL_CODE),
                ROLE             = NVL(p_role, ROLE),
                STREET           = NVL(p_street, STREET),
                PESEL            = NVL(p_pesel, PESEL),
                DATE_OF_BIRTH    = NVL(p_date_of_birth, DATE_OF_BIRTH)
            WHERE ID_USER = p_user_id;
        END IF;
    END;

END USER_INTERFACE;
/
