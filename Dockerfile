FROM alpine:3.20

COPY scripts/ /scripts/
RUN apk update && \
    apk add --no-cache telegraf python3 py3-pip && \
    pip install -r /scripts/requirements.txt --break-system-packages

COPY telegraf.conf /etc/telegraf/telegraf.conf
CMD ["telegraf"]
