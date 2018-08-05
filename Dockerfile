FROM python:2.7-slim

ENV PYTHONPATH /app
ENV LOG_CONFIG flask
ENV LOG_BASE /
ENV TZ=America/Los_Angeles

WORKDIR /app

COPY core core
COPY requirements.txt .
COPY config-local.ini .

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir -p /logs

# install sys tools
RUN apt-get update -y && \
    apt-get install -y unzip \
    libnss3 \
    libgconf-2-4 \
    vim \
    curl \
    wget \
    iputils-ping \
    dnsutils \
    net-tools \
    iproute \
    iptables \
    traceroute \
    tcpdump

# install pip reqs
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# add entrypoint
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "core.wsgi", "2>&1", "|", "tee", "-a", "/logs/core.log"]
