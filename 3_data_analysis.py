# Import modules.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()

# Read .csv and update column headers.
df = pd.read_csv('cars.csv')
df.columns = ['ID', 'Make Model', 'Make', 'Segment', 'Price', 'Depreciation', 'Reg Date', 'Manu Year', 'Mileage', 'Tranny', 'Eng Cap', 'Road Tax', 'Power', 'Weight', 'Features', 'Accessories', 'Description', 'COE Left', 'COE Price', 'OMV', 'ARF', 'Owners', 'Veh Type', 'Category', 'Date Posted', 'Updated Date', 'Tags', 'Date Sold', 'Last Edited', 'Days to Sell', 'Premium Ad', 'Direct Owner', 'Day Posted', 'Day Sold']

# Quick look at the data with a scatterplot of Days to Sell against Depreciation, coloured according to Segment.
sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', hue = 'Segment', s = 15, edgecolor=None,
                     data=df)
plt.title('Vehicle Segments')

# Remove outliers and reset DataFrame index.
df = df[df['Depreciation'] < 75000]
df = df.reset_index(drop=True)

# Break up the DataFrame into multiple DataFrames representing the various segments.
exotic = df[df['Segment'] == 'Exotic']
ultra_luxury = df[df['Segment'] == 'Ultra Luxury']
luxury = df[df['Segment'] == 'Luxury']
mid_level = df[df['Segment'] == 'Mid Level']
economy = df[df['Segment'] == 'Economy']
budget = df[df['Segment'] == 'Budget']

# Plot segments sequentially for a visual check on segmentation accuracy.
sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', s = 15, edgecolor=None,
                     data=exotic)
plt.xlim(0,80000)
plt.ylim(0,80)
plt.title('Exotic')

sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', s = 15, edgecolor=None,
                     data=ultra_luxury)
plt.title('Exotic + Ultra Luxury')

sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', s = 15, edgecolor=None,
                     data=luxury)
plt.title('(Exotic, Ultra Luxury) + Luxury')

sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', s = 15, edgecolor=None,
                     data=mid_level)
plt.title('(Exotic, Ultra Luxury, Luxury) + Mid Level')

sns.scatterplot(x = 'Depreciation', y = 'Days to Sell", s = 15, edgecolor=None,
                     data=economy)
plt.title('(Exotic, Ultra Luxury, Luxury, Mid Level) + Economy')

# colour of marker changed to white, default colour assigned is too difficult to spot on the plot.
sns.scatterplot(x = 'Depreciation', y = 'Days to Sell', s = 15, color = 'white', edgecolor=None,
                     data=budget)
plt.title('(Exotic, Ultra Luxury, Luxury, Mid Level, Economy) + Budget')


### Question 1: To Buy from a Direct Owner or a Dealer?
# Break up the dataframe into two, into cars sold by their direct owners and cars sold by dealers.
directowner_df = df[df['Direct Owner'] == 1]
dealer_df = df[df['Direct Owner'] == 0]

# Generate the descriptive statistics.
desc_directowner = directowner_df.describe()
desc_dealer = dealer_df.describe()

# Remove listings with mileage = 0.
directowner_df = directowner_df[directowner_df['Mileage'] != 0]
dealer_df = dealer_df[dealer_df['Mileage'] != 0]

# Rerun the descriptive statistics.
desc_directowner = directowner_df.describe()
desc_dealer = dealer_df.describe()

# Plot histogram for direct vs non-direct owner sales.
sns.distplot(directowner_df['Mileage'], label='Direct Owner', color='red', bins=50, kde=True)
sns.distplot(dealer_df['Mileage'], label='Dealer', color='mediumblue', bins=50, kde=True)
plt.title('Mileage (in km) - Direct Owner vs Dealer Sales')
plt.legend()
plt.show()

# Plot Depreciation distribution and KDE for direct owners vs dealers.
sns.distplot(directowner_df['Depreciation'], label='Direct Owner', color='red', bins = 100, kde=True)
sns.distplot(dealer_df['Depreciation'], label='Dealer', color='mediumblue', bins = 100, kde=True)
plt.title('Depreciation - Direct Owner vs Dealer Sales')
plt.legend()
plt.show()


