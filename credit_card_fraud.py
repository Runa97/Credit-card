# -*- coding: utf-8 -*-
"""Credit Card fraud.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uWASHJ14fKVGl_PbnEQ4kO5xyXhaomem
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install dtale

!pip install pydantic-settings

!pip install --upgrade pandas-profiling

!pip install --upgrade joblib markupsafe

!pip install autoviz

"""**1: Importing libraries**"""

!pip install catboost

!pip install xgboost matplotlib seaborn scikit-learn

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve, auc, cohen_kappa_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns
from catboost import CatBoostClassifier
import time
from sklearn.metrics import confusion_matrix, roc_curve, auc


# For handling warnings
import warnings
warnings.filterwarnings('ignore')

"""**2: Load dataset**"""

# Load the dataset
#data = pd.read_csv('/content/csv_result-Autism-Adult-Data_.csv')
data = pd.read_csv('/content/drive/MyDrive/Capstion/credit_card_transactions.csv')

data.head()

from autoviz.AutoViz_Class import AutoViz_Class
import pandas as pd


# Initialize AutoViz
AV = AutoViz_Class()

# Generate EDA plots
viz = AV.AutoViz(filename='', dfte=data)

data = data.drop(['Unnamed: 0','dob', 'trans_date_trans_time','trans_num'], axis=1)
data.head()

"""**3: Data Cleaning**"""



"""# Find the most common value in the column
mode_value1 = data['relation'].mode()[0]
mode_value2 = data['ethnicity'].mode()[0]

# Replace '?' with the mode value
data['relation'] = data['relation'].replace('?', mode_value1)
data['ethnicity'] = data['ethnicity'].replace('?', mode_value2)
"""

# Check for missing values
missing_values = data.isnull().sum()
print("Missing values before cleaning:\n", missing_values)

data = data.drop(['merch_zipcode'], axis=1)

# Assuming data is your DataFrame

data = data.apply(lambda col: col.astype('category') if col.dtype == 'object' else col)

data.dtypes

# Assuming data is your DataFrame

cat_cols = data.select_dtypes(include='category').columns.tolist()
cat_cols

"""**level encoding**"""

from sklearn.preprocessing import LabelEncoder
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

data.head(20)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load your dataset
# data = pd.read_csv('your_dataset.csv')
data = pd.read_csv('/content/drive/MyDrive/Capstion/credit_card_transactions.csv')
# Identify numerical and categorical features
numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
categorical_features = data.select_dtypes(include=['object', 'category']).columns

# Plotting numerical features
for feature in numerical_features:
    plt.figure(figsize=(10, 6))

    # Histogram
    plt.subplot(1, 2, 1)
    sns.histplot(data[feature], kde=True, bins=30)
    plt.title(f'Distribution of {feature}')

    # Box plot
    plt.subplot(1, 2, 2)
    sns.boxplot(y=data[feature])
    plt.title(f'Box plot of {feature}')

    plt.tight_layout()
    plt.show()

# Plotting categorical features
for feature in categorical_features:
    plt.figure(figsize=(10, 6))

    # Count plot
    sns.countplot(x=data[feature])
    plt.title(f'Count plot of {feature}')

    plt.tight_layout()
    plt.show()

# Pair plot for relationships between numerical features
sns.pairplot(data[numerical_features])
plt.show()

"""**Data Spliting**"""

# 3. Train-Test Split
from imblearn.over_sampling import SMOTE
X = data.drop(columns='is_fraud')
y = data['is_fraud']

# Apply SMOTE to handle imbalance in the dataset
smote = SMOTE(random_state=42)
X_res, y_res =smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.25,stratify=y_res, random_state=42)

"""Checking sample counts before smoothing and spliting

"""

# Before applying SMOTE, check the class distribution
class_counts_before = y.value_counts()

# Print the counts of each class
print("Class counts before balancing:")
print(class_counts_before)

# If you want the percentage as well
class_percentages_before = (class_counts_before / len(y)) * 100
print("\nClass percentages before balancing:")
print(class_percentages_before)

"""Smoothing, spliting and checking sample counts

