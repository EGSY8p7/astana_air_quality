#!/usr/bin/env python3

import sys
import os
import sqlite3
import requests
import pickle
import json
import scraperwiki
#import pandas as pd

def main(argv):

    city = 'astana'
    accesstoken = '153147500b88026a9bc053bdf5c2b382cb90e806'
    notify = 'False'
    sendTrayNotification = False


    url = 'http://api.waqi.info/feed/'+city+'/?token=' + accesstoken
    #print('URL: ',url)

    r = requests.get(url, auth=('user', 'pass'))

    if r.status_code == 200:
        import json
        data = r.json()
        with open('aqi.json', 'w') as outfile:
            json.dump(data, outfile)

        value = data['data']['iaqi']['pm25']['v']
        toDisplay = str(value)


        if value > 0 and value < 50:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Healthy - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Healthy - " + toDisplay)

        elif value > 50 and value < 100:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Moderate - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Moderate - " + toDisplay)

        elif value > 100 and value < 150:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Sensitive - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Sensitive - " + toDisplay)

        elif value > 150 and value < 200:
            notify = 'notify-send "Air Quality Alert:" "Current Value: UnHealhty - "' + toDisplay
            print ("Air Quality Alert:" "Current Value: UnHealhty - " + toDisplay)

        elif value > 200 and value < 250:
            notify = 'notify-send "Air Quality Alert:" "Current Very Unhealhty - "' + toDisplay
            print ("Air Quality Alert:" "Current Very Unhealhty - " + toDisplay)

        elif value > 250 and value > 300:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Hazardous -  "' + toDisplay
            print ("Air Quality Alert:" "Current Value: Hazardous -  " + toDisplay)

    else:
        notify = 'notify-send "Error: " "Unable to Connect"'
        print ('Error: Unable to connect to server')

    if sendTrayNotification:
        os.system(notify)
    else:
        print ('[Debug] Tray Notification is off.')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
class Object(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
with open('aqi.json', encoding='utf-8') as data_file:
    datat = json.loads(data_file.read())
with open('saveobj1.pkl', 'wb') as output:
    data1 = Object('Date', datat['data']['time']['s'])
    pickle.dump(data1, output, pickle.HIGHEST_PROTOCOL)
    data2 = Object('Pm25', datat['data']['iaqi']['pm25']['v'])
    pickle.dump(data2, output, pickle.HIGHEST_PROTOCOL)
del data1
del data2
with open('saveobj1.pkl', 'rb') as input:
    data1 = pickle.load(input)
    data2 = pickle.load(input)
coll = (2, data1.value, data2.value)
scraperwiki.sqlite.save(unique_keys=['id'], data={"date": DATE, "pm25": INT}) 
scraperwiki.sql.select("* from data where 'date'= data1.value")
scraperwiki.sql.select("* from data where 'date'= data2.value")
#con = sqlite3.connect('aqi.sqlite')
'''with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS AirData")
    cur.execute("CREATE TABLE  AirData(Id INT, Date DATE, Pm25 INT)")
    cur.execute("INSERT INTO AirData VALUES (?, ?, ?)", coll)
table = pd.read_sql_query("SELECT * FROM AirData", con)
table.head()'''
