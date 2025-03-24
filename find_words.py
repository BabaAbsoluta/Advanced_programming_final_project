import pandas as pd


def load_movie_data(csv_path):
    try:
        # Load CSV file into DataFrame
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded {len(df)} movies from {csv_path}")
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None


def find_matching_movies(df, search_words):
    # Dictionary to store match counts for each movie
    match_counts = {}

    # Dictionary to store which words matched for each movie
    matched_words = {}

    # Dictionary to store the whole row
    matched_rows = {}

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        movie_title = row['Name'] if 'Name' in row else row[0]  # Handle different column names
        match_count = 0
        words_matched = set()

        # Convert the entire row to a string for searching
        row_str = ' '.join(str(cell).lower() for cell in row)

        # Check for each search word
        for word in search_words:
            if word.lower() in row_str:
                match_count += 1
                words_matched.add(word)

         # Store the match count and matched words and whole tow if there were any matches
        if match_count > 0:
            match_counts[movie_title] = match_count
            matched_words[movie_title] = words_matched
            matched_rows[movie_title] = row  

    # Sort movies by match count (descending)
    sorted_movies = sorted(match_counts.items(), key=lambda x: x[1], reverse=True)

    # Get the top 3 matches (or fewer if there aren't 3 matches)
    top_matches = []
    for title, count in sorted_movies[:3]:
        top_matches.append((matched_rows[title], count, matched_words[title]))

    return top_matches

