# Credit-Scoring
A machine learning method is used in the risk-based pricing model to evaluate the likelihood of default using five features. Then, taking into account the cost of funds, default premium, operative costs and a profit margin, it calculates the interest rate to be charged to the loan.

# File description
Risk_based_pricing.py: A python file which contains all the code regarding data cleaning, model training, default probability estimation and loan pricing.

Risk_based_pricing.xlsm: A macro-enabled Excel workbook in which data to train the model, as well as new customer data, can be entered. Model output is also displayed (for details on the separate sheets, please see the #Implementation section below).

VBA code (Run Python script).txt: A text file with the VBA code employed so that the python script could be run on Excel.


# Data collection
The data was provided by a small lender in Colombia, which has been in the market for four years, carrying out 69 loans (at the date when the data frame was obtained). The data frame includes data from those 69 loans with 26 variables, including customer information, loan details, and business estimates.
As per business request, the data file or the variables employed in the credit scoring will not be disclosed.

# Data cleaning
Non-informative variables such as internal ID numbers and customer personal information (e.g. name) were discarded from the data frame in order to estimate default probabilities. Additionally, other variables which could leak information regarding a customer's credit risk were also discarded (i.e. interest rate charged to the customer contains information about credit assessment done by the business which would bias the model to estimate default probabilities based on current business practices).

Categorical variables were transformed into dummy variables, and finally, all the variables were scaled.

# Feature selection
In order to obtain the variables to be employed in the model, it was necessary to reduce the dimensionality of the problem (i.e. reduce the number of variables). The following steps were carried out to reduce the number of variables from 26 to 5.

Correlation matrix: As an initial step, a correlation matrix was calculated, and variables with strong correlation (more than 0.2 in absolute terms) were identified as possible candidates.

PCA: Through principal component analysis, it is possible to remove multicollinearity issues and display graphically the relevance of the variables. By employing a biplot chart, it was possible to determine which variables had the highest impact on the target variable.

RFE (recursive feature elimination): This technique fits a model to the data (a logistic regression in this case) and indicates which are the strongest and weakest variables in terms of statistical significance.

Business understanding: Since the dataset presented was relatively small, some of the results obtained did not make sense when compared to conventional financial theory. For instance, the model claimed that duration was not an important feature, while it is well-known that short-term loans are less risky than longer-term loans, and default probability increases with time. Therefore, the results obtained from the previous procedures were contrasted with financial theory and business understanding in order to make the final selection of features.

# Model selection
Since the output of the model is a binary variable (Default or not) a classification model such as logistic regression is a viable model. Other possibilities involve decision trees or random forests which were not employed for this project. A more complex model would involve Artificial Neural Networks, but it requires a large data set to be employed, a condition which is not fulfilled by the current data frame.

# Model tuning
Dealing with a small dataset was one of the main obstacles of this project, so the following concepts were tested in an effort to enhance the outcomes:

Oversampling: The dataset is clearly not balanced, with defaults representing around 10% of the dataset. Using SMOTE (Synthetic Minority Oversampling Technique), new examples could be created based on existing examples. However, upon implementation, the results obtained were not satisfactory as the model would estimate default probabilities close to 80% in some cases, which does not make sense in practice. A person with an 80% of default probability would be in a precarious financial situation, but none of the customers of the business had such obvious financial issues. 

Hyperparameter tuning: The logistic regression model in Python includes a parameter "C", which is a form of regularization. After testing for many values of C using grid-search cross-validation, the model seemed to favour higher values of C, meaning a model that overall is more likely to generalize future data, which is not a desirable feature in a model that aims to estimate default probabilities. Therefore, the default value of C=1.0 was chosen instead. 

# Model validation
After training and testing the logistic regression model, a few indicators were taken into account to determine whether the results provided by the model were satisfactory:

AUC ROC score: 0.88, indicating that the model is good at identifying correct defaults vs non-defaults
F1 weighted score: The F1 score is preferred in this example since the aim of the model is not to have overall correct estimates (such a model would simply classify all customers as non-defaults), but to minimize default customers being classified as non-defaults, also known as a false negative. A score of 0.79 is a good sign that the model is working correctly.

New data: To test model coherence, data on imaginary customers was generated, and the new customer data was passed onto the model, sorting them from high to low default probability. The ranking was deemed reasonable by the business as they mostly classified them in the same way (from less risky to riskier).

# Risk-based pricing
Once default probabilities have been estimated, it is possible to put a risk-based pricing model into place. This model would acknowledge the cost of funds, default premium, operative costs and a target profit margin in order to price the loans (set an adequate interest rate). The following parameters were needed in order to proceed:

Cost of funds: Defined in this case as the "risk-free" opportunity cost for the business, the rate chosen was the 10-year yield of Colombian sovereign bonds (the country in which the business operates). To ensure that the risk-free rate is up to date, the model obtains the latest quote from a website specialising in macroeconomic data.

Recovery rate: The percentage of funds that can be recovered once the customer is in default. The estimation of this parameter becomes complex once collaterals are added to the loan request. For simplicity, the business used historical data on its past transactions to determine a feasible level of recovery.

Fees and other OP costs: In other words, transaction costs and other expenses directly related to loan disbursements. Estimated using historical business data.

Base rate: Risk-free rate + Default premium + Operative costs (Fees), this is the fair price of the loan, the minimum rate to be charged for the business to reach break-even.

Target profit: A spread over the base rate decided by the business, and affected by market conditions (competitors). 

Annual interest rate: Base rate + Target profit, is the interest rate to be charged to the customer.

# Implementation
Once the model was approved, the next step was to make it user-friendly and easy to handle by the business. By creating an excel file with the following sheets, it was ensured that the business would have no problems using the script on a daily basis:

Data: A hidden sheet that contains the data used to train the model. With the pace of time, as the number of loans increases, new information should be fed into this tab.

Parameters: Includes recovery rate, fees and target profit margin.

Customers: This is where new customer information can be entered. It also includes an "Estimate rates" button which triggers a VBA script that in turn runs the Python script.

Loan pricing: This is where the model output is displayed.