"""

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

X = data.drop(columns='is_fraud')
y = data['is_fraud']

# Apply SMOTE to handle imbalance in the dataset
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Print the number of samples in the balanced dataset
print(f"Number of samples in X_res: {X_res.shape[0]}")
print(f"Number of samples in y_res: {y_res.shape[0]}")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.25, stratify=y_res, random_state=42)
# Class distribution before splitting
train_counts = y_train.value_counts()
test_counts = y_test.value_counts()

# Print class distribution before and after split
print("Training set class distribution:")
print(train_counts)

print("\nTesting set class distribution:")
print(test_counts)

import pandas as pd
from sklearn.feature_selection import f_classif

# Apply ANOVA test
anova_scores, p_values = f_classif(X_train, y_train)

# Convert to a DataFrame for better readability
anova_scores_df = pd.DataFrame({'Feature': X.columns, 'ANOVA Score': anova_scores, 'P-Value': p_values})

# Sort by ANOVA Score in descending order
anova_scores_df = anova_scores_df.sort_values(by='ANOVA Score', ascending=False)

print(anova_scores_df)

#X_train = X_train.drop(['jundice', 'contry_of_res','used_app_before'], axis=1)
#X_test = X_test.drop(['jundice', 'contry_of_res','used_app_before'], axis=1)

"""**Hypothesis Testing: ANOVA**"""

unique_categories = len(np.unique(y_train))
print("Unique categories:", unique_categories)

"""**Feature Selection - Chi-Square Test**"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import chi2, SelectKBest

# Initialize MinMaxScaler
scaler = MinMaxScaler()

# Scale the training data
X_train_scaled = scaler.fit_transform(X_train)

# Perform Chi-Square feature selection
chi2_selector = SelectKBest(chi2, k=unique_categories - 1)
X_kbest = chi2_selector.fit_transform(X_train_scaled, y_train)

# Get the names of the selected features
selected_features = X_train.columns[chi2_selector.get_support()]

# Print the selected features
print("Selected Features using Chi-Square Test:")
for feature in selected_features:
    print(feature)

"""from sklearn.feature_selection import chi2, SelectKBest

# Perform Chi-Square feature selection
chi2_selector = SelectKBest(chi2, k=unique_categories-1)
X_kbest = chi2_selector.fit_transform(X_train, y_train)

# Get the names of the selected features
selected_features = X_train.columns[chi2_selector.get_support()]

# Print the selected features
print("Selected Features using Chi-Square Test:")
for feature in selected_features:
    print(feature)
"""

selected_features

X_train = X_train[selected_features]
X_test = X_test[selected_features]
X_train.head()

X_test.shape

X_train.shape

"""**Initial Parameter Settings for Models**"""

import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
import joblib


# Define the Decision Tree model
dt = DecisionTreeClassifier()

