import sys
import os
import logging
import argparse
import argcomplete
from argcomplete.completers import (
    ChoicesCompleter,
    FilesCompleter,
    # _wrapcall
)


dir =os.getcwd()
print dir
sys.path.append(dir+'/src')
from core import loader
from core import diff
import viewer


def create_argparse_intersect(subparsers):
    subparse = subparsers.add_parser(
        "i",  # aliases=("analyze",),
        help="intersect of given STL files",
    )

    subparse.add_argument(
        dest="path1", type=str,
        help="first stl file path",
    ).completer = FilesCompleter(directories=False)

    subparse.add_argument(
        dest="path2", type=str,
        help="seond stl file path",
    ).completer = FilesCompleter(directories=False)

    group = subparse.add_mutually_exclusive_group()
    group.add_argument(
        "-o", "--output", dest="output", type=str,
        help="The file to write the stl output to",
    )

    def intersect(path1,path2, output):
        filename1 = path1
        filename2 = path2

        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)

        try:
            obj1=loader.load_stl(filename1)
            obj2=loader.load_stl(filename2)
        except RuntimeError as e:
            raise RuntimeError(e)
        sys.setrecursionlimit(recursionlimit)

        result = diff.intersect(obj1,obj2)
        if not output:
            loader.save_stl(result,'intersect.stl')
        elif output:
            with open(output, 'wb') as file:
                loader.save_stl(result,output+'/intersect.stl')
        else:
            assert False  # Error in logic
        viewer.show(result)

    subparse.set_defaults(func=lambda args: intersect(
        args.path1,
        args.path2,
        args.output,
    ),)

def create_argparse_subtract(subparsers):
    subparse = subparsers.add_parser(
        "s",  # aliases=("analyze",),
        help="subtract of given STL files",
    )

    subparse.add_argument(
        dest="path1", type=str,
        help="first stl file path",
    ).completer = FilesCompleter(directories=False)

    subparse.add_argument(
        dest="path2", type=str,
        help="seond stl file path",
    ).completer = FilesCompleter(directories=False)

    group = subparse.add_mutually_exclusive_group()
    group.add_argument(
        "-o", "--output", dest="output", type=str,
        help="The file to write the stl output to",
    )

    def subtract(path1,path2, output):
        filename1 = path1
        filename2 = path2

        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        try:
            obj1=loader.load_stl(filename1)
            obj2=loader.load_stl(filename2)
        except RuntimeError as e:
            raise RuntimeError(e)
        sys.setrecursionlimit(recursionlimit)

        result = diff.subtract(obj1,obj2)
        if not output:
            loader.save_stl(result,'subtract.stl')
        elif output:
            with open(output, 'wb') as file:
                loader.save_stl(result,output+'/subtract.stl')
        else:
            assert False  # Error in logic
        viewer.show(result)

    subparse.set_defaults(func=lambda args: subtract(
        args.path1,
        args.path2,
        args.output,
    ),)

def create_argparse_union(subparsers):
    subparse = subparsers.add_parser(
        "u",  # aliases=("analyze",),
        help="union of given STL files",
    )

    subparse.add_argument(
        dest="path1", type=str,
        help="first stl file path",
    ).completer = FilesCompleter(directories=False)

    subparse.add_argument(
        dest="path2", type=str,
        help="seond stl file path",
    ).completer = FilesCompleter(directories=False)

    group = subparse.add_mutually_exclusive_group()
    group.add_argument(
        "-o", "--output", dest="output", type=str,
        help="The file to write the stl output to",
    )

    def union(path1,path2, output):
        filename1 = path1
        filename2 = path2

        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        try:
            obj1=loader.load_stl(filename1)
            obj2=loader.load_stl(filename2)
        except RuntimeError as e:
            raise RuntimeError(e)
        sys.setrecursionlimit(recursionlimit)

        result = diff.union(obj1,obj2)
        if not output:
            loader.save_stl(result,'union.stl')
        elif output:
            with open(output, 'wb') as file:
                loader.save_stl(result,output+'/union.stl')
        else:
            assert False  # Error in logic
        viewer.show(result)
    subparse.set_defaults(func=lambda args: union(
        args.path1,
        args.path2,
        args.output,
    ),)







def create_argparse():
    usage_text = ("")

    parser = argparse.ArgumentParser(
        prog="3d-diff",
        description=usage_text,
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='Be verbose',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO
    )

    parser.add_argument(
        '-q',
        '--quiet',
        help='Hide most output',
        action="store_const",
        dest="loglevel",
        const=logging.ERROR
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        help='additional help',
    )

    create_argparse_intersect(subparsers)
    create_argparse_subtract(subparsers)
    create_argparse_union(subparsers)

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = create_argparse()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)

    # Setup basic logging
    logging.basicConfig(
        level=args.loglevel,
        format='%(levelname)7s:%(name)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # call subparser callback
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
