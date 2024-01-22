BEGIN
    EXECUTE IMMEDIATE 'CREATE TABLE USER_ARCHIVE
        (ID_USER NUMBER, APARTMENT_NUMBER VARCHAR2(255), BUILDING_NUMBER VARCHAR2(255), CITY VARCHAR2(255), COUNTRY VARCHAR2(255), EMAIL VARCHAR2(255), FIRST_NAME VARCHAR2(255), LAST_NAME VARCHAR2(255), LOGIN VARCHAR2(255), PASSWORD VARCHAR2(255), PHONE_NUMBER VARCHAR2(255), POSTAL_CODE VARCHAR2(255), ROLE VARCHAR2(10), STREET VARCHAR2(255), PESEL VARCHAR2(11), DATE_OF_BIRTH DATE, ARCHIVE_DATE DATE)';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            NULL;
        ELSE
            RAISE;
        END IF;
END;
/

CREATE OR REPLACE TRIGGER archive_user_trigger
    AFTER DELETE
    ON "USER"
    FOR EACH ROW
DECLARE
BEGIN
    INSERT INTO USER_ARCHIVE
    VALUES (:OLD.ID_USER, :OLD.APARTMENT_NUMBER, :OLD.BUILDING_NUMBER, :OLD.CITY,
            :OLD.COUNTRY, :OLD.EMAIL, :OLD.FIRST_NAME, :OLD.LAST_NAME, :OLD.LOGIN,
            :OLD.PASSWORD, :OLD.PHONE_NUMBER, :OLD.POSTAL_CODE, :OLD.ROLE, :OLD.STREET,
            :OLD.PESEL, :OLD.DATE_OF_BIRTH, SYSDATE);
END;
/

CREATE OR REPLACE TRIGGER validate_pesel_trigger
    BEFORE INSERT OR UPDATE
    ON "USER"
    FOR EACH ROW
DECLARE
    v_valid_pesel BOOLEAN;
BEGIN
    v_valid_pesel := TRUE;
    if :NEW.PESEL IS NOT NULL THEN
        v_valid_pesel := VALIDATORS.BIRTHPESEL(:NEW.PESEL, :NEW.DATE_OF_BIRTH);
    END IF;
    IF NOT v_valid_pesel THEN
        RAISE_APPLICATION_ERROR(-20004, 'Invalid PESEL for the given DATE_OF_BIRTH.');
    END IF;
END;
/