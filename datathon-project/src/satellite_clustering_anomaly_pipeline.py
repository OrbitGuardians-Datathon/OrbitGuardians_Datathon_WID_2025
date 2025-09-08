# satellite_clustering_anomaly_pipeline by Nisrin Dhoondia

# Import necessary libraries
import json
import math
import pandas as pd
import matplotlib.pyplot as plt
# SGP4 (Simplified General Perturbations 4) is a python library that implements SGP4 orbital model
from sgp4.api import Satrec
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Load dataset & extract features from TLEs

with open("satellite_data.json", "r") as f:
    raw = json.load(f)

rows = []
for obj in raw:
    tle = obj.get("TLE_DATA")
    if not tle or not tle.get("TLE_LINE1") or not tle.get("TLE_LINE2"):
        continue
    try:
        satellite = Satrec.twoline2rv(tle["TLE_LINE1"], tle["TLE_LINE2"])
        # Satellites in orbit are tracked using TLE (Two-Line Element) data
        # Satrec (Satellite Record) module helps to parse TLE lines
        # into a satellite object and extract orbital parameters.
        # Extract orbital features
        # print("Inclination (deg):", satellite.inclo)
        # print("Eccentricity:", satellite.ecco)
        # print("RAAN (Right Ascension of Ascending Node):", satellite.nodeo)
        # print("Argument of Perigee:", satellite.argpo)
        # print("Mean Anomaly:", satellite.mo)
        # print("Mean Motion:", satellite.no_kozai)
        rows.append({
            "OBJECT_NAME": obj.get("OBJECT_NAME", "UNKNOWN"),
            "NORAD_CAT_ID": obj.get("NORAD_CAT_ID", ""),
            "COUNTRY": obj.get("COUNTRY", ""),
            "LAUNCH_DATE": obj.get("LAUNCH_DATE", ""),
            # use numeric orbital parameters from the parsed TLE
            "inclination": float(satellite.inclo),      # degrees
            "eccentricity": float(satellite.ecco),      # unitless
            # "raan": float(satellite.nodeo),             # degrees
            # "arg_perigee": float(satellite.argpo),      # degrees
            # "mean_anomaly": float(satellite.mo),        # degrees
            # satellite.no_kozai → radians / minute
            # * 1440 → radians / day
            # / (2π) → revolutions / day
            "mean_motion": float(satellite.no_kozai) * 1440.0 / (2 * math.pi)
        })
    except Exception as e:
        # skip problematic TLEs
        continue

df = pd.DataFrame(rows)
if df.empty:
    raise SystemExit("No valid TLEs parsed. Check satellite_data.json and sgp4 installation.")
else:
    print(df)
    print("\n")

# Feature matrix (for clustering) and scaling
print("mean_motion:", df["mean_motion"].describe())

# feature_cols = ["inclination", "eccentricity", "raan", "arg_perigee", "mean_anomaly", "mean_motion"]
feature_cols = ["inclination", "eccentricity", "mean_motion"]
X = df[feature_cols].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# DBSCAN clustering

# eps (epsilon) and min_samples are reasonable starting values for scaled data.
db = DBSCAN(eps=0.6, min_samples=50, n_jobs=-1)
labels = db.fit_predict(X_scaled)
df["cluster"] = labels  # -1 = noise

# Evaluate clustering (excluding DBSCAN noise points -1 when computing metrics)
mask = labels != -1 # exclude noise/outlier
# checking if equal or more than 2 points are clustered after excluding the mask,
# cannot compute metrics like silhouette (they need at least 2 samples).
if mask.sum() >= 2 and len(set(labels[mask])) > 1:
    # Silhouette Score Range: -1 to 1
    # Closer to 1 = well - separated clusters
    # Around 0 = overlapping clusters
    # Negative = misclassified
    sil = silhouette_score(X_scaled[mask], labels[mask])
    # Davies-Bouldin Index (DBI) Lower is better
    # Measures average similarity between clusters (compactness + separation)
    dbi = davies_bouldin_score(X_scaled[mask], labels[mask])
    # Calinski - Harabasz Index(CH) Higher is better
    # Ratio of between-cluster dispersion to within-cluster dispersion
    ch = calinski_harabasz_score(X_scaled[mask], labels[mask])
else:
    sil, dbi, ch = None, None, None

print("DBSCAN Clustering Metrics")
print(f"Silhouette Score: {sil}")
print(f"Davies-Bouldin Index: {dbi}")
print(f"Calinski-Harabasz Index: {ch}")
print("Cluster counts (including -1 = noise):")
print(df["cluster"].value_counts())
print("\n")

# Save DBSCAN clustering metrics to CSV
cluster_counts = df["cluster"].value_counts().to_dict()

