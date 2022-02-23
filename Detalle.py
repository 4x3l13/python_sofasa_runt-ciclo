# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 20:45:14 2022

@author: px03412
"""
from Answer import Answer
from Connection import Connection
from MainFunctions import MainFunctions

class Detalle():
    """
    This class is a model of Detalle on DBIntegracion
    
    Public Methods
    --------------
    insertEjecucion
    """
    def __init__(self,ejecucion, mensaje):
        self.__ejecucion = ejecucion
        self.__mensaje = mensaje
        self.__connection = Connection()
        self.__mf = MainFunctions()
    
    def insertDetalle(self):
        """
        This method allows insert a row on DBIntegracion table detalle

        Returns
        -------
        answer : Class
            Returns state, message.

        """
        answer = Answer()
        try:
            query = self.__mf.readConfigSP("INSERT_DETALLE").getData() + " " + str(self.__ejecucion) + ",'" + self.__mensaje +"'"
            if self.__connection.getConnection().getStatus():
               if self.__connection.executeQuery(query).getStatus():
                   self.__connection().closeConnection()
                   answer.load(True, 'Detalle was inserted', None)
        except Exception as e:
            answer.load(False, "Detalle.insertDetalle: "+ str(e), None)
        return answer