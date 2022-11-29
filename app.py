#!/usr/bin/env python

import logging
import os
import platform
import sys
import click
from flask import Flask, json, jsonify, request
from newrelic_telemetry_sdk import Event, EventClient  # type: ignore


app = Flask(__name__, static_url_path='')


@app.route('/status')
def get_status():
  return jsonify({'status': u'\ud83d\udc4d'})


@app.route('/webhook', methods=['POST'])
def post_webhook():
  body = json.loads(request.form['payload'])

  event_payload = {
    "event": body["event"],
  }

  if "Account" in body:
    event_payload.update({
      "account_id": body["Account"]["id"],
      "account_name": body["Account"]["title"],
    })

  if "Server" in body:
    event_payload.update({
      "server_name": body["Server"]["title"],
      "server_id": body["Server"]["uuid"],
    })

  if "Player" in body:
    event_payload.update({
      "player_local": body["Player"]["local"],
      "player_address": body["Player"]["publicAddress"],
      "player_name": body["Player"]["title"],
      "player_id": body["Player"]["uuid"],
    })

  if "Metadata" in body:
    event_payload.update({
      "metadata_type": body["Metadata"]["type"],
      "metadata_name": body["Metadata"]["title"],
      "metadata_parent_name": body["Metadata"]["parentTitle"],
      "metadata_grandparent_name": body["Metadata"]["grandparentTitle"],
      "metadata_key": body["Metadata"]["key"],
      "metadata_parent_key": body["Metadata"]["parentKey"],
      "metadata_grandparent_key": body["Metadata"]["grandparentKey"],
      "metadata_section": body["Metadata"]["librarySectionType"],
      "metadata_section_id": body["Metadata"]["librarySectionID"],
      "metadata_guid": body["Metadata"]["guid"],
    })

  event = Event("PlexWebhookEvent", event_payload)
  EventClient(os.environ['NEW_RELIC_INSERT_KEY']).send(event)

  return jsonify(event)


@click.command()
@click.option("--host", type=click.STRING, envvar="PLEX_NR_HOST", default="0.0.0.0")
@click.option("--port", type=click.STRING, envvar="PLEX_NR_PORT", default=8080)
@click.option("--debug", type=click.BOOL, envvar="DEBUG", default=False)
@click.option("--insert-key", type=click.STRING, envvar="NEW_RELIC_INSERT_KEY")
@click.option("--hostname", type=click.STRING, envvar="PLEX_NR_HOSTNAME")
def main(host, port, debug, insert_key, hostname):
  logging.basicConfig(
      stream=sys.stdout, level=logging.DEBUG if debug else logging.INFO
  )

  event_client = EventClient(insert_key)
  event_static_tags = {
      "hostname": hostname or platform.node(),
      "architecture": platform.machine(),
      "operating_system": platform.system(),
      "operating_system_version": platform.release(),
  }

  app.run(host=host, port=port, debug=debug, threaded=True)