metrics_dict = {
    "Silhouette Score": [sil],
    "Davies-Bouldin Index": [dbi],
    "Calinski-Harabasz Index": [ch],
    "Cluster Counts": [cluster_counts]  # store counts as dict
}

metrics_df = pd.DataFrame(metrics_dict)
metrics_df.to_csv("DBSCAN_Clustering_Metrics.csv", index=False)
print("DBSCAN clustering metrics saved to DBSCAN_Clustering_Metrics.csv. \n")


plt.figure(figsize=(10,6))
scatter = plt.scatter(df["inclination"], df["mean_motion"],
                      c=df["cluster"], cmap="tab10", s=50, alpha=0.7)

plt.xlabel("Inclination (deg)")
plt.ylabel("Mean Motion (rev/day)")
plt.title("DBSCAN Clustering Output (Noise = -1)")
plt.colorbar(scatter, label="Cluster ID")
plt.grid(True, alpha=0.3)
plt.savefig("DBSCAN_Clustering.png", dpi=150)
plt.show()

# Assigning clusters to orbit types (LEO / MEO / GEO)
#
# Satellites can be grouped by how many times they go around Earth per day,
# which is called "mean motion":
#
# - Low Earth Orbit (LEO): 12 or more orbits per day (fast, close to Earth)
# - Medium Earth Orbit (MEO): between 2 and 12 orbits per day
# - Geostationary Orbit (GEO): about 1 orbit per day (appears fixed above Earth)
#
# simple rules to label each cluster as LEO, MEO, or GEO.

cluster_means = df.groupby("cluster")["mean_motion"].mean().to_dict()

def map_mean_motion_to_orbit(mm):
    # mm = mean motion in rev/day
    if mm is None or math.isnan(mm):
        return "Unclassified"
    if mm > 12.0:
        return "LEO"
    elif 2.0 < mm <= 12.0:
        return "MEO"
    elif abs(mm - 1.0) < 0.2:  # GEO ~1 rev/day
        return "GEO"
    else:
        return "Unclassified"

# Map each cluster to an orbit type and attach that mapping to dataframe
cluster_orbit_type = {}
for c, mm in cluster_means.items():
    orbit_type = map_mean_motion_to_orbit(mm)
    cluster_orbit_type[c] = {"mean_motion_mean": mm, "orbit_type": orbit_type}
    print(f"\nCluster {c}: orbit_type={orbit_type} (cluster mean mean_motion = {mm:.3f})\n")

print(cluster_orbit_type)
print("\n")
print("cluster_means:", cluster_means)
print("\n")
print("Cluster Interpretations")

interpretation_rows = []
for c, vals in cluster_orbit_type.items():
    orbit_type = vals["orbit_type"]
    mean_motion = vals["mean_motion_mean"]

    if orbit_type == "LEO":
        comment = "Low Earth Orbit (LEO): Fast orbits, typically debris or small satellites (close to Earth)."
    elif orbit_type == "MEO":
        comment = "Medium Earth Orbit (MEO): Medium-altitude, often navigation satellites like GPS/BeiDou."
    elif orbit_type == "GEO":
        comment = "Geostationary Orbit (GEO): Communication/TV satellites, appear fixed above Earth."
    else:
        comment = "Does not match typical orbital regimes (possibly Unclassified)."

    print(f"Cluster {c}: {orbit_type} "
          f"(avg mean_motion={mean_motion:.2f} rev/day) → {comment}")

    # Save structured info for CSV
    interpretation_rows.append({
        "cluster": c,
        "orbit_type": orbit_type,
        "mean_motion_avg": mean_motion,
        "comment": comment
    })

print("\n")

# Convert to DataFrame and save
interpret_df = pd.DataFrame(interpretation_rows)
interpret_df.to_csv("Cluster_Interpretations.csv", index=False)
print("Cluster interpretations saved to Cluster_Interpretations.csv. \n")

# create a new DataFrame (copy) with orbit type
df_clusters = df.copy()
df_clusters["cluster_mean_motion"] = df_clusters["cluster"].map(lambda c: cluster_orbit_type.get(c, {}).get("mean_motion_mean"))
df_clusters["orbit_type"] = df_clusters["cluster"].map(lambda c: cluster_orbit_type.get(c, {}).get("orbit_type", "Unclassified"))

# Plot clusters with orbit types
plt.figure(figsize=(10,6))
scatter = plt.scatter(df_clusters["inclination"], df_clusters["mean_motion"],
                      c=df_clusters["cluster"], cmap="tab10", s=50, alpha=0.7)
