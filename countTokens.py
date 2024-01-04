import tiktoken
from model_inputs import readfile

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

chars = readfile("suibook2.txt")
print(num_tokens_from_string(chars, "cl100k_base"))