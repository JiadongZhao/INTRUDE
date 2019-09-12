import mysql.connector
import sys
import os
import platform

# Connect to MySQL database
with open('./input/mysqlParams.txt') as f:
    MYSQL_USER, MYSQL_PASS, MYSQL_HOST, PORT = f.read().splitlines()
# conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host=MYSQL_HOST, database='repolist', port='3306')
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host=MYSQL_HOST, database='fork', port=PORT)
cur = conn.cursor()
cur.execute("SELECT * FROM duppr_pair WHERE notes LIKE '%FP%'")  # get info about pr pair
FP_PR_info = cur.fetchall()
print("")