plt.xlabel("Inclination (deg)")
plt.ylabel("Mean Motion (rev/day)")
plt.title("DBSCAN Clustering with Orbit Type Labels")
plt.colorbar(scatter, label="Cluster ID")
plt.grid(True, alpha=0.3)
# Annotate cluster orbit types at cluster centroids
for c, vals in cluster_orbit_type.items():
    subset = df_clusters[df_clusters["cluster"] == c]
    if len(subset) > 0:
        cx = subset["inclination"].mean()
        cy = subset["mean_motion"].mean()
        plt.text(cx, cy, vals["orbit_type"], fontsize=10, weight="bold",
                 ha="center", va="center", bbox=dict(facecolor="white", alpha=0.6))
plt.savefig("DBSCAN_Clustering_OrbitType.png", dpi=150)
plt.show()
print("\n")
# Save intermediate clusters file
df_clusters.to_csv("SatelliteClusters_Before_AnomalyDetection.csv", index=False)

# IsolationForest anomaly detection inside each non-noise cluster
# By default, keeping every satellite is 1 (normal)
# If IsolationForest flags it, then it will be change to -1 (anomaly).
df_clusters["anomaly"] = 1  # 1 is normal, -1 is anomaly

# store per-cluster anomaly scores and details
anomaly_rows = []
for c in sorted(df_clusters["cluster"].unique()):
    if c == -1:
        # skip DBSCAN noise; those are already outliers for DBSCAN
        continue
    cluster_df = df_clusters[df_clusters["cluster"] == c]
    if len(cluster_df) < 10:
        # not enough points to train a reliable IsolationForest
        continue

    iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=42, n_jobs=-1)
    iso_preds = iso.fit_predict(cluster_df[feature_cols])
    # attach predictions
    df_clusters.loc[cluster_df.index, "anomaly"] = iso_preds

    # collect flagged rows for reporting
    flagged = cluster_df[iso_preds == -1]
    for idx, row in flagged.iterrows():
        # Build a concise, data-driven explanation (no hallucination)
        name = row["OBJECT_NAME"]
        nid = row["NORAD_CAT_ID"]
        orbit_type = row["orbit_type"]
        incl = row["inclination"]
        mm = row["mean_motion"]
        country = row.get("COUNTRY", "Unknown"),
        cluster_mm = cluster_orbit_type[c]["mean_motion_mean"]
        # rule-based textual tagging based on name strings
        if "DEB" in str(name).upper():
            reason_short = "unusual orbital drift within its group (debris)."
        elif "R/B" in str(name).upper() or "ROCKET" in str(name).upper():
            reason_short = "might be tumbling or decaying (rocket body)."
        else:
            reason_short = "not moving like its neighbors (active satellite)."

        # Compose a careful, data-backed message
        diff_from_cluster_mean = mm - cluster_mm if not pd.isna(cluster_mm) else None
        explanation = (f"{name} (NORAD {nid}) in Cluster {c} [{orbit_type}] : reason is {reason_short} "
                       f"inclination={incl:.3f} deg, mean_motion={mm:.3f} rev/day, "
                       f"cluster_mean_mean_motion={cluster_mm:.3f}, diff={diff_from_cluster_mean:.3f}")
        anomaly_rows.append({
            "OBJECT_NAME": name,
            "NORAD_CAT_ID": nid,
            "COUNTRY": row.get("COUNTRY", "Unknown"),
            "cluster": c,
            "orbit_type": orbit_type,
            "inclination": incl,
            "mean_motion": mm,
            "cluster_mean_motion": cluster_mm,
            "diff_from_cluster_mean": diff_from_cluster_mean,
            "explanation": explanation
        })

# Build flagged anomalies DataFrame and save
flagged_df = pd.DataFrame(anomaly_rows)
flagged_df.to_csv("Flagged_Anomalies.csv", index=False)

# Anomaly rate by object type
def classify_object_type(name):
    """Classify object based on its name (DEB = debris, R/B = rocket body, else satellite)."""
    name = str(name).upper()
    if "DEB" in name:
        return "Debris"
    elif "R/B" in name or "ROCKET" in name:
        return "Rocket Body"
    else:
        return "Satellite"

df_clusters["object_type"] = df_clusters["OBJECT_NAME"].apply(classify_object_type)

# Count anomalies per object type
# debris, rockets, or satellites are behaving unusually
anomaly_by_type = (
    df_clusters[df_clusters["anomaly"] == -1]
    .groupby("object_type")
    .size()
    .reset_index(name="anomaly_count")
)

# Add total objects of each type
total_by_type = df_clusters.groupby("object_type").size().reset_index(name="total_count")
anomaly_rate_by_type = pd.merge(anomaly_by_type, total_by_type, on="object_type", how="outer").fillna(0)
anomaly_rate_by_type["anomaly_rate_percent"] = (
    anomaly_rate_by_type["anomaly_count"] / anomaly_rate_by_type["total_count"] * 100
)

anomaly_rate_by_type.to_csv("AnomalyRate_by_ObjectType.csv", index=False)
print("Anomaly rate by object type saved to AnomalyRate_by_ObjectType.csv")

