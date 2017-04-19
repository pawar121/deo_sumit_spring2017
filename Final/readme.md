[![N|Solid](http://p9.zdassets.com/hc/settings_assets/680652/200062887/j1ixQzAxY6SfuZ2YTKbDOQ-lending_club_logo_new.png)](https://nodesource.com/products/nsolid)
# Overview
Lending Club is the world’s largest online credit marketplace for peer to peer lending, facilitating personal loans, business loans, and financing for elective medical procedures. Borrowers access these loans through fast and easy online or mobile interfaces. Investors provide the capital to enable many of the loans in exchange for earning interest. Peer-to-peer (P2P) lending is the practice of lending money to individuals or businesses through online services that match lenders directly with borrowers. Since the P2P lending companies offering these services operate entirely online, they can run with lower overhead and provide the service more cheaply than traditional financial institutions. Thus, lenders often earn higher returns compared to savings and investment products offered by banks, while borrowers can borrow money at lower interest rates, even after the P2P lending company has taken a fee for providing the match-making platform and credit checking the borrower. The interest rates are set by lenders who compete for the lowest rate on the reverse auction model or fixed by the intermediary company based on an analysis of the borrower's credit.

[![N|Solid](https://image.slidesharecdn.com/lendingclubanalysis-140625032301-phpapp01/95/lendingclub-analysis-2014-11-638.jpg?cb=1403666626)](https://nodesource.com/products/nsolid)

# Lending Club’s Business Model
The process of an application for a loan to its approval can be explained primarily in three steps:
  - Customers interested in a loan complete a simple application at LendingClub.com.
  - Lending Club leverages online data and technology to quickly assess risk, determine a credit rating and assign appropriate interest rates. Qualified applicants receive offers and can evaluate loan options with no impact to their credit score.
  - Investors ranging from individuals to institutions select loans in which to invest and can earn monthly returns.
---
# Goal of the project
We will present and explore the data provided by LC. This data was made available to us after the creation of an investor account. The data consists in 4 files updated every quarter on the same day as the quarterly results of the company are released. They contain information on almost all the loans issued by LC. The only loans missing from these files are the few loans where LC was not authorized to release publicly the details of the transactions.
The information available for each loan consists of all the details of the loans at the time of their issuance as well as more information relative to the latest status of loan such as how much principal has been paid so far, how much interest, if the loan was fully paid or defaulted, or if the borrower is late on payments etc.

* **Data Download** - [Data-download Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data%20Download.ipynb) describes the step by step implementation of downloading the dataset provided on the website by the Loan Lending club.
* **Store Data** - [Data-storage-LoanData Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data%20Download.ipynb) & [Data-Storage-DeclinedLoanData Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data-Storage-DeclinedLoanData.ipynb) describe the step by step process to clean and consolidate all the downloaded files into files per quarter.
* **Analysis 1** - [ana_1 Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/analysis/ana_1.ipynb) performs Exploratory data analysis on Approved loans vs Declined loans from year 2007 to 2016.
* **Analysis 2** - describe
* **Analysis 3** - describe
---
## Data Download
### Installation
[Data-download Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data%20Download.ipynb) has following dependency.
```sh
$ pip install MechanicalSoup
$ pip install beautifulsoup4
```
### Get login credentials
```
username = input("Lending-club username : ")
password = input("Lending-club password : ")
```
<img src ="extras/screenshots/login.PNG" />

### Loging to the lending-club
```
browser = mechanicalsoup.Browser()
login_page = browser.get(loginURL)
login_form = login_page.soup.find('form', {"id":"member-login"})
login_form.find("input", {"name" : "login_email"})["value"] = username
login_form.find("input", {"name" : "login_password"})["value"] = password
response = browser.submit(login_form, login_page.url)
```

### Check if username & password are correct
```
if (response.url == 'https://www.lendingclub.com/account/summary.action'):
    print(username + " logged in successfully!")
    --download files--
else:
    print("Either username or password or both are wrong..")
```
### Download & unzip files
```
with urlopen(baseURL + extn) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(path)
```
---

## Data Consolidation & Storage
### Installation
[Data-storage-LoanData Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data%20Download.ipynb) & [Data-Storage-DeclinedLoanData Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/Data-Storage-DeclinedLoanData.ipynb) have following dependency.

```sh
$ pip install pandas
$ pip install numpy
```
### Drop unwanted rows
There are number of unwanted rows which are either empty or contains some junk data. Below figure shows some of such rows.

<img src ="extras/screenshots/drop_rows.PNG" />

Below function will remove all such rows.
```
def funDropRows(df):
    df.dropna(thresh = 2, inplace = True)
    return df
```
### Select required columns
Below function will select only the columns which will be used for an analysis.
```
def funDropColumns(df):
    selected_colums = list of columns to be selected
    df = df[selected_colums]
    return df
```

### Clean Data
In the columns int_rate, term & emp_length contains some noise data, which is need to be removed. Below rows are some of such examples.

> Loan Data

<img src ="extras/screenshots/drop_columns.PNG" />

Below function will clean all such columns.
```
def funCleanData(df):
    df['term'] = (df['term'].str.extract('(\d+)')).astype(int)

    df['emp_length'] = df['emp_length'].str.extract('(\d+)')
    df['emp_length'] = df['emp_length'].fillna(0).astype(int)

    df['int_rate'] = df['int_rate'].apply(lambda x: float(x.rstrip("%")))

    return df
```

> Declined-Loan Data

<img src ="extras/screenshots/drop_columns_declined.PNG" />

Below function will clean all such columns.
```
def funCleanData(df):

    df['Employment Length'] = df['Employment Length'].str.extract('(\d+)')
    df['Employment Length'] = df['Employment Length'].fillna(0).astype(int)

    df['Debt-To-Income Ratio'] = df['Debt-To-Income Ratio'].apply(lambda x: float(x.rstrip("%")))

    return df
```

### Fill missing data
Below function will fill all the NaNs with some default values.
> Loan Data

```
def funFillMissingData(df):
    df['home_ownership'] = df['home_ownership'].fillna('ANY')
    df['emp_title'] = df['emp_title'].fillna('Unknown')
    df['purpose'] = df['purpose'].fillna('other')
    df['inq_last_6mths'] = (df['inq_last_6mths'].fillna(0)).astype(int)
    df['loan_status'] = df['loan_status'].fillna('other')

    df['verification_status'] = np.where(df['verification_status'] == 'Not Verified' , 'Not Verified', 'Verified')

    return df
```
> Declined-Loan Data

```
def funFillMissingData(df):
    df['Loan Title'] = df['Loan Title'].fillna('Unknown')

    df['Risk_Score'] = df['Risk_Score'].fillna(111).astype(int)
    df['Risk_Score'].replace(0, 111,inplace=True)

    return df
```
### Write data to CSVs in chunks
```
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
```
### Snapshot of cleaned data
> Loan Data

<img src ="extras/screenshots/cleaned_loan_data.PNG" />

> Declined-Loan Data

<img src ="extras/screenshots/cleaned_declined_loan_data.PNG" />

### Snapshot of processed data folder
> Loan Data

The data will be divided in to the four quarters of the year and will be saved as 'year-Quarter.CSV'.

<img src ="extras/screenshots/folder_struct_loans.PNG" />

> Declined-Loan Data

The data will be divided in to the four quarters of the year and will be saved as 'year-Quarter.CSV'.

<img src ="extras/screenshots/folder_struct_declined.PNG" />

---

## Analysis 1

Exploratory data analysis on Approved vs Declined loans from year 2006 to 2016.

### Installation
[ana_1 Notebook](https://github.com/sumit91188/deo_sumit_spring2017/blob/master/Final/analysis/ana_1.ipynb) has following dependency.

```sh
$ pip install pandas
$ pip install numpy
$ pip install seaborn
$ pip install plotly
```
### Consolidate the data into single data frame
Below code will read each of the accepted/declined loans CSVs and consolidate the whole data into a data frame.

> Loan Data

```
dfLoanData = pd.DataFrame()
for directory, subdirectory, filenames in  os.walk(dataDir + 'loan_data\\'):
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), encoding = 'ISO-8859-1')
        dfLoanData =  pd.concat([df, dfLoanData], ignore_index=True)
```
> Declined-Loan Data

```
dfDecLoanData = pd.DataFrame()
for directory, subdirectory, filenames in  os.walk(dataDir + 'declined_loan_data\\'):
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), encoding = 'ISO-8859-1')
        dfDecLoanData =  pd.concat([df, dfLoanData], ignore_index=True)
```

### Summarizing data by States
  - Summary of accepted and rejected loans are displayed on the plot using plotly in offline mode.
  - Group the data by State and take average/mode of the required columns.
  - Create a dictionary of the summary and display on the plotly plot.
  - Hover over each state to get the summary.

> Accepted-Loans Summary

<img src ="extras/screenshots/loans_Sum_State.png" />

> Declined-Loans Summary

<img src ="extras/screenshots/dec_loans_Sum_State.png" />

### Time-Series analysis of number of loans
> Loan Data Summary

```
seriesCount = dfLoanData['LoanAmt'].groupby(dfLoanData['IssuedYear']).count()
seriesLA = dfLoanData['LoanAmt'].groupby(dfLoanData['IssuedYear']).mean()

columns=['Year', 'Accepted Loans', 'Avg Loan Amount']
dfAcceptedSummary = pd.DataFrame({'Year':seriesCount.index,'Accepted Loans': seriesCount/1000,
                          'Avg Loan Amount':seriesLA})
```
> Declined-Loan Data Summary

```
seriesCount = dfDecLoanData['LoanAmt'].groupby(dfDecLoanData['IssuedYear']).count()
seriesLA = dfDecLoanData['LoanAmt'].groupby(dfDecLoanData['IssuedYear']).mean()

columns=['Year', 'Declined Loans', 'Avg Dec-Loan Amount']
dfDeclinedSummary = pd.DataFrame({'Year':seriesCount.index,'Declined Loans': seriesCount/1000,
                          'Avg Dec-Loan Amount':seriesLA})
```
> Join above to summaries by year

```
dfSummary = pd.merge(dfAcceptedSummary, dfDeclinedSummary, on='Year')
```

>Below graph supports the fact that in Year 2014, Lending Club went public and started providing loans to small businesses. It also partnered with Union Bank and in the end of 2014, Lending club raised $900 million which we can see with the spike in the number of applications.

<img src ="extras/screenshots/NumberOfLoansByYear.PNG" />
