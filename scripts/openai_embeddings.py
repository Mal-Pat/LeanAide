import json
from openai import OpenAI


def ada_embeddings():
    client = OpenAI()

    with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp, open("rawdata/mathlib4-prompts-embeddings.jsonl", 'a', encoding='utf-8') as out:
        
        # Adjust the start and end points
        # set this to one less than the number not present in output jsonl file
        count = 0
        js = json.load(inp)[count:]

        # for each line, compute the embeddings
        for l in js:
            response = client.embeddings.create(
                input=l["docString"],
                model="text-embedding-ada-002",
            )
            
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            
            print(l["docString"])
            count = count + 1
            print(f"Completed {count} out of {len(js)}")

            # write the embedding to `out`
            json.dump(l, out, ensure_ascii=False)
            out.write("\n")


def small_embeddings_prompt():
    client = OpenAI()

    with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp, open("rawdata/mathlib4-docStrings-small-embeddings.jsonl", 'a', encoding='utf-8') as out:
        
        # Adjust the start and end points
        # set this to one less than the number not present in output jsonl file
        count = 0
        js = json.load(inp)[count:]

        # for each line, compute the embeddings
        for l in js:
            response = client.embeddings.create(
                input=l["docString"],
                model="text-embedding-3-small",
            )
            
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            
            print(l["docString"])
            count = count + 1
            print(f"Completed {count} out of {len(js)}")
        
            # write the embedding to `out`
            json.dump(l, out, ensure_ascii=False)
            out.write("\n")


def small_embeddings_descs():
    client = OpenAI()

    # set this to one less than the number not present in output jsonl file
    count = 0

    with open("rawdata/mathlib4-descs-embeddings-small.jsonl", 'a', encoding='utf-8') as out:
        with open("resources/mathlib4-descs.jsonl", 'r', encoding='utf-8') as reader:
            i = 0
            for line in reader:
                i += 1
                if i <= count:
                    continue
                l = json.loads(line)
                for field in ["description", "concise-description"]:
                    if field in l and l[field]:
                        response = client.embeddings.create(
                            input=l[field],
                            model="text-embedding-3-small"
                        )

                        embedding = response.data[0].embedding
                        l[field + "-embedding"] = embedding
                        print("Field: ", field)
                        print(l[field])
                    else:
                        print(f"Field {field} not found")
                
                count = count + 1
                print(f"Completed {count}")
            
                json.dump(l, out, ensure_ascii=False)
                out.write("\n")