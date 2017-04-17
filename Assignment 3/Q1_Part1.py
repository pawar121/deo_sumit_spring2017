#improting all the required packages
import os
import logging
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
    df = pd.read_csv(fileName ,parse_dates=['DATE'])
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
    logFilePath = fileDir+'\\Logs\\Q1_Part1.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from vehicle_collisions.csv")
    csvName = fileDir+'\\Data\\vehicle_collisions.csv'
    dfVehCol = readCSVFile(csvName)

    #filtering months to take 2016 data
    logger.info("Filtering months to take 2016 data")
    dfVehCol = dfVehCol[dfVehCol['DATE'].dt.year == 2016]

    #deriving month column from the date
    logger.info("Deriving month column from the date")
    dfVehCol['MONTH'] = dfVehCol['DATE'].dt.strftime('%b')

    #group-by by MONTH and count the total number of records
    logger.info("Grouping by MONTH and counting the total number of records")
    seriesNYC = dfVehCol['UNIQUE KEY'].groupby(dfVehCol['MONTH']).count()

    #group-by by MONTH and count total number of records for which BOROUGH = MANHATTAN
    logger.info("Grouping by MONTH and counting total number of records for which BOROUGH = MANHATTAN")
    seriesMANHATTAN = dfVehCol['UNIQUE KEY'][dfVehCol['BOROUGH'] == 'MANHATTAN'].groupby(dfVehCol['MONTH']).count()

    #combining NYC and MANHATTAN Series into summary Metrix data frame
    logger.info("Combining NYC and MANHATTAN Series into summary Metrix data frame")
    columns=['MONTH', 'MANHATTAN', 'NYC', 'PERCENTAGE']
    dfSummary = pd.DataFrame({'MONTH':seriesNYC.index,'MANHATTAN': seriesMANHATTAN,'NYC':seriesNYC})

    #calculating PERCENTAGE from the NYC & MANHATTAN columns
    logger.info("Calculating PERCENTAGE from the NYC & MANHATTAN columns")
    dfSummary['PERCENTAGE'] = dfSummary['MANHATTAN']/dfSummary['NYC']

    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q1_Part1.csv")
    resultsPath = fileDir+'\\Results\\Q1_Part1.csv'
    funCheckDir(resultsPath)
    dfSummary[columns].to_csv(resultsPath, index=False, encoding='utf-8')
    logger.info("Summary metrix is available at "+resultsPath)

    #printing sample summary metrix
    print('Summary metrix for the vehicle_collisions data...')
    print(dfSummary[columns].head().to_string(index=False))

    #Logging finished
    logger.info("Application finished....")
    logging.shutdown()

#calling main() function
if __name__ == '__main__':
    main()
