**Nirikshana End to End Water Monitoring System (Prototype 1)**

Nirikshana utilises a robust hardware device to collect and wirelessly transmit water-quality data using numerous sensors (pH, turbidity, tds, water flow). 
The data is then sent to the backend where it is passed through an ML pipeline to predict water safety, and the finalised data is sent to an interative dashboard 
where one can see alerts, statistics and recently collected data to get an extensive overview. 

<p align="center">
  <img src="images/Nirikshana.png" alt="Nirikshana logo" height="300" width="auto" />
</p>


**Hardware**

Shell material: Plant-based bioplastic (WIP)

Energy system: Solar power (WIP)

Sensors: pH, Turbidity, TDS, Water flow

Prototype Brain: Arduino UNO

*Rough Sketches:*

<p>
  <img src="images/hw_rough_sketch.jpeg" alt="Nirikshana hardware sketch" height="300" width="auto" />
</p>
<p>
  <img src="images/unit_dist_sketch.jpeg" alt="Nirikshana distribution sketch" height="300" width="auto" />
</p>

<br>

**Machine Learning Model**

Currently Used: Random Forest with 'max_depth': None, 'min_samples_split': 2, 'n_estimators': 500 (Available in *models* folder)

Planned: XGBoost -> Custom deep learning pipeline

Originally trained in Google Colab, then downloaded using joblib.

<br>

**Backend**

FastAPI enables creation of multiple API endpoints, interacting with an SQLLite database to ensure a simple yet effective prototype design

<br>

**Dashboard**

Utilises HTML, CSS, Javascript, Chart.js to create an interactive viewer experience

