FROM python:2.7-slim

ENV PYTHONPATH /app
ENV LOG_CONFIG default
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
    net-tools \
    git-core

# install pip reqs
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# add entrypoint
ENTRYPOINT ["/bin/bash"]
CMD ["./core/run_prog.sh"]
