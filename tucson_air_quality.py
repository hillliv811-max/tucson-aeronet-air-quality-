import pandas as pd
import matplotlib.pyplot as plt

#1. load the aeronet 2025 data
file_path = "20250101_20251231_Tucson.lev20"

df= pd.read_csv(
    file_path,
    skiprows=6,
    na_values=[-999, "-999."])

#2. convert the date column
df["Date"] = pd.to_datetime(
df["Date(dd:mm:yyyy)"],
format="%d:%m:%Y",
errors="coerce",
)

#3. Keep only the columns we need
df = df[[
        "Date",
        "AOD_500nm",
        "440-870_Angstrom_Exponent"
]].copy()

#4. rename columns to make them easier to read/use
df = df.rename(columns={
    "AOD_500nm": "AOD",
    "440-870_Angstrom_Exponent": "AE"
})

#5. measurements need to me numeric
df["AOD"] = pd.to_numeric(df["AOD"], errors="coerce")
df["AE"] = pd.to_numeric(df["AE"], errors="coerce")

#6. only observations from 2025
df = df[
    (df["Date"] >= "2025-01-01") &
     (df["Date"] <= "2025-12-31")
].copy()

#7 sort the dates and set them as the index
df = df.sort_values ("Date")
df = df.set_index("Date")

print(df.head())
print(df.info())
print(df.describe())


