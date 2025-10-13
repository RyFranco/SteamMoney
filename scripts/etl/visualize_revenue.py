import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def estimate_copies_sold(row):
    year = row["release_year"]
    reviews = row["user_reviews"]

    if year < 2014:
        multiple = 60
    elif 2014 <= year <= 2016:
        multiple = 50
    elif year == 2017:
        multiple = 40
    elif 2018 <= year <= 2019:
        multiple = 35
    else:  # 2019 and later
        multiple = 30

    return reviews * multiple

def log_normalized_revenue_histogram(paid_df):
    # Create the log-transformed revenue with log1p to handle zero values safely 
    # because log(0) is undefined if there are any zero revenues
    paid_df["log_estimated_revenue"] = np.log1p(paid_df["estimated_revenue"])
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    # First plot with raw estimated revenue to show the wide range
    plt.hist(paid_df["estimated_revenue"], bins=50, edgecolor='black')
    plt.title("Estimated Revenue (Raw Scale)")
    plt.xlabel("Revenue ($)")
    plt.ylabel("Count")
    plt.xscale("log")
    
    # Second plot with log-normalized revenue to show distribution better
    plt.subplot(1, 2, 2)
    plt.hist(paid_df["log_estimated_revenue"], bins=50, edgecolor='black', color='orange')
    plt.title("Estimated Revenue (Log-Normalized)")
    plt.xlabel("log(1 + Revenue)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

def scatter_reviews_vs_revenue(paid_df):
    # Scatter plot of user reviews vs estimated revenue
    plt.figure(figsize=(10, 6))
    plt.scatter(paid_df["user_reviews"], paid_df["estimated_revenue"], alpha=0.6, color='orange', edgecolor='k')
    plt.title("Game-Level Estimated Revenue vs User Reviews (Paid Games)")
    plt.xlabel("User Reviews")
    plt.ylabel("Estimated Revenue ($)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def smoothed_trend_line(paid_df):
    # Create bins for user reviews on a logarithmic scale
    # Logarthmic bins are divided into 30 intervals where the min and max are determined by the data
    bins = np.logspace(np.log10(paid_df["user_reviews"].min()+1),
            np.log10(paid_df["user_reviews"].max()), 30)
    
    # Review_bin column categorizes user reviews into these logarithmic bins
    # pd.cut assigns each review count to a bin
    paid_df["review_bin"] = pd.cut(paid_df["user_reviews"], bins=bins)
    
    # Trend DataFrame calculates the mean estimated revenue for each review bin
    # observed=True ensures only bins with data are included
    trend = paid_df.groupby("review_bin", observed=True)["estimated_revenue"].mean().reset_index()
    trend["midpoint"] = [interval.mid for interval in trend["review_bin"]]
    plt.figure(figsize=(10,6))
    # Plots the raw data points in light gray for context
    plt.scatter(paid_df["user_reviews"], paid_df["estimated_revenue"], alpha=0.3, color='lightgray', s=10)
    # Trend line in steelblue for visibility
    plt.plot(trend["midpoint"], trend["estimated_revenue"], color='steelblue', linewidth=3)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Smoothed Relationship: User Reviews vs Estimated Revenue")
    plt.xlabel("User Reviews")
    plt.ylabel("Estimated Revenue ($)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def visualize_revenue_distribution():
    merged_df = pd.read_pickle("../../data/interim/merged_data.pkl")
    merged_df["release_year"] = pd.to_datetime(merged_df["release"]).dt.year
    merged_df["copies_sold_reviews_proxy"] = merged_df.apply(estimate_copies_sold, axis=1)
    merged_df["estimated_revenue"] = merged_df["Price"] * merged_df["copies_sold_reviews_proxy"]
    merged_df["f2p_flag"] = merged_df["Price"] == 0
    paid_df = merged_df[merged_df["Price"] > 0].copy()
    log_normalized_revenue_histogram(paid_df)
    scatter_reviews_vs_revenue(paid_df)
    smoothed_trend_line(paid_df)
    return merged_df

merged_df = visualize_revenue_distribution()
    
