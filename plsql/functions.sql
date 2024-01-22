CREATE OR REPLACE FUNCTION birthPesel(pesel IN VARCHAR2) RETURN VARCHAR2 IS
    year_part  VARCHAR2(20);
    month_part VARCHAR2(20);
    day_part   VARCHAR2(20);
    whatDecade NUMBER;
    r          NUMBER;
BEGIN
    year_part := SUBSTR(pesel, 1, 2);
    month_part := SUBSTR(pesel, 3, 2);
    day_part := SUBSTR(pesel, 5, 2);
    whatDecade := TO_NUMBER(SUBSTR(month_part, 0, 1));
    r := MOD(TO_NUMBER(SUBSTR(month_part, 0, 1)), 2);
    IF r = 0 THEN
        dbms_output.PUT_LINE('');
    ELSE
        whatDecade := whatDecade - 1;
    END IF;
    whatDecade := CEIL(whatDecade) * 10;
    month_part := TO_CHAR(TO_NUMBER(month_part) - whatDecade);

    IF whatDecade = 80 THEN
        whatDecade := 18;
    ELSIF whatDecade = 00 THEN
        whatDecade := 19;
    ELSIF whatDecade = 20 THEN
        whatDecade := 20;
    ELSIF whatDecade = 40 THEN
        whatDecade := 21;
    ELSE
        whatDecade := 22;
    END IF;

    year_part := TO_CHAR(whatDecade) || year_part;
    return year_part || '-' || month_part || '-' || day_part;
end;