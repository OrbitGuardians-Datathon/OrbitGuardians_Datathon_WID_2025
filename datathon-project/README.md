# Satellite Clustering and Anomaly Detection



This project applies **unsupervised machine learning** and **orbital mechanics** to cluster satellites into orbital regimes (**LEO, MEO, GEO**) and detect anomalies such as **debris, rocket bodies, and unusual satellites**.



It was developed as part of a **Women in Data Space-Aware Datathon** to demonstrate how **data science + physics** can support **Space Situational Awareness (SSA)**.



## Pipeline



**TLE → sgp4 Feature Extraction → Scaling → DBSCAN Clustering → Orbit Type Mapping → IsolationForest Anomaly Detection → Outputs (CSVs + Plots)**



* Extract orbital parameters (Inclination, Eccentricity, Mean Motion) from TLE using **sgp4**
* Scale features and cluster satellites using **DBSCAN**
* Map clusters to **LEO / MEO / GEO** regimes
* Apply **IsolationForest** to detect anomalies within each cluster
* Produce plots, CSVs, and summaries to interpret clustering and anomaly detection results



## Project Structure



datathon-project/

│

├── src/

│ └── [satellite_clustering_anomaly_pipeline.py](src/satellite_clustering_anomaly_pipeline.py)

│

├── data/

│ └── [satellite_data.json](data/satellite_data.json)

│

├── results/

│ ├── [DBSCAN_Clustering_Metrics.csv](results/DBSCAN_Clustering_Metrics.csv)

│ ├── [DBSCAN_Clustering.png](results/DBSCAN_Clustering.png)

│ ├── [Cluster_Interpretations.csv](results/Cluster_Interpretations.csv)

│ ├── [SatelliteClusters_Before_AnomalyDetection.csv](results/SatelliteClusters_Before_AnomalyDetection.csv)

│ ├── [DBSCAN_Clustering_OrbitType.png](results/DBSCAN_Clustering_OrbitType.png)

│ ├── [Flagged_Anomalies.csv](results/Flagged_Anomalies.csv)

│ ├── [DBSCAN_IsolationForest_Anomalies.png](results/DBSCAN_IsolationForest_Anomalies.png)

│ ├── [DBSCAN_IsolationForest_Anomalies_Clean.png](results/DBSCAN_IsolationForest_Anomalies_Clean.png)

│ ├── [AnomalyRate_by_ObjectType.csv](results/AnomalyRate_by_ObjectType.csv)

│ └── [Cluster_Contamination_Rates.csv](results/Cluster_Contamination_Rates.csv)

│

├── docs/

│ ├── [Satellite_Clustering_and_Anomaly_Detection.pdf](docs/Satellite%20Clustering%20and%20Anomaly%20Detection.pdf)

│

├── notebooks/

│ └── [EDA.ipynb](notebooks/EDA.ipynb)

│

├── [README.md](README.md)

└── [requirements.txt](requirements.txt)



## Documentation



For the detailed methodology, results, and interpretation, see the full report:



[docs/Satellite_Clustering_and_Anomaly_Detection.pdf](docs/Satellite%20Clustering%20and%20Anomaly%20Detection.pdf)



## Highlights



* **Physics-grounded features**: Inclination, eccentricity, mean motion (from sgp4)
* **DBSCAN clustering**: Natural grouping into orbital regimes
* **IsolationForest anomalies**: Detects debris, rocket bodies, unusual satellites
* **Actionable insights**: Supports space traffic management and collision risk assessment
