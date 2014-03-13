#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Settings.settings")

    from django.core.management import execute_from_command_line

#    celery.app.current_app().control.inspect(callback=on_reply, timeout=5).active_queues()
#    import celery.apps.worker as celeryworker
#    import exampleSettings.celery
#    worker = celeryworker.Worker(app=exampleSettings.celery.app, hostname=None)

#    worker.run
    execute_from_command_line(sys.argv)
