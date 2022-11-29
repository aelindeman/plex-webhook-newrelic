# plex-webhook-newrelic

Reports Plex events to New Relic

## Setup

1. Create an insert key on New Relic (_Account → API Keys → Create a key → Key type: "Ingest - License"_)

1. Build and run the image

    ```
    docker build -t plex-webhook-newrelic:latest .
    docker run \
      -d
      -e NEW_RELIC_INSERT_KEY
      -p 8080:8080 \
      plex-webhook-newrelic:latest
    ```

1. Open [Plex webhook settings](https://app.plex.tv/desktop/#!/settings/webhooks), and add the webhook `http://localhost:8080/webhook`

## Usage & example queries

Play a couple items in Plex, and query in New Relic

- All events:

    ```
    FROM PlexWebhookEvent SELECT *
    ```

- Play counts per media type:

    ```
    FROM PlexWebhookEvent SELECT count(*) WHERE event IN ('media.play') FACET metadata_section
    ```

- Most popular items:

    ```
    FROM PlexWebhookEvent SELECT count(*) WHERE event IN ('media.play') FACET metadata_grandparent_name, metadata_parent_name
    ```

- Heatmap of plays by day of the week and time:

    ```
    FROM PlexWebhookEvent SELECT histogram(numeric(capture(hourOf(timestamp), '^(?P<hour>[0-9]{2}):.+$')), 24, 12) FACET weekdayOf(timestamp) WHERE event IN ('media.play')
    ```

## Development

- [poetry](https://python-poetry.org/)
- [click](https://click.palletsprojects.com/)
- [flask](https://flask.palletsprojects.com/)
- [newrelic-telemetry-sdk-python](https://github.com/newrelic/newrelic-telemetry-sdk-python)

## License

Creative Commons BY-SA 4.0
