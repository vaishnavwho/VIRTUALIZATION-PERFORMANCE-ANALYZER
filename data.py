"""Benchmark data for the Virtualization Performance Analyzer."""

BENCHMARK_DATA = {
    "VMware": {
        "CPU Usage (%)": 38,
        "RAM Usage (GB)": 4.2,
        "Disk Performance (MB/s)": 245,
        "Boot Time (seconds)": 28,
    },
    "VirtualBox": {
        "CPU Usage (%)": 46,
        "RAM Usage (GB)": 4.8,
        "Disk Performance (MB/s)": 205,
        "Boot Time (seconds)": 36,
    },
}

METRIC_DETAILS = {
    "CPU Usage (%)": {"lower_is_better": True, "description": "Average CPU used during workload."},
    "RAM Usage (GB)": {"lower_is_better": True, "description": "Average memory consumed by the VM."},
    "Disk Performance (MB/s)": {"lower_is_better": False, "description": "Average disk read/write speed."},
    "Boot Time (seconds)": {"lower_is_better": True, "description": "Guest OS startup time."},
}