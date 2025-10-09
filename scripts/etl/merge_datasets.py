import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def created_merged_df():
    main_df = pd.read_csv("../../data/raw/initial_games_data.csv")
    platform_df = pd.read_csv("../../data/raw/platform_game_data.csv")
    main_df = main_df.drop(columns=["Unnamed: 0"]) # Drop unnecessary index column
    main_df = main_df.iloc[:, :4] # Keep only the first 4 columns
    main_df = main_df.drop_duplicates(subset='link', keep='first')
    main_df["app_id"] = main_df["link"].str.extract(r'/app/(\d+)/')
    main_df['app_id'] = main_df['app_id'].astype(int) 
    main_df = main_df.drop(columns=['link'])
    cols = ['app_id'] + [c for c in main_df.columns if c != 'app_id']
    main_df = main_df[cols]
    print(f"Main Dataset: {main_df.shape[0]} Second dataset: {platform_df.shape[0]}")
    platform_df = platform_df.drop(columns=["rating", "positive_ratio", "price_final", "discount", "steam_deck"])
    merged_df = pd.merge(main_df, platform_df, on='app_id')
    merged_df = merged_df.drop(columns=["game", "date_release"])
    return merged_df, main_df, platform_df

merged_df, main_df, platform_df = created_merged_df()



