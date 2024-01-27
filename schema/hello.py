import os
import requests
import json
import pandas as pd
from typing import TypedDict, List, Optional

class FundDataset(TypedDict):
    fund_name: str # ファンドID
    nav: int # 基準価格
    cmp_prev_day: int # 前日比価格
    percentage_change: int # 前月比率


class ApiResponse(TypedDict):
    datasets: List[FundDataset]

def fetch_data_from_api(id: int) -> Optional[ApiResponse]:
    base_url = os.environ.get("MUFG_API_BASE_URL")
    if not base_url:
        raise RuntimeError("MUFG_API_BASE_URL environment variable is not set")

    url = f"{base_url}/fund_information_latest/fund_cd/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def process_data_with_pandas(data: ApiResponse) -> dict:
    if data and "datasets" in data:
        df = pd.DataFrame(data["datasets"])
        fund = {
            "id": "253266",  # IDは固定値または動的に設定
            "fundName": df.iloc[0]["fund_name"],
            "currentPrice": float(df.iloc[0]["nav"]),
            "currentPriceGets": float(df.iloc[0]["cmp_prev_day"]),
            "currentRate": float(df.iloc[0]["percentage_change"])
        }
        return fund
    else:
        return {"id": "", "fundName": "", "nav": 0.0}

def resolve_hello(*_, id: int) -> dict:
    data = fetch_data_from_api(id)
    fund_data = process_data_with_pandas(data)
    return fund_data