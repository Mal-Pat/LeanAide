import json
from openai import OpenAI

client = OpenAI()

file_name = "rawdata/batch_inp_ada_40001_to_end_61219.jsonl"

# Create the file ===================================
'''
with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp, open(file_name, 'a', encoding='utf-8') as out:
    count = 40000
    js = json.load(inp)[count:]

    # for each line, compute the embeddings
    for l in js:
        count = count + 1      
        d = {"custom_id": str(count), "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-ada-002", "input": l["docString"]}}
        json.dump(d, out, ensure_ascii=False)
        out.write("\n")
'''

'''
# Upload the file ===================================
batch_input_file = client.files.create(
    file=open(file_name, "rb"),
    purpose="batch"
)

print(batch_input_file)

# Create the batch ===================================
batch_input_file_id = batch_input_file.id
create_batch = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/embeddings",
    completion_window="24h",
    metadata={
        "description": "ada_embeddings batch 40001 to end 61219 newdocs"
    }
)

print(create_batch)
'''

#====================================================================================================

# newdocs small batches
'''
# Check status of batch =================================== small_embeddings batch 0 to 20000 newdocs
batch = client.batches.retrieve("batch_6770406d7a048190bb0f67593953f166")
print(batch)

# Check status of batch =================================== small_embeddings batch 20001 to 40000 newdocs
batch = client.batches.retrieve("batch_67704147e1308190975e1217395f7b99")
print(batch)

# Check status of batch =================================== small_embeddings batch 40001 to end 61219 newdocs
batch = client.batches.retrieve("batch_67704228bfe48190a22728df5a295a02")
print(batch)
'''

# newdocs small batch results
'''
# Get results ===================================
file_response = client.files.content("file-PQ7NttPTMBGYWpu2kZi6em")
with open('rawdata/newdocs_batch_out_small_0_to_20000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("file-JjcEe9s4yfJkkcNe9peHYw")
with open('rawdata/newdocs_batch_out_small_20001_to_40000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("file-9Rw9MzDTz7Wz9Y8s5bUwn4")
with open('rawdata/newdocs_batch_out_small_40001_to_end_61219.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)
'''

#====================================================================================================

# newdocs small256 batches

'''
# Check status of batch =================================== small256_embeddings batch 0 to 20000 newdocs
batch = client.batches.retrieve("batch_6770e1613a6c8190a2bd902e6648d736")
print(batch)


# Check status of batch =================================== small256_embeddings batch 20001 to 40000 newdocs
batch = client.batches.retrieve("batch_6770e4278afc81908af92b2ceee39cbb")
print(batch)


# Check status of batch =================================== small256_embeddings batch 40001 to end 61219 newdocs
batch = client.batches.retrieve("batch_6770e49dbea881909b60571cca970afa")
print(batch)
'''

# newdocs small256 batch results
'''
# Get results ===================================
file_response = client.files.content("file-CJUEaoPs3N224ERoNEZGBK")
with open('rawdata/newdocs_batch_out_small256_0_to_20000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("file-Eg5GGXPwirtjxmxAqL86Cp")
with open('rawdata/newdocs_batch_out_small256_20001_to_40000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("file-29neFoduEeqMxFXcUBFhFo")
with open('rawdata/newdocs_batch_out_small256_40001_to_end_61219.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)
'''

#====================================================================================================

# newdocs ada batches

'''
# Check status of batch =================================== ada_embeddings batch 0 to 20000 newdocs
batch = client.batches.retrieve("batch_677255e97f048190b9a03af5ee38b9d4")
print(batch)
'''

'''
# Check status of batch =================================== ada_embeddings batch 20001 to 40000 newdocs
batch = client.batches.retrieve("batch_67725679c4b88190a88bfdd74d2267d4")
print(batch)
'''

'''
# Check status of batch =================================== ada_embeddings batch 40001 to end 61219 newdocs
batch = client.batches.retrieve("batch_677256d21f80819084fa1c11d23f1b41")
print(batch)
'''

# newdocs small256 batch results
'''
# Get results ===================================
file_response = client.files.content("")
with open('rawdata/newdocs_batch_out_ada_0_to_20000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("")
with open('rawdata/newdocs_batch_out_ada_20001_to_40000.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)


# Get results ===================================
file_response = client.files.content("")
with open('rawdata/newdocs_batch_out_ada_40001_to_end_61219.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)
'''