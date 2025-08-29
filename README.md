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
     


     ## Global Risk prediction view via interactive world map:
     

---

## 📊 Example Prediction (India)

- **Predicted Frequent Disasters**: Floods, Earthquakes, Cyclones  
- **Probabilities**: Floods (72%), Earthquakes (18%), Cyclones (10%)  
- **Z-scores**: Floods (2.1 → Extreme Danger), Earthquakes (0.7 → Moderate), Cyclones (-0.3 → Low)  
- **Risk Summary**: Floods are the highest-risk disaster for India.  
---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/disaster-prediction.git
cd disaster-prediction


## 



