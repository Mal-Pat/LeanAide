import requests
import urllib

'''

from openai import OpenAI

client = OpenAI()

prompt = "If the condensation points of a topological space is the set of all open sets which are clopen, then that implies that  the statement every closed set is homeomorphic to the Hausdorff space and for all open balls in T4 space, there is an isomorphism between the set of all countable points and its power set."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": f"You are a mathematician. From the given statement, ONLY output a list of mathematical terms that may be unknown to graduate level mathematics students: {prompt}"
        }
    ],
    response_format={
        "type": "json_schema", 
        "json_schema": {
            "name": "mathematical_terms",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "math_terms": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["math_terms"],
                "additionalProperties": False
            }
        }
    }
)

print(response.choices[0].message.content)

'''

def leansearch_api(query,num):
    URL = f"https://leansearch.net/api/search?query={urllib.parse.quote(query)}&num_results={str(num)}"
    r = requests.get(url=URL)
    print(r.json())

leansearch_api("0<1",6)