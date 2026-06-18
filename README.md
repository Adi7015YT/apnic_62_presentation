

```sh
chmod 777 ./de/bind/
docker compose up
dig @127.0.0.1 bund.de
```

Open <IP>:3000


Load :
```sh
/usr/bin/python3 client/app.py
```

Monitor :
```sh
watch -n 1 dig @172.20.0.3 DNSKEY de. +dnssec
watch -n 1 docker compose exec -it de rndc dnssec -status de
```

Rollover keys
```sh
docker compose exec -it de rndc dnssec -rollover -key 19266 de && ls /var/cache/bind
docker compose exec -it de rndc dnssec -checkds -key <new-key-id> published de
# Example : docker compose exec -it de rndc dnssec -checkds -key 07309 published de
```

Add NTA
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