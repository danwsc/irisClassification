# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:28:22 2021

@author: Lenovo
"""
from config.Settings import Settings
import mariadb

import sys

class DatabasePool:
    
    # class variable
    try:
        connection_pool = mariadb.ConnectionPool(
            pool_name = 'ws_pool',
            pool_size = 5,
            host = Settings.host,
            port = 3306,
            user = Settings.user,
            password = Settings.password,
            database=Settings.database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    @classmethod
    def getConnection(cls):
        dbConn = cls.connection_pool.get_connection()
    
        return dbConn
