'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
import datetime

# Build the graph
g = nx.Graph()

# Initialize a list to store edges for DataFrame creation
edges = []

# Load in the dataset
with open('data/imdb_movies_2000to2022.prolific.json') as in_file:
    for line in in_file:
        this_movie = json.loads(line)

        # Add nodes for each actor
        for actor_id, actor_name in this_movie['actors']:
            g.add_node(actor_id, label=actor_name)
        
        # Create edges between all pairs of actors in the same movie
        i = 0
        for left_actor_id, left_actor_name in this_movie['actors']:
            for right_actor_id, right_actor_name in this_movie['actors'][i + 1:]:
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                    g.add_edge(left_actor_id, right_actor_id, weight=1)
                edges.append({
                    'left_actor_name': left_actor_name,
                    '<->': '<->',
                    'right_actor_name': right_actor_name
                })
            i += 1

# Define the current datetime for file naming
current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Create a DataFrame from the edges list
df_edges = pd.DataFrame(edges)

# Calculate degree centrality metrics
centrality = nx.degree_centrality(g)
centrality_df = pd.DataFrame.from_dict(centrality, orient='index', columns=['degree_centrality'])

# Get the top 10 nodes by degree centrality
top_10_central = centrality_df.nlargest(10, 'degree_centrality')
top_10_central['name'] = top_10_central.index.map(lambda x: g.nodes[x]['label'])

# Save the top 10 central nodes to a CSV file
output_centrality_path = f'data/network_centrality_{current_datetime}.csv'
top_10_central.to_csv(output_centrality_path, index=True)

# Output the final DataFrame to a CSV named 'network_edges_{current_datetime}.csv' to `/data`
output_edges_path = f'data/network_edges_{current_datetime}.csv'
df_edges.to_csv(output_edges_path, index=False)

# Print the info below
print("Nodes:", len(g.nodes))
print(f"Network centrality metrics saved to {output_centrality_path}")
print("Top 10 most central nodes:")
print(top_10_central[['name', 'degree_centrality']])
print(f"Edges saved to {output_edges_path}")
