import numpy as np
from qdrant_client import QdrantClient


class EMA:
    """
    Exponentional moving average
    """
    def __init__(self, alpha = 0.5):
        self.alpha = alpha
        self.previous_ema = None
    
    def update(self, vector):
        if self.previous_ema is None:
            self.previous_ema = vector
        else:
            self.previous_ema = self.alpha * vector + (1 - self.alpha) * self.previous_ema
        return self.previous_ema


class Recommender:
    """
    Main class for recomend videos
    """
    def __init__(self, user_vector):
        self.previously_seen = [] 
        self.user_vector = user_vector
        self.EMA_counter = EMA(0.5)
        self.EMA_counter.update(self.user_vector)
        self.client = QdrantClient(host='51.250.12.111', port=6333)
        self.collection_name = "video_vectors"
        self.user_collection_name = 'user_vectors'
        self.check = None
        
        
    def get_vector_video(self, video_id):
        results = self.client.retrieve(collection_name=self.collection_name, ids=video_id, with_vectors=True)
        result_dict = dict(zip([result.id for result in results], [result.vector for result in results]))
        return result_dict
    
    
    def update_user_vector(self, dict_front):
        current_videos_streamlit = self.previously_seen[-10:]
        vectores_videos = np.array(list(self.get_vector_video(current_videos_streamlit).values())) # 10x95
        durations = np.array([response_metrics[0] * 0.01 for response_metrics in dict_front.values()]).reshape((10, 1)) # 10x1
        likes = np.array([response_metrics[1] for response_metrics in dict_front.values()]).reshape((10, 1)) # 10x1
        dislikes = np.array([response_metrics[2] for response_metrics in dict_front.values()]).reshape((10, 1)) # 10x1
        logical_good = (likes^dislikes)
        # ----------------------------------------------------
        coeffs = durations * (logical_good * (likes  + ((-1) * dislikes)) + (~logical_good * (0.5)))
        updated_state = coeffs * vectores_videos
        # ----------------------------------------------------
        self.user_vector = self.EMA_counter.update(updated_state.sum(axis=0).reshape((95,)))
        return 0
    

    def get_nearest_users(self):
        results = self.client.search(
            collection_name=self.user_collection_name,
            query_vector=self.user_vector,
            limit=200
        )
        ids = [result.id for result in results]
        return ids
    

    def get_nearest_users_videos(self, ids, top=5):
        results = self.client.retrieve(collection_name=self.user_collection_name, ids=ids, with_vectors=True)
        result_dict = dict(zip([result.id for result in results], [result.vector for result in results]))
        nearest_videos_id = []
        for vect in result_dict.values():
            nearest_videos = self.client.search(
                collection_name=self.collection_name,
                query_vector=vect,
                limit=200
                )
            
            nearest_videos_id.extend(list([res.id for res in nearest_videos]))
        nearest_videos_id = set(nearest_videos_id).difference(set(self.previously_seen))
        new_vids = np.random.choice(list(nearest_videos_id), top)
        self.previously_seen.extend(list(new_vids))
        return dict(zip(range(10-top + 1, 11), new_vids))

    
    def get_ids(self):
        dict_first = self.get_nearest_video(top=8)
        dict_last = self.get_nearest_users_videos(self.get_nearest_users(), 2)
        dict_first.update(dict_last)
        return dict_first

    
    def get_nearest_video(self, top=5):
        self.check = self.user_vector
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=self.user_vector,
            limit=200
        )
        
        ids = [result.id for result in results]
        new_vids = list(set(ids).difference(set(self.previously_seen)))[-1:-top-1:-1]
        self.previously_seen.extend(new_vids)
        return dict(zip(range(1, top + 1), new_vids))
