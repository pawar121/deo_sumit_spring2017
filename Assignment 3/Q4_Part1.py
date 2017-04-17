#improting all the required packages
import os
import logging
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd


#function to generate the loggs
def getLogger(dir):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    handler = logging.FileHandler(dir)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

#function to read large CSV files in chunks
def readCSVFile(fileName):
    df = pd.read_csv(fileName)
    return df

#function to check is directory exists
def funCheckDir(path):
    directory = os.path.dirname(path) # defining directory path
    if not os.path.exists(directory): # checking if directory already exists
        os.makedirs(directory) # making a directory

#function to perform aggregations
def main():

    #defining the file-directory
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    #Logging started
    logFilePath = fileDir+'\\Logs\\Q4_Part1.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from movies_awards.csv")
    csvName = fileDir+'\\Data\\movies_awards.csv'
    dfMovies = readCSVFile(csvName)

    #filtering the data frame for which awards is N/A
    logger.info("Filtering the data frame for which awards is N/A")
    dfMovies = dfMovies[~ pd.isnull(dfMovies['Awards'])]
    logger.info("Total number of movies for which award information is available is "+str(len(dfMovies)))

    #splitting data from column Awards
    dfMovies['Awards Nominations'] = dfMovies['Awards'].str.extract('(\d+ nomination)', expand=True)
    dfMovies['Awards Wins'] = dfMovies['Awards'].str.extract('(\d+ win)', expand=True)
    dfMovies['Oscar Nominations'] = dfMovies['Awards'].str.extract('(Nominated for \d+ Oscar)', expand=True)
    dfMovies['Oscar Wins'] = dfMovies['Awards'].str.extract('(Won \d+ Oscar)', expand=True)
    dfMovies['Primetime Emmys Nominations'] = dfMovies['Awards'].str.extract('(Nominated for \d+ Primetime Emmy)', expand=True)
    dfMovies['Primetime Emmys Wins'] = dfMovies['Awards'].str.extract('(Won \d+ Primetime Emmy)', expand=True)
    dfMovies['Golden Globe Nominations'] = dfMovies['Awards'].str.extract('(Nominated for \d+ Golden Globe)', expand=True)
    dfMovies['Golden Globe Wins'] = dfMovies['Awards'].str.extract('(Won \d+ Golden Globe)', expand=True)
    dfMovies['BAFTA Nominations'] = dfMovies['Awards'].str.extract('(Nominated for \d+ BAFTA)', expand=True)
    dfMovies['BAFTA Wins'] = dfMovies['Awards'].str.extract('(Won \d+ BAFTA)', expand=True)

    #taking integers from the split strings
    dfMovies['Awards Nominations'] = dfMovies['Awards Nominations'].str.extract('(\d+)')
    dfMovies['Awards Wins'] = dfMovies['Awards Wins'].str.extract('(\d+)')
    dfMovies['Oscar Nominations'] = dfMovies['Oscar Nominations'].str.extract('(\d+)')
    dfMovies['Oscar Wins'] = dfMovies['Oscar Wins'].str.extract('(\d+)')
    dfMovies['Primetime Emmys Nominations'] = dfMovies['Primetime Emmys Nominations'].str.extract('(\d+)')
    dfMovies['Primetime Emmys Wins'] = dfMovies['Primetime Emmys Wins'].str.extract('(\d+)')
    dfMovies['Golden Globe Nominations'] = dfMovies['Golden Globe Nominations'].str.extract('(\d+)')
    dfMovies['Golden Globe Wins'] = dfMovies['Golden Globe Wins'].str.extract('(\d+)')
    dfMovies['BAFTA Nominations'] = dfMovies['BAFTA Nominations'].str.extract('(\d+)')
    dfMovies['BAFTA Wins'] = dfMovies['BAFTA Wins'].str.extract('(\d+)')

    #filling NaN with 0
    dfMovies['Awards Nominations'] = dfMovies['Awards Nominations'].fillna(0)
    dfMovies['Awards Wins'] = dfMovies['Awards Wins'].fillna(0)
    dfMovies['Oscar Nominations'] = dfMovies['Oscar Nominations'].fillna(0)
    dfMovies['Oscar Wins'] = dfMovies['Oscar Wins'].fillna(0)
    dfMovies['Primetime Emmys Nominations'] = dfMovies['Primetime Emmys Nominations'].fillna(0)
    dfMovies['Primetime Emmys Wins'] = dfMovies['Primetime Emmys Wins'].fillna(0)
    dfMovies['Golden Globe Nominations'] = dfMovies['Golden Globe Nominations'].fillna(0)
    dfMovies['Golden Globe Wins'] = dfMovies['Golden Globe Wins'].fillna(0)
    dfMovies['BAFTA Nominations'] = dfMovies['BAFTA Nominations'].fillna(0)
    dfMovies['BAFTA Wins'] = dfMovies['BAFTA Wins'].fillna(0)

    #converting the data-type from string to int
    dfMovies['Awards Nominations'] = dfMovies['Awards Nominations'].astype(int)
    dfMovies['Awards Wins'] = dfMovies['Awards Wins'].astype(int)
    dfMovies['Oscar Nominations'] = dfMovies['Oscar Nominations'].astype(int)
    dfMovies['Oscar Wins'] = dfMovies['Oscar Wins'].astype(int)
    dfMovies['Primetime Emmys Nominations'] = dfMovies['Primetime Emmys Nominations'].astype(int)
    dfMovies['Primetime Emmys Wins'] = dfMovies['Primetime Emmys Wins'].astype(int)
    dfMovies['Golden Globe Nominations'] = dfMovies['Golden Globe Nominations'].astype(int)
    dfMovies['Golden Globe Wins'] = dfMovies['Golden Globe Wins'].astype(int)
    dfMovies['BAFTA Nominations'] = dfMovies['BAFTA Nominations'].astype(int)
    dfMovies['BAFTA Wins'] = dfMovies['BAFTA Wins'].astype(int)

    #calculating total number of nominations and awards
    dfMovies['Awards Nominations'] = dfMovies['Awards Nominations'] + dfMovies['Oscar Nominations'] + dfMovies['Primetime Emmys Nominations'] + dfMovies['Golden Globe Nominations'] + dfMovies['BAFTA Nominations']
    dfMovies['Awards Wins'] = dfMovies['Awards Wins'] + dfMovies['Oscar Wins'] + dfMovies['Primetime Emmys Wins'] + dfMovies['Golden Globe Wins'] + dfMovies['BAFTA Wins']

    #columns to be printed on the console
    columns = ['Title', 'Awards', 'Awards Nominations', 'Awards Wins', 'Oscar Nominations', 'Oscar Wins', 'Primetime Emmys Nominations', 'Primetime Emmys Wins', 'Golden Globe Nominations', 'Golden Globe Wins', 'BAFTA Nominations', 'BAFTA Wins']

    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q4_Part1.csv")
    resultsPath = fileDir+'\\Results\\Q4_Part1.csv'
    funCheckDir(resultsPath)
    dfMovies[columns].to_csv(resultsPath, index=False, encoding='utf-8')
    logger.info("Summary metrix is available at "+resultsPath)

    #printing sample summary metrix
    print('Summary metrix for the employee_compensation data...')
    print(dfMovies[columns].head().to_string(index=False))
    #Logging finished
    logger.info("Application finished....")
    logging.shutdown()

#calling main() function
if __name__ == '__main__':
    main()
