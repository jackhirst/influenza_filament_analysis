# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:28:49 2019

@author: 2263524H
"""
import os
import glob
import csv

currentDirectory = "C:/"
outputDirectory =  "C:/"

target = "Length"

def findPenultimate(text, pattern):
    return text.rfind(pattern, 0, text.rfind(pattern))

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def goUp():
    directory = os.getcwd()
    newDirectory = directory[0:directory.rfind("\\")+1]
    os.chdir(newDirectory)
    print(newDirectory)       

def listContents(contents):
    for index, content in enumerate(contents):
        print(index, content)

def goDown():
    contents = next(os.walk('.'))[1]
    listContents(contents)
    newFolderIndex = input("Enter the number of the folder you like to go to: ")
    newDirectory = os.getcwd() + "\\" + contents[int(newFolderIndex)] + "\\"
    os.chdir(newDirectory)
    print(newDirectory)    

def goSideways():
    goUp()
    goDown()

def getRegularCSVTitle(directory):
    final = directory.rfind("\\")
    title = directory[final+1:len(directory)] + ".csv"
    return(title)

def equilibrateLengths(listOfLists):
    maxLength = len(max(listOfLists, key=len))
    newList = []
    for iList in listOfLists:
        newList = newList + [iList + [None] * (maxLength - len(iList))]
    return(newList)

def CSVColumnToList(columnOfInterest):
    lengthList = []
    fileList = glob.glob("*csv")
    for file in fileList:
        print("processing " + file)
        if os.stat(file).st_size > 2: #avoid empty files
            with open (file, "r") as csvfile:
                myReader = csv.reader(csvfile, delimiter=',')
                headers = next(myReader)
                columnIndex = headers.index(columnOfInterest)
                for row in myReader:
                    if len(row) > 0:
                        lengthList = lengthList + [row[columnIndex]]
    return(lengthList)

def combineCSVs(columnOfInterest):
    lengths = CSVColumnToList(columnOfInterest)
    currentDirectory = os.getcwd()
    title =  "tidied " + getRegularCSVTitle(currentDirectory)
    print("Creating " + os.getcwd() + "\\" + title)
    with open (title, "w", newline = "") as outputFile:
        myWriter = csv.writer(outputFile, delimiter = ',')
        myWriter.writerow([columnOfInterest])
        for length in lengths:
            myWriter.writerow([length])

def getCompiledCSVTitle(directory):
    final = directory.rfind("\\")
    pen = findPenultimate(directory, "\\")
    pretitle = directory[pen:final] + ".csv"
    newpen = findnth(pretitle, " ", 2) + 1
    title = pretitle[newpen:len(pretitle)]
    return(title)

def combineConditions(keyword, outputDirectory):
    combinedLengths = []
    filesUsed =[]
    startDirectory = os.getcwd() + "\\"
    myDirectories = next(os.walk('.'))[1]
    outputTitle = getCompiledCSVTitle(startDirectory)
    for i in myDirectories:
        filesUsed += [i]
        lengths = []
        os.chdir(startDirectory + i)
        tidyFile = glob.glob("*" + keyword + "*")
        with open(tidyFile[0], "r") as csvfile:
            myReader = csv.reader(csvfile, delimiter = ',')
            next(myReader) #Skip the header row...
            for row in myReader:
                lengths += row
        combinedLengths += [lengths]
    extendedLengths = equilibrateLengths(combinedLengths)
    os.chdir(outputDirectory)
    print("Saving final compilation as " + os.getcwd() + "\\" + outputTitle)
    with open(outputTitle, 'w', newline='') as outputFile:
        myWriter = csv.writer(outputFile, delimiter = ',')
        myWriter.writerow(filesUsed)
        for i in range(0, len(extendedLengths[0])):
            myRow = []
            for j in extendedLengths:
                myRow = myRow + [j[i]]
            myWriter.writerow(myRow)
    os.chdir(startDirectory)  #return to start directory
    
def processFolder(columnOfInterest, keyword, outputDirectory):
    myDirectories = next(os.walk('.'))[1]
    startDirectory = os.getcwd() + "\\"
    for i in myDirectories:
        os.chdir(startDirectory + i)
        combineCSVs(columnOfInterest)
    os.chdir(startDirectory)
    combineConditions(keyword, outputDirectory)
        
os.chdir(currentDirectory)
print("Current directory: " + currentDirectory)

while True:
    print("q to quit. up to move the directory up a level. down to move the directory down a level. side to move up then down. p to process a folder")
    myInput = input()
    if myInput == "q":
        break
    if myInput == "up":
        goUp()
    if myInput == "down":
        goDown()
    if myInput == "side":
        goSideways()
    if myInput == 'p':
        processFolder(target, "tidied", outputDirectory)
    