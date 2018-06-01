## Welcome to my solution!

### My name is Ryan Hebel and thank you for taking the time to take a look at my program. 

I wrote the entirety of the program in Python and compiled using version 3.6.3. The only dependencies needed for the program are the os library, the datetime library, and the time library. 

###### The general logic of my program is as follows: 

The program begins by establishing the path to the input and output, clearing any current data in sessionization.txt and reading in the inactivity period as well as the variable positions given by the header in log.csv
	
Next, the program begins iterating through each line of log.csv. For each iteration:
	
i. I begin by checking if the time for the current log differs from the previously recorded time. If so, the program iterates through each active session and ends the session if it has been inactive for too long. This means the program only checks if a session has expired when a time step occurs.

ii. Next, the program checks to see if the ip address for the current log already has an active session. If there is already an active session associated with the ip address, the program adds one to the document count and updates the session so that it reflects the last time the user accessed a document. If a session does not already exist for the ip address, a new session is created by using the information provided in the log.

Once every line has been seen in log.csv, the program ends all of the currently active sessions using the time the session started and the time the user last accessed a document.

###### Some additional notes about my approach:

1. I start the program by creating a Session class that includes all of the required data members as well as some helper methods to  perform operations with Session objects. I used slots to declare the data types of the Session objects to save time and memory when dealing with large amounts of data. I decided to use a Class instead of a dict due to the fact that they have very similar access times, however I thought creating the Session class would allow the program to be more versatile in the future and allowed me to encapsulate the necessary data and important functions in the same class. 

2. Although the README provided in the edgar-analytics github repo identified six variables that were of imortance, I found that cik, accession, and extention were not necessary for any operations performed by the program so I decided to ignore them when parsing the variable names in the header of the log.csv file. 

3. I decided to store all of the active sessions in a list. This is because it requires linear time to add an element to a list, you are able to remove elements from lists very quickly using list comprehensions, and lists maintain an order of their elements (as opposed to sets). This means that adding and removing sessions from the list of currently active sessions happens very fast, and also means that I do not have to sort through the list in order to end sessions in the desired order. Sessions that have the earliest starting time will be ended first (since the input is assumed to be in chronological order and the sessiosn are removed by traversing the list in order), and sessions with the same starting time but that were listed first will also be ended first (again, since they are initial stored in the correct order).