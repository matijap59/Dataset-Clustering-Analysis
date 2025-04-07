from flask import Flask, request, jsonify

from data_fetching import get_webenv_and_querykey, get_gds_ids, get_summaries
from preprocess_text import process_text_data
from tf_idf import calculate_tfidf_matrix
from clustering import elbow_method, kmeans_clustering_umap, reorganize_clusters

app = Flask(__name__)

@app.route('/cluster_datasets', methods=['POST'])
def cluster_datasets_by_pmids():
    data = request.get_json()
    pubmed_ids = data.get('pubmed_ids', [])

    webenv, query_key = get_webenv_and_querykey(pubmed_ids)
    gds_ids = get_gds_ids(webenv, query_key)
    data = get_summaries(gds_ids)

    processed_data = process_text_data(data)

    tfidf_df = calculate_tfidf_matrix(processed_data)   #TF-IDF vectors are constructed from scratch without utilizing tools such as TfidfVectorizer.

    #elbow_method(tfidf_df)      # Based on the analysis using the elbow method, selecting k=5 yields optimal clustering results.

    k = 5
    data_clustered = kmeans_clustering_umap(tfidf_df, processed_data, k)    # By clicking on any result, all key information about the corresponding dataset is displayed, including its association with the specific PMID
    final_data_clustered = reorganize_clusters(data_clustered, k)

    return jsonify(final_data_clustered)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
