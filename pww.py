"""
pww: Python Without Whitespace
a python-based programming language, with no whitespace required
instead of using ':' it uses '{' and '}' to denote blocks
instead of using newlines to denote the end of a statement, it uses ';'

example:
def main():
    print("Hello, World!")
    for i in range(10):
        print(i)

becomes:
def main() {
    print("Hello, World!");
    for i in range(10) {
        print(i);
    }
}
"""
import re


def main(infile, outfile):
    with open(infile, "r") as f:
        code = f.read()
    
    ##### LEXER #####
    tokens = []
    token = ""
    code = code.strip()
    code = code.replace("\s+", " ")
    for char in code:
        if char in "{};":
            if token and token.strip():
                tokens.append(token.strip())
                token = ""
            tokens.append(char)
        else:
            token += char
    if token:
        tokens.append(token)
    
    ##### PARSER #####
    code = ""
    indent = 0
    for token in tokens:
        if token == "{":
            indent += 1
            code += ":\n"
        elif token == "}":
            indent -= 1
            pass
        elif token == ";":
            code += "\n"
        else:
            code += "\t" * indent + token + " "
    
    ##### CLEAN UP #####
    code = code.replace("\t", "    ")
    code = code.replace(" :", ":")
    code = re.sub(r"\n\s*\n", "\n", code) # remove empty lines
    if code[-1] == " ": # remove trailing whitespace
        code = code[:-1]
    if code[-1] == " ": # remove trailing whitespace
        code = code[:-1]
    if code[-1] != "\n": # add trailing newline
        code += "\n"

    with open(outfile, "w") as f:
        f.write(code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1], sys.argv[1].replace(".py", ".pww"))
    else:
        print("Usage: pww.py <infile> [outfile]")