# Define the parameter grid
param_dist = {
    'max_depth': list(range(1, 21)),  # Max depth from 1 to 20
    'min_samples_split': list(range(2, 11)),  # Min samples to split from 2 to 10
    'min_samples_leaf': list(range(1, 11)),  # Min samples per leaf from 1 to 10
    'criterion': ['gini', 'entropy'],  # Criterion for splitting
    'max_features': ['auto', 'sqrt', 'log2', None],  # Features to consider for splits
    'ccp_alpha': [0.0, 0.0001, 0.0002, 0.001, 0.002, .99]  # Values for pruning
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(dt, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42,  verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)  # Replace 'target_column' with your target column name

# Extract the best parameters
best_params = random_search.best_params_
print(best_params)
# Initialize the Decision Tree model with the best parameters (assuming best_params is available)
best_dt = DecisionTreeClassifier(**best_params)

# Start the timer for training time
start_time = time.time()

# Train the model
best_dt.fit(X_train, y_train)
model_params = best_dt.get_params()
print("Model Parameters:", model_params)
# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_dt.predict(X_train))

# Predict on the test set
y_pred = best_dt.predict(X_test)
y_pred_proba = best_dt.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score (for binary classification, you can specify average='binary')
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC (only for binary classification)
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"
# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_dt.classes_, yticklabels=best_dt.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
print("Classification Report:")
print(class_report)

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Plot the decision tree
plt.figure(figsize=(20,10))  # Adjust the figure size as needed
plot_tree(best_dt, feature_names=X_train.columns, class_names=True, filled=True, rounded=True)
plt.show()
# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained SVC model
joblib.dump(best_dt, 'dt_model.pkl')

print("Model saved as 'dt_model.pkl'")

import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV

# Define the Random Forest model
rf = RandomForestClassifier()

# Define the parameter grid
param_dist = {
    'n_estimators': [100, 200, 300, 400, 500],  # Number of trees
    'max_depth': list(range(1, 21)),  # Max depth from 1 to 20
    'min_samples_split': list(range(2, 11)),  # Min samples to split from 2 to 10
    'min_samples_leaf': list(range(1, 11)),  # Min samples per leaf from 1 to 10
    'max_features': ['auto', 'sqrt', 'log2', None],  # Features to consider for splits
    'bootstrap': [True, False],  # Whether bootstrap samples are used when building trees
    'ccp_alpha': [0.0, 0.0001, 0.0002, 0.001, 0.002, 0.99]  # Values for pruning (if supported)
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(rf, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42, n_jobs=-1, verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)

# Extract the best parameters
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Initialize the Random Forest model with the best parameters
best_rf = RandomForestClassifier(**best_params)

# Start the timer for training time
start_time = time.time()

# Train the model
best_rf.fit(X_train, y_train)
model_params = best_rf.get_params()
print("Model Parameters:", model_params)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_rf.predict(X_train))

# Predict on the test set
y_pred = best_rf.predict(X_test)
y_pred_proba = best_rf.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC (only for binary classification)
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"
# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_rf.classes_, yticklabels=best_rf.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)
# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained SVC model
joblib.dump(best_rf, 'rf_model.pkl')

print("Model saved as 'rf_model.pkl'")

import time
import matplotlib.pyplot as plt
import seaborn as sns
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV

# Define the CatBoost model
catboost = CatBoostClassifier(learning_rate=0.1, depth=6, iterations=500, verbose=0)  # Default parameters

# Define the parameter grid
param_dist = {
    'iterations': [100, 200, 300, 400, 500],  # Number of boosting iterations
    'depth': list(range(4, 11)),  # Depth of the trees
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],  # Learning rate
    'l2_leaf_reg': [1, 3, 5, 7, 9],  # L2 regularization term
    'min_child_samples': [1, 5, 10, 20],  # Minimum number of samples in a leaf
    'border_count': [32, 50, 100]  # Number of splits for categorical features
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(catboost, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42, n_jobs=-1, verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)

# Extract the best parameters
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Initialize the CatBoost model with the best parameters
best_catboost = CatBoostClassifier(**best_params, verbose=0)

# Start the timer for training time
start_time = time.time()

# Train the model
best_catboost.fit(X_train, y_train)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_catboost.predict(X_train))

# Predict on the test set
y_pred = best_catboost.predict(X_test)
y_pred_proba = best_catboost.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC (only for binary classification)
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"
# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_catboost.classes_, yticklabels=best_catboost.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)

# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained SVC model
joblib.dump(best_catboost, 'catboost_model.pkl')
print("Model saved as 'catboost_model.pkl'")



import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.model_selection import RandomizedSearchCV
import joblib  # For saving and loading the model

# Define the SVC model
svc = SVC(probability=True, random_state=42)  # Enable probability estimates for ROC-AUC

# Define the parameter grid
param_dist = {
    'C': [0.1, 1, 10, 100, 1000],  # Regularization parameter
    'gamma': ['scale', 'auto'] + list(10.0 ** -np.arange(1, 4)),  # Kernel coefficient
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],  # Kernel type
    'degree': [2, 3, 4, 5],  # Degree for the polynomial kernel
    'class_weight': [None, 'balanced']  # Class weights
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(svc, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42, n_jobs=-1, verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)

# Extract the best parameters
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Initialize the SVC model with the best parameters
best_svc = SVC(**best_params, probability=True, random_state=42)

# Start the timer for training time
start_time = time.time()

# Train the model
best_svc.fit(X_train, y_train)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_svc.predict(X_train))

# Predict on the test set
y_pred = best_svc.predict(X_test)
y_pred_proba = best_svc.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"

# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_svc.classes_, yticklabels=best_svc.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)

# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained SVC model
joblib.dump(best_svc, 'svc_model.pkl')
print("Model saved as 'svc_model.pkl'")

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.model_selection import RandomizedSearchCV
import joblib  # For saving and loading the model

# Define the Gradient Boosting model
gbm = GradientBoostingClassifier(random_state=42)  # Default parameters

