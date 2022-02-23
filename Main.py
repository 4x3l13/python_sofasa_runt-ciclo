# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 09:23:24 2022

@author: Jonathan Martínez
"""

from Connection import Connection
from ConnectionFTP import ConnectionFTP
from MainFunctions import MainFunctions
from Ejecucion import Ejecucion
from Detalle import Detalle
from Answer import Answer

class Main():
    def __init__(self):
        self.__mf = MainFunctions()
        self.__cnx = Connection()
        self.__ejecucion = Ejecucion(di= 0, tarea= self.__mf.readConfigTask().getData(), estado= 'E')
        self.__ftp = ConnectionFTP()
        self._load()
        
    def _load(self):
        self._createFolders()
        self._writeLogFile("Application launch")
        if self._openConnection():
            if self._ejecucion():
                self._writeLogs('Start task')
                if self._removeLocalFiles():
                    self._getData('RUNT')
                    self._getData('CICLO')
                    if self._openFTP():
                        sent = self._sentFileFTP()
                        self._writeLogs(sent.getMessage())
                        if sent.getStatus():
                            self._writeLogs('End task')
                            self.__ejecucion.updateEjecucion('F')
                            self._writeLogFile("Updated ejecucion")
            self.__cnx.closeConnection()
        self._writeLogFile("Finished application")

    def _createFolders(self):
        folder = self.__mf.readConfigLocalFolder("LOG_FOLDER")
        if folder.getStatus():
            self.__logFolder = folder.getData()
            self.__mf.createFolder(self.__logFolder)
            folder = self.__mf.readConfigLocalFolder("FILE_FOLDER")
        if folder.getStatus():
            self.__fileFolder = folder.getData()
            self.__mf.createFolder(self.__fileFolder)

    def _openConnection(self):
        cnx = self.__cnx.getConnection()
        self._writeLogFile(cnx.getMessage())
        return cnx.getStatus()
    
    def _ejecucion(self):
        ejecucion = self.__ejecucion.insertEjecucion()
        self._writeLogFile(ejecucion.getMessage())
        return ejecucion.getStatus()
    
    def _writeLogs(self,message):
        self._writeLogFile(message)
        detalle = Detalle(ejecucion= self.__ejecucion.getId(), mensaje= message)
        detalle.insertDetalle()
        
    def _writeLogFile(self,message):
        self.__mf.writeLogFile(self.__logFolder + '/Log', message)
    
    def _removeLocalFiles(self):
        remove = self.__mf.removeLocalFiles(self.__fileFolder)
        self._writeLogs(remove.getMessage())
        return remove.getStatus()
    
    def _getData(self,option):
        query = self.__mf.readConfigSP(option).getData()
        if self.__cnx.getConnection().getStatus():
            cnx = self.__cnx.getQuery(query)
            if cnx.getStatus():
                columns = cnx.getData()[0]
                data = cnx.getData()[1]
                self._writeLogs('Get data ' + option)
                self._writeLogs(self.__mf.createCSV(folder= self.__fileFolder, fileName= option,columns= columns, data= data).getMessage() + ' in folder '+ self.__fileFolder)
            else:
                self._writeLogFile(cnx.getMessage())
        else:
            self._writeLogFile(self.__connection.getConnection().getMessage())
          
    def _openFTP(self):
        ftp = self.__ftp.getConnection()
        self._writeLogs(ftp.getMessage())
        return ftp.getStatus()
        
    def _sentFileFTP(self):
        answer = Answer()
        try:
            self.__ftp.changePath()
            self._writeLogs('Path was changed')
            read = self.__mf.readLocalFiles(self.__fileFolder)
            if read.getStatus():
                files = read.getData()[0]
                fileNames = read.getData()[1]
                for file in files:
                    self.__ftp.uploadFile(file, fileNames[files.index(file)])
                    self._writeLogs(fileNames[files.index(file)] + ' file was send to FTP')
            else:
                self._writeLogs('Local Files no found')
            self.__ftp.closeConnection()
            answer.load(True, 'The connection to FTP was closed', None)
        except Exception as e:
            answer.load(False, 'Main._sentFileFTP: ' + str(e), None)    
        return answer
        
if __name__ == '__main__':
    main = Main()
