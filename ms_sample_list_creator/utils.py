# import csv
# from tkinter.ttk import Treeview
# from typing import Any, Dict

# import requests


# def get_primary_key(endpoint: str, identifier: str, field_name: str) -> int:
#     print(33)
#     """
#     Retrieves the primary key of an entry from a Directus collection.

#     Args:
#         endpoint (str): The API endpoint to query.
#         identifier (str): The value of the field to search for.
#         field_name (str): The field name to match the identifier against.

#     Returns:
#         int: The primary key if found, -1 otherwise.
#     """
#     try:
#         response = requests.get(endpoint)
#         response.raise_for_status()
#         data = response.json().get("data", [])
#         for item in data:
#             if str(item.get(field_name)) == identifier:
#                 return item["id"]
#     except requests.RequestException as e:
#         print(f"Error fetching primary key from {endpoint}: {e}")
#     return -1


# def directus_login(username: str, password: str) -> str:
#     print(34)
#     """
#     Logs into Directus and retrieves an access token.

#     Args:
#         username (str): Directus username.
#         password (str): Directus password.

#     Returns:
#         str: Access token if login succeeds, empty string otherwise.
#     """
#     login_url = "https://emi-collection.unifr.ch/directus/auth/login"
#     try:
#         response = requests.post(login_url, json={"email": username, "password": password})
#         response.raise_for_status()
#         return response.json()["data"]["access_token"]
#     except requests.RequestException as e:
#         print(f"Login failed: {e}")
#         return ""


# def get_directus_token(email: str, password: str) -> str:
#     print(37)
#     """Récupère un token d'authentification Directus."""
#     response = requests.post(
#         "https://emi-collection.unifr.ch/directus/auth/login", json={"email": email, "password": password}
#     )
#     response.raise_for_status()
#     return response.json()["data"]["access_token"]


# def post_sample_to_directus(token: str, sample_data: Dict[str, Any]) -> Dict[str, Any]:
#     print(38)
#     """Envoie un échantillon à Directus."""
#     url = "https://emi-collection.unifr.ch/directus/items/MS_Data"
#     headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
#     response = requests.post(url, headers=headers, json=sample_data)
#     response.raise_for_status()
#     return response.json()


# def export_treeview_to_csv(treeview: Treeview, file_path: str) -> None:
#     print(39)
#     """Exporte le contenu d'un Treeview vers un fichier CSV."""
#     with open(file_path, mode="w", newline="") as file:
#         writer = csv.writer(file)
#         columns = treeview["columns"]
#         writer.writerow(columns)
#         for row in treeview.get_children():
#             writer.writerow(treeview.item(row)["values"])


# from typing import Dict

# import requests

# # def post_sample_with_retry(
# #     session: DirectusSessionData, sample: dict, login_func: Callable[[], DirectusSessionData]
# # ) -> dict:
# #     try:
# #         return post_sample_to_directus(session.access_token, sample)
# #     except requests.HTTPError as e:
# #         if e.response.status_code == 401:
# #             # Token expiré : se reconnecter
# #             new_session = login_func()
# #             session.access_token = new_session.access_token
# #             return post_sample_to_directus(session.access_token, sample)
# #         else:
# #             raise
