import json
import os
import argparse
from openai import OpenAI


def openai_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def jsonl_line_count(path):
    with open(path, 'r', encoding='utf-8') as inp:
        return sum(1 for line in inp if line.strip())


def iter_jsonl(path, start_line=1):
    with open(path, 'r', encoding='utf-8') as inp:
        for line_no, line in enumerate(inp, start=1):
            if line_no < start_line:
                continue
            line = line.strip()
            if line:
                yield line_no, json.loads(line)


def write_jsonl_line(out, obj):
    out.write(json.dumps(obj, ensure_ascii=False) + "\n")
    out.flush()


def ada_embeddings(start_line=1):
    client = openai_client()
    input_path = "resources/mathlib4-prompts.jsonl"
    output_path = "rawdata/mathlib4-prompts-embeddings.jsonl"
    total = jsonl_line_count(input_path)
    mode = 'a' if start_line > 1 else 'w'

    with open(output_path, mode, encoding='utf-8') as out:
        # for each line, compute the embeddings
        for line_no, l in iter_jsonl(input_path, start_line):
            response = client.embeddings.create(
                input=l["doc"],
                model="text-embedding-ada-002",
            )
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            print(l["doc"])
            print(f"Completed {line_no} out of {total}")
            write_jsonl_line(out, l)


def small_embeddings(start_line=1):
    client = openai_client()
    input_path = "resources/mathlib4-prompts.jsonl"
    output_path = "rawdata/mathlib4-prompts-small-embeddings.jsonl"
    total = jsonl_line_count(input_path)
    mode = 'a' if start_line > 1 else 'w'

    with open(output_path, mode, encoding='utf-8') as out:
        for line_no, l in iter_jsonl(input_path, start_line):
            response = client.embeddings.create(
                input=l["doc"],
                model="text-embedding-3-small",
                # dimensions = 256
            )
            embedding = response.data[0].embedding
            l["embedding"] = embedding
            print(l["doc"])
            print(f"Completed {line_no} out of {total}")
            write_jsonl_line(out, l)


def small_embeddings_prompt(start_line=1):
    small_embeddings(start_line)


def small_embeddings_descs(start_line=1):
    client = openai_client()
    input_path = "resources/mathlib4-descs.jsonl"
    output_path = "rawdata/mathlib4-descs-embeddings-small.jsonl"
    total = jsonl_line_count(input_path)
    mode = 'a' if start_line > 1 else 'w'

    with open(output_path, mode, encoding='utf-8') as out:
        for line_no, l in iter_jsonl(input_path, start_line):
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
            print(f"Completed {line_no} out of {total}")
            write_jsonl_line(out, l)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "start_line",
        nargs="?",
        type=int,
        help="1-based input line to start from. Use the next line after the last completed line.",
    )
    args = parser.parse_args()
    start_line = args.start_line
    if start_line is None:
        start = input("Start from line (1 for beginning): ").strip()
        start_line = int(start) if start else 1
    if start_line < 1:
        raise ValueError("start_line must be at least 1")

    small_embeddings(start_line)
    small_embeddings_descs(start_line)


if __name__ == "__main__":
    main()