### Question 2: Is sgCarMart Forgoing Revenue from the Lower Segments?
# Find out the count of direct owner vs dealer sales for the various segments. Execute the following line-by-line and save the output in an external table.
exotic['Direct Owner'].value_counts()
ultra_luxury['Direct Owner'].value_counts()
luxury['Direct Owner'].value_counts()
mid_level['Direct Owner'].value_counts()
economy['Direct Owner'].value_counts()
budget['Direct Owner'].value_counts()

### Question 3: Premium Ads — Do They Work?
# Break up the dataframe into two, for premium and non-premium ads. Remove rows with mileage = 0 before that. 2002 entries out of 10006 removed.
df_mileage0 = df[df['Mileage'] != 0]
premiumad_df = df_mileage0[df_mileage0['Premium Ad'] == 1]
nonpremiumad_df = df_mileage0[df_mileage0['Premium Ad'] == 0]

# Run descriptive statistics.
desc_premiumad = premiumad_df.describe()
desc_nonpremiumad = nonpremiumad_df.describe()

# Perform count on premium ad vs non-premium ad, for the various segments.
exotic['Premium Ad'].value_counts()
ultra_luxury['Premium Ad'].value_counts()
luxury['Premium Ad'].value_counts()
mid_level['Premium Ad'].value_counts()
economy['Premium Ad'].value_counts()
budget['Premium Ad'].value_counts()


### Question 4: What Keywords I Should Use in Describing the Vehicle?
# Combine the 3 columns of descriptive text into 1 for easy processing.
df['Text'] = df['Features'] + ' ' + df['Accessories'] + ' ' + df['Description']

# Import the modules and clean up the text
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, len(df)):
    text = re.sub('[^a-zA-Z]', ' ', df['Text'][i])
    text = text.lower()
    text = text.split()
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text if not word in set(stopwords.words('english'))]
    text = ' '.join(text)
    corpus.append(text)
    
    
# Create the bag of words model
from sklearn.feature_extraction.text import TfidfVectorizer
tv = TfidfVectorizer(max_features = 1000, ngram_range = (1,2), norm = None)
X = tv.fit_transform(corpus).toarray()
y = df['Days to Sell'].values   


# Split dataset into training and test sets.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)

# Perform Grid Search on the SVR model to find the optimal parameters to achieve a lower MSE.
# The poly kernel was excluded as it never converged to a solution. The same was done for C values 10, 100 and 1000 for the linear kernel.
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
regressor = SVR(kernel = 'linear')
parameters = [{'C': [1], 'kernel': ['linear']},
              {'C': [1, 10, 100, 1000], 'kernel': ['rbf']},
              {'C': [1, 10, 100, 1000], 'kernel': ['sigmoid']}]
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           scoring = 'neg_mean_squared_error',
                           n_jobs = -1)

# Fit GridSearchCV to the training dataset.
grid_search = grid_search.fit(X_train, y_train)

# Look at the results for grid search.
cv_results = grid_search.cv_results_
cv_results = pd.DataFrame(cv_results)

# SVR optimal paramters found. Next, SVR regressor fitting iterated.
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
svr_rmse = []
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)
    regressor = SVR(kernel = 'rbf', C = 10)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    rmse = (mean_squared_error(y_test, y_pred)) ** 0.5
    svr_rmse.append(rmse)
    
## Decision tree regressor fitting iterated.
from sklearn.tree import DecisionTreeRegressor
dectree_rmse = []
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    rmse = (mean_squared_error(y_test, y_pred)) ** 0.5
    dectree_rmse.append(rmse)

# Linear regressor fitting iterated.
from sklearn.linear_model import LinearRegression
linreg_rmse = []
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    rmse = (mean_squared_error(y_test, y_pred)) ** 0.5
    linreg_rmse.append(rmse)

# Re-iterate the linear regression model, this time creating a list of features and their corresponding coefficients.
from sklearn.linear_model import LinearRegression
linreg_rmse = []
coef_list = []
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    rmse = (mean_squared_error(y_test, y_pred)) ** 0.5
    linreg_rmse.append(rmse)
    coef = regressor.coef_
    coef_list.append(coef)
