import logging
import azure.functions as func
from datetime import datetime, timedelta, timezone
from azure.storage.queue import QueueClient, TextBase64EncodePolicy
import json

from ..shared import parserUtils
from ..shared import NBAParser, NFLParser
from ..shared import models

# create queue trigger that will read from end queue
# if ongoing: requeue 10 mins else upsert
def main(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    logging.info(msg)

    match = models.blobToMatch(json.loads(msg.get_body().decode('utf-8')))
    logging.info(f"Event: {match.to_dict()}")

    updatedMatch = parserUtils.matchToParsers(match).getMatchByID(match.ID)
    updatedMatch.startTime = match.startTime
    logging.info(f"Updated Event: {updatedMatch.to_dict()}")
    
    if updatedMatch.status == "ONGOING":
        logging.info("Match is still going, requeing.")
        endClient = QueueClient.from_connection_string(parserUtils.AZURE_SA_CON_STR, parserUtils.endQ, message_encode_policy=TextBase64EncodePolicy())
        endClient.send_message(json.dumps(match.to_dict()), visibility_timeout=600)
    else:
        logging.info(f"Match has entered terminal state: {updatedMatch.to_dict()}.")
        parserUtils.submitEvents([updatedMatch], updatedMatch.sportalLeague)