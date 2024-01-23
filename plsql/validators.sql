CREATE
    OR REPLACE PACKAGE VALIDATORS AS
    FUNCTION birthPesel(p_pesel in VARCHAR2, p_date_of_birth DATE) RETURN BOOLEAN;
end VALIDATORS;
/

CREATE OR REPLACE PACKAGE BODY VALIDATORS AS
    FUNCTION birthPesel(p_pesel IN VARCHAR2, p_date_of_birth DATE) RETURN BOOLEAN IS
        v_year_part  VARCHAR2(20);
        v_month_part VARCHAR2(20);
        v_day_part   VARCHAR2(20);
        v_whatDecade NUMBER;
        v_r          NUMBER;
        v_calc_date  DATE;
    BEGIN
        v_year_part := SUBSTR(p_pesel, 1, 2);
        v_month_part := SUBSTR(p_pesel, 3, 2);
        v_day_part := SUBSTR(p_pesel, 5, 2);
        v_whatDecade := TO_NUMBER(SUBSTR(v_month_part, 0, 1));
        v_r := MOD(TO_NUMBER(SUBSTR(v_month_part, 0, 1)), 2);
        IF v_r = 0 THEN
            dbms_output.PUT_LINE('');
        ELSE
            v_whatDecade := v_whatDecade - 1;
        END IF;
        v_whatDecade := CEIL(v_whatDecade) * 10;
        v_month_part := TO_CHAR(TO_NUMBER(v_month_part) - v_whatDecade, 'FM00');

        IF v_whatDecade = 80 THEN
            v_whatDecade := 18;
        ELSIF v_whatDecade = 00 THEN
            v_whatDecade := 19;
        ELSIF v_whatDecade = 20 THEN
            v_whatDecade := 20;
        ELSIF v_whatDecade = 40 THEN
            v_whatDecade := 21;
        ELSE
            v_whatDecade := 22;
        END IF;

        v_year_part := TO_CHAR(v_whatDecade) || v_year_part;
        DBMS_OUTPUT.PUT_LINE(v_year_part || '-' || v_month_part || '-' || v_day_part);
        v_calc_date := TO_DATE(v_year_part || '-' || v_month_part || '-' || v_day_part, 'YYYY-MM-DD');
        return v_calc_date = p_date_of_birth;
    end;
end VALIDATORS;
/