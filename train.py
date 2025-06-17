import requests

URL = "https://api-v3.mbta.com"
APIKEY = "0bb673745a154df0a0d7363a97d41d1a"

def getRoutes(line):
    try:
        headers = {
            'X-Api-Key': APIKEY
        }
        
        response = requests.get(f"{URL}/vehicles?filter[route]={line}", headers = headers)
        if response.status_code == 200:
            trainInfo = response.json()
            trainData = trainInfo["data"]
            return trainData
        else:
            print('Error fetching data in getRoutes. Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error in getRoutes. Error:', e)
        return None

def getCommuterRoutes(line):
    try:
        headers = {
            'X-Api-Key': APIKEY
        }
        
        response = requests.get(f"{URL}/vehicles?filter[route_type]=2", headers = headers)
        if response.status_code == 200:
            trainInfo = response.json()
            trainData = trainInfo["data"]
            trains = []
            
            for train in trainData:
                #print(train["relationships"]["route"]["data"]["id"])
                #print('\n')
                if train["relationships"]["route"]["data"]["id"] == line:
                    trains.append(train)
            
            return trains
        else:
            print('Error fetching data in getRoutes. Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error in getRoutes. Error:', e)
        return None

def stoppedTrains(line):
    data = getRoutes(line)
    trains = []
    index = 1
        
    for train in data:
        trainID = train["relationships"]["stop"]["data"]["id"]
        directionID = train["attributes"]["direction_id"]
        trainStatus = train["attributes"]["current_status"]
        
        direction = "INBOUND" if directionID == 1 else "OUTBOUND"
        vehicleType = "BUS" if not train["attributes"]["carriages"] else "TRAIN"
        stopName = filterStop(trainID)
        
        print(f"{vehicleType} #{index}: {trainStatus}, {direction}, {stopName} \n")
        trains.append({
            vehicleType: {"number": index, "status": trainStatus, "direction": direction, "stopName": stopName}
        })
        index += 1
    
    if not trains:
        print("No trains available.")

def stoppedCommuter(line):
    data = getCommuterRoutes(line)
    trains = []
    index = 1
        
    for train in data:
        trainID = train["relationships"]["stop"]["data"]["id"]
        directionID = train["attributes"]["direction_id"]
        trainStatus = train["attributes"]["current_status"]
        
        direction = "INBOUND" if directionID == 1 else "OUTBOUND"
        stopName = filterStop(trainID)
        
        print(f"COMMUTER #{index}: {trainStatus}, {direction}, {stopName} \n")
        trains.append({
            "COMMUTER": {"number": index, "status": trainStatus, "direction": direction, "stopName": stopName}
        })
        index += 1
    
    if not trains:
        print("No trains available.")
    
    
def filterStop(stopID):
    stops = getStops()
    
    for stop in stops:
        #print(f"STOP: {stop} \n")
        if stop["id"] == stopID:
            return stop["attributes"]["name"]
    return None
    
def getStops():
    try:
        headers = {
            'X-Api-Key': APIKEY
        }
        
        response = requests.get(f"{URL}/stops", headers = headers)
        if response.status_code == 200:
            stopInfo = response.json()
            stopData = stopInfo["data"]
            return stopData
        else:
            print('Error fetching data in getStops. Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error in getStops. Error:', e)
        return None
    
def m():
    headers = {
        'X-Api-Key': APIKEY
    }
        
    response = requests.get(f"{URL}/stops", headers = headers)
    stop = response.json()
    stopData = stop["data"]
    
    places = []
    for place in stopData:
        places.append({"name": place["id"], "municipality": place["attributes"]["municipality"], "name": place["attributes"]["name"], "description": place["attributes"]["description"], "at_street": place["attributes"]["at_street"], "on_street": place["attributes"]["on_street"]})
    return places

def main():
    #print(getStops())
    #print(getRoutes("Blue"))
    #print(getCommuterRoutes("CR-Kingston"))
    #stoppedCommuter("CR-Kingston")
    #stoppedTrains("Orange")
    #stoppedTrains("116")
    #stoppedTrains("CR_Newburyport")
    #print(filterStop("70043"))
    f = open("stops.txt", "w")
    f.write(str(m()))

if __name__ == '__main__':
    main()
    
# "1001011101" each bit is a stop; string return; 1 at station 0 not station; blue line 12 stops
#bowdoin, gov center, state, aquarium, maverick, airport, wood island, orient heights, suffolk downs, beachmont, revere beach, wonderland
#Green-B, CR-Newburyport

