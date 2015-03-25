# mongobackupd

`mongobackupd` performs automated backups of MongoDB replica sets deployed on
EC2. mongobackupd finds a secondary member of the replica set and snapshots
the volume's EBS volume. It also removes stale backups according to retention
settings.

`mongobackupd` is a Docker container that runs backup.py according to the
backup schedule set in the included crontab. The mongobackupd container is
intended to be run as a daemon using the -d Docker flag.

`mongobackupd` will also optionally use Slack to notify your team of successful
backups and errors.

`mongobackupd` is a tool I wrote to address a need I had when setting up a
replica set on EC2. It's helpful for my purposes, but it may not be the best
fit for you. Services like [MMS](https://mms.mongodb.com/) and
[MongoLab](https://www.mongolab.com/) handle automated backups out-of-the-
box, and may be a better fit depending on your needs and budget.

## Credentials

Set your EC2 and Mongo credentials in `settings.py`. Required credentials are:

- `AWS_ACCESS_KEY`
- `AWS_SECRET_KEY`
- `MONGO_USERNAME`
- `MONGO_PASSWORD`
- `MONGO_DATABASE`
- `MONGO_PORT`

Optionally, you may also set `SLACK_TOKEN` to enable Slack notifications.

## Instance filters

`settings.INSTANCE_FILTERS` is used to indentify instances in the Mongo
replica-set.

As an example, to target instances that have names starting with "mongo-", you
would do:

```python
INSTANCE_FILTERS = {"tag:Name": "mongo-*"}
```

Instance filters support wildcards `*` and `?`, but do not support regular
expressions. For more information on the filter syntax, see Amazon's
[filtering documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/U
sing_Filtering.html).

## Backup schedule

Your backup schedule is set in `crontab`. For information on Cron's syntax,
run `man cron` or see [wikipedia](http://en.wikipedia.org/wiki/Cron).

The default `crontab` is configured to perform a backup on boot and then
perform hourly backups going forward.

## Snapshot retention

`mongobackupd` automatically removes stale snapshots according to your
retention settings. As an example, the default settings retain hourly backups
for a day, retain daily backups for a week, and retain monthly backups for
three months:

```python
RETAIN_HOURLY = 24
RETAIN_DAILY = 7
RETAIN_MONTHLY = 3
```

## Building and running

To build the docker container:

```term
sudo docker build -t shebson/mongobackupd .
```

To run the container as daemon and restart it whenever Docker starts:

```term
sudo docker run -d --restart=always shebson/mongobackupd
```

## Tests

This grew out of a simple backup script (and is still, really, just a simple
backup script), so I initially didn't attempt to follow TDD when putting it
together. I've gone back and added some tests before open-sourcing it, but the
test suite is not complete.

## Python 3.x

As of Boto 2.36.0, Boto's `trim_snapshots` method is broken on Python 3. Unfortunately,
this means that mongobackupd also does not support Python 3. I plan to port this to
Python 3 once [Boto](https://github.com/boto/boto) completes their Python 3 port.

## License

MIT
