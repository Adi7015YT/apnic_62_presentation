#!/bin/bash

# ==========================================
# IPv4 TLD Nameservers (.de, .nl, .in)
# ==========================================
IPV4_TARGETS=(
  # .de
  "194.0.0.53" "77.67.63.105" "195.243.137.26" "81.91.164.5" "194.246.96.1" "194.146.107.6"
  # .nl
  "194.0.25.24" "194.0.28.53" "185.159.199.200"
  # .in (trs-dns)
  "64.78.205.1" "64.96.1.1" "64.78.204.1" "64.96.2.1"
)

# ==========================================
# IPv6 TLD Nameservers (.de, .nl, .in)
# ==========================================
IPV6_TARGETS=(
  # .de
  "2001:678:2::53" "2001:668:1f:11::105" "2003:8:14::53" "2a02:568:0:2::53" "2a02:568:fe02::de" "2001:67c:1011:1::53"
  # .nl
  "2001:678:20::24" "2001:678:2c:0:194:0:28:53" "2620:10a:80ac::200"
  # .in (trs-dns)
  "2620:171:813:1534:8::1" "2620:57:4001::1" "2620:171:812:1534:8::1" "2620:57:4002::1"
)

echo "Removing iptables DROP rules for TLD nameservers..."

# Clean up IPv4
for ip in "${IPV4_TARGETS[@]}"; do
  iptables -D DOCKER-USER -d "$ip" -p udp --dport 53 -j DROP 2>/dev/null
  iptables -D DOCKER-USER -d "$ip" -p tcp --dport 53 -j DROP 2>/dev/null
done

# Clean up IPv6
for ip in "${IPV6_TARGETS[@]}"; do
  ip6tables -D DOCKER-USER -d "$ip" -p udp --dport 53 -j DROP 2>/dev/null
  ip6tables -D DOCKER-USER -d "$ip" -p tcp --dport 53 -j DROP 2>/dev/null
done

echo "Cleanup complete. BIND can reach the nameservers again."
