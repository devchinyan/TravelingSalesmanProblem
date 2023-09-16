from .graphAlgorithm import GraphAlgorithm
from .helper.distance.haversineDistance import HaversineDist
from typing import Dict
from os import getcwd

class TrainNetwork(GraphAlgorithm):
    def __init__(self):
        super().__init__()

    def dataLoadingAndPreprocessing(self,data:Dict):
        try:
            # initialization
            Vertices = []
            Edges = []
            
            #load data
            # data = loadData()
            keys = list(data.keys())
            values = list(data.values())
            
            #process data
            for key in keys:
                for value in values:
                    if value.get(key) :
                        stations = value.get(key)
                        for i in range(len(stations)):
                            Vertices.append({ 
                                "id": stations[i]["id"],
                                "stationName": stations[i]["stationName"], 
                                "coordinate": stations[i]["coordinate"] 
                            })

                            #Station Edges
                            if(i<len(stations)-1):
                                fromID = stations[i]["id"]
                                toID = stations[i+1]["id"]

                                disRes = HaversineDist(stations[i]["coordinate"],stations[i+1]["coordinate"])
                                if(disRes.get("err")): raise Exception(f'haversine dist error : {str(disRes["err"])}' )
                                distance = disRes["res"]

                                #Bidirectional
                                Edges.append({ "fromID":fromID, "toID":toID, "distance":distance});
                                Edges.append({ "toID": fromID, "fromID": toID, "distance":distance});

                            # Interchange Station Edges
                            if(stations[i].get("interchangeStation")):
                                for itc in stations[i]["interchangeStation"]:
                                    distRes = HaversineDist(stations[i]["coordinate"],itc["coordinate"])
                                    if(distRes.get("err")): raise Exception("exec2 "+str(distRes.get("err")))
                                    dist = distRes["res"]

                                    Edges.append({"fromID": stations[i]["id"], "toID": itc["id"], "distance":dist})
                                 
            return {"Vertices":Vertices,"Edges":Edges}
 
                    
        except Exception as error:
            print("dataLoadingAndPreprocessing error: ",error)
            return {"err":str(error), "errInfo":["class TrainNetwork","method verticesAndEdgesPopulation"]}
            
    def verticesAndEdgesPopulation(self):
        try:
            loadRes = self.dataLoadingAndPreprocessing()
            if(loadRes.get("err")): raise Exception(loadRes.get("err"))
            Vertices = loadRes["Vertices"]
            Edges = loadRes["Edges"]
                
            for v in Vertices:
                self.addVertices(v)

            for e in Edges:
                fromID = e["fromID"] 
                toID = e["toID"]
                distance = e["distance"]
                self.addEdges(fromID, toID, {"distance":distance})

        except Exception as error:
            return {"err":str(error), "errInfo":["class TrainNetwork","method verticesAndEdgesPopulation"]}



# def getTrainNetwork()->TrainNetwork:  
#     print(getcwd())
#     trainNetwork = TrainNetwork() 
#     trainNetwork.load("./trainNetwork.save.json")
#     return trainNetwork

# t = getTrainNetwork()