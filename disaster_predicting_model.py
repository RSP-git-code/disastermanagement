import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
#Returns vector numeric which helps the hardware to detect if the region lies in danger zone or not
from sklearn.preprocessing import OneHotEncoder,StandardScaler
#helps in keeping preprocessing model together so that i can integrate it in django later on
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
df=pd.read_csv("Disaster_Zones.csv")
df=df.dropna()
print(df.head())
#Features of the model:
# Log-transform skewed features
df["Economic_Loss($)"] = np.log1p(df["Economic_Loss($)"])
df["Fatalities"] = np.log1p(df["Fatalities"])

# Keep Danger_Score as float
df["Danger_Score"] = pd.to_numeric(df["Danger_Score"], errors="coerce").fillna(0)
X=df[['Disaster_Type','Location','Magnitude','Fatalities','Economic_Loss($)','Danger_Score']]
Y=df[['Zone_Category']]
df["Danger_Score"] = pd.to_numeric(df["Danger_Score"], errors="coerce").fillna(0).astype(int)
preprocessor=ColumnTransformer(
    transformers=[
        ('preprocess',OneHotEncoder(handle_unknown='ignore'),['Disaster_Type','Location']),
        ('step',StandardScaler(),['Magnitude','Fatalities','Economic_Loss($)'])
    ]
)
#Creating a Multinomial LR classification model
model=Pipeline(steps=[
    ('preprocessor',preprocessor),
    ('classifier',LogisticRegression(solver='lbfgs',max_iter=1000,class_weight='balanced'))
])
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)
model.fit(X_train,Y_train)
y_pred=model.predict(X_test)
print(f"Accuracy :{accuracy_score(Y_test,y_pred )}")
print(f"Classification report:\n{classification_report(Y_test,y_pred)}")
print(f"Confusion matrix:\n:{confusion_matrix(Y_test,y_pred)}")
#For integrating this model later in django
joblib.dump(model, "danger_zone_model.pkl")
print("Model saved as danger_zone_model.pkl")
