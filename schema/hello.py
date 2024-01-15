import requests
import json
import pandas as pd
from typing import TypedDict, List, Optional

class FundDataset(TypedDict):
    fund_name: str
    nav: int

class ApiResponse(TypedDict):
    datasets: List[FundDataset]

def fetch_data_from_api() -> Optional[ApiResponse]:
    url = "https://developer.am.mufg.jp/fund_information_latest/fund_cd/253266"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def process_data_with_pandas(data: ApiResponse) -> str:
    if data and "datasets" in data:
        df = pd.DataFrame(data["datasets"])
        fund_name = df.iloc[0]["fund_name"]
        nav = df.iloc[0]["nav"]
        return f"Fund Name: {fund_name}, NAV: {nav}"
    else:
        return "No data available"

def resolve_hello(*_, name: str = "stranger") -> str:
    data = fetch_data_from_api()
    processed_data = process_data_with_pandas(data)
    return f"Hello, {name}! {processed_data}"
