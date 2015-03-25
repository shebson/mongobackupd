"""Finds an EC2 instance running a MongoDB secondary and snapshots it"""

from boto import ec2
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import settings, reporting

def get_connection():
    """Connects to AWS using credentials from settings.py"""
    return ec2.connection.EC2Connection(
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
        )

def get_mongo_url(host):
    """Gets Mongo URL from EC2 instance and credentials in settings.py"""
    return "mongodb://" + \
        settings.MONGO_USERNAME + ":" + \
        settings.MONGO_PASSWORD + "@" + \
        host + settings.MONGO_PORT + "/" + \
        settings.MONGO_DATABASE

def is_secondary(instance):
    """Checks if EC2 instance is a seconday member of a replica set"""
    public_dns = instance.public_dns_name
    try:
        client = MongoClient(
            host=get_mongo_url(public_dns)
            )
    except ConnectionFailure:
        return False
    if client.is_primary:
        client.disconnect()
        return False
    client.disconnect()
    return True

def get_volume_from_instance(instance, connection):
    """Gets the EBS volume attached to the EC2 instance"""
    if len(instance.block_device_mapping) != 1:
        return False

    mappings = connection.get_instance_attribute(
        instance_id=instance.id,
        attribute='blockDeviceMapping'
        )['blockDeviceMapping']
    _, volume = mappings.popitem()
    return volume.volume_id

def get_volume(connection):
    """Finds an EC2 instance that is seconday member and returns its EBS volume"""
    reservations = connection.get_all_reservations(filters=settings.INSTANCE_FILTERS)
    for reservation in reservations:
        for instance in reservation.instances:
            if is_secondary(instance):
                volume = get_volume_from_instance(instance, connection)
                if volume:
                    return volume
    return None

def make_snapshot(connection):
    """Finds appropriate volume and snapshots it"""
    volume = get_volume(connection)
    if volume is None:
        reporting.error("Could not find a volume to backup")
        exit(1)
    try:
        connection.create_snapshot(
            volume,
            description="Automatically created by backup daemon"
            )
    except:
        reporting.error("Error saving snapshot")
        return
    reporting.success("Snapshot saved of volume " + volume)

def trim_snapshots(connection):
    """Removes old snapshots based on retention settings from settings.py"""
    try:
        return connection.trim_snapshots(
            hourly_backups=settings.RETAIN_HOURLY,
            daily_backups=settings.RETAIN_DAILY,
            monthly_backups=settings.RETAIN_MONTHLY
            )
    except:
        reporting.error("Error trimming snapshots")

def backup():
    """Finds and snapshots a running secondary and removes stale snapshots"""
    connection = get_connection()
    make_snapshot(connection)
    trim_snapshots(connection)

if __name__ == "__main__":
   backup()
