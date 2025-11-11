import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from merge_datasets import create_merged_df_for_platforms

merged_df, main_df, platform_df = create_merged_df_for_platforms()

def create_review_era_viz(merged_df):
    merged_df["release_year"] = pd.to_datetime(merged_df["release"], errors='coerce').dt.year
    yearly_total = merged_df.groupby("release_year")["user_reviews"].sum().sort_index()
    yearly_total = yearly_total[yearly_total.index >= 2010]
    values = yearly_total.values
    years = yearly_total.index
    peaks, _ = find_peaks(values, height=0)
    plt.figure(figsize=(10,6))
    plt.plot(years, values, linewidth=3, color='steelblue', label='Total Reviews')
    for peak in peaks:
        plt.scatter(years[peak], values[peak], color='green', zorder=5)
        plt.text(years[peak], values[peak]*1.02, f"{values[peak]:,.0f}", 
             ha='center', fontsize=9, color='green')

    plt.axvline(2013, color='red', linestyle='--', alpha=0.5)
    plt.text(2013.1, values.max()*0.75, '2013: Steam Greenlight\nIndie Expansion', 
         rotation=90, va='center', fontsize=9, color='black')

    plt.axvline(2017, color='red', linestyle='--', alpha=0.5)
    plt.text(2017.1, values.max()*0.6, '2017: Combating Dishonest Reviews', 
         rotation=90, va='center', fontsize=9, color='black')

    plt.axvline(2019, color='red', linestyle='--', alpha=0.7)
    plt.text(2019.1, values.max()*0.4, 
         '2019: Steam adds in-game review prompts',
         rotation=90, va='center', fontsize=9, color='black')

    plt.title("Total Steam User Reviews by Release Year (with Peaks & Platform Events)", fontsize=14)
    plt.xlabel("Release Year", fontsize=12)
    plt.ylabel("Total User Reviews", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()
    

create_review_era_viz(merged_df)

