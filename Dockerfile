FROM apache/airflow:2.9.3-python3.11  
# Install selenium and Chrome driver
USER root

RUN apt-get update \
    && apt-get install -y wget \
    && apt-get install -y zip chromium gosu

RUN wget https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.40/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv ./chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver

USER airflow

# Install pip dependencies
RUN pip install --no-cache-dir \
    selenium==4.15.0 \
    beautifulsoup4==4.12.3 \
    python-dotenv==1.0.1 \
    Pillow \
    requests==2.32.3 \
    webdriver-manager==4.0.1

# COPY requirements.txt /
# RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt