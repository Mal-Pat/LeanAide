import json
import os
from openai import OpenAI


def openai_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def iter_jsonl(path):
    with open(path, 'r', encoding='utf-8') as inp:
        for line in inp:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl_line(out, obj):
    out.write(json.dumps(obj, ensure_ascii=False) + "\n")
    out.flush()


def ada_embeddings():
    client = openai_client()
    count = 0

    with open("rawdata/mathlib4-prompts-embeddings.jsonl", 'w', encoding='utf-8') as out:
        # for each line, compute the embeddings
        for l in iter_jsonl("resources/mathlib4-prompts.jsonl"):
            response = client.embeddings.create(
                input=l["doc"],
                model="text-embedding-ada-002",
            )
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            print(l["doc"])
            count = count + 1
            print(f"Completed {count}")
            write_jsonl_line(out, l)


def small_embeddings():
    client = openai_client()
    count = 0

    with open("rawdata/mathlib4-prompts-small-embeddings.jsonl", 'w', encoding='utf-8') as out:
        for l in iter_jsonl("resources/mathlib4-prompts.jsonl"):
            response = client.embeddings.create(
                input=l["doc"],
                model="text-embedding-3-small",
                # dimensions = 256
            )
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            count = count + 1
            print(l["doc"])
            print(f"Completed {count}")
            write_jsonl_line(out, l)


def small_embeddings_prompt():
    small_embeddings()


def small_embeddings_descs():
    client = openai_client()
    count = 0

    with open("rawdata/mathlib4-descs-embeddings-small.jsonl", 'w', encoding='utf-8') as out:
        for l in iter_jsonl("resources/mathlib4-descs.jsonl"):
            for field in ["description", "concise-description"]:
                if field in l and l[field]:
                    response = client.embeddings.create(
                        input=l[field],
                        model="text-embedding-3-small"
                        # dimensions = 256
                    )
                    embedding = response.data[0].embedding
                    l[field + "-embedding"] = embedding
                    print("Field: ", field)
                    print(l[field])
                else:
                    print(f"Field {field} not found")
            count = count + 1
            print(f"Completed {count}")
            write_jsonl_line(out, l)


def main():
    small_embeddings()
    small_embeddings_descs()


if __name__ == "__main__":
    main()
