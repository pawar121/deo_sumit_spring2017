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
    logFilePath = fileDir+'\\Logs\\Q2_Part1.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from employee_compensation.csv")
    csvName = fileDir+'\\Data\\employee_compensation.csv'
    dfEmpComp = readCSVFile(csvName)

    #grouping by Organization Group & Department and calculating mean of total compensation
    logger.info("Grouping by Organization Group & Department and calculating mean of total compensation")

    # Define the aggregation calculations
    aggregations = {
        'Total Compensation' : 'mean'
    }

    df = dfEmpComp.groupby(['Organization Group', 'Department']).agg(aggregations)
    df = df['Total Compensation'].groupby(level=0, group_keys=False)

    logger.info("Sorting the data frame by Total Compensation")
    dfSummary = pd.DataFrame(df.nlargest())

    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q2_Part1.csv")
    resultsPath = fileDir+'\\Results\\Q2_Part1.csv'
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
