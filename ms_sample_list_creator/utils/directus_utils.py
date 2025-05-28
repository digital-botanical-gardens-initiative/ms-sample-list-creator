from typing import List

import requests

from ms_sample_list_creator.implementations.result import Result
from ms_sample_list_creator.structure import Batch, DirectusCredentials, Instrument, Method, Path


def get_batches() -> List[Batch]:
    """
    Fetches batches from Directus and returns a list of Batch
    """

    batches = []

    url = "https://emi-collection.unifr.ch/directus/items/Batches"
    headers = {"Content-Type": "application/json"}
    params = {"filter[batch_type][_eq]": 6, "fields": "batch_id,id", "sort[]": "-batch_id"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]
    except requests.RequestException as e:
        print(f"Error fetching batches: {e}")
        batches.append(Batch(name="None", identifier=-1))
        return batches

    # Add placeholders
    new_batch = Batch(name="New batch", identifier=0)
    batches.append(new_batch)

    # Extract batches from directus request
    for item in data:
        batch = Batch(name=item.get("batch_id", ""), identifier=item.get("id", ""))
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
        "sort[]": "instrument_id",
    }
    headers = {"Content-Type": "application/json"}

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
            name=item["instrument_model"].get("instrument_model") + " (" + item.get("instrument_id", "") + ")",
            identifier=item.get("id", ""),
        )
        instruments.append(instrument)

    return instruments


def test_credentials(credentials: DirectusCredentials) -> Result[str, str]:
    """
    Attempts to connect to Directus using the provided user data.

    If the connection is successful, the access token is stored.

    Args:
        user_data (dict): The dictionary containing the necessary user data.

    Returns:
        None
    """

    base_url = "https://emi-collection.unifr.ch/directus"
    login_url = base_url + "/auth/login"

    try:
        response = requests.post(
            login_url, json={"email": credentials.username, "password": credentials.password}, timeout=10
        )
        response.raise_for_status()

        return Result(value=response.json()["data"]["access_token"])

    except requests.HTTPError as e:
        return Result(error=f"HTTPError during Directus login: {e}")

    except requests.RequestException as e:
        return Result(error=f"RequestException during Directus login: {e}")


def test_batch(batch: Batch, token: str) -> Result[Batch, str]:
    """
    Check that batch exists in Directus. If not, create it.

    Args:
        batch (Batch): The batch to check
        token (str): The directus token
    """

    if batch.identifier == -1:
        return Result(error="No batch selected")

    if batch.identifier > 0:
        return Result(value=batch)

    url = "https://emi-collection.unifr.ch/directus/items/Batches"
    params = {"sort[]": "-batch_id", "limit": 1}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    session = requests.Session()
    session.headers.update(headers)

    # Get last batch
    try:
        response = session.get(url=url, params=params)
        response.raise_for_status()
        json_data = response.json()
        last_value: str = json_data["data"][0]["batch_id"] if json_data["data"] else ""
        last_number = int(last_value.split("_")[1]) if last_value != "" else 0
    except (requests.RequestException, IndexError, ValueError) as e:
        return Result(error=f"Failed to get last batch: {e}")

    new_batch = f"batch_{last_number + 1:06d}"

    # Create payload and post to Directus
    payload = {
        "batch_id": new_batch,
        "batch_type": 6,
        "short_description": "ms batch",
        "description": "ms batch",
    }

    try:
        response = session.post(url=url, json=payload, timeout=10)
        response.raise_for_status()
        new_batch = Batch(name=new_batch, identifier=int(response.json()["data"]["id"]))
        return Result(value=new_batch)
    except requests.RequestException as e:
        print(f"Failed to create batch: {e}")
        return Result(error=f"Failed to create batch: {e}")


def get_methods(methods_list: List[str], token: str) -> List[Method]:
    """
    Adds an injection method to Directus and returns its ID if successful.

    If the method already exists, fetches its ID instead of failing.

    Args:
        access_token (str): The JWT access token for authentication.
        method_file (str): The name of the method to add.

    Returns:
        int: The Directus ID of the method, or -1 if it failed completely.
    """

    print(f"methods: {methods_list}")

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    base_url = "https://emi-collection.unifr.ch/directus"
    method_name = Path(method_file).stem
    payload = {"method_name": method_name}

    try:
        # Try posting the new method
        response = session.post(f"{base_url}/items/Injection_Methods/", json=payload)
        response.raise_for_status()
        return int(response.json()["data"]["id"])

    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 400:
            # Likely already exists — try to fetch it
            print(f"Method '{method_name}' already exists. Fetching ID...")

            get_response = session.get(
                f"{base_url}/items/Injection_Methods", params={"filter[method_name][_eq]": method_name}
            )

            if get_response.ok:
                data = get_response.json().get("data")
                if data:
                    return int(data[0]["id"])
                else:
                    print(f"Method '{method_name}' not found despite 400 error.")
            else:
                print(f"Failed to fetch existing method '{method_file}'. Status code: {get_response.status_code}")
                print("Response content:", get_response.text)
        else:
            print(f"Failed to add method '{method_name}': {e}")
            if e.response is not None:
                print("Response content:", e.response.text)

    return -1
