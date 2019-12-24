import requests
import json
from xlwt import *
import mysql.connector
import xlrd

url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1.json?&state=CA&limit=10&api_key=yZd77LzcdXQO85ACkp908Wgcb9liyUTTYgPNhZ1h&format=JSON'
response = requests.get(url)

response = requests.get(url)
data = response.json()

for fuel_station in data["fuel_stations"]:
    filename = '1.json'
    # Writing JSON data
    f =  open(filename, 'w')
    json.dump(data, f, indent=4)
    #print(response.text)

    w = Workbook()
    ws = w.add_sheet('stations')
    row = 0
    ws.write(row,0,"Name")
    ws.write(row,1,"Zip")
    ws.write(row,2,"Fuel_Type")
    row += 1 
    for fuel_station in data["fuel_stations"]:
        ws.write(row,0,fuel_station["station_name"])
        ws.write(row,1,fuel_station["zip"])
        ws.write(row,2,fuel_station["fuel_type_code"])
        row += 1

w.save('2.xls')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Data2019",
    database="datarepresentation"
)
cursor = db.cursor()


# Adapated from: https://stackoverflow.com/questions/51268991/importing-data-from-an-excel-file-using-python-into-sql-server 
# Open the workbook and define the worksheet
book = xlrd.open_workbook("2.xls")
sheet = book.sheet_by_name("stations")

sql="CREATE TABLE STATION (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250), fuel_type VARCHAR(250), zip INT)"
query = "INSERT INTO STATION (Name, Zip,Fuel_type) VALUES (%s,%s,%s)"

cursor.execute(sql)

for r in range(1, sheet.nrows):
    Name = sheet.cell(r,0).value
    Zip = sheet.cell(r,1).value
    Fuel_Type = sheet.cell(r,2).value


    # Assign values from each row
    values = (Name, Zip, Fuel_Type)

    # Execute sql Query
    cursor.execute(query, values)

# Commit the transaction
db.commit()

db.close()