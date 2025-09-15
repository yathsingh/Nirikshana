**Nirikshana End to End Water Monitoring System**

TO RUN, OPEN TERMINAL AND ENTER: 
1. python simulate_live.py
2. uvicorn app:app --reload
3. add /dashboard at the end of the link

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

<p style="display: flex; gap: 40px; justify-content: center;">
  <img src="images/hw_rough_sketch.jpeg" alt="Nirikshana hardware sketch" height="300" style="width: auto;" />
  <img src="images/unit_dist_sketch.jpeg" alt="Nirikshana distribution sketch" height="300" style="width: auto;" />
</p>

*Hardware mock-up:*

<p style="display: flex; gap: 40px; justify-content: center;">
  <img src="images/hw_proto_rough.jpeg" alt="hw proto" height="300" style="width: auto;" />
  <img src="images/hw_proto_rough_inside.jpeg" alt="hw proto inside" height="300" style="width: auto;" />
</p>

<br>

**Machine Learning Model**

Currently Used: Random Forest with 'max_depth': None, 'min_samples_split': 2, 'n_estimators': 500 (Model .pkl file is available at *backend/models*)

Planned: XGBoost -> Custom deep learning pipeline

Originally trained synthetic data in Google Colab, then downloaded using joblib (Synthetic data .csv file is available at *backend/models*)

*Model performance metrics:*

<p style="display: flex; gap: 40px; justify-content: center;">
  <img src="images/rf_cf.png" alt="cf" height="300" style="width: auto;" />
  <img src="images/rf_imp.png" alt="imp" height="300" style="width: auto;" />
</p>

<br>

**Backend**

FastAPI enables creation of multiple API endpoints, interacting with an SQLLite database to ensure a simple yet effective prototype design.

*seed.py* generates mock historic data, while *simulate_live.py* inputs live data at intervals to simulate the real pipeline.

<br>

**Dashboard**

Utilises HTML, CSS, Javascript, Chart.js to create an interactive viewer experience

<p style="display: flex; gap: 40px; justify-content: center;">
  <img src="images/niri_dash_1.png" alt="cf" height="300" style="width: auto;" />
  <img src="images/niri_dash_3.png" alt="imp" height="300" style="width: auto;" />
</p>
