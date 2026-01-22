import requests
from typing import List, Dict

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def pubmed(
    query: str,
    max_results: int = 5,
) -> List[Dict]:
    """
    search article from text request

    Args:
        query (str): ex: "type 2 diabetes metformin"
        max_results (int): max result number

    Returns:
        List[Dict]: list of articles
    """

    search_resp = requests.get(
        f"{NCBI_BASE_URL}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
        },
        timeout=10,
    )
    search_resp.raise_for_status()
    id_list = search_resp.json()["esearchresult"]["idlist"]

    if not id_list:
        return []

    summary_resp = requests.get(
        f"{NCBI_BASE_URL}/esummary.fcgi",
        params={
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json",
        },
        timeout=10,
    )
    summary_resp.raise_for_status()
    summaries = summary_resp.json()["result"]

    results = []
    for pmid in id_list:
        item = summaries.get(pmid)
        if not item:
            continue

        results.append(
            {
                "pmid": pmid,
                "title": item.get("title"),
                "journal": item.get("fulljournalname"),
                "year": item.get("pubdate", "")[:4],
                "authors": [a["name"] for a in item.get("authors", [])],
            }
        )

    return results
