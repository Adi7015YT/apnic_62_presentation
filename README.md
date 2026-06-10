

```sh
chmod 777 ./de/bind/
chmod 777 ./de/bind/db.de.signed.jnl 
docker compose up
/usr/bin/python3 client/app.py
watch -n 1 dig @127.0.0.1 bund.de
docker compose exec -it de rndc dnssec -rollover -key 19266 de
```