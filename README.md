
# 🧠 Tokenizer — Lexical Analyzer for Python Code

This project is a **lexical analyzer (scanner)** that processes Python source code and breaks it into individual **tokens** such as keywords, identifiers, literals, operators, and delimiters.  
It provides a structured view of how source code is read and interpreted during the first phase of compilation — **tokenization**.

---

## 🚀 Features

- Identifies **Python keywords, identifiers, numbers, operators, and strings**  
- Detects and skips **spaces, tabs, and newlines**  
- Flags **unrecognized characters as errors**  
- Exports tokens to a **CSV file** for further analysis  
- Displays tokens in a **clean tabular format**

---

## 🧩 How It Works

The program uses:
- **Regular Expressions (`re`)** for pattern-based token detection  
- **The `keyword` module** to recognize reserved Python keywords  
- **Pandas** for displaying and exporting token data to CSV  

Each line of the source code is scanned, matched against predefined token patterns, and categorized into meaningful groups.

```python
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
