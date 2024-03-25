from litellm import embedding
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text):
    return embedding(model="text-embedding-ada-002", input=text).data[0]['embedding']

def vector_search(abilities, task_embedding):
    similarities = [cosine_similarity([task_embedding], [ability.description_embedding])[0][0] for ability in abilities]
    best_ability = max(zip(abilities, similarities), key=lambda x: x[1])[0]
    return best_ability