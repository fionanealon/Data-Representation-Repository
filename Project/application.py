from flask import Flask, jsonify, request, abort
from stationDAO import stationDAO

app = Flask(__name__, static_url_path='', static_folder='.')

fuel_stations=[
    { "id":1, "station_name":"PG&E - New York City", "fuel_type_code":"CNG", "zip":"85126"},
    { "id":2, "station_name":"PG&E - Raleigh", "fuel_type_code":"ELEC", "zip":"83611",},
    { "id":3, "station_name":"Hilton - Charleston", "fuel_type_code":"LNG", "zip":"81911"}
]
nextId=4

# curl "http://127.0.0.1:5000/fuel_stations"
@app.route('/fuel_stations')
def getAll():
    #print("in getall")
    results = stationDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/fuel_stations/1"
@app.route('/fuel_stations/<int:id>')
def findById(id):
    foundFuel_station = stationDAO.findByID(id)

    return jsonify(foundFuel_station)


#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books
@app.route('/fuel_stations', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    fuel_station = {
        "station_name": request.json['station_name'],
        "fuel_type_code": request.json['fuel_type_code'],
        "zip": request.json['zip'],
    }
    values =(fuel_station['station_name'],fuel_station['fuel_type_code'],fuel_station['zip'])
    newId = stationDAO.create(values)
    fuel_station['id'] = newId
    return jsonify(fuel_station)

# curl  -i -H "Content-Type:application/json" -X PUT -d "{\"station_name\":\"Texaco New York\",\"fuel_type_code\":\"ELEC\",\"zip\":34567}" http://127.0.0.1:5000/fuel_stations/1
@app.route('/fuel_stations/<int:id>', methods=['PUT'])
def update(id):
    foundFuel_stations = list(filter(lambda t: t['id']== id, fuel_stations))
    if (len(foundFuel_stations) == 0):
        abort(404)
    foundFuel_station = foundFuel_stations[0]
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'zip' in reqJson and type(reqJson['zip']) is not int:
        abort(400)
    if 'station_name' in reqJson:
        foundFuel_station['station_name'] = reqJson['station_name']
    if 'fuel_type_code' in reqJson:
        foundFuel_station['fuel_type_code'] = reqJson['fuel_type_code']
    if 'zip' in reqJson:
        foundFuel_station['zip'] = reqJson['zip']  
    values = (foundFuel_station['station_name'],foundFuel_station['fuel_type_code'],foundFuel_station['zip'],foundFuel_station['id'])
    stationDAO.update(values)     
    return jsonify(foundFuel_station)   

#curl -X DELETE "http://127.0.0.1:5000/fuel_stations/2"      
@app.route('/fuel_stations/<int:id>' , methods=['DELETE'])
def delete(id):
    stationDAO.delete(id)
    return jsonify({"done":True})

if __name__ == '__main__' :
    app.run(debug= True)