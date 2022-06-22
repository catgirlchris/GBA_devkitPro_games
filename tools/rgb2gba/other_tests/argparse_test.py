import os
import argparse

if __name__ == '__main__':
    # preparar arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("x",  type=int, help="the base")
    parser.add_argument("y",  type=int, help="the exponent")

    parser.add_argument("-v", "--verbosity", action="count", default=0, 
                        help="increase output verbosity")

    # comienza el parseo 8w8
    args = parser.parse_args()
    answer = args.x**args.y
    
    # tratamiento de los argumentos
    if args.verbosity >= 2:
        print(f"{args.x} to the power {args.y} equals {answer}")
    elif args.verbosity == 1:
        print(f"{args.x}^{args.y} == {answer}")
    else:
        print(answer)