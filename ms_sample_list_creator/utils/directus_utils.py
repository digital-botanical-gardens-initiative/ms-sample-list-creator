from typing import List

import requests

from ms_sample_list_creator.structure import Batch, Instrument

def get_batches() -> List[Batch]:
    """
    Fetches batches from Directus and returns a list of Batch
    """

    batches = []

    url = "https://emi-collection.unifr.ch/directus/items/Batches"
    headers = {"Content-Type": "application/json"}
    params = {
        "filter[batch_type][_eq]": 6,
        "fields": "batch_id,id",
        "sort[]": "-batch_id"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]
    except requests.RequestException as e:
        print(f"Error fetching batches: {e}")
        batches.append(Batch(
            name = "None",
            identifier = -1
        ))
        return batches

    # Add placeholders
    select_batch = Batch(
        name = "Select a batch",
        identifier = -1
    )
    new_batch = Batch(
        name = "New batch",
        identifier = 0
    )
    batches.append(select_batch, new_batch)

    # Extract batches from directus request
    for item in data:
        batch = Batch(
            name = item.get("batch_id", ""),
            identifier = item.get("id", "")
        )
        batches.append(batch)

    return batches

def get_instruments() -> List[Instrument]:
    """
    Fetches instrument IDs from Directus and returns a list of Instrument
    """

    instruments = []

    url = "https://emi-collection.unifr.ch/directus/items/Instruments"
    params = {
        "filter[instrument_model][instrument_type][_eq]": 1,
        "fields": "instrument_id,instrument_model.instrument_model,id",
        "sort[]": "instrument_id"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]
    except requests.RequestException as e:
        print(f"Error fetching instruments: {e}")
        instruments.append(Instrument())
        return instruments
    
    # Extract instruments from directus request
    for item in data:
        instrument = Instrument(
            name = item["instrument_model"].get("instrument_model") + " (" + item.get("instrument_id", "") + ")",
            identifier = item.get("id", "")
        )
        instruments.append(instrument)

    return instruments