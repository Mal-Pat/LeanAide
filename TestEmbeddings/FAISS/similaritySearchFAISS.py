# Write the input theorem at the end of the `main` function

import os
import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Config
MODEL_NAME = 'all-MiniLM-L6-v2' 
THEOREMS_FILE_PATH = '/home/malpat/LeanAide/TestEmbeddings/UnpickledFiles/prompt_emb.txt'
INDEX_FILE_PATH = '/home/malpat/LeanAide/TestEmbeddings/FAISSIndex/theorems_all-MiniLM-L6-v2.index'
OUTPUT_FILE_PATH = '/home/malpat/LeanAide/TestEmbeddings/NearestTheoremsResults/resultsFAISS.txt'

def check_GPU():
  try:
      res = faiss.StandardGpuResources()
      index = faiss.GpuIndexFlatL2(res, 10)
      print("FAISS GPU index created successfully.")
  except Exception as e:
      print(f"Failed to create FAISS GPU index: {e}")

def load_theorems(file_path):
    print(f"Loading theorems from '{file_path}'...")
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        theorems = [theorem.strip() for theorem in file_content.split("===")]
    print(f"Found {len(theorems)} theorems.")
    return theorems

def create_and_save_index(theorems, model, index_path):
    print("No existing index found. Creating a new one...")
    start_time = time.time()
    
    # Encode all theorems into vectors
    print(f" modeli Embedding {len(theorems)} theorems with '{MODEL_NAME}'... (This may take a while)")
    embeddings = model.encode(theorems, show_progress_bar=True)
    
    # Get the dimension of the embeddings
    d = embeddings.shape[1]
    
    # Build a FAISS index. IndexFlatL2 is a basic but effective index for dense vectors.
    # It performs an exhaustive search.
    index = faiss.IndexFlatL2(d)
    index.add(embeddings) # Add the theorem vectors to the index
    
    # Save the index to disk
    print(f"Saving index to '{index_path}'...")
    faiss.write_index(index, index_path)
    
    end_time = time.time()
    print(f"Index created and saved in {end_time - start_time:.2f} seconds.")
    
    return index

def find_similar_theorems(query, model, index, theorems_list, output_file, k=10):
    start_time = time.time()
    
    # Encode the query theorem into a vector
    query_vector = model.encode([query])
    
    # Search the FAISS index
    # D: distances, I: indices of the nearest neighbors
    distances, indices = index.search(query_vector, k)
    
    end_time = time.time()
    print(f"🔍 Search completed in {end_time - start_time:.4f} seconds.")
    
    # Print and write the results into output file
    print(f"\nTop {k} most similar theorems to: '{query}'\n" + "="*50)
    with open(output_file, 'a', encoding='utf-8') as file:
      file.write(f"THEOREM : {query}\n\nNEAREST EMBEDDINGS:\n\n")
      for i, idx in enumerate(indices[0]):
          # The L2 distance
          dist = distances[0][i]
          theorem_text = theorems_list[idx]
          print(f" {i+1}. [Distance: {dist:.4f}] - {theorem_text}")
          file.write("-----------------------------------------\n")
          file.write(f"{theorem_text}\n")
      file.write("\n*****************************************\n\n")


if __name__ == "__main__":
    # Load the sentence embedding model
    print("Loading sentence transformer model...")
    model = SentenceTransformer(MODEL_NAME, device='cuda') # Use 'cpu' if no GPU

    # Load the list of theorems from the file
    if not os.path.exists(THEOREMS_FILE_PATH):
        print(f"Error: The file '{THEOREMS_FILE_PATH}' was not found.")
    else:
        theorems_list = load_theorems(THEOREMS_FILE_PATH)

        # Load or create the FAISS index
        if os.path.exists(INDEX_FILE_PATH):
            print(f"Loading existing FAISS index from '{INDEX_FILE_PATH}'.")
            index = faiss.read_index(INDEX_FILE_PATH)
        else:
            index = create_and_save_index(theorems_list, model, INDEX_FILE_PATH)

        # Input the theorem
        input_theorem = "Prove that $$\sum_{r=0}^{\lfloor\frac{n-1}{2}\rfloor} \left(\frac{n - 2r}{n} {n \choose r}\right)^2 = \frac{1}{n} {{2n - 2} \choose {n - 1}}$$ for every positive integer $n$."
        
        find_similar_theorems(input_theorem, model, index, theorems_list, OUTPUT_FILE_PATH, k=10)