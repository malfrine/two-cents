import requests
import json
import time
from copy import copy
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.utils import timezone
from django.views.debug import ExceptionReporter


class SlackExceptionHandler(AdminEmailHandler):
    def __init__(self, include_html=False, email_backend=None, reporter_class=None):
        self.SLACK_ERROR_LEVEL = ["ERROR", "CRITICAL"]
        self.SLACK_WEBHOOK_URL = settings.SLACK_WEBHOOK_URL
        super().__init__()

    def _get_record_color(self, level_name):
        color = ""
        if level_name == "CRITICAL":
            color = "#563d7c"
        if level_name == "ERROR":
            color = "#ff0018"
        if level_name == "WARNING":
            color = "#ffbd00"
        if level_name == "INFO":
            color = "#0078f0"
        if level_name == "DEBUG":
            color = "#d6d8da"
        return color

    def emit(self, record, *args, **kwargs):
        try:
            request = record.request
            subject = "%s (%s IP): %s" % (
                record.levelname,
                (
                    "internal"
                    if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                    else "EXTERNAL"
                ),
                record.getMessage(),
            )
        except Exception:
            subject = "%s: %s" % (record.levelname, record.getMessage())
            request = None
        subject = self.format_subject(subject)

        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (
            self.format(no_exc_record),
            reporter.get_traceback_text(),
        )

        color = self._get_record_color(record.levelname)

        attachments = [
            {
                "title": subject,
                "color": color,
                "fields": [
                    {
                        "title": "Level",
                        "value": record.levelname,
                        "short": True,
                    },  # noqa E231
                    {
                        "title": "Datetime",
                        "value": str(timezone.now()),
                        "short": True,
                    },  # noqa: E231
                    {
                        "title": "Method",
                        "value": request.method if request else "No Request",
                        "short": True,
                    },
                    {
                        "title": "Path",
                        "value": request.path if request else "No Request",
                        "short": True,
                    },
                    {
                        "title": "User",
                        "value": (
                            (
                                request.user.username
                                + " ("
                                + str(request.user.pk)
                                + ")"
                                if request.user.is_authenticated
                                else "Anonymous"
                            )
                            if request
                            else "No Request"
                        ),
                        "short": True,
                    },
                    {
                        "title": "Status Code",
                        "value": record.status_code
                        if hasattr(record, "status_code")
                        else "No Request",
                        "short": True,
                    },
                    {
                        "title": "UA",
                        "value": (
                            request.META["HTTP_USER_AGENT"]
                            if request and request.META
                            else "No Request"
                        ),
                        "short": False,
                    },
                    {
                        "title": "GET Params",
                        "value": json.dumps(request.GET) if request else "No Request",
                        "short": False,
                    },
                    {
                        "title": "POST Data",
                        "value": json.dumps(request.POST) if request else "No Request",
                        "short": False,
                    },
                    {"title": "Traceback Message", "value": message, "short": False},
                ],
            },
        ]

        main_text = f"{record.levelname} at " + time.strftime(
            "%A, %d %b %Y %H:%M:%S +0000", time.gmtime()
        )

        data = {
            "payload": json.dumps({"main_text": main_text, "attachments": attachments}),
        }

        if record.levelname in self.SLACK_ERROR_LEVEL or (
            self.SLACK_ERROR_LEVEL == "*" or self.SLACK_ERROR_LEVEL == ["*"]
        ):
            webhook_url = settings.SLACK_WEBHOOK_URL
            requests.post(webhook_url, data=data)
