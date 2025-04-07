# Dataset-Clustering-Analysis

This repository includes a web application built with **Flask** that clusters **GEO datasets** linked to a list of **PubMed IDs (PMIDs)**. The application processes the descriptions of these datasets using **TF-IDF** vector representation to convert the text data into numerical form and then applies **K-Means** clustering to group similar datasets together.

## Installation

1. **Clone the Repository**:


    ```
    git clone https://github.com/matijap59/Dataset-Clustering-Analysis.git
    ```
2. **Create Virtual Environment**:
    ```
    python -m venv venv
    ```
3. **Activate Virtual Environment**:
    ```
    venv\Scripts\activate
    ```
4. **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```
5. **Position to the Project Directory**:
    ```
    cd src
    ```
6. **Run the Flask Application**:
    ```
    flask run --host=0.0.0.0 --port=5000 --debug
    ```
7. **Send a POST Request to Cluster Datasets**

    After starting the application, send a POST request to:
    ```
    http://localhost:5000/cluster_datasets
    ```

    Here's an example of the request body containing a list of PubMed IDs (`pubmed_ids`):

    ```
        {
            "pubmed_ids": [
                30530648, 31820734, 31018141, 38539015, 33763704, 32572264, 31002671, 33309739, 
                21057496, 27716510, 34059805, 34941412, 33879573, 35440059, 33879573, 29462153, 
                29794063, 25939354, 30322904, 36879017, 35419551, 31501549, 23042784, 22219169, 
                20670891, 20385583, 19723310, 20602769, 26566685, 38030723, 30498128, 20485568, 
                21613409, 31076851, 37169753, 39800688, 36510023, 38177678, 36539615, 37871105, 
                35235788, 27799057, 30820472, 31666070, 34686734, 22384383, 34033742, 33589615, 
                31792364, 29576475, 39762647, 32084358, 38977847, 25493933, 31125107, 26749252, 
                39587714, 30333487, 33743111, 35172154, 32025611, 31136284, 26740022, 37989753, 
                39838364, 39367016, 36650381, 35511946, 38641753, 38287646, 36840360, 36544018, 
                36840360, 39637179, 35767948, 31801092, 38909241, 36544018, 32384151, 26280576, 
                38379415, 29550329, 19211887, 36803569, 30320226, 35920937, 37958987, 25340342, 
                37277533, 24223949
            ]
        }
    ```

    **Notes**:

    This JSON object sends the list of PubMed IDs to the server, which will process the data and return a visualization of the dataset clusters.

    You can use tools like Postman to send this POST request.