from botbot.apps.logs.models import Log
from botbot.apps.plugins.utils import convert_nano_timestamp
from botbot_plugins.base import BasePlugin

class Plugin(BasePlugin):
    """
    Logs all activity.

    I keep extensive logs on all the activity in `{{ channel.name }}`.
    You can read and search them at {{ SITE }}{{ channel.get_absolute_url }}.
    """
    def logit(self, line):
        """Log a message to the database"""
        # If the Channel do not startswtih "#" that means the message
        # is part of a /query
        if line._channel_name.startswith("#"):
            timestamp = convert_nano_timestamp(line._received)
            Log.objects.create(
                channel_id=line._channel.pk,
                timestamp=timestamp,
                nick=line.user,
                text=line.full_text,
                room=line._channel,
                command=line._command,
                raw=line._raw)

    logit.route_rule = ('firehose', ur'(.*)')
