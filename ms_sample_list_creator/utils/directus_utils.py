from pathlib import Path as PathlibPath
from typing import List

import requests

from ms_sample_list_creator.implementations.result import Result
from ms_sample_list_creator.structure import Batch, DirectusCredentials, Instrument, Method, SampleContainer, SampleData


def get_batches() -> Result[List[Batch], str]:
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
        return Result(error=f"Error fetching batches: {e}")

    # Add placeholders
    new_batch = Batch(name="New batch", identifier=0)
    batches.append(new_batch)

    # Extract batches from directus request
    for item in data:
        batch = Batch(name=item.get("batch_id", ""), identifier=item.get("id", ""))
        batches.append(batch)

    return Result(value=batches)


def get_instruments() -> Result[List[Instrument], str]:
    """
    Fetches instrument IDs from Directus and returns a list of Instrument
    """

    instruments: List[Instrument] = []

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
        return Result(error=f"Error fetching instruments: {e}")

    # Extract instruments from directus request
    for item in data:
        try:
            model_data = item.get("instrument_model")
            model_name = model_data.get("instrument_model") if model_data else "Unknown model"
            instrument_id = item.get("instrument_id")
            instrument_id_value = item.get("id")

            # Validate and convert id
            identifier = int(instrument_id_value)
            instrument: Instrument = Instrument(name=f"{model_name} ({instrument_id})", identifier=identifier)

            instruments.append(instrument)
        except (TypeError, ValueError) as e:
            return Result(error=f"Error processing instrument: {e}")

    return Result(value=instruments)


def login_to_directus(credentials: DirectusCredentials) -> Result[str, str]:  # TODO: Handle reconnection when time
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


def get_methods(methods_list: List[str], token: str) -> Result[List[Method], str]:
    """
    Adds an injection method to Directus and returns its ID if successful.

    If the method already exists, fetches its ID instead of failing.

    Args:
        access_token (str): The JWT access token for authentication.
        method_file (str): The name of the method to add.

    Returns:
        int: The Directus ID of the method, or -1 if it failed completely.
    """

    base_url = "https://emi-collection.unifr.ch/directus/items/Injection_Methods"
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    method_names = [PathlibPath(m).stem for m in methods_list]

    params = {"filter[method_name][_in]": method_names}

    try:
        response = session.get(f"{base_url}", params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
    except requests.RequestException as e:
        return Result(error=f"Failed to fetch existing methods: {e}")

    # Existing methods from Directus
    existing_methods = {
        method["method_name"]: Method(name=method["method_name"], identifier=method["id"]) for method in data
    }

    results: List[Method] = list(existing_methods.values())

    # Add missing methods
    for name in method_names:
        if name not in existing_methods:
            payload = {"method_name": name}
            try:
                post_response = session.post(f"{base_url}", json=payload, timeout=10)
                post_response.raise_for_status()
                created = post_response.json()["data"]
                method = Method(name=created["method_name"], identifier=created["id"])
                results.append(method)
            except requests.RequestException as e:
                return Result(error=f"Failed to create method '{name}': {e}")

    return Result(value=results)


def get_aliquot(aliquot_id: str) -> Result[SampleContainer, str]:
    if not aliquot_id:
        return Result(error="Aliquot ID cannot be empty")

    # base_url = "https://emi-collection.unifr.ch/directus/items/Aliquoting_Data"

    # params = {
    #     "filter[sample_container][container_id][_eq]": aliquot_id,
    #     "fields": "sample_container.container_id,sample_container.id",
    # }

    try:
        # TODO: Uncomment this for production use
        # response = requests.get(f"{base_url}", params=params, timeout=10)
        # response.raise_for_status()
        # data = response.json().get("data", [])
        # if not data:
        #     return Result(error=f"No aliquot found with ID: {aliquot_id}")
        # sample_container = SampleContainer(
        #     name=data[0]["sample_container"]["container_id"], identifier=data[0]["sample_container"]["id"]
        # )
        sample_container = SampleContainer(name=aliquot_id, identifier=1)  # Placeholder for testing
    except requests.RequestException as e:
        return Result(error=e)

    return Result(value=sample_container)


def insert_ms_sample(token: str, timestamp: str, operator: str, sample: SampleData) -> Result[bool, str]:
    payload = []
    for method in sample.injection_methods:
        filename = timestamp + "_" + operator + "_" + method.name + "_" + sample.parent_sample_container.name
        payload.append(
            {
                "filename": filename,
                "parent_sample_container": sample.parent_sample_container.identifier,
                "injection_volume": sample.injection_volume,
                "injection_volume_unit": sample.injection_volume_unit,
                "injection_method": method.identifier,
                "instrument_used": sample.instrument.identifier,
                "batch": sample.batch.identifier,
            }
        )

    # url = "https://emi-collection.unifr.ch/directus/items/MS_Data"
    # headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        # TODO: Uncomment this for production use
        # response = requests.post(url=url, json=payload, timeout=10, headers=headers)
        # response.raise_for_status()
        return Result(value=True)
    except requests.RequestException as e:
        return Result(error=f"Failed to insert samples: {e}")
