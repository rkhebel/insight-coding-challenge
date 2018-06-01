#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ryanhebel
"""

import os #used to find path information for input/output
from datetime import datetime #used for calculating session duration
import time

""" ======================================================================================================== """

#a session class that defines all relevant variables and functions needed 
#to initialize and maintain a session
class Session:
    
    #reduce the time to create and access data associated with session objects
    __slots__ = "ip", "firstDate", "firstTime", "lastDate", "lastTime", "documentCount"
    
    def __init__(self, ip, firstDate, firstTime, lastDate, lastTime):
        self.ip = ip
        self.firstDate = firstDate
        self.firstTime = firstTime
        self.lastDate = lastDate
        self.lastTime = lastTime
        self.documentCount = 1
        
    #add a document to the count 
    def addDocument(self):
        self.documentCount += 1
        
    #calculates the elapsed time between a start date/time and end date/time
    #used to check if a session has expired and to report the total session time
    def calculateElapsedTime(self, startDate, startTime, endDate, endTime):
        try:
            beginning = datetime.strptime(startDate + startTime, "%Y-%m-%d%H:%M:%S") #converts string to datetime object
            end = datetime.strptime(endDate + endTime, "%Y-%m-%d%H:%M:%S")
            elapsedTime = end - beginning
            elapsedTime = elapsedTime.total_seconds() + 1 #calculates the total seconds that have elapsed, add 1 to elapsedTime because inclusive (i.e. 0->1 is 2 seconds)
            return int(elapsedTime)
        except ValueError:
            print("The argument for calculateElapsedTime is not a valid date\n")

    #end the session by calculating the elapsed time of the session and 
    #writing the session information to the output
    def endSession(self, path, startDate, startTime, endDate, endTime):
        elapsedTime = self.calculateElapsedTime(startDate, startTime, endDate, endTime) 
        with open(path + "/output/sessionization.txt", "a") as output: 
            output.write("{0},{1} {2},{3} {4},{5},{6}\n".format(self.ip, self.firstDate, self.firstTime, self.lastDate, self.lastTime, elapsedTime, self.documentCount))
        
""" ======================================================================================================== """

#main file for reading inputs, interating through the EDGAR logs, and outputting
#information to a text file
def main():
    
    #returns the path to the parent directory 
    path = os.path.split(os.getcwd())[0]
    
    #clears output file in case there is already information present
    with open(path + "/output/sessionization.txt", "w") as output:
            output.write("")
        
    #navigates to the log.csv file in the input directory
    with open(path + "/input/log.csv", "r") as edgarData, open(path + "/input/inactivity_period.txt", "r") as inactivityPeriod:
        #obtains the inactivity period from the inactivity_period.txt file 
        #located in the input directory
        INACTIVITY_PERIOD = int(inactivityPeriod.readline())
        #determine the positions of the variables for the input file
        variables = edgarData.readline().strip().split(",") #returns a list of variables names, eliminating spaces and the newline character
        #iterates through the variables names and records the index of important variables
        for index, variable in enumerate(variables):
            if variable == "ip":
                IP_INDEX = index
            if variable == "date":
                DATE_INDEX = index
            if variable == "time":
                TIME_INDEX = index
              
        activeSessions = list() #a list is used to store all of the active sessions 
        previousTime = 0 #used to determine if the time has incremented and if we need to check if sessions have expired 
        expiredSessions = list() #a list is used to keep track of expired sessions after each time increment
        
        #iterate through the input one line at a time, creating session objects,
        #updating document counts, and ending sessions as appropriate
        for line in edgarData:
            accessInformation = line.split(",")
            
            #if the time has changed since the last entry, check to see if any of the
            #sessions have expired
            if previousTime != accessInformation[TIME_INDEX]:
                previousTime = accessInformation[TIME_INDEX]
                for session in activeSessions:
                    #calculate the elapsed time. if the user has been inactive
                    #longer than the specified inactivity period, end the session
                    elapsedTime = session.calculateElapsedTime(session.lastDate, session.lastTime, accessInformation[DATE_INDEX], accessInformation[TIME_INDEX])
                    if elapsedTime > INACTIVITY_PERIOD + 1:
                        session.endSession(path, session.firstDate, session.firstTime, session.lastDate, session.lastTime)
                        expiredSessions.append(session)                 
            
            #update the activeSessions list to reflect expired sessions
            activeSessions[:] = [element for element in activeSessions if element not in expiredSessions]
            
            ipExists = 0 #used as a flag to see if a user already has an active session
            #search the list of active sessions to see if the ip has an active session
            for session in activeSessions:
                if accessInformation[IP_INDEX] == session.ip:
                    currentSession = session
                    ipExists = 1
                    break #reduces number of iterations through list
                    
            #if there is an active session with the same ip address, increment the document
            #count for that session and update the time of the last access
            #test: assert(currentSession)
            if ipExists:
                currentSession.addDocument()
                currentSession.lastTime = accessInformation[TIME_INDEX]
                currentSession.lastDate = accessInformation[DATE_INDEX]
                
            #if the ip does not have an active session, create one and append it to the 
            #list of active sessions
            if not ipExists:
                newSession = Session(accessInformation[IP_INDEX],accessInformation[DATE_INDEX],accessInformation[TIME_INDEX],accessInformation[DATE_INDEX],accessInformation[TIME_INDEX])
                activeSessions.append(newSession)
            
        #once the end of the file has been reached, end all active sessions
        #in the correct order
        for session in activeSessions:
            session.endSession(path, session.firstDate, session.firstTime, session.lastDate, session.lastTime) #the variables previousDate and previousTime hold the seen date and time 


    
#run the main script 
if __name__ == "__main__":
    startTime = time.time()
    main()
    print(" --- {0} seconds ---".format(time.time() - startTime))
