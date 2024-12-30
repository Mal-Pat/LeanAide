import json

# Main input prompts file and main output prompts + embeddings file
with open("resources/mathlib4-prompts.json", 'r', encoding='utf-8') as inp1, open("rawdata/mathlib4-newdocs-docStrings-small256-embeddings.jsonl", 'a', encoding='utf-8') as out:
    
    js_load = json.load(inp1)

    # Give each subfile containing a part of the embeddings and adjust the count accordingly

    with open("rawdata/small256_output/newdocs_batch_out_small256_0_to_20000.jsonl", 'r', encoding='utf-8') as inp2:    
        count = 0
        js1 = js_load[count:20000]
        for l in js1:
            count = count + 1
            check = 0
            for line in inp2:
                js2 = json.loads(line)
                if int(js2["custom_id"]) == count:
                    l["embedding"] = js2["response"]["body"]["data"][0]["embedding"]
                    check += 1
                    break
            if check == 0:
                print('error')
            json.dump(l, out, ensure_ascii=False)
            out.write("\n")

    with open("rawdata/small256_output/newdocs_batch_out_small256_20001_to_40000.jsonl", 'r', encoding='utf-8') as inp2:    
        count = 20000
        js1 = js_load[count:40000]
        for l in js1:
            count = count + 1
            check = 0
            for line in inp2:
                js2 = json.loads(line)
                if int(js2["custom_id"]) == count:
                    l["embedding"] = js2["response"]["body"]["data"][0]["embedding"]
                    check += 1
                    break
            if check == 0:
                print('error')
            json.dump(l, out, ensure_ascii=False)
            out.write("\n")
    
    with open("rawdata/small256_output/newdocs_batch_out_small256_40001_to_end_61219.jsonl", 'r', encoding='utf-8') as inp2:    
        count = 40000
        js1 = js_load[count:]
        for l in js1:
            count = count + 1
            check = 0
            for line in inp2:
                js2 = json.loads(line)
                if int(js2["custom_id"]) == count:
                    l["embedding"] = js2["response"]["body"]["data"][0]["embedding"]
                    check += 1
                    break
            if check == 0:
                print('error')
            json.dump(l, out, ensure_ascii=False)
            out.write("\n")
