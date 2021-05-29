# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
from model.DatabasePool import DatabasePool
# from model.DatabasePoolMySQL import DatabasePool
from datetime import datetime

class Prediction:
    
    @classmethod
    def initPredInfo(cls):
        info = {}
        info['userid'] = -1
        info['sepalLength'] = 0.000
        info['sepalWidth'] = 0.000
        info['petalLength'] = 0.000
        info['petalWidth'] = 0.000
        info['prediction'] = 'Unknown'
        info['InsertionDate'] = datetime.now()

        return info

    @classmethod
    def loadPredInfo(cls, uid, spl, spw, ptl, ptw, prd):
        info = {}
        info['userid'] = uid
        info['sepalLength'] = spl
        info['sepalWidth'] = spw
        info['petalLength'] = ptl
        info['petalWidth'] = ptw
        info['prediction'] = prd
        info['InsertionDate'] = datetime.now()

        return info

    @classmethod
    def get(cls, predictionId):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM irisprediction WHERE predictionId=%s;"
            cursor.execute(sql,(predictionId,))
            predInfo = cursor.fetchone()
            return predInfo
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def insert(cls, info):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "INSERT INTO irisprediction (userid,sepalLength,sepalWidth,petalLength,petalWidth,prediction) \
                VALUES (%s,%s,%s,%s,%s,%s);"
            users = cursor.execute(sql, (info['userid'],
                                         info['sepalLength'],
                                         info['sepalWidth'],
                                         info['petalLength'],
                                         info['petalWidth'],
                                         info['prediction']))
            dbConn.commit()

            # rows = cursor.rowcount
            lastInsertId = cursor.lastrowid
            return lastInsertId
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def delete(cls, userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE FROM irisprediction WHERE predictionid=%s;"
            users = cursor.execute(sql, (userid,))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

