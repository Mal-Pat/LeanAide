import json
from openai import OpenAI

client = OpenAI()

file_name = "rawdata/input_data_prompts_37001_to_end.jsonl"

'''
# Create the file ===================================
with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp, open(file_name, 'a', encoding='utf-8') as out:
    count = 37000
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
        "description": "batch embeddings 37001 to end"
    }
)

print(create_batch)
'''

'''
# Check status of batch =================================== 20001 to 25000 DONE
batch = client.batches.retrieve("batch_676a7cf2d1408190bedd5cd193f9ab60")
print(batch)
'''

'''
# Check status of batch =================================== 25001 to 30000 DONE
batch = client.batches.retrieve("batch_676a7da5c4e08190b6c5804a2bb1d0b4")
print(batch)
'''

'''
# Check status of batch =================================== 30001 to 37000
batch = client.batches.retrieve("batch_676a80301ccc819096d968cc7207b550")
print(batch)
'''

'''
# Check status of batch =================================== 37001 to end
batch = client.batches.retrieve("batch_676a849da37c8190844949f10687e84f")
print(batch)
'''

'''
# Get results ===================================
file_response = client.files.content("file-XLQvba1wxye2XML7VramBw")
with open('rawdata/output_data_prompts_37001_to_end.jsonl', 'w', encoding='utf-8') as outfile:
    outfile.write(file_response.text)
'''

