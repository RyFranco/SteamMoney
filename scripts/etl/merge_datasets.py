import pandas as pd
import os

def create_merged_df_for_platforms():
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
    platform_df = platform_df.drop(columns=["rating", "positive_ratio", "price_original", "price_final", "discount", "steam_deck"])
    merged_df = pd.merge(main_df, platform_df, on='app_id')
    merged_df = merged_df.drop(columns=["game", "date_release"])
    return merged_df

merged_df = create_merged_df_for_platforms()

def create_merged_df_for_categories_tags_and_genre(merged_df):
    categories_tags_and_genre_df = pd.read_csv("../../data/raw/games.csv", index_col=False)
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

# Save the merged dataframe to a pickle file because pickle is more efficient for storing dataframes
def save_merged_df(merged_df):
    interim_path = "../../data/interim/merged_data.pkl"
    os.makedirs(os.path.dirname(interim_path), exist_ok=True)
    merged_df.to_pickle(interim_path)
    print(f"Merged dataset saved to {interim_path}")


save_merged_df(merged_df)
