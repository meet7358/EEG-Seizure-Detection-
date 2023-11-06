# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('Epileptic Seizure Recognition.csv')
print(data)

#rows X columns
print(data.shape)

dic = {5: 0, 4: 0, 3: 0, 2: 0, 1: 1}
data['y'] = data['y'].map(dic)

print(data['y'].value_counts())


#remove 'unnamed' column as it  has no relevent information
data = data.drop('Unnamed', axis = 1)

#now let us have a look on the description of our data
print(data.describe())

print(data.info())


#Let us group all the Epileptic occureses and Non Epileptic
print('Number of records of Non Epileptic {0} VS Epilepttic {1}'.format(len(data[data['y'] == 0]), len(data[data['y'] == 1])))

#Mean and std. deviation for epileptic
print('Totall Mean VALUE for Epiletic: {}'.format((data[data['y'] == 1].describe().mean()).mean()))
print('Totall Std VALUE for Epiletic: {}'.format((data[data['y'] == 1].describe().std()).std()))

#Mean and std. deviation for non-epileptic
print('Totall Mean VALUE for NON Epiletic: {}'.format((data[data['y'] == 0].describe().mean()).mean()))
print('Totall Std VALUE for NON Epiletic: {}'.format((data[data['y'] == 0].describe().std()).std()))

#big diffrence between values hence we will try to scale/normalize data


# data visualization

#Few cases of Non-Epileptic case
print([(plt.figure(figsize=(8,4)), plt.title('Not Epileptic'), plt.plot(data[data['y'] == 0].iloc[i][0:-1])) for i in range(5)])

#Few cases of Epileptic case
print([(plt.figure(figsize=(8,4)), plt.title('Epileptic'), plt.plot(data[data['y'] == 1].iloc[i][0:-1])) for i in range(5)])


#lists of arrays containing all data without y column
not_epileptic = [data[data['y']==0].iloc[:, range(0, len(data.columns)-1)].values]
epileptic = [data[data['y']==1].iloc[:, range(0, len(data.columns)-1)].values]

#We will create and calculate 2d indicators in order plot data in 2 dimensions;

def indic(data):
    """Indicators can be different. In our case we use just min and max values
    Additionally, it can be mean and std or another combination of indicators"""
    max = np.max(data, axis=1)
    min = np.min(data, axis=1)
    return max, min

x1,y1 = indic(not_epileptic)
x2,y2 = indic(epileptic)

fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(111)

ax1.scatter(x1, y1, s=10, c='b', label='Not Epiliptic')
ax1.scatter(x2, y2, s=10, c='r', label='Epileptic')
plt.legend(loc='lower left');
plt.show()


#Just Epileptic
x,y = indic(data[data['y']==1].iloc[:, range(0, len(data.columns)-1)].values)
plt.figure(figsize=(14,4))
plt.title('Epileptic')
plt.scatter(x, y, c='r')

#Just Non-Epileptic
x,y = indic(data[data['y']==0].iloc[:, range(0, len(data.columns)-1)].values)
plt.figure(figsize=(14,4))
plt.title('NOT Epileptic')
plt.scatter(x, y)

# ML Model

import imblearn
#use undersampling approach in order to prevent imbalanced issue
oversample = imblearn.over_sampling.RandomOverSampler(sampling_strategy='minority')
# fit and apply the transform
X, y = oversample.fit_resample(data.drop('y', axis=1), data['y'])
print(X.shape, y.shape)



#Check the balance for y
#Let us group all the Epileptic occureses and Non Epileptic
print('Number of records of Non Epileptic {0} VS Epilepttic {1}'.format(len(y == True), len(y == False)))

#Noramlizing  Data
from sklearn.preprocessing import normalize, StandardScaler
normalized_df = pd.DataFrame(normalize(X))
print(normalized_df)

#Concat back in order to check description:
normalized_df['y'] = y

print('Normalized Totall Mean VALUE for Epiletic: {}'.format((normalized_df[normalized_df['y'] == 1].describe().mean()).mean()))
print('Normalized Totall Std VALUE for Epiletic: {}'.format((normalized_df[normalized_df['y'] == 1].describe().std()).std()))

print('Normalized Totall Mean VALUE for NOT Epiletic: {}'.format((normalized_df[normalized_df['y'] == 0].describe().mean()).mean()))
print('Normalized Totall Std VALUE for NOT Epiletic: {}'.format((normalized_df[normalized_df['y'] == 0].describe().std()).std()))


#split dataset into  train and test and than invoke validation approach
from sklearn.model_selection import train_test_split
X = normalized_df.drop('y', axis=1)
y = normalized_df['y']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Check the shapes after splitting
he = X_train, X_test, y_train, y_test
print([arr.shape for arr in he])

#model
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
clf =RandomForestClassifier()

# train model
train_data = clf.fit(X_train,y_train)

# predictions 
predictions = train_data.predict(X_test)
print(predictions)

score = train_data.score(X_test, y_test)
print(score)

import pickle
with open('train_data.pkl', 'wb') as file:
    pickle.dump(train_data, file)