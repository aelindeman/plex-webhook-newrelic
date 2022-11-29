# plex-webhook-newrelic

Reports Plex events to New Relic

## Usage

1. Create an Insights insert key on New Relic
1. Build and run the image:

    ```
    docker build -t plex-webhook-newrelic:latest .
    docker run \
      -e NEW_RELIC_INSERT_KEY
      -p 8080:8080 \
      plex-webhook-newrelic:latest
    ```

1. Open [Plex webhook settings](https://app.plex.tv/desktop/#!/settings/webhooks) and add the webhook `http://localhost:8080/webhook`

