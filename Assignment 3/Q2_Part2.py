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
    logFilePath = fileDir+'\\Logs\\Q2_Part2.log'
    funCheckDir(logFilePath)
    logger = getLogger(logFilePath)
    logger.info("Application started....")

    #reading data from ~/data/vehicle_collisions.csv
    logger.info("Reading data from employee_compensation.csv")
    csvName = fileDir+'\\Data\\employee_compensation.csv'
    dfEmpComp = readCSVFile(csvName)

    #filtering the data frame to get Calendar year records only
    logger.info("Filtering the data frame to get Calendar year records only")
    dfEmpComp = dfEmpComp[dfEmpComp['Year Type'] == 'Calendar']
    logger.info("Number of records for which Year Type is Calendar : " + str(len(dfEmpComp)))

    #sorting the data frame by Employee Identifier & Job Family
    logger.info("Sorting the data frame by Employee Identifier & Job Family")
    dfEmpComp = dfEmpComp.sort_values(by = ['Employee Identifier', 'Job Family'])

    #grouping by Employee Identifier & Job Family and calculating mean of Salaries
    logger.info("Grouping by Employee Identifier & Job Family and calculating mean of Salaries")
    seriesSal = dfEmpComp['Salaries'].groupby([dfEmpComp['Employee Identifier'], dfEmpComp['Job Family']]).mean()

    #grouping by Employee Identifier & Job Family and calculating mean of Overtime
    logger.info("Grouping by Employee Identifier & Job Family and calculating mean of Overtime")
    seriesOT = dfEmpComp['Overtime'].groupby([dfEmpComp['Employee Identifier'], dfEmpComp['Job Family']]).mean()

    #grouping by Employee Identifier & Job Family and calculating mean of Total Benefits
    logger.info("Grouping by Employee Identifier & Job Family and calculating mean of Total Benefits")
    seriesTB = dfEmpComp['Total Benefits'].groupby([dfEmpComp['Employee Identifier'], dfEmpComp['Job Family']]).mean()

    #grouping by Employee Identifier & Job Family and calculating mean of Total Compensation
    logger.info("Grouping by Employee Identifier & Job Family and calculating mean of Total Compensation")
    seriesTC = dfEmpComp['Total Compensation'].groupby([dfEmpComp['Employee Identifier'], dfEmpComp['Job Family']]).mean()

    #combining all Series into summary Metrix data frame
    logger.info("Combining all Series into summary Metrix data frame")
    columns=['Employee Identifier', 'Job Family', 'Salaries', 'Overtime', 'Total Benefits', 'Total Compensation']

    dfSummary = pd.DataFrame({
        'Employee Identifier':seriesSal.index.get_level_values('Employee Identifier'),
        'Job Family':seriesSal.index.get_level_values('Job Family'),
        'Salaries':seriesSal,
        'Overtime':seriesOT,
        'Total Benefits':seriesTB,
        'Total Compensation':seriesTC
    })

    #filtering the records for which Overtime is greater than 5% of Salaries
    logger.info("Filtering the records for which Overtime is greater than 5% of Salaries")
    dfSummary = dfSummary[dfSummary['Overtime'] > dfSummary['Salaries']*0.05]

    #grouping by Job Family and calculating mean of Total Benefits
    logger.info("Grouping by Job Family and calculating mean of Total Benefits")
    seriesTB = dfSummary['Total Benefits'].groupby(dfSummary['Job Family']).mean()

    #grouping by Job Family and calculating mean of Total Compensation
    logger.info("Grouping by Job Family and calculating mean of Total Compensation")
    seriesTC = dfSummary['Total Compensation'].groupby(dfSummary['Job Family']).mean()


    #combining all Series into summary Metrix data frame
    logger.info("Combining all Series into summary Metrix data frame")
    columns=['Job Family', 'Total Benefits', 'Total Compensation', 'Percent_Total_Benefit']

    dfSummary = pd.DataFrame({
        'Job Family':seriesTB.index,
        'Total Benefits':seriesTB,
        'Total Compensation':seriesTC,
        'Percent_Total_Benefit':seriesTB/seriesTC
    })


    #sorting the data frame by Percent_Total_Benefit
    logger.info("Sorting the data frame by Percent_Total_Benefit")
    dfSummary = dfSummary.sort_values(by = 'Percent_Total_Benefit', ascending = False)

    #writing summary metrix to csv
    logger.info("Writing summary metrix to Q2_Part2.csv")
    resultsPath = fileDir+'\\Results\\Q2_Part2.csv'
    funCheckDir(resultsPath)
    dfSummary[columns].to_csv(resultsPath, index=False, encoding='utf-8')
    logger.info("Summary metrix is available at "+resultsPath)

    #printing sample summary metrix
    print('Summary metrix for the employee_compensation data...')
    print(dfSummary[columns].head().to_string(index=False))

    #Logging finished
    logger.info("Application finished....")
    logging.shutdown()

#calling main() function
if __name__ == '__main__':
    main()
