# coding=utf-8
import pyodbc


def Server_1(ip):
    server = 'localhost'
    database = 'SHOP'
    username = 'sa'
    password = '123456'

    con = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
        autocommit=True)
    cursor = con.cursor()
    return cursor
