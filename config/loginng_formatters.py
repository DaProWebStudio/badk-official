from datetime import datetime, timezone

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')