features = tv.get_feature_names()
features = pd.DataFrame(features)
coef_list = pd.DataFrame(coef_list)
coef_list = coef_list.transpose()
coef_features = pd.concat([features, coef_list], axis = 1, sort = False)
coef_features.columns = ['Feature', 'Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4', 'Iteration 5', 'Iteration 6', 'Iteration 7', 'Iteration 8', 'Iteration 9', 'Iteration 10']

# Quick and dirty average of the coefficients and sort the averages to see which coefficients may be important.
coef_features['Mean'] = coef_features.mean(axis=1)
coef_features = coef_features.sort_values(by=['Mean'])

# Search through the Text column for feature matches.
df['non oblig'] = np.where(df['Text'].str.contains('Non Oblig|Non-Oblig|Non-oblig'), 1, 0)
df['fog'] = np.where(df['Text'].str.contains('Fog'), 1, 0)
df['sta vicom'] = np.where(df['Text'].str.contains('STA/Vicom|STA/vicom|Sta/Vicom|Sta/vicom|STA Vicom|Sta Vicom'), 1, 0)
df['drive away'] = np.where(df['Text'].str.contains('Drive Away|Drive-Away|Drive-away'), 1, 0)
df['evalu'] = np.where(df['Text'].str.contains('Evalu'), 1, 0)

# Plot histograms for a check if the distribution of days taken to sell a car is affected by the presence of the 5 features.
# 'non oblig'
sns.distplot(df[df['non oblig'] == 1]['Days to Sell'], label="'non oblig' TRUE; Count=" + str(df['non oblig'].sum()), color='red', bins=40, kde=True)
sns.distplot(df[df['non oblig'] == 0]['Days to Sell'], label="'non oblig' FALSE; Count=" + str(df.shape[0] - df['non oblig'].sum()), color='mediumblue', bins=40, kde=True)
plt.title("Feature 1 - 'non oblig'")
plt.legend()
plt.show()

# 'fog'
sns.distplot(df[df['fog'] == 1]['Days to Sell'], label="'fog' TRUE; Count=" + str(df['fog'].sum()), color='red', bins=40, kde=True)
sns.distplot(df[df['fog'] == 0]['Days to Sell'], label="'fog' FALSE; Count=" + str(df.shape[0] - df['fog'].sum()), color='mediumblue', bins=40, kde=True)
plt.title("Feature 2 - 'fog'")
plt.legend()
plt.show()

# 'sta vicom'
sns.distplot(df[df['sta vicom'] == 1]['Days to Sell'], label="'sta vicom' TRUE; Count=" + str(df['sta vicom'].sum()), color='red', bins=40, kde=True)
sns.distplot(df[df['sta vicom'] == 0]['Days to Sell'], label="'sta vicom' FALSE; Count=" + str(df.shape[0] - df['sta vicom'].sum()), color='mediumblue', bins=40, kde=True)
plt.title("Feature 3 - 'sta vicom'")
plt.legend()
plt.show()

# 'drive away'
sns.distplot(df[df['drive away'] == 1]['Days to Sell'], label="'drive away' TRUE; Count=" + str(df['drive away'].sum()), color='red', bins=40, kde=True)
sns.distplot(df[df['drive away'] == 0]['Days to Sell'], label="'drive away' FALSE; Count=" + str(df.shape[0] - df['drive away'].sum()), color='mediumblue', bins=40, kde=True)
plt.title("Feature 4 - 'drive away'")
plt.legend()
plt.show()

# 'evalu'
sns.distplot(df[df['evalu'] == 1]['Days to Sell'], label="'evalu' TRUE; Count=" + str(df['evalu'].sum()), color='red', bins=40, kde=True)
sns.distplot(df[df['evalu'] == 0]['Days to Sell'], label="'evalu' FALSE; Count=" + str(df.shape[0] - df['evalu'].sum()), color='mediumblue', bins=40, kde=True)
plt.title("Feature 5 - 'evalu'")
plt.legend()
plt.show()

# Generate descriptive statistics of the 5 key features in a combined pandas DataFrame.
features = ['non oblig', 'fog', 'sta vicom', 'drive away', 'evalu']
describe_features = pd.DataFrame()

for feature in features:
    describe_features[str(feature + ' TRUE')] = df[df[feature] == 1]['Days to Sell'].describe()
    describe_features[str(feature + ' FALSE')] = df[df[feature] == 0]['Days to Sell'].describe()
