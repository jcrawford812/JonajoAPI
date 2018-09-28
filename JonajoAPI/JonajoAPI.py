from flask import Flask, request
import pymongo
from pymongo import MongoClient
import json
import pprint

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Root of API"

@app.route("/search")
def search():
    html = """<form method="post" action="/results">
    <p>Search for a city by name:</p>
    <tr><td>City:</td><td><input name="city" type="text" width="60" /></td></tr>
    <p><input value="Search" type="submit" /></p>
    </form>"""    
    return html

@app.route("/results", methods = ['post'])
def results():
    #With some time of authentication enabled allow the call to happen and return results.
    #if validAPIRequest(request.form['apikey']):
        results = []
        for result in collection.find({"city": {'$regex':'^'+str.upper(request.form['city'])}}):
            results.append(result)
        return json.dumps(results)
    #else
    #   return "API Key not authorized"
 
#Verifing calls against API
def validAPIrequest(APIKey):
    #Collection contains list of all API Key data, max uses, uses so far.
    securityDB = client.APISecurityDB
    secCollection = securityDB.SecurityCollection
    #Verify we find their submitted key
    if secCollection.findone({'_id' : APIKey}).count == 1:
        key = secCollection.findone({'_id' : APIKey}).count
        #Check key is valid and they still have calls remaining. Then increase their calls used somewhere in process
        if { key : 'valid'} == 'T' and {key :'max uses'} - {key:'total uses'} > 0:
            return True
    return False

client = MongoClient("mongodb+srv://JonajoAPIUser:APIUser123!@cluster0-vyv3g.mongodb.net/test?retryWrites=true")
db = client.JonajoAPI
collection = db.Collection1

if __name__ == '__main__':
    app.run(debug=False)