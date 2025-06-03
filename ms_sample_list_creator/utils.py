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
