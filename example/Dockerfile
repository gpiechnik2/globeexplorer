FROM gpiechnik2/globeexplorer:1.0

# Copy modules, scenarios and wordlist
COPY . /app
WORKDIR /app

RUN apk add --no-cache git make musl-dev go g++ gcc libxslt-dev

# Nmap
RUN apk add nmap --no-cache && rm -f /var/cache/apk/*
RUN apk add nmap-scripts

# SSLyze
RUN pip3 install --upgrade pip setuptools
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip3 install --editable ./modules/sslyze/

# SecretFinder
RUN pip3 install -r ./modules/secretfinder/requirements.txt

# CRLF-Injection-Scanner
RUN pip3 install eventlet
RUN pip3 install click
RUN pip3 install validators

# ScanQLi
RUN pip3 install -r ./modules/ScanQLi/requirements.txt
RUN apk add --update --no-cache py3-numpy

# FDsploit
RUN pip3 install -r ./modules/FDsploit/requirements.txt

ENTRYPOINT ["python3", "globecli.py"]