# Cluster-specific contamination rates
# certain orbital groups (DBSCAN clusters) have higher instability.
cluster_anomaly_counts = (
    df_clusters.groupby("cluster")["anomaly"]
    .apply(lambda x: (x == -1).sum())  # anomalies per cluster
    .reset_index(name="anomaly_count")
)

cluster_total_counts = (
    df_clusters.groupby("cluster")["anomaly"]
    .size()
    .reset_index(name="total_count")
)

cluster_rates = pd.merge(cluster_anomaly_counts, cluster_total_counts, on="cluster", how="outer").fillna(0)
cluster_rates["contamination_rate_percent"] = (
    cluster_rates["anomaly_count"] / cluster_rates["total_count"] * 100
)

cluster_rates.to_csv("Cluster_Contamination_Rates.csv", index=False)
print("Cluster-specific contamination rates saved to Cluster_Contamination_Rates.csv")

# Output summary to console for quick inspection
print("Summary")
print(f"Total objects parsed: {len(df)}")
print("Clusters and orbit types (sample):")
for c, info in cluster_orbit_type.items():
    print(f"  Cluster {c}: orbit_type={info['orbit_type']}, mean_mean_motion={info['mean_motion_mean']:.3f}")
print("\n")
print(f"Total anomalies flagged by IsolationForest (inside clusters): {len(flagged_df)}")
if not flagged_df.empty:
    print("\nSample flagged anomalies (from dataset -> factual):")
    for i, r in flagged_df.head(10).iterrows():
        print(" -", r["explanation"])
print("\n")

# Plot: Inclination vs Mean Motion, clusters colored, anomalies marked
# Prepare plotting colors per cluster (map orbit types to colors for clarity)
orbit_color_map = {"LEO": "tab:blue", "MEO": "tab:orange", "GEO": "tab:green", "Unclassified": "tab:gray"}
unique_clusters = sorted(df_clusters["cluster"].unique())
cluster_to_color = {c: orbit_color_map.get(cluster_orbit_type.get(c, {}).get("orbit_type","Unclassified"), "tab:gray")
                    for c in unique_clusters}

plt.figure(figsize=(12,7))
for c in unique_clusters:
    subset = df_clusters[df_clusters["cluster"] == c]
    plt.scatter(subset["inclination"], subset["mean_motion"],
                c=cluster_to_color.get(c, "tab:gray"),
                s=40, label=f"Cluster {c} ({cluster_orbit_type.get(c, {}).get('orbit_type','?')})",
                alpha=0.6, edgecolor='k', linewidth=0.2)

# Plot DBSCAN noise (-1) separately in black with lower alpha
if -1 in unique_clusters:
    noise = df_clusters[df_clusters["cluster"] == -1]
    plt.scatter(noise["inclination"], noise["mean_motion"], c="black", s=30, label="DBSCAN noise (-1)", alpha=0.5)

# Overplot anomalies with red X marker
if not flagged_df.empty:
    plt.scatter(flagged_df["inclination"], flagged_df["mean_motion"], c="red", marker="x", s=90, label="IsolationForest anomaly", linewidths=2)

plt.xlabel("Inclination (deg) — angle of orbit relative to Earth's equator")
plt.ylabel("Mean Motion (rev/day) — how many orbits per day (higher is lower altitude)")
plt.title("Satellite Clusters (DBSCAN) with IsolationForest Anomalies Highlighted")
plt.legend(loc="best", fontsize="small", ncol=2)
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("DBSCAN_IsolationForest_Anomalies.png", dpi=150)
plt.show()

plt.figure(figsize=(12,7))
for c in unique_clusters:
    if c == -1:
        continue  # skip DBSCAN noise
    subset = df_clusters[df_clusters["cluster"] == c]
    plt.scatter(subset["inclination"], subset["mean_motion"],
                c=cluster_to_color.get(c, "tab:gray"),
                s=40, label=f"Cluster {c} ({cluster_orbit_type.get(c, {}).get('orbit_type','?')})",
                alpha=0.6, edgecolor='k', linewidth=0.2)

# Overplot anomalies with red X marker
if not flagged_df.empty:
    plt.scatter(flagged_df["inclination"], flagged_df["mean_motion"],
                c="red", marker="x", s=90, label="IsolationForest anomaly", linewidths=2)

plt.xlabel("Inclination (deg) — angle of orbit relative to Earth's equator")
plt.ylabel("Mean Motion (rev/day) — how many orbits per day (higher is lower altitude)")
plt.title("Satellite Clusters (DBSCAN) with IsolationForest Anomalies Highlighted (Noise Removed)")
plt.legend(loc="best", fontsize="small", ncol=2)
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("DBSCAN_IsolationForest_Anomalies_Clean.png", dpi=150)
plt.show()

