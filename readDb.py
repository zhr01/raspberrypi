#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('total.db')
print("Opened database successfully");

name=""
cursor = conn.execute("SELECT dname, code, type, sale FROM drinkcount WHERE code=6911988014276")

for row in cursor:
   print("dname = ", row[0])
   name = row[0]
   # print("code = ", row[1])
   # print("type = ", row[2])
   # print("sale = ", row[3], "\n")

if name != "" :
	print("exist")
else :
	print("do not exist")

print("Operation done successfully");
conn.close()