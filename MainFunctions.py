# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 15:41:17 2022

@author: Jonathan Martínez
"""
import csv
import os
from datetime import datetime
import json
from Answer import Answer

class MainFunctions():
    """
    This class has main methods that can be used across other classes. 
    
    Methods
    -------
    createCSV,
    createFolder,
    getCurrentDate,
    getCurrentTime,
    readConfig,
    readConfigDB,,
    readConfigFTP,
    readConfigLocalFolder,
    readConfigSP,
    readLocalFiles,
    removeLocalFiles,
    writeFile,
    writeLogFile.
    
    """
    
    def createCSV(self, folder,fileName,columns, data):
        """
        This method allows to create a CSV file in a local folder.

        Parameters
        ----------
        folder : string
            This is the folder name where CSV file will be saved.
        fileName : string
            This is the CSV file name.
        columns : list
            These are the columns name.
        data : list
            These are the data.

        Returns
        -------
        answer : Class
            Return status, message.

        """
        answer = Answer()
        try:
            with open(os.getcwd() + '/' + folder + '/' + fileName + '.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(col[0] for col in columns)
                for row in data:
                    csvwriter.writerow(row)
            answer.load(True, 'The CSV file was created', None)
        except Exception as e:
            answer.load(False, 'MainFunction.createCSV: ' + str(e), None)
        return answer
                
    def createFolder(self, folderName):
        """
        This method allows to create a local folder

        Parameters
        ----------
        folderName : string
            This is the folder name that will be created.

        Returns
        -------
        answer : Class
            Return status, message.

        """
        answer = Answer()
        try:
            if os.path.exists(os.getcwd() + '/' + folderName) == False:
                os.mkdir(folderName)
                answer.load(True, 'Folder created', None)
        except Exception as e:
            answer.load(False, 'MainFunction.createFolder: ' + str(e), None)
        return answer
            
    def getCurrentDate(self):
        """
        This method returns the current date.

        Returns
        -------
        answer : Class
            Return status, message, data str(current date in format yyyy-mm-dd).

        """
        answer = Answer()
        try:
            now = datetime.now()
            answer.load(True,'Current date',str(now.year) + "-" + str('0' + str(now.month))[-2:] + "-" + str('0' + str(now.day))[-2:])
        except Exception as e:
            answer.load(False, 'MainFunction.getCurrentDate: ' + str(e), None)
        return answer
    
    def getCurrentTime(self):
        """
        This method returns current time.

        Returns
        -------
        answer : Class
            Return status, message, data str(current time in format hh:mm:ss).

        """
        answer = Answer()
        try:
            now = datetime.now()
            answer.load(True,'Current time',str('0' + str(now.hour))[-2:] + ':' + str('0' + str(now.minute))[-2:] + ':' + str('0' + str(now.second))[-2:])
        except Exception as e:
            answer.load(False, 'MainFunction.getCurrentTime: ' + str(e), None)
        return answer     
   
    def readConfig(self):
        """
        This method read the setup from the JSON file.

        Returns
        -------
        answer : Class
            Return status, message, data dict(values read from JSON file)

        """
        answer = Answer()
        try:
            with open('config.json') as file:
                answer.load(True,'Read setup',json.load(file))
        except Exception as e:
            answer.load(False, 'MainFunction.readConfig: ' + str(e), None)
        return answer     
          
    def readConfigLocalFolder(self,folder):
        """
        This method returns the value to create a local folder from the section LOCAL_FOLDER in the JSON file.

        Parameters
        ----------
        folder : string
            it must be the key name from the section LOCAL_FOLDER.

        Returns
        -------
        string
            Returns the key value.

        """
        answer = Answer()
        try:
            config = self.readConfig().getData()
            answer.load(True,'Read local folder setup',config['LOCAL_FOLDER'][folder])
        except Exception as e:
            answer.load(False, 'MainFunction.readConfigLocalFolder: ' + str(e), None)
        return answer
    
    def readConfigSP(self,sp):
        """
        This method returns the value to execute a stored procedure from the section STORED PROCEDURE in the JSON file.

        Parameters
        ----------
        sp : string
            it must be the key name from the section STORED PROCEDURE.

        Returns
        -------
        answer : Class
            Returns status, message data str().

        """
        answer = Answer()
        try:
            config = self.readConfig().getData()
            answer.load(True,'Read SP setup',config['STORED_PROCEDURE']['SP_' + sp])
        except Exception as e:
            answer.load(False, 'MainFunction.readConfigSP: ' + str(e), None)
        return answer
    
    def readConfigTask(self):
        """
        This method returns the task value from the section TASK in the JSON file.

        Parameters
        ----------
        None
        
        Returns
        -------
        answer : Class
            Returns status, message data str().

        """
        answer = Answer()
        try:
            config = self.readConfig().getData()
            answer.load(True,'Read SP setup',config['TASK']['ID'])
        except Exception as e:
            answer.load(False, 'MainFunction.readConfigTask: ' + str(e), None)
        return answer
    
    def readLocalFiles(self,path):
        """
        This method returns the full path, name of files

        Parameters
        ----------
        path : string
            This is the folder full path that we want to read.

        Returns
        -------
        files : list
            File full paths.
        files2 : list
            File names.

        """
        answer = Answer()
        try:
            files = []
            files2 = os.listdir(path)
            for file in files2:
                files.append(os.path.abspath(path + '/' + file))
            answer.load(True, 'Read files', [files,files2])
        except Exception as e:
            answer.load(False,'MainFunction.readLocalFiles: ' + str(e), None)
        return answer
        
    def removeLocalFiles(self,path):
        """
        This method remove local files of a folder

        Parameters
        ----------
        path : string
            Folder full path of the files that we want to remove.

        Returns
        -------
        None.

        """
        answer = Answer()
        try:
            files = os.listdir(path)
            for file in files:
                os.remove(os.path.abspath(path + '/' + file))
            answer.load(True, 'The local files were removed', None)
        except Exception as e:
            answer.load(False, 'MainFunctions.removeLocalFiles: ' + str(e), None)
        return answer
            
    def writeFile(self, fileName, message):
        """
        This method allows write into a flat file

        Parameters
        ----------
        fileName : string
            File name to write.
        message : string
            Text to write into of flat file.

        Returns
        -------
        None.

        """
        answer = Answer()
        try:
            file = open(fileName + '.txt','a')
            file.write(message + '\n')
            file.close()
            answer.load(True, 'Written file', None)
        except Exception as e:
            answer.load(False, 'MainFunctions.writeFile: ' + str(e), None)
        return answer
            
    def writeLogFile(self, fileName, message):
        """
        This method allows write into a log flat file

        Parameters
        ----------
        fileName : string
            File name to write.
        message : string
            Text to write into of flat file.

        Returns
        -------
        None.

        """
        try:
            self.writeFile(fileName + self.getCurrentDate().getData(), '[' + self.getCurrentTime().getData() + '] ' + message + '\n')
        except Exception as e:
            print('writeLogFile: ', e)