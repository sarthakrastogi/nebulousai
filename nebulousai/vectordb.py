from litellm import embedding
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text):
    return embedding(model="text-embedding-ada-002", input=text).data[0]['embedding']

def vector_search(tools, task_embedding):
    similarities = [cosine_similarity([task_embedding], [tool.description_embedding])[0][0] for tool in tools]
    best_tool = max(zip(tools, similarities), key=lambda x: x[1])[0]
    return best_tool