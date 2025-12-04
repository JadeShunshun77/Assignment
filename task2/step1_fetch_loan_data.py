import requests
import pandas as pd

INDICATORS = {
    "FR.INR.LEND": "lending_interest_rate",
    "FB.AST.NPER.ZS": "nonperforming_loan_ratio",
    "FS.AST.PRVT.GD.ZS": "credit_to_private_gdp",
}

COUNTRIES = {
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "AU": "Australia",
}


def fetch_indicator_for_countries(indicator_code: str) -> pd.DataFrame:
    rows = []
    for country_code, country_name in COUNTRIES.items():
        url = (
            f"https://api.worldbank.org/v2/country/{country_code}"
            f"/indicator/{indicator_code}?format=json&per_page=2000"
        )
        print(f"Fetching {indicator_code} for {country_code} ...")

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print("Warning:", e)
            continue

        data = r.json()
        if len(data) < 2:
            continue
        observations = data[1]

        for obs in observations:
            rows.append({
                "country_code": country_code,
                "country_name": country_name,
                "year": int(obs["date"]),
                indicator_code: pd.to_numeric(obs["value"], errors="coerce"),
            })
    return pd.DataFrame(rows)



def build_loan_dataset() -> pd.DataFrame:
    dfs = []
    for indicator_code in INDICATORS.keys():
        df_ind = fetch_indicator_for_countries(indicator_code)
        dfs.append(df_ind)

    df_merged = dfs[0]
    for df in dfs[1:]:
        df_merged = df_merged.merge(
            df,
            on=["country_code", "country_name", "year"],
            how="outer",
        )

    df_merged = df_merged.rename(columns=INDICATORS)
    df_merged = df_merged.sort_values(["country_code", "year"])
    return df_merged

if __name__ == "__main__":
    df = build_loan_dataset()
    print("Dataset shape (rows, columns):", df.shape)
    print(df.head())

    output_path = "loan_worldbank_dataset.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Saved to {output_path}")

