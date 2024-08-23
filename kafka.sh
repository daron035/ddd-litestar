#!/bin/sh

echo "Waiting for Kafka to be ready..."
cub kafka-ready -b kafka:29092 1 20

# # Delete all existing topics
# echo "Listing all topics..."
# topics=$(kafka-topics --list --bootstrap-server kafka:29092)

# for topic in $topics; do
#   echo "Deleting topic $topic..."
#   kafka-topics --delete --topic "$topic" --bootstrap-server kafka:29092
# done

# Create topics if they do not exist
kafka-topics --create --topic Chat --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server kafka:29092
kafka-topics --create --topic Message --partitions 2 --replication-factor 1 --if-not-exists --bootstrap-server kafka:29092
kafka-topics --create --topic iouwruiuiqwruirqwuiqwrui --partitions 2 --replication-factor 1 --if-not-exists --bootstrap-server kafka:29092

# Alter partitions for existing topics
kafka-topics --alter --topic Chat --partitions 1 --bootstrap-server kafka:29092
kafka-topics --alter --topic Message --partitions 4 --bootstrap-server kafka:29092

echo "Topics updated!"
