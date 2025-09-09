# Satellite Clustering and Anomaly Detection



This project applies **unsupervised machine learning** and **orbital mechanics** to cluster satellites into orbital regimes (**LEO, MEO, GEO**) and detect anomalies such as **debris, rocket bodies, and unusual satellites**.



It was developed as part of a **Women in Data Space-Aware Datathon** to demonstrate how **data science + physics** can support **Space Situational Awareness (SSA)**.



## Pipeline



**TLE → sgp4 Feature Extraction → Scaling → DBSCAN Clustering → Orbit Type Mapping → IsolationForest Anomaly Detection → Outputs (CSVs + Plots)**



- Extract orbital parameters (Inclination, Eccentricity, Mean Motion) from TLE using **sgp4**

- Scale features and cluster satellites using **DBSCAN**

- Map clusters to **LEO / MEO / GEO** regimes

- Apply **IsolationForest** to detect anomalies within each cluster

- Generate metrics, plots, and anomaly statistics



## Project Structure



datathon-project/

│

├── src/

│ └── satellite_clustering_anomaly_pipeline.py

│

├── data/

│ └── satellite_data.json

│

├── results/

│ ├── AnomalyRate_by_ObjectType.csv

│ ├── Cluster_Contamination_Rates.csv

│ ├── Cluster_Interpretations.csv

│ ├── DBSCAN_Clustering_Metrics.csv

│ ├── Flagged_Anomalies.csv

│ ├── SatelliteClusters_Before_AnomalyDetection.csv

│ ├── DBSCAN_Clustering.png

│ ├── DBSCAN_Clustering_OrbitType.png

│ ├── DBSCAN_IsolationForest_Anomalies.png

│ └── DBSCAN_IsolationForest_Anomalies_Clean.png

│

├── docs/

│ ├── Satellite_Clustering_and_Anomaly_Detection.docx

│

├── notebooks/

│ └── EDA.ipynb

│

├── README.md

└── requirements.txt



## Documentation



For the detailed methodology, results, and interpretation, see the full report:



[docs/Satellite_Clustering_and_Anomaly_Detection.docx](https://github.com/OrbitGuardians-Datathon/OrbitGuardians_Datathon_WID_2025/tree/main/datathon-project/docs)



## Highlights



- **Physics-grounded features**: Inclination, eccentricity, mean motion (from sgp4)  

- **DBSCAN clustering**: Natural grouping into orbital regimes  

- **IsolationForest anomalies**: Detects debris, rocket bodies, unusual satellites  

- **Actionable insights**: Supports space traffic management and collision risk assessment





