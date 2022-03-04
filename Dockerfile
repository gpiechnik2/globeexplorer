FROM python:3.9-alpine
MAINTAINER gpiechnik2
LABEL Name=globeexplorer Version=1.0

RUN apk add --no-cache git make musl-dev go

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin

# Install subfinder
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@v2.4.9

# Install ffuf
RUN go get -u github.com/ffuf/ffuf@v1.3.1

# Install pip3
RUN apk add --update py-pip

# Copy and install app with single one dependency
COPY . /app
WORKDIR /app

# Install globeexplorer
RUN pip3 install -r requirements.txt
RUN pip install --editable .

ENTRYPOINT ["globeexplorer"]
