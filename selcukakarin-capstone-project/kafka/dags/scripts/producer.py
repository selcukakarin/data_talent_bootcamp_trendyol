from kafka import KafkaProducer
import json
from random import randint, choice
from datetime import datetime


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def generate_fake_data():
    """
    Generates data in the following format
        {
          "id": 1
          "timestamp": “2020-01-01 15:00:00”,
          "type": “ios”
        }
    """
    # Type list
    type_list = ["ios", "android", "web", "mobile-web"]

    id_ = randint(1, 1000000)
    now_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    type_ = choice(type_list)
    # Create a fake data
    fake_data = {"id": id_, "timestamp": now_, "type": type_}
    return fake_data


def produce_data():
    """
    It generates data between 100 and 1000 data & send to kafka topic
    """
    # Kafka topic name
    topic_name = "click_stream"
    # Initialize a KafkaProducer instance
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                             # api_version=(0,1,0),
                             value_serializer=json_serializer
                             )
    # Produce random size data and send to kafka
    size = randint(100, 1000)
    for i in range(size):
        producer.send(topic_name, generate_fake_data())


if __name__ == "__main__":
    # Start producer
    produce_data()
