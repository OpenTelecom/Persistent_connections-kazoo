# Websockets
By using multiple bindings, subscribe to multiple kazoo websocket bindings and parse the data, in Real time and store the data on a database, we will be using PostgreSQL.

## Blackhole && Kazoo subscription

Use RESTful API Getting the auth_token from crossbar by providing an MD5 hash of the username/password
Using the auth_token to create accounts, get subscribe to crossbar - access endpoints


# Webhooks
Successfully hook to kazoo and be notified in real time about call and object events.

Use flask, which is a python Web Server Gateway Interface library in python.

Responses received in type : `x-www-form-urlencoded` format and not json

NOTES: check the ```wikki``` page

# Polling
Use Cron to poll kazoo and update database.