# Define the parameter grid
param_dist = {
    'n_estimators': [100, 200, 300, 400, 500],  # Number of boosting stages to be run
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],  # Step size at each iteration
    'max_depth': [3, 4, 5, 6, 7],  # Maximum depth of the individual trees
    'min_samples_split': [2, 5, 10, 20],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 5, 10],  # Minimum number of samples required to be at a leaf node
    'subsample': [0.8, 0.9, 1.0]  # Fraction of samples used for fitting the trees
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(gbm, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42, n_jobs=-1, verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)

# Extract the best parameters
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Initialize the Gradient Boosting model with the best parameters
best_gbm = GradientBoostingClassifier(**best_params, random_state=42)

# Start the timer for training time
start_time = time.time()

# Train the model
best_gbm.fit(X_train, y_train)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_gbm.predict(X_train))

# Predict on the test set
y_pred = best_gbm.predict(X_test)
y_pred_proba = best_gbm.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"

# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_gbm.classes_, yticklabels=best_gbm.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)

# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained Gradient Boosting model
joblib.dump(best_gbm, 'gbm_model.pkl')

print("Model saved as 'gbm_model.pkl'")

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.model_selection import RandomizedSearchCV
import joblib  # For saving and loading the model

# Define the Logistic Regression model
log_reg = LogisticRegression(random_state=42)  # No solver specified here, will be set in RandomizedSearchCV

# Define the parameter grid
param_dist = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Inverse of regularization strength
    'penalty': ['l1', 'l2'],  # Type of regularization
    'solver': ['liblinear', 'saga'],  # Optimization algorithm
    'max_iter': [100, 200, 300]  # Maximum number of iterations
}

# Set up the RandomizedSearchCV
random_search = RandomizedSearchCV(log_reg, param_distributions=param_dist,
                                   n_iter=100, scoring='accuracy',
                                   cv=5, random_state=42, n_jobs=-1, verbose=1)

# Fit the RandomizedSearchCV to find the best parameters
random_search.fit(X_train, y_train)

# Extract the best parameters
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Initialize the Logistic Regression model with the best parameters
best_log_reg = LogisticRegression(**best_params, random_state=42)

# Start the timer for training time
start_time = time.time()

# Train the model
best_log_reg.fit(X_train, y_train)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, best_log_reg.predict(X_train))

# Predict on the test set
y_pred = best_log_reg.predict(X_test)
y_pred_proba = best_log_reg.predict_proba(X_test)[:, 1]  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"

# Compute ROC Curve Data
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=best_log_reg.classes_, yticklabels=best_log_reg.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)

# Plot ROC Curve
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curve')
plt.legend(loc='best')
plt.show()

# Save the trained Logistic Regression model
joblib.dump(best_log_reg, 'log_reg_model.pkl')

print("Model saved as 'log_reg_model.pkl'")

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.model_selection import train_test_split
import joblib  # For saving and loading the model

# Assuming you have X_train, X_test, y_train, and y_test already defined
# If not, replace them with your actual dataset and split the data as follows:

# Define the Naive Bayes model
nb = GaussianNB()

# Start the timer for training time
start_time = time.time()

# Train the model
nb.fit(X_train, y_train)

# End the timer for training time
training_time = time.time() - start_time

# Calculate training accuracy
train_accuracy = accuracy_score(y_train, nb.predict(X_train))

# Predict on the test set
y_pred = nb.predict(X_test)
y_pred_proba = nb.predict_proba(X_test)[:, 1] if len(set(y_test)) == 2 else np.zeros_like(y_test)  # For ROC-AUC, if binary classification

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, y_pred)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# Calculate ROC-AUC (only for binary classification)
roc_auc = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) == 2 else "Not Applicable"

# Compute ROC Curve Data (only for binary classification)
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba) if len(set(y_test)) == 2 else (np.array([]), np.array([]), np.array([]))

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

# Print results
print(f"Training Time: {training_time:.4f} seconds")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc}")
print("Confusion Matrix:")

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=nb.classes_, yticklabels=nb.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(class_report)

# Plot ROC Curve (only for binary classification)
if len(set(y_test)) == 2:
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, marker='o', label='ROC Curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Curve')
    plt.legend(loc='best')
    plt.show()
else:
    print("ROC Curve not applicable for non-binary classification.")

# Save the trained Naive Bayes model
joblib.dump(nb, 'naive_bayes_model.pkl')

print("Model saved as 'naive_bayes_model.pkl'")