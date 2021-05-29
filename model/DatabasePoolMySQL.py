# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:28:22 2021

@author: Lenovo
"""
from config.Settings import Settings
from mysql.connector import Error, pooling

import sys

class DatabasePool:
    
    # class variable
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name = 'ws_pool',
            pool_size = 5,
            host = Settings.host,
            port = 3306,
            user = Settings.user,
            password = Settings.password,
            database= Settings.database
        )
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        sys.exit(1)
    
    @classmethod
    def getConnection(cls):
        dbConn = cls.connection_pool.get_connection()
    
        return dbConn
