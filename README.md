# ip-api
Get to know IP information

## Installation

```
git clone https://github.com/Simatwa/ip-api.git
cd ip-api
pip install -r requirements.txt
```

## Usage

Ensure you have [python>=3.9](https://python.org) in your system

<details>

<summary>

- Trace your own IP : `python main.py me`

</summary>

```
-----------  -------------------------------
status       success
country      Kenya
countryCode  KE
region       20
regionName   Nairobi
city         Nairobi
zip          09831
lat          -8.2841
lon          32.8155
timezone     Africa/Nairobi
isp          Truth Wireless Limited
org          Truth Wireless Limited
as           AS329254 TRUTH WIRELESS LIMITED
query        102.212.11.xx
-----------  -------------------------------

```

</details>

<details>

<summary>

- Trace any other IP : `python main.py ip -q 172.217.170.174`

</summary>

```
-----------  ------------------
status       success
country      United States
countryCode  US
region       NY
regionName   New York
city         New York
zip          10065
lat          40.7652
lon          -73.9588
timezone     America/New_York
isp          Google LLC
org          Google LLC
as           AS15169 Google LLC
query        172.217.170.174
-----------  ------------------
```

</details>

For more info run `python main.py <me/ip> --help`