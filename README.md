# Lite Proto EGTS Parser

欲速则不达。

https://www.swe-notes.ru/post/protocol-egts/ - The ready package for checking was taken from here, so you can verify the correctness of the data.

### Can help to create vitrual environment

```bash

python -m venv venv
venv\Scripts\activate

```

### Can help to run light clint to send come packs to server's receiver

```bash

python -u ".\client\run_mini_client.py" ".\client\to_test_egts_packages.csv"

```

### Can help to run light server to receive and come packs to clients

```bash

python -u -m server.run_mini_server -c ".\config\conf.yaml"

```

### Can help to install dependencies

```bash

pip install -r requirements.txt

```