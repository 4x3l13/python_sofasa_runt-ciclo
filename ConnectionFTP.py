# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:40:03 2022

@author: Jonathan Martinez
"""
from MainFunctions import MainFunctions
from Answer import Answer
from ftplib import FTP

class ConnectionFTP():
    """
    This class allows the connection with a FTP server, the connection data are on the JSON file.
    
    Public Methods
    --------------
    chagePath,
    closeConnection,
    getConnection,
    uploadFile.
    
    Privated Methods
    ----------------
    _readConfig
    
    """
    def __init__(self):
        self.__mf = MainFunctions()
        config = self._readConfig()
        if config.getStatus():
            self.__server = config.getData()[0]
            self.__port = config.getData()[1]
            self.__user = config.getData()[2]
            self.__password = config.getData()[3]
            self.__path = config.getData()[4]
            self.__connection = None
    
    def changePath(self):
        """
        This methos change Path on the FTP server, the path are in the section FTP

        Returns
        -------
        None.

        """
        answer = Answer()
        try:
            self.__connection.cwd(self.__path)
            answer.load(True, 'Changed path', None)
        except Exception as e:
            answer.load(False, 'ConnectionFTP.changePath: ' + str(e), None)
        return answer
            
    def closeConnection(self):
        """
        This method closes the connection to SQL Server.

        Returns
        -------
        None.

        """
        self.__connection.close()
    
    def getConnection(self):
        """
        This method gets the connection to a FTP server, the data are in the section FTP
        Returns
        -------
        answer : Class
            Returns status, message.

        """
        answer = Answer()
        try:
            self.__connection = FTP(host= self.__server, user= self.__user, passwd= self.__password)
            answer.load(True, 'Stablished Connection to FTP', None)
        except Exception as e:
            answer.load(False, 'ConnectionFTP.getConnection: ' + str(e), None)
        return answer
        
    def uploadFile(self, originalFile, endFile):
        """
        This method allows upload a file to FTP server

        Parameters
        ----------
        originalFile : string
            This is the absolute path of the file to upload to FTP.
        endFile : string
            This is the file name with which it will be saved in the FTP.

        Returns
        -------
        None.

        """
        answer = Answer()
        try:
            f = open(originalFile, 'rb')
            self.__connection.storbinary('STOR ' + endFile, f)
            f.close()
            answer.load(True, 'Uploaded file to FTP', None)
        except Exception as e:
            answer.load(False, 'ConnectionFTP.uploadFile: ' + str(e), None)
        return answer
            
    def _readConfig(self):
        """
        This method returns the values for the connection to FTP Server from the section FTP in the JSON file.

        Returns
        -------
        answer : Class
            return status, message, data list(FTP values read from JSON file)..

        """
        answer = Answer()
        try:
            config = self.__mf.readConfig().getData()
            answer.load(True,'Read FTP setup',[config['FTP']['SERVER'], config['FTP']['PORT'], config['FTP']['USER'], config['FTP']['PASSWORD'], config['FTP']['PATH']])
        except Exception as e:
            answer.load(False, 'ConnectionFTP.readConfig: ' + str(e), None)
        return answer