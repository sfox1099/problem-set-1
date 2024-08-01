'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import pandas as pd
import json
from sklearn.metrics import DistanceMetric
import datetime

# Define the current datetime for file naming
current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Load the dataset
with open('data/imdb_movies_2000to2022.prolific.json') as in_file:
    movies = [json.loads(line) for line in in_file]

# Initialize dictionaries to store actor genre counts
actor_genre_count = {}
genre_set = set()

# Populate the dictionaries with genre counts per actor
for movie in movies:
    genres = movie.get('genres', [])
    for actor_id, actor_name in movie.get('actors', []):
        if actor_id not in actor_genre_count:
            actor_genre_count[actor_id] = {'name': actor_name}
        for genre in genres:
            genre_set.add(genre)
            if genre not in actor_genre_count[actor_id]:
                actor_genre_count[actor_id][genre] = 0
            actor_genre_count[actor_id][genre] += 1

# Create a DataFrame from the actor genre count dictionary
genre_list = sorted(genre_set)  # Sort genres for consistent column order
df = pd.DataFrame.from_dict(actor_genre_count, orient='index').fillna(0)
df = df.reindex(columns=genre_list, fill_value=0)

# Define the query actor
query_actor_id = 'nm1165110'

# Check if the query actor is in the DataFrame
if query_actor_id not in df.index:
    raise ValueError(f"Query actor ID {query_actor_id} is not in the dataset")

# Extract the query actor's feature vector
query_vector = df.loc[query_actor_id].values.reshape(1, -1)

# Calculate cosine distance between the query actor and all other actors
dist = DistanceMetric.get_metric('cosine')
distances = dist.pairwise(df.values, query_vector).flatten()

# Create a DataFrame to hold the distances
dist_df = pd.DataFrame({
    'actor_id': df.index,
    'name': df['name'],
    'distance': distances
})

# Find the top 10 most similar actors
top_10_similar = dist_df.nsmallest(10, 'distance')

# Save the top 10 similar actors to a CSV file
output_path = f'data/similar_actors_genre_{current_datetime}.csv'
top_10_similar.to_csv(output_path, index=False)

# Print the results
print(f"Top 10 most similar actors to {actor_genre_count[query_actor_id]['name']} based on cosine distance:")
print(top_10_similar[['actor_id', 'name', 'distance']])
print(f"Results saved to {output_path}")