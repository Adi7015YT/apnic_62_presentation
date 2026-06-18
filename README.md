

```sh
chmod 777 ./de/bind/
chmod 777 ./de/bind/db.de.signed.jnl 
docker compose up
/usr/bin/python3 client/app.py
watch -n 1 dig @127.0.0.1 bund.de
```
```sh
docker compose exec -it de rndc dnssec -rollover -key 19266 de && date
docker compose exec -it de rndc dnssec -checkds -key <new-key-id> published de && date
# docker compose exec -it de rndc dnssec -checkds -key 07309 published de && date
watch -n 1 docker compose exec -it de rndc dnssec -status de
# docker compose exec -it de rndc managed-keys sync
# docker compose exec -it de rndc thaw de
# docker compose exec -it de rndc reload de
```

```sh
docker compose exec -it de rndc nta de
```

If any record is changed in .de, run the following command
```sh
docker compose exec -it de rm -r /etc/bind/db.de.jbk  /etc/bind/db.de.signed /etc/bind/db.de.signed.jnl
docker compose exec -it de rndc reconfig
docker compose exec -it de rndc reload de
docker compose restart de
```