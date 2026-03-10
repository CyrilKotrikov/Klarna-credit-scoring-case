# Klarna credit scoring case
Klarna credit scoring case by Cyril K

Initial model selection – I decided to use both linear and non-linear models to approach this case. Logistic regression was selected as the main model because it provides strong scope for structured data preprocessing. In parallel, I used XGBoost as a non-linear benchmark model, as both research and my personal experience suggest that it often outperforms logistic regression in predictive tasks. (It is important to note that the objective of this case study is not to build the best possible model, but to demonstrate a structured modeling approach.)

Initial data inspection showed that the dataset contains missing values and that several continuous variables exhibit significant outliers and right-skewed distributions. Additionally, the target variable is imbalanced. All above is common in credit scoring datasets.

Data Preparation & Feature Engineering
To address skewness and the presence of outliers in continuous variables, I applied binning followed by Weight of Evidence (WoE) transformation. I also calculated Information Value (IV) to evaluate the predictive strength of the predictors and filter out weak variables.
Finally, I used Variance Inflation Factor (VIF) to assess multicollinearity among predictors and remove highly correlated variables to improve model stability.

Several preprocessing and feature engineering steps were applied to improve data quality and capture meaningful borrower behaviour signals. Missing values and data inconsistencies were addressed through imputation, indicator variables, and basic data corrections. Additional behavioural and exposure-related features were created to better represent repayment behaviour and financial activity, while time-based features were derived to capture potential seasonal patterns. Finally, the target variable was defined based on outstanding balance after 21 days, and the dataset was split into training and testing sets using stratified sampling to maintain class balance.

After splitting the data into training and test sets, merchant-related categorical variables were encoded using historical default rates instead of dummy variables. For merchant groups, smoothing was applied to stabilize estimates for low-frequency categories. Unseen categories were assigned the overall training default rate, and the original categorical variables were removed.

Metrics
Model performance was evaluated using ROC-AUC, recall, F1-score, and the KS (Kolmogorov–Smirnov) statistic

Models performance

Logistic regression model: 
The model achieved a ROC-AUC of 0.65 on the training set and 0.63 on the test set, indicating moderate-low predictive power and suggesting that the model do not show strong overfitting. The model achieves a recall of 0.62 for the default class, meaning that approximately 62% of default cases are correctly identified. However, the precision for defaults remains low (0.08), indicating a relatively high number of false positives where good customers are classified as risky.
Overall, the model demonstrates the ability to capture meaningful risk signals but remains relatively conservative in its predictions. In a production setting, the classification threshold could be adjusted to better balance default detection and approval rates depending on business risk tolerance.
Currently the model is not suitable for production deployment due to its low precision, which leads to a high number of false positives and could result in rejecting many creditworthy customers, negatively impacting approval rates and customer satisfaction.

Xgboost model:
The XGBoost model was trained with hyperparameters optimization and evaluated using ROC-AUC, KS statistic, recall, precision, and F1-score. The classification threshold was selected on the validation set to ensure a minimum recall of 0.70 for the default class, prioritizing the detection of risky borrowers.
On the test set, the model achieves recall of 0.72 for default cases, meaning that the majority of risky loans are successfully identified. However, the precision also remains low (0.085), indicating a large number of false positives where non-default customers are classified as high risk.
The model achieved a ROC-AUC of 0.69, indicating moderate predictive performance and the ability to distinguish between good and bad borrowers better than random classification, though there remains room for improvement.

Deployment
To demonstrate a potential production setup, the trained model was deployed on Render as a backend service, with a Streamlit application used as the frontend interface.
https://klarna-credit-scoring-case.onrender.com

Scope for improvement

- SMOTE (Synthetic Minority Over-sampling Technique) to better handle the class imbalance in the dataset. (from my previous experience additional care should be taken)
- Dataset augmentation with additional features
- In this analysis, binning and Weight of Evidence (WoE) transformation were applied to handle skewness and outliers; however, alternative preprocessing approaches such as winsorization, value capping, or additional regularization could also be explored to further improve model robustness.
- I started implementing a FastAPI endpoint (in addition to Streamlit), but did not complete the implementation due to time limitations.

Files description:
- data
Contains the datasets used in the project, including both the original raw data and the cleaned or preprocessed versions used for model training and evaluation.
- app
Contains the Streamlit application used to interact with the trained model. This app provides a simple interface where users can input loan information and receive a credit risk prediction from the model.
- data_preprocessing_and_tests
Contains Jupyter notebooks with detailed annotations covering data exploration, feature engineering, preprocessing steps, and model experiments. These notebooks document the analytical process and testing performed during model development.





