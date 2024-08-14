from dataclasses import asdict


def convert_event_to_json(event):
    return asdict(event)
