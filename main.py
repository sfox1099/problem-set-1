'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import analysis_network_centrality
import analysis_similar_actors_genre

# Ingest and save the imbd_movies dataset
def ingestion(url, path):
    response = requests.get(url)
    with open(path, 'w') as f:
        json.dump(response.json(), f)


# Call functions / instanciate objects from the two analysis .py files
def main():
    dataset_url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    save_path = "data/imdb_movies_2000to2022.prolific.json"
    ingestion(dataset_url, save_path)

    with open(save_path, 'r') as f:
        imdb_movies = json.load(f)

    analysis_similar_actors_genre.analyze_genre(imdb_movies)
    analysis_network_centrality.analyze_centrality(imdb_movies)
    
if __name__ == "__main__":
    main()