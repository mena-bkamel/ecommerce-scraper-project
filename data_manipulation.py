import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from textblob import TextBlob


class PriceAnalysis:
    def __init__(self):
        self.df = None

    def load_data(self, file_path: tuple | list):
        """
        Load a CSV file and merge it into the DataFrame.
        """
        data_frames = [pd.read_csv(file) for file in file_path]
        if data_frames:
            self.df = pd.concat(data_frames, ignore_index=True)
        else:
            print("No files loaded.")

        self.display()
        return self

    def clean_df(self):
        """
        Clean the DataFrame: strip column names, handle missing values, and clean data.
        """
        if self.df is not None:
            if 'Price' in self.df.columns:
                self.df['Price'] = self.df['Price'].replace(r"[\$,]", "", regex=True).astype(float)
            self.df.dropna()
        else:
            print("No data loaded to clean.")

        self.display()
        return self

    def display(self, rows=5):
        """
        Display the first few rows of the DataFrame.
        """
        if self.df is not None:
            print(self.df.head(rows))
        else:
            print("No data to display.")
        return self

    def save(self, output_file):
        """
        Save the cleaned DataFrame to a CSV file.
        """
        if self.df is not None:
            self.df.to_csv(output_file, index=False)
            print(f"Data saved to {output_file}.")
        else:
            print("No data to save.")
        return self

    def get_platform_stats(self):
        """
        Display descriptive statistics of prices grouped by platform.
        """
        if self.df is not None:
            platform_stats = self.df.groupby('Platform')['Price'].describe()
            print(platform_stats)

        else:
            print("No data available.")
        return self

    def plot_average_prices(self):
        """
        Plot the average prices by platform as a bar chart.
        """
        if self.df is not None:
            avg_prices = self.df.groupby('Platform')['Price'].mean()
            avg_prices.plot(kind='bar', color='skyblue', figsize=(8, 5))
            plt.title('Average Prices by Platform')
            plt.ylabel('Average Price')
            plt.xlabel('Platform')
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No data available.")
        return self

    def plot_price_distributions(self):
        """
        Create a boxplot to visualize price distributions by platform.
        """
        if self.df is not None:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='Platform', y='Price', data=self.df, palette='pastel')
            plt.title('Price Distributions by Platform')
            plt.ylabel('Price')
            plt.xlabel('Platform')
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No data available.")
        return self

    def get_lowest_avg_price_platform(self):
        """
        Identify and display the platform with the lowest average price.
        """
        if self.df is not None:
            avg_prices = self.df.groupby('Platform')['Price'].mean()
            lowest_avg_price_platform = avg_prices.idxmin()
            lowest_avg_price = avg_prices.min()
            print(f"Platform with the lowest average price: {lowest_avg_price_platform} (${lowest_avg_price:.2f})")
        else:
            print("No data available.")
        return self

    def identify_price_outliers(self):
        """
        Identify and display the number of price outliers.
        """
        if self.df is not None:
            outliers = self.df[(self.df['Price'] > self.df['Price'].quantile(0.95)) |
                               (self.df['Price'] < self.df['Price'].quantile(0.05))]
            print(f"Number of outliers: {len(outliers)}")
        else:
            print("No data available.")
        return self

    def perform_sentiment_analysis(self):
        """
        Perform sentiment analysis on the 'Review' column and create a new 'Sentiment' column.
        """
        if self.df is not None and 'Review' in self.df.columns:
            self.df['Sentiment'] = self.df['Review'].apply(self.analyze_sentiment)
            print("Sentiment analysis completed.")
        else:
            print("Review column not found.")
        return self

    def analyze_sentiment(self, review):
        """
        Analyze the sentiment of a given review.
        Returns: 'positive', 'neutral', or 'negative'
        """
        analysis = TextBlob(review)
        # Classify the polarity of the review: positive, neutral, or negative
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def plot_sentiment_distribution(self):
        """
        Visualize the distribution of sentiment (positive, neutral, negative).
        """
        if self.df is not None and 'Sentiment' in self.df.columns:
            sentiment_counts = self.df['Sentiment'].value_counts()
            plt.figure(figsize=(7, 7))
            sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90,
                                  colors=['#66b3ff', '#99ff99', '#ff6666'])
            plt.title("Sentiment Distribution")
            plt.ylabel('')
            plt.show()
        else:
            print("Sentiment column not found.")

    def plot_sentiment_trends(self):
        """
        Track sentiment trends over time.
        """
        if self.df is not None and 'Sentiment' in self.df.columns and 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            sentiment_trends = self.df.groupby([self.df['Date'].dt.to_period('M'), 'Sentiment']).size().unstack(
                fill_value=0)
            sentiment_trends.plot(kind='line', figsize=(10, 6), marker='o')
            plt.title("Sentiment Trends Over Time")
            plt.ylabel('Count of Sentiments')
            plt.xlabel('Month')
            plt.xticks(rotation=45)
            plt.legend(title='Sentiment', labels=['Positive', 'Neutral', 'Negative'])
            plt.show()
        else:
            print("Sentiment or Date column not found.")
