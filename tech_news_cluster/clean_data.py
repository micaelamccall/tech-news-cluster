from settings import DATA_PATH, PUBLICATIONS
import pandas as pd
import os
import datetime

files = {}

for pub in PUBLICATIONS:
    files[pub.lower()] = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv") and f.startswith(pub.lower())]
del(files, pub)

def load_news_data():
    """
    A function to load scraped news data from data folder
    """

    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]
    file_list = []
    for filename in files:
        df = pd.read_csv(os.path.join(DATA_PATH, filename))
        file_list.append(df)
    df_full = pd.concat(file_list, join='outer').drop_duplicates()
    return df_full


news_df = load_news_data()

news_df.describe()
news_df.shape

for col in news_df:
    print(col, type(col))

for col in news_df:
    news_df[news_df[col]]


for pub in news_df['publication'].unique():
    print(pub, news_df[news_df.publication==pub].date[0])


datetime.date.fromisoformat()


# def process_date_attrib()

# Take out the time from the date columns by replacing the dates in publications that have time included without the time
repl_dict = {}
for row in news_df.itertuples():
    if row.publication== 'Vox':
        repl_dict[row.date] = row.date[0:-13]
    elif row.publication == 'Vice':
        repl_dict[row.date] =row.date[0:-8].strip()
    elif row.publication == 'Buzzfeed News':
        repl_dict[row.date] = row.date[:-11].strip()
    else:
        repl_dict[row.date] = row.date

news_df.date = news_df.date.replace(repl_dict)

# If any dates end with a comma, take that out
repl_dict = {}
for row in news_df.itertuples():
    if str(row.date).endswith(','):
        repl_dict[row.date] = row.date[:-1]
    else:
        repl_dict[row.date] = str(row.date).strip()

news_df.date = news_df.date.replace(repl_dict)

news_df.date.value_counts()

# Separate the year and daymonth from the date strings
year = []
daymonth = []
for row in news_df.itertuples():
    if row.publication == 'Wired':
        year.append('20' + str(row.date)[-2:])
        daymonth.append(str(row.date[:-3]))
    else:
        year.append(str(row.date)[-4:])
        daymonth.append(str(row.date)[:-4].strip())
        
# Append year and daymonth columns
news_df['year'] = year
news_df['daymonth'] = daymonth

news_df.year.value_counts()
news_df.daymonth.value_counts()

del(year, daymonth)

# If any daymonths end with a comma, take that out
repl_dict = {}
for row in news_df.itertuples():
    if str(row.daymonth).strip().endswith(','):
        print(row.daymonth)
        repl_dict[row.daymonth] = row.daymonth.strip()[:-1]
    else:
        repl_dict[row.daymonth] = str(row.daymonth).strip()

news_df.daymonth = news_df.daymonth.replace(repl_dict)

# Separate out day and month
day = []
month = []
for row in news_df.itertuples():
    if row.publication == 'The Gradient':
        day.append(str(row.daymonth)[:2])
        month.append(str(row.daymonth[3:6]))
    elif row.publication == 'Wired':
        day.append(str(row.daymonth)[-2:].strip())
        month.append(str(row.daymonth)[:-3].strip())
    else:
        day.append(str(row.daymonth)[-2:].strip())
        month.append(str(row.daymonth).strip()[:-2])
        
# Append day and month columns
news_df['day'] = day
news_df['month'] = month

del(day, month)

# If any months end with a comma, take that out
repl_dict = {}
for row in news_df.itertuples():
    if str(row.month).strip().endswith('.'):
        repl_dict[row.month] = row.month.strip()[:-1]
    else:
        repl_dict[row.month] = str(row.month).strip()

news_df.month = news_df.month.replace(repl_dict)


repl_dict = {
    'May':'05',
    'Jun':'06', 'June':'06', 
    'Jul': '07', 'July':'07', 
    'Aug':'08', 'August': '08', 
    'Sep': '11', 'September': '11', 
    'Oct': '10', 'October': '10', 
    'Nov':'11', 'November': '11', 
    'Dec': '12', 'December': '12', 
    'Jan':'01', 'January':'01', 
    'Feb':'02', 'February':'02', 
    'Mar': '03', 'March': '03', 
    'Apr':'04', 'April':'04'}


