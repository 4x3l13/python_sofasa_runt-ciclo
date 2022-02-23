# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 19:33:53 2022

@author: px03412
"""
from Answer import Answer
from Connection import Connection
from MainFunctions import MainFunctions

class Ejecucion():
    """
    This class is a model of Ejecucion on DBIntegracion
    
    Public Methods
    --------------
    getId
    insertEjecucion,
    updateEjecucion
    """
    def __init__(self, di, tarea, estado):
        self.__id = di
        self.__tarea = tarea
        self.__estado = estado
        self.__connection = Connection()
        self.__mf = MainFunctions()
        
    def getId(self):
        return self.__id
        
    def insertEjecucion(self):
        """
        This method allows insert a row on DBIntegracion table ejecucion

        Returns
        -------
        answer : Class
            Returns status, message, data str(ejecucionid).

        """
        answer = Answer()
        try:
            query = self.__mf.readConfigSP("INSERT_EJECUCION").getData() + " " + str(self.__tarea) + "," + str(self.__estado)
            if self.__connection.getConnection().getStatus():
                cnx = self.__connection.getQuery(query)
                if cnx.getStatus():
                    data = cnx.getData()[1]
                    for dt in data:
                        self.__id = dt[0]
                    answer.load(True, 'Ejecucion was inserted', str(self.__id))
        except Exception as e:
            answer.load(False, "Ejecucion.insertEjecucion: "+ str(e), None)
        return answer
        
    def updateEjecucion(self,estado):
        """
        This method allows update a row on DBIntegracion table ejecucion

        Parameters
        ----------
        estado : string
            state of ejecucion.

        Returns
        -------
        answer : Class
            Returns status, message.

        """
        answer = Answer()
        try:
            self.__estado = estado
            query = self.__mf.readConfigSP("UPDATE_EJECUCION").getData() + " " + str(self.__id) + ',' + self.__estado
            self.__connection.executeQuery(query)
            answer.load(True, 'Ejecucion was updated', None)
        except Exception as e:
            answer.load(False, "Ejecucion.updateEjecucion: "+ str(e), None)
        return answer
        
    