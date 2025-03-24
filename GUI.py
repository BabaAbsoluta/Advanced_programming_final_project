import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from strip_and_clean import clean_and_extract_words
from find_words import load_movie_data, find_matching_movies


class MovieSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Search Engine")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)

        self.movie_df = None
        self.create_widgets()

        self.status_var.set("Loading movie database...")
        loading_thread = threading.Thread(target=self.load_data)
        loading_thread.daemon = True
        loading_thread.start()

    def load_data(self):
        self.movie_df = load_movie_data("cleaned_data.csv")

        if self.movie_df is None:
            self.status_var.set("Failed to load movie database.")
        else:
            self.status_var.set("Database loaded successfully! Ready to search.")
            self.search_button.config(state=tk.NORMAL)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        # Search frame (query input and button)
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        # Search label
        search_label = ttk.Label(search_frame, text="Enter your search query:")
        search_label.pack(side=tk.LEFT, padx=(0, 10))

        # Search entry
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", self.search)

        # Search button
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))
        self.search_button.config(state=tk.DISABLED)  # Initially disabled until data loads

        # Results notebook with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.results_tab = ttk.Frame(self.notebook)
        self.words_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.results_tab, text="Results")
        self.notebook.add(self.words_tab, text="Query Analysis")

        # Results text area
        self.results_text = scrolledtext.ScrolledText(self.results_tab, wrap=tk.WORD, font=("Segoe UI", 11))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)

        # Configure tags for better font styling
        self.results_text.tag_config("title", font=("Segoe UI", 14, "bold"))
        self.results_text.tag_config("label", font=("Segoe UI", 11, "bold"))

        # Words text area
        self.words_text = scrolledtext.ScrolledText(self.words_tab, wrap=tk.WORD, font=("Segoe UI", 11))
        self.words_text.pack(fill=tk.BOTH, expand=True)
        self.words_text.config(state=tk.DISABLED)

    def search(self, event=None):
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.words_text.config(state=tk.NORMAL)
        self.words_text.delete(1.0, tk.END)

        # Get query
        query = self.search_entry.get().strip()

        if not query:
            self.status_var.set("Please enter a search query.")
            self.results_text.config(state=tk.DISABLED)
            self.words_text.config(state=tk.DISABLED)
            return

        if self.movie_df is None:
            self.status_var.set("Database not loaded yet. Please wait.")
            self.results_text.config(state=tk.DISABLED)
            self.words_text.config(state=tk.DISABLED)
            return

        # Process query
        important_words = clean_and_extract_words(query)

        # Update Words tab
        self.words_text.insert(tk.END, f"Your query: {query}\n\n")
        self.words_text.insert(tk.END, f"Extracted important words: {important_words}\n")
        self.words_text.insert(tk.END, f"Number of important words extracted: {len(important_words)}\n")
        self.words_text.config(state=tk.DISABLED)

        # Handle no words case
        if not important_words:
            self.results_text.insert(tk.END, "No searchable words found. Please try another query.")
            self.results_text.config(state=tk.DISABLED)
            self.status_var.set("No searchable words found.")
            return

        # Search for matches
        top_matches = find_matching_movies(self.movie_df, important_words)

        # Display results
        if not top_matches:
            self.results_text.insert(tk.END, "No matches found.")
        else:
            self.results_text.insert(tk.END, "🎬 Top Matching Movies\n\n", "title")
            for i, (row, count, matched) in enumerate(top_matches):
                self.results_text.insert(tk.END, f"{'-'*60}\n")
                self.results_text.insert(tk.END, f"{i + 1}. {row['Name']}\n", "title")
                self.results_text.insert(tk.END, "Matched Words: ", "label")
                self.results_text.insert(tk.END, f"{', '.join(matched)} ({count} match{'es' if count != 1 else ''})\n\n")

                self.results_text.insert(tk.END, "🕒 Duration: ", "label")
                self.results_text.insert(tk.END, f"{row.get('Duration', 'N/A')}\n")
                self.results_text.insert(tk.END, "🎭 Genre: ", "label")
                self.results_text.insert(tk.END, f"{row.get('Genre', 'N/A')}\n")
                self.results_text.insert(tk.END, "⭐ IMDb Rating: ", "label")
                self.results_text.insert(tk.END, f"{row.get('IMDb Rating', 'N/A')}\n")
                self.results_text.insert(tk.END, "🎬 Director: ", "label")
                self.results_text.insert(tk.END, f"{row.get('Director', 'N/A')}\n")
                self.results_text.insert(tk.END, "🎞️ Stars: ", "label")
                self.results_text.insert(tk.END, f"{row.get('Stars', 'N/A')}\n\n")
                self.results_text.insert(tk.END, "🎞️ Plot: ", "label")
                self.results_text.insert(tk.END, f"{row.get('Plot', 'N/A')}\n\n")

                self.results_text.insert(tk.END, f"{'-'*60}\n\n")

        self.results_text.config(state=tk.DISABLED)
        self.status_var.set(f"Found {len(top_matches)} matching movies.")

        # Switch to results tab
        self.notebook.select(0)


def main():
    root = tk.Tk()
    app = MovieSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
