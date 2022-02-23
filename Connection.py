# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 08:00:24 2022

@author: Jonathan Martínez
"""

from MainFunctions import MainFunctions
from Answer import Answer
import pyodbc

class Connection():
    """
    This Class allows the connection to SQL Server, the connection data are on the JSON file.
    
    Public Methods
    --------------
    closeConnection,
    executeQuery,
    getConnection,
    getQuery.
    
    Privated Methods
    ----------------
    _readConfig.
    
    """

    def __init__(self):
        self.__mf = MainFunctions()
        config = self._readConfig()
        if config.getStatus():
            self.__server = config.getData()[0]
            self.__database = config.getData()[1]
            self.__user = config.getData()[2]
            self.__password = config.getData()[3]
            self.__connection = None
    
    def closeConnection(self):
        """
        This method closes the connection to SQL Server.

        Returns
        -------
        None.

        """
        self.__connection.close()
        
    def executeQuery(self,query):
        """
        This method allows execute a query into DB

        Parameters
        ----------
        query : string
            You can do an insert,update, delete or execute a stored procedure..

        Returns
        -------
        answer : Class
            Return status, message.

        """
        answer = Answer()
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(query)
            answer.load(True, "Query executed", None)
        except Exception as e:
            answer.load(False, "Connection.executeQuery: " + str(e), None)
        return answer
        
    def getConnection(self):
        """
        This method gets the connection to SQL Server, the data are in the section CONNECTION.

        Returns
        -------
        answer : Class
            Returns status, message.

        """
        answer = Answer()
        try:
            self.__connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.__server +';DATABASE='+ self.__database +';UID='+ self.__user +';PWD=' + self.__password)
            answer.load(True, 'Stablished Connection', None)
        except Exception as e:
            answer.load(False, 'Connection.getConnection: ' + str(e), None)
        return answer
         
    def getQuery(self,query):
        """
        This method allows to execute a query in SQL Server.

        Parameters
        ----------
        query : string
            You can do a select or execute a stored procedure.

        Returns
        -------
        answer : Class
            Returns status, message, date lists(columns,data).

        """
        answer = Answer()
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                columns = cursor.description
            answer.load(True, 'Query obtained', [columns,data])
        except Exception as e:
            answer.load(False, 'Connection.getQuery: ' + str(e), None)
        return answer
    
    def _readConfig(self):
        """
        This method returns the values for the connection to SQL Server from the section CONNECTION in the JSON file.

        Returns
        -------
        answer : Class
            Return status, message, data list(DB values read from JSON file).

        """
        answer = Answer()
        try:
            config = self.__mf.readConfig().getData()
            answer.load(True,'Read DB setup',[config['CONNECTION']['DB_SERVER'],config['CONNECTION']['DB_NAME'], config['CONNECTION']['DB_USER'], config['CONNECTION']['DB_PASSWORD']])
        except Exception as e:
            answer.load(False, 'Connection.readConfig: ' + str(e), None)
        return answer