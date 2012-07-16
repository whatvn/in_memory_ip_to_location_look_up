#!/usr/bin/env python
"""
Querry db information and create a tree map of
IP, Location, Service local cache
"""

import MySQLdb
from collections import OrderedDict

class IPGeoDB(object):
    conn = None
    cursor = None
    
    def __init__(self, host, user, password, dbName, _temp = {}, IPGeoValue = OrderedDict()):
        self.db_host = host 
        self.db_user = user
        self.db_password = password 
        self.db_name = dbName
        self.IPGeoValue = IPGeoValue
        self._temp 		= _temp 

    def get(self, endNum, beginNum, info):
        self._temp[endNum] = [beginNum, info] 
   
    def sortedTree(self):
        for key in sorted(self._temp):
            self.IPGeoValue[key] = self._temp.get(key)
        return self.IPGeoValue 

    def connect(self):
        self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def RecoverDB(self): 
        self.connect()
        self.cursor.execute("select beginNum, endNum, Location, Service from ip_detail")         
        rows = self.cursor.fetchall() 
        for sqlResult in rows:
            self.get(sqlResult[1], sqlResult[0], sqlResult[2] + sqlResult[3]) 
        GeoCache  = OrderedDict()
        GeoCache = self.sortedTree() 
        return GeoCache 
