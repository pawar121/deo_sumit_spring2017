#improting all the required packages
import os
import logging
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
    logFilePath = fileDir+'\\Logs\\Q3_Part1.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from cricket_matches.csv")
    csvName = fileDir+'\\Data\\cricket_matches.csv'
    dfCricMatches = readCSVFile(csvName)

    #filtering the data frame for which host is the winner
    logger.info("Filtering the data frame for which host is the winner")
    dfCricMatches = dfCricMatches[dfCricMatches['home'] == dfCricMatches['winner']]
    logger.info("Total number of matches where host team won is "+str(len(dfCricMatches)))

    #deriving another column winnerScore to keep wining team's score
    logger.info("Deriving another column winnerScore to keep wining team's score")
    dfCricMatches['winnerScore'] = np.where(dfCricMatches['winner'] == dfCricMatches['innings1'], dfCricMatches['innings1_runs'], dfCricMatches['innings2_runs'])

    # Define the aggregation calculations
    aggregations = {
        'winnerScore' : 'mean'
    }

    df = dfCricMatches.groupby('home').agg(aggregations)
    df = df['winnerScore'].groupby(level=0, group_keys=False)

    logger.info("Sorting the data frame by Total Compensation")
    dfSummary = pd.DataFrame(df.nlargest())

    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q3_Part1.csv")
    resultsPath = fileDir+'\\Results\\Q3_Part1.csv'
    funCheckDir(resultsPath)
    dfSummary.to_csv(resultsPath, index=True, encoding='utf-8')
    logger.info("Summary metrix is available at "+resultsPath)

    #printing sample summary metrix
    print('Summary metrix for the employee_compensation data...')
    print(dfSummary.head().to_string(index=True))

    #Logging finished
    logger.info("Application finished....")
    logging.shutdown()

#calling main() function
if __name__ == '__main__':
    main()
