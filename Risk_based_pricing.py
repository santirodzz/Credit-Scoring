# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:55:23 2022

@author: Santiago
"""

#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, classification_report,confusion_matrix
import xlwings as xw


#read excel file
path="C:\\your_path\\Risk_based_pricing.xlsm" #The excel file is a macro enabled book, this the .xlsm is crucial

raw= pd.read_excel(path,index_col=0,sheet_name='Data')

#Variable description
#Due to customer request, full data set will not be disclosed
#However, some of the variables were not taken into account since they did not contain useful information
#for the effects of estimating default probability i.e. (customer name, ID number, etc)
#On the other hand, some variables would leak information regarding customer credit risk and would severely bias the model,
#i.e (interest rate set by the business and agreed monthly installments), such variables were discarded as well.


#Cleaning data: Drop non-informative variables

df=raw.drop(['variables deeemed as non-informative or variables which would potentially leak information about customer risk'],axis=1)
print(df.info())

#Transform dummy variables
#Default variable was set as a string (Yes/No), therefore it needs to be transformed to a dumy variable

d_dummy=pd.get_dummies(df['Default'],drop_first=True) #1= Default
dummies=pd.concat([d_dummy],axis=1)

#Prepare to introduce variables
#Intermediate step to introduce the transformed variable

df_drop=df.drop(['Default'],axis=1)

#Definitive data frame

ddf=pd.concat([df_drop,dummies],axis=1)
ddf.rename(columns={'Yes':'Default'},inplace=True)

#Scaling
#Some variables such as past loans with the lenders range from 1 to 10
#While customer income and loan amount are in millions of Colombian pesos
#The huge difference in variance would have unwanted effects in the model, 
#therefore it is necessary to scale all the variables.

scaler=StandardScaler()
scaler.fit(ddf)
StandardScaler(copy=True,with_mean=True,with_std=True)
ddf_scaled=scaler.transform(ddf)


#Setting Default as target variable
#The process to determine the predictive variables contained in X followed PCA analysis, clustering, 
#correlation matrix, recurrent feature elimination, and business understanding.
#Those steps are not contained in the present file.

ddf_scaled=pd.DataFrame(data=ddf_scaled,index=ddf.index.values,columns=ddf.columns.values)
X=ddf_scaled.drop(['Default'],axis=1)
Y=ddf['Default']

#Machine learning algorithm (logistic regression)
#Given the number of observations (69), and the outcome variable being binary (deafult or not)
#a logistic regression is a feasible model to be employed.
#Train and test data split

X_train, X_test, Y_train, Y_test= train_test_split(X,Y, test_size=0.3,random_state=0)
logreg=LogisticRegression()
logreg.fit(X_train,Y_train)
y_pred=logreg.predict(X_test)

#predicting probabilities
y_pred_probs=logreg.predict_proba(X_test)[:,1]

#ROC

fpr,tpr,thresholds=roc_curve(Y_test,y_pred_probs)
plt.plot(fpr,tpr)


roc_score=roc_auc_score(Y_test, y_pred_probs)

#Confusion matrix and classification report

confusionm=confusion_matrix(Y_test, y_pred)
class_rep=classification_report(Y_test, y_pred)

#Testing with new clients

#Obtain new custome data from the excel file
x2=pd.read_excel(path,index_col=0,sheet_name='Customers')
params=pd.read_excel(path,index_col=0,sheet_name='Parameters') #Creating parameters dataframe

#Standardise variables
scaler=StandardScaler()
scaler.fit(x2)
StandardScaler(copy=True,with_mean=True,with_std=True)
x2_scaled=scaler.transform(x2)
x2_scaled=pd.DataFrame(data=x2_scaled,columns=x2.columns.values,index=x2.index.values)

#Estimate default probabilities for new customers

y_pred2=logreg.predict(x2_scaled)
default_prob=logreg.predict_proba(x2_scaled)[:,1]


#Risk based pricing

#Risk free rate (Cost of funds):
#Acknowledge opportunity cost (rate of "risk free" sovereign bonds of the Colombian government, since Colombia is the
#country in which the business operates)

datos_macro=pd.read_html('https://datosmacro.expansion.com/bono/colombia')
bond_yields=datos_macro[1]
#Setting up risk free rate with the latest quote on 10-years government bonds
rf=bond_yields.loc[0,'Rendimiento']
rf=rf.replace(',','.')
rf=float(rf.replace('%',''))/100

#Loan pricing

#Recovery rate: Estimated from business past experiences, refers to the amount recovered when the customer defaults
recovery=float(params.loc['Recovery rate','Value'])
#Fees: Estimated fees incurred by the business for loan disbursements
fees=float(params.loc['Fees','Value'])
#Margin: desired profit
margin=float(params.loc['Margin','Value'])
#Calculating default premium
default_premium=(1-recovery)*default_prob
#Fees as a percentage of loan amount
op_cost=fees/x2.loc[:,'Amount'].to_numpy()
#Basic cost: Defined as the break even interest rate
basic_cost=rf+default_premium+op_cost
#Final rate to be charged, includes profit margin established by the business
lending_r=basic_cost+margin

#Preparing table to be exported to Excel
rate=pd.DataFrame({'Default prob':default_prob,'Default premium':default_premium,'Costos op':op_cost,'Tasa base':basic_cost,'Tasa colocación E.A.':lending_r},index=x2.index.values)

table=pd.concat([x2,rate],axis=1)


#Export to Excel

#load book
app=xw.App(visible=False)
wb=xw.Book(path)
ws=wb.sheets['Loan pricing']

#Update workbook
ws.range('A2').options(index=True).value=table

#Close WB

wb.save()
wb.close()
app.quit()










