from parser import planoutParser
import semantics
import time

def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()

    now = time.time()
    parser = planoutParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        semantics=semantics.PlanoutSemantics(),
        whitespace=whitespace)
    end = time.time()
    #print('AST:')
    #print(ast)
    #print()
    print(json.dumps(ast, indent=4))
    print end - now

if __name__ == '__main__':
    import sys
    main(sys.argv[1], 'seq', trace=False)
