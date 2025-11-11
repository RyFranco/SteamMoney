import pandas as pd
import os

def create_merged_df_for_platforms():
    main_df = pd.read_csv("../../data/raw/initial_games_data.csv")
    platform_df = pd.read_csv("../../data/raw/platform_game_data.csv")
    # Drop unnecessary index column
    main_df = main_df.drop(columns=["Unnamed: 0"]) 
    # Keep only the first 4 columns
    main_df = main_df.iloc[:, :4] 
    # Keeps the first occurrence of each game via link
    main_df = main_df.drop_duplicates(subset='link', keep='first')
    # Extract app_id from the link column and convert to integer
    main_df["app_id"] = main_df["link"].str.extract(r'/app/(\d+)/')
    main_df['app_id'] = main_df['app_id'].astype(int) 
    # Drops the link column since we have the app_id now
    main_df = main_df.drop(columns=['link'])
    # Reorder columns to have 'app_id' first, not necessary but cleaner
    cols = ['app_id'] + [c for c in main_df.columns if c != 'app_id']
    main_df = main_df[cols]
    # Keep only relevant columns from platform_df
    platform_df = platform_df.drop(columns=["rating", "positive_ratio", "price_original", "price_final", "discount", "steam_deck"])
    merged_df = pd.merge(main_df, platform_df, on='app_id')
    merged_df = merged_df.drop(columns=["game", "date_release"])
    return merged_df

merged_df = create_merged_df_for_platforms()

def create_merged_df_for_categories_tags_and_genre(merged_df):
    categories_tags_and_genre_df = pd.read_csv("../../data/raw/games.csv", index_col=False)
    # Picking the attributes to keep for dataset 3
    categories_tags_and_genre_df = categories_tags_and_genre_df[["AppID", "Categories", "Genres", "Tags", "Price"]]
    categories_tags_and_genre_df = categories_tags_and_genre_df.rename(columns={"AppID": "app_id"})
    merged_df = pd.merge(
        merged_df,
        categories_tags_and_genre_df,
        on="app_id",
        how="inner" 
    )
    return merged_df
    
merged_df = create_merged_df_for_categories_tags_and_genre(merged_df)

def create_merged_df_for_sentiment(merged_df):
    df_sentiment = pd.read_pickle(".../../../../data/processed/app_level_sentiment.pkl")
    merged_df = merged_df.merge(
        df_sentiment[["app_id", "avg_sentiment"]],
        on="app_id",
        how="left" 
    )
    # Create a binary column indicating presence of sentiment data
    merged_df['has_sentiment'] = merged_df['avg_sentiment'].notna().astype(int)
    return merged_df

merged_df = create_merged_df_for_sentiment(merged_df)

# Save the merged dataframe to a pickle file because pickle is more efficient for storing dataframes
def save_merged_df(merged_df):
    interim_path = "../../data/interim/merged_data.pkl"
    os.makedirs(os.path.dirname(interim_path), exist_ok=True)
    merged_df.to_pickle(interim_path)
    print(f"Merged dataset saved to {interim_path}")


save_merged_df(merged_df)

