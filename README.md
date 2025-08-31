#  Disaster Risk Prediction Web App

This project is a **Django-based web application** that predicts and visualizes disaster risks for different countries.  
It uses past disaster data and a **Multinomial Logistic Regression model** to identify the probability and risk level of different disaster types. 
This project is developed as part of my **Engineering Clinics (Semester 5)** coursework.
## Features :
-  **Disaster risk prediction** using Multinomial Logistic Regression  
-  **Country-wise risk breakdown** with probabilities and Z-scores  
- **Risk categorization** into Safe, Low, Moderate, Danger, and Extreme Danger  
- **Interactive pie charts** using Plotly for disaster type distribution  
- **Explain Graph** button for easy interpretation of results  
-  **Dropdown with aliases** to avoid invalid user input (e.g., "US" → "United States of America","Russian Federation ": Russia,"United Kingdom of Ireland and Britain":UK)  
-  **Tabular summary** of predicted disasters with frequency, probability, Z-score, and risk level  

## Project Structure:
This is important to implement the Django :
<img width="758" height="353" alt="image" src="https://github.com/user-attachments/assets/13e70eba-580a-444c-b803-5819126ef7f0" />

---

## Working of the website:

1. User selects a **country** from the dropdown (aliases supported).  
2. Data from `Disaster_Zones.csv` is retrieved for that country.  
3. The **Multinomial Logistic Regression model (`danger_zone_model.pkl`)** predicts disaster risk categories.  
4. A statistical **Z-score** is also computed to normalize disaster frequency.  
5. Each disaster is assigned a **Risk Level**:
   - Safe (≤ -0.5)
   - Low (≤ 0.5)
   - Moderate (≤ 1.0)
   - Danger (≤ 2.0)
   - Extreme Danger (> 2.0)
6. Results are displayed as:
    ## Country wise analysis
   - Prediction table (disaster type, probability, Z-score, risk level)  
   - Interactive pie chart of predicted disaster distribution  
   -  Explanation of the graph using gemini AI :
     <img width="1577" height="784" alt="image" src="https://github.com/user-attachments/assets/53c4474f-4f39-45e8-9fba-b26a98744a81" />
     <img width="1471" height="621" alt="image" src="https://github.com/user-attachments/assets/9c198280-7b7c-42de-91bb-94e9531d8053" />
     <img width="1443" height="256" alt="image" src="https://github.com/user-attachments/assets/35a7a6dd-00f5-4377-a623-d15f5475009b" />

     ## Global Risk prediction view via interactive world map:
   <img width="1919" height="836" alt="image" src="https://github.com/user-attachments/assets/30da344e-913a-4f0b-a94f-cd269f6fe5fb" />

---

## 📊 Example Prediction (India)

- **Predicted Frequent Disasters**: Floods, Earthquakes, Cyclones  
- **Probabilities**: Floods (72%), Earthquakes (18%), Cyclones (10%)  
- **Z-scores**: Floods (2.1 → Extreme Danger), Earthquakes (0.7 → Moderate), Cyclones (-0.3 → Low)  
- **Risk Summary**: Floods are the highest-risk disaster for India.  
---
---

## ⚙️ Setup

1. Create a virtual environment and activate it.  
2. Install the required Python libraries using `pip install -r requirements.txt`.  
3. Place the dataset file **`Disaster_Zones.csv`** in the project directory.  
4. Place the trained model file **`danger_zone_model.pkl`** in the same directory.  
5. Run database migrations with `python manage.py migrate`.  
6. Start the Django development server using `python manage.py runserver` in command prompt.  
7. Open the web application in your browser by the local link generated in the commandprompt.  

---

## Requirements

- Python 3.9 or higher  
- Django (web framework)  
- Pandas (data processing)  
- Plotly (visualizations)  
- Scikit-learn (Multinomial Logistic Regression model)  
- Joblib (model persistence/loading)  
---Gemini API key(for explaining predicted  graph and table in country analysis)
---

##  Sources

- [EM-DAT: The International Disaster Database](https://www.emdat.be/) – Historical disaster occurrence data.  
- [Kaggle Datasets](https://www.kaggle.com/) – Supplementary disaster datasets for training and validation.  
- [Scikit-learn Documentation](https://scikit-learn.org/stable/) – Multinomial Logistic Regression and model utilities.  
- [Django Documentation](https://docs.djangoproject.com/) – Web framework reference.  
- [Plotly Documentation](https://plotly.com/python/) – Interactive data visualization.  
- [Pandas Documentation](https://pandas.pydata.org/docs/) – Data analysis and preprocessing.  

---



