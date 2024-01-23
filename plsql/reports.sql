CREATE TABLE "MONTHLY_REPORT"
(
    month   DATE,
    revenue NUMBER
);

CREATE TABLE "QUARTERLY_REPORT"
(
    quarter DATE,
    revenue NUMBER
);

CREATE TABLE "YEARLY_REPORT"
(
    year    DATE,
    revenue NUMBER
);


CREATE OR REPLACE PACKAGE REPORTS AS
    PROCEDURE GENERATE_MONTHLY(p_type IN VARCHAR2, p_meal IN VARCHAR2);
    PROCEDURE GENERATE_QUARTERLY(p_type IN VARCHAR2, p_meal IN VARCHAR2);
    PROCEDURE GENERATE_YEARLY(p_type IN VARCHAR2, p_meal IN VARCHAR2);
END REPORTS;
/

CREATE OR REPLACE PACKAGE BODY REPORTS AS
    PROCEDURE GENERATE_MONTHLY(p_type IN VARCHAR2, p_meal IN VARCHAR2) IS
    BEGIN
        DELETE FROM MONTHLY_REPORT;
        FOR monthly_data IN (
            SELECT TRUNC(DATE_OF_DIET, 'MM') AS month, SUM(i.COST) AS revenue
            FROM DAILY_SCHEDULE ds
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT P on P.ID_PRODUCT = ds.ID_PRODUCT
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT_INGREDIENT PI on P.ID_PRODUCT = PI.ID_PRODUCT
                     LEFT JOIN INGREDIENT i on i.ID_INGREDIENT = PI.ID_INGREDIENT
            WHERE (p_type IS NULL OR P.TYPE = p_type)
              AND (p_meal IS NULL OR P.MEAL = p_meal)
            GROUP BY TRUNC(DATE_OF_DIET, 'MM')
            ORDER BY TRUNC(DATE_OF_DIET, 'MM')
            )
            LOOP
                INSERT INTO MONTHLY_REPORT (month, revenue)
                VALUES (monthly_data.month, monthly_data.revenue);
            END LOOP;
    END;

    PROCEDURE GENERATE_QUARTERLY(p_type IN VARCHAR2, p_meal IN VARCHAR2) IS
    BEGIN
        DELETE FROM QUARTERLY_REPORT;
        FOR monthly_data IN (
            SELECT TRUNC(DATE_OF_DIET, 'Q') AS quarter, SUM(i.COST) AS revenue
            FROM DAILY_SCHEDULE ds
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT P on P.ID_PRODUCT = ds.ID_PRODUCT
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT_INGREDIENT PI on P.ID_PRODUCT = PI.ID_PRODUCT
                     LEFT JOIN INGREDIENT i on i.ID_INGREDIENT = PI.ID_INGREDIENT
            WHERE (p_type IS NULL OR P.TYPE = p_type)
              AND (p_meal IS NULL OR P.MEAL = p_meal)
            GROUP BY TRUNC(DATE_OF_DIET, 'Q')
            ORDER BY TRUNC(DATE_OF_DIET, 'Q')
            )
            LOOP
                INSERT INTO QUARTERLY_REPORT (quarter, revenue)
                VALUES (monthly_data.quarter, monthly_data.revenue);
            END LOOP;
    END;

    PROCEDURE GENERATE_YEARLY(p_type IN VARCHAR2, p_meal IN VARCHAR2) IS
    BEGIN
        DELETE FROM YEARLY_REPORT;
        FOR monthly_data IN (
            SELECT TRUNC(DATE_OF_DIET, 'YYYY') AS year, SUM(i.COST) AS revenue
            FROM DAILY_SCHEDULE ds
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT P on P.ID_PRODUCT = ds.ID_PRODUCT
                     LEFT JOIN WOJCIECHOWSKIB.PRODUCT_INGREDIENT PI on P.ID_PRODUCT = PI.ID_PRODUCT
                     LEFT JOIN INGREDIENT i on i.ID_INGREDIENT = PI.ID_INGREDIENT
            WHERE (p_type IS NULL OR P.TYPE = p_type)
              AND (p_meal IS NULL OR P.MEAL = p_meal)
            GROUP BY TRUNC(DATE_OF_DIET, 'YYYY')
            ORDER BY TRUNC(DATE_OF_DIET, 'YYYY')
            )
            LOOP
                INSERT INTO YEARLY_REPORT (year, revenue)
                VALUES (monthly_data.year, monthly_data.revenue);
            END LOOP;
    END;

END REPORTS;
/

