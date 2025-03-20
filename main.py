from strip_and_clean import clean_and_extract_words
from find_words import load_movie_data, find_matching_movies
import nltk



def main():
    print("Welcome to the Movie Search Engine")
    print("----------------------------------")
    print("Type 'exit' to quit the program")

    # Load the movie data at startup
    print("\nLoading movie database...")
    movie_df = load_movie_data("cleaned_data.csv")

    if movie_df is None:
        print("Failed to load movie database. Exiting program.")
        return

    print("Database loaded successfully!")

    while True:
        # Get user input
        query = input("\nEnter your search query: ")

        # Check if user wants to exit
        if query.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break

        # Process the query to extract important words
        important_words = clean_and_extract_words(query)

        # Display extracted words
        print("\nYour query:", query)
        print("Extracted important words:", important_words)
        print("Number of important words extracted:", len(important_words))

        # If no words were extracted, continue to next iteration
        if not important_words:
            print("No searchable words found. Please try another query.")
            continue

        # Search for matching movies
        top_matches = find_matching_movies(movie_df, important_words)

        # Display results
        print("\nTop matching movies:")
        if not top_matches:
            print("No matches found.")
        else:
            for i, (title, count, matched) in enumerate(top_matches):
                print(f"{i + 1}. {title} - {count} matches")
                print(f"   Matched words: {', '.join(matched)}")


if __name__ == "__main__":
    main()