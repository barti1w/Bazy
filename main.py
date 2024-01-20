import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")
connection = cx_Oracle.connect(user="wojciechowskib", password="bartosz",
                               dsn="213.184.8.44:1521/ORCL")
cursor = connection.cursor()

def run_sql_file(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')
    sqlCommands.pop()

    for command in sqlCommands:
        cursor.execute(command)

try:
    run_sql_file('sql/Create.sql')
except:
    run_sql_file('sql/Drop.sql')
