import re
import keyword
import pandas as pd

# -------------------------------
# Define Token Patterns
# -------------------------------

token_specification = [
    ('STRING',      r'(\'[^\']*\'|"[^"]*")'),          # String literals
    ('NUMBER',      r'\b\d+(\.\d+)?\b'),               # Integer or decimal numbers
    ('IDENTIFIER',  r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),    # Identifiers
    ('OPERATOR',    r'==|!=|<=|>=|<|>|\+|-|\*|/|%|//|\*\*|=|\+=|-=|\*=|/=|%=|&|\||\^|~|>>|<<'),  # Operators
    ('DELIMITER',   r'[\(\)\[\]\{\},:.;@]'),           # Delimiters
    ('NEWLINE',     r'\n'),                            # Line breaks
    ('SKIP',        r'[ \t]+'),                        # Skip spaces/tabs
    ('MISMATCH',    r'.'),                             # Any other character
]

# Combine patterns into one regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)


# -------------------------------
# Tokenizer Function
# -------------------------------

def tokenize_python_code(code):
    tokens = []
    line_num = 1
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'IDENTIFIER':
            if value in keyword.kwlist:
                kind = 'KEYWORD'
        elif kind == 'MISMATCH':
            kind = 'ERROR'
        tokens.append((value, kind, line_num))
    return tokens


# -------------------------------
# Run Example
# -------------------------------

if __name__ == "__main__":
    code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""

    token_list = tokenize_python_code(code)

    # Display as table
    df = pd.DataFrame(token_list, columns=["Lexeme", "Token Type", "Line No"])
    print(df)

    # Optional: save to CSV
    df.to_csv("tokens_output.csv", index=False)
    print("\nTokens saved to tokens_output.csv")

