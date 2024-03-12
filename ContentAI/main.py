import pandas as pd
import matplotlib as plt
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import os, pickle

# define model name
filename = "model.sav"

# import data
df = pd.read_csv("data.csv")
print(df.head())

le = LabelEncoder()

def organizeData():

  ### label encode all columns and create them as new columns ###  
  title_encoded = le.fit_transform(df['webpage title'])
  hashtag1_encoded = le.fit_transform(df['hashtag1'])
  hashtag2_encoded = le.fit_transform(df['hashtag2'])
  hashtag3_encoded = le.fit_transform(df['hashtag3'])
  caption_encoded = le.fit_transform(df['caption']) 
  url_encoded = le.fit_transform(df['url'])

  df['url_encoded']  = url_encoded  
  df['title_encoded']= title_encoded
  df['hashtag1_encoded'] = hashtag1_encoded
  df['hashtag2_encoded'] = hashtag2_encoded
  df['hashtag3_encoded'] = hashtag3_encoded
  df['caption_encoded'] = caption_encoded

  # create inputs
  x = df[['url_encoded', 'title_encoded', 'hashtag1_encoded', 'hashtag2_encoded', 'hashtag3_encoded', 'caption_encoded']]

  # create outputs
  timewasting_encoded = le.fit_transform(df['time-wasting'])
  y = timewasting_encoded

  X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=39)
  
  return X_train, X_test, y_train, y_test


def create_model():
  if(os.path.isfile(filename)):
    ### currently model is a linear regression model
    model = pickle.load(open(filename, 'rb'))
  else:
    model = LinearRegression()

  # return the new or loaded model
  return model
  

def train(model, X_train, X_test, y_train, y_test):
  # fit the model to the training data
  model.fit(X_train, y_train)

  # make predictions on the test data
  y_pred = model.predict(X_test)

  # Calculate the accuracy of the model
  accuracy = accuracy_score(y_test, y_pred)

  print("Accuracy:", accuracy)
  print("Classification Report:\n", classification_report(y_test, y_pred))
  # Compute the confusion matrix
  cm = confusion_matrix(y_test, y_pred)


def prediction(model, data):
  predicted_value = model.predict([data])
  print('predicted numerical value: ', predicted_value)
  # convert the numerical value back to its original categorical label
  label = le.inverse_transform(predicted_value)

  return label[0]


if __name__ == "__main__":
  # check if model exists
  X_train, X_test, y_train, y_test = organizeData()
  model = create_model()

  train(model, X_train, X_test, y_train, y_test)

  # now re-dump the model 
  pickle.dump(model, open(filename, 'wb'))

