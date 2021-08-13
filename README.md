# MaliciousPowershell
This project was sponsored by the Joint Artificial Intelligence Center, in order to provide a method to predict whether or not a certain Powershell script is obfuscated. The project as it stands now is largely split into two parts: a parser and a series of machine learning models. 

The machine learning models are written in Python, and are largely dependent on the scikit-learn library in order to sustain their functionality. The models included here are a logistic regression (lr.py), a support vector machine (svm.py), a BaggingClassifier/DecisionTree (bdt.py), and a neural network (nn.py). In the near future, all of these models will get remade using SMOTE, a dataset balancing tool available in Python's imbalanced-learn library that should make the outcome more relevant.

The parser...
