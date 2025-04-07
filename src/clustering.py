import pandas as pd
import umap
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

def elbow_method(tfidf_df, max_k=10):
    tfidf_normalized = normalize(tfidf_df)  # Normalize the TF-IDF matrix

    inertia = []  # List to store inertia values
    k_values = range(2, max_k + 1)  # Range of k values to test

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)   # KMeans model with k clusters
        kmeans.fit(tfidf_normalized)    # Fit the model to the normalized data
        inertia.append(kmeans.inertia_)    # Inertia is the sum of squared distances of samples to their closest cluster center

    plt.plot(k_values, inertia, marker='o')  # Plot inertia vs. number of clusters
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.grid(True)
    plt.show()


def kmeans_clustering_umap(tfidf_df, geo_pmid, k, visualize=True):

    tfidf_normalized = normalize(tfidf_df)      #Normalization by rows (L2 norm)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)           # Clustering with Euclidean distance was used because it gave better results than cosine similarity.
    clusters = kmeans.fit_predict(tfidf_normalized)

    for i, geo_id in enumerate(tfidf_df.index):
        geo_pmid[geo_id]["cluster"] = clusters[i]
        del geo_pmid[geo_id]["tokens"]

    if visualize:
        reducer = umap.UMAP(n_components=3, random_state=42)
        reduced = reducer.fit_transform(tfidf_normalized)

        df_plot = pd.DataFrame({
            "Component 1": reduced[:, 0],
            "Component 2": reduced[:, 1],
            "Component 3": reduced[:, 2],
            "Cluster": clusters,
            "GEO ID": tfidf_df.index.astype(str)
        })

        df_plot["PMIDs"] = df_plot["GEO ID"].map(
            lambda gse: geo_pmid.get(gse, {}).get("pubmed_ids", [])
        )

        fig = px.scatter_3d(
            df_plot,
            x="Component 1", y="Component 2", z="Component 3",
            color="Cluster",
            hover_name="GEO ID",
            hover_data={"Cluster": True, "PMIDs": True}
        )

        fig.update_layout(title="3D Clusters of GEO Datasets (with PMIDs)", legend_title="Cluster")
        fig.show()

    return geo_pmid

def reorganize_clusters(data_clustered, k):

    final_data_clustered = {}

    for cluster_id in range(k):
        final_data_clustered[f"cluster_{cluster_id}"] = []

    for geo_id, data in data_clustered.items():
        cluster_id = data['cluster']
        cluster_key = f"cluster_{cluster_id}"
        final_data_clustered[cluster_key].append({
            'geo_id': geo_id,
            'pubmed_ids': data['pubmed_ids']
        })

    return final_data_clustered