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
    logFilePath = fileDir+'\\Logs\\Q1_Part2.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from vehicle_collisions.csv")
    csvName = fileDir+'\\Data\\vehicle_collisions.csv'
    dfVehCol = readCSVFile(csvName)

    #filtering the data frame from 2015 to present
    logger.info("Filtering the data frame from 2015 to present")
    dfVehCol = dfVehCol[dfVehCol['DATE'].dt.year >= 2015]

    #filtering the data frame from 2015 to present
    logger.info("Filtering the data frame for which VEHICLE TYPE is NaN")
    dfVehCol = dfVehCol[~ pd.isnull(dfVehCol['VEHICLE 1 TYPE'])]

    #filling NaN with default values
    logger.info("filling NaN with default values for BOROUGH with Unknown")
    dfVehCol['BOROUGH'] = dfVehCol['BOROUGH'].fillna('Unknown')

    #filtering the data frame for which 1 vehicle involved
    logger.info("Filtering the data frame for which only 1 vehicle was involved")
    dfVehCol1 = dfVehCol[pd.isnull(dfVehCol['VEHICLE 2 TYPE'])]
    logger.info("Total number of collisions with only 1 vehicle : "+str(len(dfVehCol1)))

    #filtering the data frame for which 2 vehicles were involved
    logger.info("Filtering the data frame for which 2 vehicles were involved")
    #removing collisions with only 1 vehicle
    dfVehCol = dfVehCol[~dfVehCol['UNIQUE KEY'].isin(dfVehCol1['UNIQUE KEY'])]
    dfVehCol2 = dfVehCol[pd.isnull(dfVehCol['VEHICLE 3 TYPE'])]
    logger.info("Total number of collisions with 2 vehicles : "+str(len(dfVehCol2)))

    #filtering the data frame for which 3 vehicles were involved
    logger.info("Filtering the data frame for which 3 vehicles were involved")
    #removing collisions with less than 3 vehicle
    dfVehCol = dfVehCol[~dfVehCol['UNIQUE KEY'].isin(dfVehCol2['UNIQUE KEY'])]
    dfVehCol3 = dfVehCol[pd.isnull(dfVehCol['VEHICLE 4 TYPE'])]
    logger.info("Total number of collisions with 3 vehicles : "+str(len(dfVehCol3)))

    #filtering the data frame for which 4 or more vehicles were involved
    logger.info("Filtering the data frame for which 4 or more vehicles were involved")
    #removing collisions with less than 4 vehicle
    dfVehCol = dfVehCol[~dfVehCol['UNIQUE KEY'].isin(dfVehCol3['UNIQUE KEY'])]
    dfVehCol4 = dfVehCol
    logger.info("Total number of collisions with 4 or more vehicles : "+str(len(dfVehCol4)))


    #grouping by BOROUGH and counting total number of records for collisions with 1 vehicle involved
    logger.info("Grouping by BOROUGH and counting total number of records for collisions with 1 vehicle involved")
    series1Veh = dfVehCol1['UNIQUE KEY'].groupby(dfVehCol1['BOROUGH']).count()

    #grouping by BOROUGH and counting total number of records for collisions with 2 vehicles involved
    logger.info("Grouping by BOROUGH and counting total number of records for collisions with 2 vehicles involved")
    series2Veh = dfVehCol2['UNIQUE KEY'].groupby(dfVehCol2['BOROUGH']).count()

    #grouping by BOROUGH and counting total number of records for collisions with 3 vehicles involved
    logger.info("Grouping by BOROUGH and counting total number of records for collisions with 3 vehicles involved")
    series3Veh = dfVehCol3['UNIQUE KEY'].groupby(dfVehCol3['BOROUGH']).count()

    #grouping by BOROUGH and counting total number of records for collisions with more than 3 vehicles involved
    logger.info("Grouping by BOROUGH and counting total number of records for collisions with more than 3 vehicles involved")
    series4Veh = dfVehCol4['UNIQUE KEY'].groupby(dfVehCol4['BOROUGH']).count()


    #combining all collisions-series into summary Metrix data frame
    logger.info("Combining all collisions-series into summary Metrix data frame")
    columns=['BOROUGH', 'ONE_VEHICLES_INVOLVED', 'TWO_VEHICLES_INVOLVED', 'THREE_VEHICLES_INVOLVED', 'MORE_VEHICLES_INVOLVED']
    dfSummary = pd.DataFrame({'BOROUGH':series4Veh.index,'ONE_VEHICLES_INVOLVED': series1Veh,'TWO_VEHICLES_INVOLVED': series2Veh
    ,'THREE_VEHICLES_INVOLVED': series3Veh,'MORE_VEHICLES_INVOLVED': series4Veh})


    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q1_Part2.csv")
    resultsPath = fileDir+'\\Results\\Q1_Part2.csv'
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
