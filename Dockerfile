FROM python:3.9-slim AS python-builder-3.9

WORKDIR /install
COPY requirements.txt ./
RUN apt-get update && apt-get install -y gcc libssl-dev g++ make git build-essential \
    && pip install --upgrade pip \
    && pip install --upgrade pyclean \
    && apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN pip install --prefix=/install -r requirements.txt && pyclean .

FROM python:3.9-slim

WORKDIR /app
COPY --from=python-builder-3.9 /install /usr/local
ADD ./hotel_merge /app/
ENV PYTHONPATH="${PYTHONPATH}:/app/"
EXPOSE 8000

CMD ["python", "main.py"]