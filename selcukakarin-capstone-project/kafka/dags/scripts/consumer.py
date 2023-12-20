from kafka import KafkaConsumer, TopicPartition
import json
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


def create_table_if_not_exists(client, table_ref):
    """
    Create table if not exist in the BigQuery
    :param client: Initialized BigQuery client
    :param table_ref: Table reference to be created
    """

    try:
        client.get_table(table_ref)  # Make an API request.
        print("Table {} already exists.".format(table_ref))
    except NotFound:
        # Create a schema template
        tbl_schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("type", "STRING", mode="REQUIRED")
        ]
        click_stream_tbl = bigquery.Table(table_ref, schema=tbl_schema)
        client.create_table(click_stream_tbl)
        print("Table {} is created.".format(table_ref))


def consume_and_load_data(client, table_ref):
    """
    Consume data from kafka & load data to BigQuery
    :param client: Initialized BigQuery client
    :param table_ref: Table reference which data is to be loaded
    """

    # Min size_of_batch
    min_size = 100
    # Kafka topic name
    topic_name = "click_stream"
    consumer_group = 'group_1'
    # Create a KafkaConsumer instance
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id=consumer_group,
        fetch_min_bytes=min_size,
        fetch_max_wait_ms=60000,
        consumer_timeout_ms=1000,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    # Get topic partition
    topic_partition = TopicPartition(topic_name, 0)
    # Get topic last offset value
    last_offset = list(consumer.end_offsets([topic_partition]).values())[0]

    # Consume kafka messages and create mini_batch
    mini_batch = []
    # If there is data in kafka topic
    if last_offset > 0:
        for msg in consumer:
            mini_batch.append(msg.value)
            if msg.offset == last_offset - 1:
                consumer.seek(topic_partition, last_offset)
                consumer.commit()
                consumer.close()
                break

    # if mini batch is not empty then load data to clickstream table
    if mini_batch:
        errors = client.insert_rows_json(table_ref, mini_batch)  # Make an API request.
        if not errors:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))


def consumer():
    """
    Connect client, create click_stream table if not exists, consume data from kafka & load to BigQuery
    """
    # Create a BigQuery client instance
    client = get_a_client()
    table_ref = "dsmbootcamp.selcuk_akarin.clickstream"

    # Create table if not exist in the BigQuery
    create_table_if_not_exists(client, table_ref)

    # Consume and load data to big query
    consume_and_load_data(client, table_ref)


if __name__ == "__main__":
    consumer()
