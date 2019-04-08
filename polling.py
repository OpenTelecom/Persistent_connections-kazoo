from crontab import CronTab

cron = CronTab(user=True)

job = cron.new(command='cd /Users/Clement/desktop/OTF-Python/Persistent_connections-kazoo && pipenv run python kazoo_cron.py>> test.txt')
job.minute.every(1)

cron.write()

print(job.is_valid())


