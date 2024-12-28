import json
from openai import OpenAI

client = OpenAI()

file_name = "rawdata/batch_inp_small_40001_to_end_61219.jsonl"

'''
# Create the file ===================================
with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp, open(file_name, 'a', encoding='utf-8') as out:
    count = 40000
    js = json.load(inp)[count:]

    # for each line, compute the embeddings
    for l in js:
        count = count + 1      
        d = {"custom_id": str(count), "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-3-small", "input": l["docString"]}}
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
        "description": "small_embeddings batch 40001 to end 61219 newdocs"
    }
)

print(create_batch)
'''

'''
# Check status of batch =================================== small_embeddings batch 0 to 20000 newdocs
batch = client.batches.retrieve("batch_6770406d7a048190bb0f67593953f166")
print(batch)
'''

'''
# Check status of batch =================================== small_embeddings batch 20001 to 40000 newdocs
batch = client.batches.retrieve("batch_67704147e1308190975e1217395f7b99")
print(batch)
'''

'''
# Check status of batch =================================== small_embeddings batch 40001 to end 61219 newdocs
batch = client.batches.retrieve("batch_67704228bfe48190a22728df5a295a02")
print(batch)
'''

'''
# Get results ===================================
file_response = client.files.content("file-XLQvba1wxye2XML7VramBw")
with open('rawdata/output_data_prompts_37001_to_end.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)
'''