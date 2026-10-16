import pandas as pd
import matplotlib.pyplot as plt

#1. Load the Tucson AERONET 2023 Dataset
file_path ="20230101_20231231_Tucson.lev20"

df = pd.read_csv(
    file_path,
    skiprows=6,
    na_values=[-999, "-999."]
)

#step 2. keep variables needed for the analysis
df["Date"] = pd.to_datetime(
    df["Date(dd:mm:yyyy)"],
    format="%d:%m:%Y",
    errors="coerce"
)

df["AOD"] = pd.to_numeric(df["AOD_500nm"], errors="coerce")
df["AE"] = pd.to_numeric(df["440-870_Angstrom_Exponent"],errors="coerce")

df = df.dropna(subset=["Date"])

#3. calculate one daily average for each variable
daily = (
    df.groupby(df["Date"].dt.normalize())[["AOD" , "AE"]]
    .mean()
    .reset_index()
)

#4 label weekdays and weekends
daily["Day_Type"] = daily["Date"].dt.dayofweek.map(
    lambda day: "Weekend" if day >= 5 else "Weekday"
)

#5 assign day to a season
season_map= {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall", 10: "Fall", 11: "Fall",
}

daily["Season"] = daily["Date"].dt.month.map(season_map)

#arrange in order of the calendar
season_order =["Winter", "Spring", "Summer", "Fall"]

print("Number of daily records:", len(daily))
print(daily.head())

#6 overall weekday vs weekend summary
overall = daily.groupby("Day_Type")[["AOD", "AE"]].agg(
    ["count", "mean", "median", "std"]
)

print("\n0verall weekday/weekend summary:")
print(overall.round(3))

# 7. Seasonal weekday vs weekend summary
seasonal = daily.groupby(["Season", "Day_Type"])[["AOD", "AE"]].agg(
    ["count", "mean", "median", "std"]
)
print("\nSeasonal weekday/weekend summary:")
print(seasonal.round(3))

#8. calculate weekend minus weekday differences
means = daily.groupby(["Season", "Day_Type"])[["AOD", "AE"]].mean()

aod_difference = (
    means["AOD"].unstack("Day_Type")["Weekend"]
    - means["AOD"].unstack("Day_Type")["Weekday"]
)

print("\nAOD difference: weekend minus weekday")
print(aod_difference.reindex(season_order).round(4))

ae_difference = (
    means["AE"].unstack("Day_Type")["Weekend"]
    - means["AE"].unstack("Day_Type")["Weekday"]
)

print("\nAE difference: weekend minus weekday")
print(ae_difference.reindex(season_order).round(4))

# 9. Fig 1: overall daily AOD distributions
daily.boxplot(column="AOD", by="Day_Type", figsize=(7, 5))
plt.title("Daily AOD: Weekdays vs. Weekends, 2023")
plt.suptitle("")
plt.xlabel("Day Type")
plt.ylabel("Daily mean AOD at 500nm")
plt.tight_layout()
plt.savefig("figure1_AOD_weekday_weekend.png", dpi=300)
plt.show()

# 10. Fig 2: overall daily AE distributions (same approach as Fig 1)
daily.boxplot(column="AE", by="Day_Type", figsize=(7, 5))
plt.title("Daily AE: Weekdays vs. Weekends, 2023")
plt.suptitle("")
plt.xlabel("Day Type")
plt.ylabel("Daily mean AE (440-870nm)")
plt.tight_layout()
plt.savefig("figure2_AE_weekday_weekend.png", dpi=300)
plt.show()

# 11. Fig 3: seasonal AOD comparison
aod_plot = daily.pivot_table(
    index="Season", columns="Day_Type", values="AOD", aggfunc="mean"
).reindex(season_order)
aod_plot = aod_plot[["Weekday", "Weekend"]]

aod_plot.plot(kind="bar", figsize=(8, 5))
plt.title("Daily Mean AOD by Day Type and Season, 2023")
plt.xlabel("Season")
plt.ylabel("Mean Daily AOD at 500nm")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figure3_seasonal_AOD.png", dpi=300)
plt.show()

# 12. Fig 4: seasonal AE comparison
ae_plot = daily.pivot_table(
    index="Season", columns="Day_Type", values="AE", aggfunc="mean"
).reindex(season_order)
ae_plot = ae_plot[["Weekday", "Weekend"]]

ae_plot.plot(kind="bar", figsize=(8, 5))
plt.title("Daily Mean AE by Day Type and Season, 2023")
plt.xlabel("Season")
plt.ylabel("Mean daily AE (440-870nm)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figure4_seasonal_AE.png", dpi=300)
plt.show()