news_df.month = news_df.month.replace(repl_dict)


repl_dict = {}

for row in news_df.itertuples():
    if len(str(row.day).strip()) < 2:
        repl_dict[row.day] = '0' + row.day.strip()
    else:
        repl_dict[row.day] = str(row.day).strip()

news_df.day = news_df.day.replace(repl_dict)


isoformat = []

for row in news_df.itertuples():
    try:
        isoformat.append(datetime.date(int(row.year), int(row.month), int(row.day)).isoformat())
    except ValueError:
        isoformat.append('NA')


news_df.date=isoformat



news_df.month.value_counts()







def binarize_categorical_variable(df, column, yescat):
    """ Fuction to turns a categorical variable in a DataFrame into a 0 or 1 response

    Arguments: 
    df = pandas DataFrame, 
    column = name of variable column as string
    yes = quoted *and bracketed* list of category names that you wish to turn to 1

    Returns: the original pandas df with new binarized variable"""

    # Change column to category dtype so that we can access it with .categories method
    df[column]=df[column].astype('category')
    
    # Create list of categories in column
    category_list = [] 
    
    for cat in df[column].cat.categories:
        category_list.append(cat)

    # Create dictionary with 1s for yes categories and 0 for no categories
    repl_dict = {}

    for cat in category_list:
        for yes in yescat:
            if cat == yes:
                repl_dict[cat] = 1   
        if repl_dict.get(cat) == None:
            repl_dict[cat] = 0

    # Replace original column in DataFrame
    df[column] = df[column].replace(repl_dict)

    return df

def new_categories(df, column, newcat):
    """ Function to replace categories in a variables with new category names
    
    Arguments:
    df =  a pandas DataFrame
    column = name of variable column as string
    newcat = a list of strings that name the new category names
    
    Output: a pandas DataFrame with new column names"""

    # Change column to category dtype so that we can access it with .categories method
    df[column]=df[column].astype('category')

    # Create list of categories in this variable
    category_list = []

    for cat in df[column].cat.categories:
        category_list.append(cat)

    # Create a dictionary of new names for each old category name
    repl_dict = {}

    for i, cat in enumerate(category_list):
        repl_dict[cat] = newcat[i]

    df[column] = df[column].replace(repl_dict)

    return df


# The NEO scores are scaled to a mean of 0 and standard deviation of 1 already, so I dont have to rescale
# Gender, Ethnicity, Education, and Country are encoded as real numbers, however there is no ordering betwen the levels of these features, so they should be treated as discrete
# One-hot encoding should therefore be applied to these features 

def cleanup_drug_df(df):
    """ A function to clean up the drug dataframe 
    
    Argument: Pandas DataFame
    
    Output: Cleaned up data as pandas DataFrame"""

    # Binarize the drug columns

    drug_df_clean = df

    for column in drug_df.columns[13:]:
        drug_df_clean = binarize_categorical_variable(drug_df_clean, column, yescat=['CL1','Cl2','CL3','CL4','CL5','CL6'])


    # Responses from individuals who said they had done an imaginary drug probably arent repliable,
    # so they are removed

    drug_df_clean = drug_df_clean[drug_df_clean.Semeron==0]

    # Change category names 
    new_categories_list = [
        ['18-24','25-34','35-44','45-54','55-64','65-100'],
        ['Female','Male'],
        ['Left school before age 16', 'Left school at age 16', 'Left school at age 17', 'Left school at age 18', 'Some college or university','Professional diploma/certificate', 'University degree', 'Masters degree', 'Doctorate degree'],
        ['USA','New Zealand','Other', 'Australia', 'Republic of Ireland','Canada', 'UK'],
        ['Black', 'Asian','White','Mixed Black/White','Other','Mixed White/Asian','Mixed Black/Asian']]

    columns_to_replace = ['Age', 'Gender', 'Education', 'Country', 'Ethnicity']

    for i, column in enumerate(columns_to_replace):
        new_categories(drug_df_clean, column, new_categories_list[i])
    
    return drug_df_clean


# Cleanup drug DataFrame
drug_df_clean=cleanup_drug_df(drug_df)

# Inspect counts for each drug column
if __name__ == '__main__':
    for column in drug_df_clean.columns[13:]:
        print(drug_df_clean[column].value_counts())
    
