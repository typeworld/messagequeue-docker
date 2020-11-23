import os
import logging
import threading
import time
import psutil
import subprocess

# Google monitoring
from google.cloud import monitoring_v3

# Environment
GCE = "messagequeue" in os.getenv("HOSTNAME")

monitoringClient = monitoring_v3.MetricServiceClient.from_service_account_json(
    "typeworld2-a2d47c52ec4e.json"
)
monitoringUpdateInterval = 60


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            ls.append(p)
    return ls


def memory_usage_psutil(pid):
    process = psutil.Process(pid)
    mem = process.memory_full_info()[0] / float(2 ** 20)
    return mem


def createSeries(channel, value):

    series = monitoring_v3.TimeSeries()
    series.metric.type = f"custom.googleapis.com/{channel}"
    series.resource.type = "gce_instance"
    # Seems like the instance_id is irrelevant
    # maybe relevant whan adding stats from several machines
    series.resource.labels["instance_id"] = "4028650832999377952"
    series.resource.labels["zone"] = "us-east1-b"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point(
        {"interval": interval, "value": {"double_value": float(value)}}
    )
    series.points = [point]

    # if not GCE:
    # logging.warning(f"{channel}, {value}")

    return series


def updateMonitoring():

    # Upload
    if GCE:

        series = [
            createSeries(
                "memoryGunicorn",
                sum(
                    [memory_usage_psutil(x.pid) for x in find_procs_by_name("gunicorn")]
                ),
            ),
            createSeries(
                "memoryMonitoring",
                memory_usage_psutil(os.getpid()),
            ),
            createSeries(
                "usedMemoryPercentage",
                psutil.virtual_memory().percent,
            ),
            createSeries(
                "tcpConnections",
                int(
                    subprocess.check_output(
                        "ss -s | awk 'NR==7 {print $2}'", shell=True
                    )
                    .decode()
                    .strip()
                ),
            ),
        ]

        try:
            monitoringClient.create_time_series(
                name="projects/typeworld2", time_series=series
            )
        except Exception as e:
            logging.error(f"Error while sending monitoring data: {e.message}, {e.args}")


# Send logs
def idleTimerr():
    while True:
        updateMonitoring()
        time.sleep(monitoringUpdateInterval)


idleTimerThread = threading.Thread(target=idleTimerr)
idleTimerThread.start()
