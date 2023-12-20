from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound


def get_a_client():
    """
    Create client object to connect to google bigquery with json file

    :return: client => authorized BigQuery client object
    """
    # Get auth file to connect bigquery
    key_path = "/usr/local/airflow/dags/auth_files/dsmbootcamp-535dfd073f87.json"
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Create a bigquery client instance
    client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
    return client


def create_sql_pivot():
    """
    Create clickstream_agg table if not exists & execute sql aggregation code
    """
    project = 'dsmbootcamp'
    dataset_id = 'selcuk_akarin'
    table_id = 'clickstream_agg'
    # Construct a BigQuery client object.
    table_ref = "{}.{}.{}".format(project, dataset_id, table_id)

    # Construct a BigQuery client object.
    client = get_a_client()

    # Create aggregation query
    QUERY = ("""
        CREATE OR REPLACE TABLE `dsmbootcamp.selcuk_akarin.clickstream_agg`
        AS
        WITH click_type AS (
                SELECT timestamp_trunc(cs.timestamp,day) click_day,
                type,
                count(distinct id) dist_user
                FROM `dsmbootcamp.selcuk_akarin.clickstream` cs
                GROUP BY 1,2
        )
        SELECT 
                click_day,
                SUM(IF(type LIKE '%ios%', dist_user, null)) ios,
                SUM(IF(type LIKE '%android%', dist_user, null)) android,
                SUM(IF(type LIKE '%web%', dist_user, null)) web,
                SUM(IF(type LIKE '%mobile_web%', dist_user, null)) mobile_web
        FROM click_type
        GROUP BY 1;
        """)
    # Exec aggregation query
    query_job = client.query(QUERY)  # API request
    query_job.result()  # Waits for query to finish


if __name__ == "__main__":
    create_sql_pivot()
