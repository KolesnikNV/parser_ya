from ast import literal_eval

import pandas as pd


async def get_excel(city, query):
    df = pd.read_csv(
        f"result_output/{query}_outputs.csv", converters={"outputs": literal_eval}
    )
    df = df.dropna(subset=["name"])
    result_df = pd.DataFrame(columns=["name", "website", "phones", "social", "count"])
    for index, row in df.iterrows():
        name = row["name"]
        website = row["website"]
        phones = (
            "".join(map(str, row["phone"]))
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
            .replace("Показать телефон", "")
        )

        social = (
            "".join(map(str, row["social"]))
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
        )

        count = df[df["name"] == name].shape[0]

        result_df = pd.concat(
            [
                result_df,
                pd.DataFrame(
                    {
                        "name": [name],
                        "website": [website],
                        "phones": [phones],
                        "social": [social],
                        "count": [count],
                    }
                ),
            ]
        )

    result_df = result_df.drop_duplicates(subset="name")
    result_df.to_excel(f"{city}_{query}.xlsx", index=False, engine="openpyxl")
