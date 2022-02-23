# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 18:21:33 2022

@author: px03412
"""

class Answer():
    """
    This Class allows to get information
    
    Public Methods
    --------------
    getData,
    getMessage,
    getStatus,
    load
    """
    
    def load(self,status,message,data):
        """
        This method allows upload information about status, message and date from a method

        Parameters
        ----------
        status : boolean
           Allows us to know if a process is correct or not.
        message : string
            Allows us to get information about a process.
        data : TYPE
            Return data.

        Returns
        -------
        None.

        """
        self.__status = status
        self.__message = message
        self.__data = data
        
    def getStatus(self):
        return self.__status
    
    def getMessage(self):
        return str(self.__message)
    
    def getData(self):
        return self.__data