\# Satellite Clustering and Anomaly Detection



This project applies \*\*unsupervised machine learning\*\* and \*\*orbital mechanics\*\* to cluster satellites into orbital regimes (\*\*LEO, MEO, GEO\*\*) and detect anomalies such as \*\*debris, rocket bodies, and unusual satellites\*\*.



It was developed as part of a \*\*Women in Data Space-Aware Datathon\*\* to demonstrate how \*\*data science + physics\*\* can support \*\*Space Situational Awareness (SSA)\*\*.



\## Pipeline



\*\*TLE → sgp4 Feature Extraction → Scaling → DBSCAN Clustering → Orbit Type Mapping → IsolationForest Anomaly Detection → Outputs (CSVs + Plots)\*\*



\- Extract orbital parameters (Inclination, Eccentricity, Mean Motion) from TLE using \*\*sgp4\*\*

\- Scale features and cluster satellites using \*\*DBSCAN\*\*

\- Map clusters to \*\*LEO / MEO / GEO\*\* regimes

\- Apply \*\*IsolationForest\*\* to detect anomalies within each cluster

\- Generate metrics, plots, and anomaly statistics



\## Project Structure



datathon-project/

│

├── src/

│ └── satellite\_clustering\_anomaly\_pipeline.py

│

├── data/

│ └── satellite\_data.json

│

├── results/

│ ├── AnomalyRate\_by\_ObjectType.csv

│ ├── Cluster\_Contamination\_Rates.csv

│ ├── Cluster\_Interpretations.csv

│ ├── DBSCAN\_Clustering\_Metrics.csv

│ ├── Flagged\_Anomalies.csv

│ ├── SatelliteClusters\_Before\_AnomalyDetection.csv

│ ├── DBSCAN\_Clustering.png

│ ├── DBSCAN\_Clustering\_OrbitType.png

│ ├── DBSCAN\_IsolationForest\_Anomalies.png

│ └── DBSCAN\_IsolationForest\_Anomalies\_Clean.png

│

├── docs/

│ ├── Satellite\_Clustering\_and\_Anomaly\_Detection.docx

│

├── notebooks/

│ └── EDA.ipynb

│

├── README.md

└── requirements.txt



\## Documentation



For the detailed methodology, results, and interpretation, see the full report:



\[`docs/Satellite\_Clustering\_and\_Anomaly\_Detection.docx`](docs/Satellite\_Clustering\_and\_Anomaly\_Detection.docx)



\## Highlights



\- \*\*Physics-grounded features\*\*: Inclination, eccentricity, mean motion (from sgp4)  

\- \*\*DBSCAN clustering\*\*: Natural grouping into orbital regimes  

\- \*\*IsolationForest anomalies\*\*: Detects debris, rocket bodies, unusual satellites  

\- \*\*Actionable insights\*\*: Supports space traffic management and collision risk assessment





