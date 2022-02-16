import logging
import azure.functions as func
from datetime import datetime, timedelta, timezone
from azure.storage.queue import QueueClient, TextBase64EncodePolicy
import json

from ..shared import parserUtils
from ..shared import NBAParser, NFLParser
from ..shared import models

#check if queued event has started 
# if upcoming: requeue 10 mins else upsert
def main(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    logging.info(msg)
    startClient = QueueClient.from_connection_string(parserUtils.AZURE_SA_CON_STR, parserUtils.startQ, message_encode_policy=TextBase64EncodePolicy())

    match = models.blobToMatch(json.loads(msg.get_body().decode('utf-8')))
    logging.info(f"Event: {match.to_dict()}")

    updatedMatch = parserUtils.matchToParsers(match).getMatchByID(match.ID)
    cur = datetime.now(timezone.utc)
    if (updatedMatch.startTime - cur) > timedelta(minutes=30):
        diff = updatedMatch.startTime - cur
        logging.info(f"Event is starting in more than 30 minutes.")
        logging.info("updating match")
        if not parserUtils.updateMatchTime(match, updatedMatch):
            logging.error("Unable to find or update match, dequeueing match.")
            logging.info(f"match: {match.to_dict()}")
            return
        logging.info(f"reqeueing match {diff}")
        logging.info(f"updated: {updatedMatch.to_dict()}")
        startClient.send_message(json.dumps(updatedMatch.to_dict()), visibility_timeout=diff.total_seconds())
        return

    updatedMatch.startTime = match.startTime
    logging.info(f"Updated Event: {updatedMatch.to_dict()}")

    if updatedMatch.status == "UPCOMING":
        logging.info("Match is still upcoming, requeing.")
        startClient.send_message(json.dumps(match.to_dict()), visibility_timeout=600)
    else:
        logging.info("Match has begun, updating.")
        parserUtils.submitEvents([updatedMatch], updatedMatch.sportalLeague)
        endClient = QueueClient.from_connection_string(parserUtils.AZURE_SA_CON_STR, parserUtils.endQ, message_encode_policy=TextBase64EncodePolicy())
        cur = datetime.now(timezone.utc)
        diff = updatedMatch.endTime - cur
        sec_diff = int(diff.total_seconds())+1
        sec_diff = max(sec_diff, 0)
        logging.info(f"Postponing by: {sec_diff}")
        endClient.send_message(json.dumps(updatedMatch.to_dict()), visibility_timeout=sec_diff)