import lexer
import analyzer
import argparse
import debug
import sys
import time

def dropResult(res, filename):
    with open(filename+'.a','w') as f:
        f.write(debug.Node2Json(res))

def main():
    parser = argparse.ArgumentParser(description='C language parser')
    parser.add_argument('input', help='input file')
    args = parser.parse_args()

    print("parsing {}".format(args.input))

    f = open(args.input, "r")
    start = time.time()

    l = lexer.Lexer(f.read())
    a = analyzer.Analyzer(l)

    res = a.parse()
    end = time.time()
    res = analyzer.normalizeAST(res)
    print(debug.AST2String(res))

    print("Time passed {}".format(end - start))



if __name__ == "__main__":
    main()
