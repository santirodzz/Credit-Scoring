# Credit-Scoring
Risk based pricing model which employs a machine learning algorithm that estimates default probability by using five features. Then, taking into account the cost of funds, default premium, operative costs and a profit margin it calculates the interest rate to be charged to the loan.

# Data collection
The data was provided by a small lender in Colombia, it has been in the market for about four years, and it has carried out 69 loans (at the date when the dataframe was obtained). The dataframe includes data of those 69 loans with 26 variables, including customer information, loan details, and business estimates.
As per business request, the data file or the variables employed in the credit scoring will not be disclosed.

# Data cleaning
The dataframe contained non-informative variables for the purpose of estimating default probabilities such as internal ID numbers and customer personal information (e.g. name), such variables were discarded. Additionally, other variables which could leak information regarding customer's credit risk were also discarded (i.e. interest rate charged to the customer contains information of a credit assesment done by the business which would bias the model to estimate default probabilities based on current business practices).

Categorical variables were transformed to dummy variables, and finally all the variables were scaled.

# Feature selection
In order to obtain the variables to be employed in the model, it was necessary to reduce the dimensionality of the problem (i.e. reduce the number of variables). The following steps were carried out to reduce the number of variables from 26 to 5.

Correlation matrix: As an initial step, a correlation matrix was calculated, variables with strong correlation (more than 0.2 in absolute terms) were identified as possible candidates.

PCA: Through principal component analysis, it is possible to remove multicollinearity issues and display graphically the relevance of the variables. By employing a biplot chart it was possible to determine which variables had the highest impact on the target variable.

RFE (recursive feature elimination): This technique fits a model to the data (a logistic regression in this case) and indicates which are the strongest and weakest variables.

Business understanding: Since the dataset presented was relatively small, some of the results obtained did not make sense when compared to conventional financial theory. For instance, the model claimed that duration was not an important feauture, while it is well known that short term loans are less risky than long term loans, and default probability increases with time. Therefore, the results obtained from the previous procedures were constrated with financial theory and business understanding in order to make the final selection of feautres.

# Model selection
Since the output of the model is a binary variable (Default nor not) a logistic regression is a viable model, other classifiers like decession trees or random forests would also be possible alternatives, but were not in scope of this project. A more complex model would  involve Artificial Neural Networks, but it requires a large data set to be employed, a condition which is not fulfilled by the current dataframe.

# Model tuning
One of the biggest challenges of this project was dealing with a small dataset, the following ideas were tested aiming to improve the results obtained:

Oversampling: The dataset is clearly inbalance, with defaults representing aroun 10% of the dataset. Using SMOTE (synthetic minority oversampling technique) new examples could be created based on existing examples. However, upon implementation the results obtained were not satisfactory as the model would estimate default probabilities close to 80% in some cases, which does not make sense in practice. A person with 80% of default probability would be in a precarious financial situation, but none of the customers of the business had such obvious financial issues. 

Hyperparameter tuning: The logistic regression model in Python includes a parameter "C", which is a form of regularization. After testing for many values of C using gridsearch cross validation, the model seemed to favor higher values of C, meaning a model that overall is more likely to generalize future data, which is not a desirable feature in a model that aims to estimate default probabilities. Therefore, the default value of C=1.0 was chose instead. 

# Model validation
