import datetime
from datetime import timedelta, timezone
import logging
from azure.storage.queue import QueueClient, TextBase64EncodePolicy
import azure.functions as func
import json

from ..shared import parserUtils
from ..shared import NBAParser, NFLParser, NHLParser
from ..shared import models

# register events with backend
# push events into startQ
def main(mytimer: func.TimerRequest) -> None:
    PARSERS = [NBAParser.NBAParser(), NFLParser.NFLParser(), NHLParser.NHLParser()]

    startClient = QueueClient.from_connection_string(parserUtils.AZURE_SA_CON_STR, parserUtils.startQ, message_encode_policy=TextBase64EncodePolicy())

    for parser in PARSERS:
        parsedMatches = parser.getMatchesForTwoDay()
        logging.info(f"Parsed Matches: {[p.to_dict() for p in parsedMatches]}")
        upcomingMatches = [m for m in parsedMatches if m.status == "UPCOMING" and not parserUtils.exists(m)]
        logging.info(f"New Upcoming Matches: {[e.to_dict() for e in upcomingMatches]}")
        try:
            resp = parserUtils.submitEvents(upcomingMatches, parser.SPORTAL_LEAGUE)
            if resp != 200:
                logging.error(f"Unable to register parser events.")
                return
        except Exception as ex:
            logging.error(f"Submitting events failed. {ex}")
            return
        logging.info(f"Upcoming matches: {upcomingMatches}")
        for m in upcomingMatches:
            logging.info(m.to_dict())
            cur = datetime.datetime.now(timezone.utc)
            diff = m.startTime - cur
            logging.info(f"Submitting event and delaying by: {diff}")
            startClient.send_message(json.dumps(m.to_dict()), visibility_timeout=int(diff.total_seconds()) + 1)
            logging.info(f"Successfully processed: {m.to_dict()}")