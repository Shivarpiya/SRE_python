import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from cassandra.cluster import Cluster
import pandas as pd
import json
from datetime import datetime
app = Flask(__name__)
cors = CORS(app)
import configparser 

config = configparser.ConfigParser()
config.read('regex.ini')

########### DB Functions #######################

## Connect to Cassandra
def connectCassandra():
    serverIP = "10.82.108.34"
    schema = 'insights'
    cluster = Cluster([serverIP])
    session = cluster.connect(schema)
    print("**** Connected to Cassandra ****")
    return session

## Select the data from Cassandra
def select_data(cql):
    print("**** SELECT FN ****")
    session = connectCassandra()
    selectDF = pd.DataFrame(list(session.execute(cql)))
    selectDict = selectDF.to_dict(orient='index')
    return selectDict

## Function to Insert / Update / Delete data from cassandra table
def cassandraTable(cql):
   print("*** INSERT/UPDATE/DELETE Data")
   session = connectCassandra()
   delete = session.execute(cql)
   print ("**** Table Updated ****")

###############################################


## Get the data from UI
@app.route('/logAggregation', methods=['POST'])
@cross_origin()
def logAggregation():
    print("** LOG Agg FN **")
    action = request.json.get("actionFlag")
    print("**** Action : "+action+" ****")
    data={}
    tablename = "logaggrigationtest1"
   
    if action == 'insert':
        data['uid'] = str(uuid.uuid1())
        data['datetime1']=datetime.now().strftime('%y-%m-%d %H:%M:%S')
        data['username']=request.json.get("username")
        data['patterntype'] = request.json.get("patternType")
        data['pattern'] =request.json.get("pattern")
        data['stringtype'] = request.json.get("serverDataType")
        #data['dateformat'] = request.json.get("dateformat")
        print(data)
        ## Get the regex pattern
        dtregex = config['DEFAULT'][data['pattern']]
        print("**** Regex : "+dtregex)
        insert_cql = "INSERT INTO "+tablename+" JSON '" + json.dumps(data)+"'"
        print("### Insert cql : "+insert_cql)
        ## Insert Data into DB
        cassandraTable(insert_cql)
        print("Inserted UID : "+data['uid'])
        ## Update config.ini file
        key=['username','sec','input','stringtype','startswith']
        values=["username = "+data['username'],"sec = "+data['patterntype'],"input = "+data['pattern'],"stringtype = "+data['stringtype'],"startswith = "+dtregex]
        for i in range(len(key)):
            updateConfig("config.ini",key[i],values[i])

    elif action == 'update':
        data['dateformat'] = request.json.get("dateformat")
        startswith = config['DEFAULT'][data['dateformat']]
        print("**** Regex : "+startswith)
        data['uid_d'] = request.json.get("uid")
        #data['editpattern'] = request.json.get("editpattern")
        data['patterntype'] = request.json.get("patterntype")
        #data['pattern'] =request.json.get("pattern")
        data['updatedPattern'] = request.json.get("updatedPattern")
        print("**** JSON Data ****")
        print(data)
        colname =  'pattern'
        value = data['updatedPattern']  
        #value =  'chittibomma123'
        #uid = '609f4852-0515-11ea-9cb3-fa163e1408a5'
        update_cql = "UPDATE "+tablename+" set "+colname+" = '"+value+"' where uid = "+data['uid_d']
        print("### Update cql : "+update_cql)
        # Update the data in DB
        cassandraTable(update_cql)
        print("Updated UID : "+data['uid_d'])
        ## Update config.ini file
        key=['input']
        values=["input = "+data['updatedPattern']]
        for i in range(len(key)):
            updateConfig("config.ini",key[i],values[i])

    elif action == 'delete':
        data['uid_d'] = request.json.get("uid")
        delete_cql = "DELETE FROM "+tablename+" WHERE uid="+data['uid_d']
        #delete_data(delete_cql)
        cassandraTable(delete_cql)
        print("Deleted UID :"+data['uid_d'])

    return "OK"


## List all the data
select_cql = "select * from logaggrigationtest1"
@app.route('/displayall', methods=['GET'])
def display_data():
    data_list = []
    data = select_data(select_cql) 
    data_list.append(data)
    return jsonify(data_list) 

## Function to update the config file
def updateConfig(filepath,searchFor,replaceWith):
    print("*** Config.ini details : ",filepath,searchFor,replaceWith)
    with open(filepath) as f:
        l = list(f)
    with open(filepath, 'w') as output:
        for line in l:
            if line.startswith(searchFor):
                output.write(replaceWith+'\n')
            else:
                output.write(line)
    return "Config File Updated"



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='9008')

