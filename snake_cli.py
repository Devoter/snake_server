import argparse
import os
import sqlite3
import settings


def init_handler(connection=None):
    db = connection if connection is not None else sqlite3.connect(settings.DATABASE)
    db.execute('DROP TABLE IF EXISTS scores')
    db.execute('CREATE TABLE scores(id CHARACTER(65) PRIMARY KEY, name VARCHAR(255), score INTEGER, created INTEGER)')
    if connection is None:
        db.close()


def load_handler(args):
    if not os.path.isfile(args.filename):
        print('File "' + args.filename + '" does not exist')
        return

    db = sqlite3.connect(settings.DATABASE)

    try:
        dump_file = open(args.filename, 'r')
    except OSError:
        print('Could not open the dump file')
        return
    dump = dump_file.read()
    dump_file.close()

    db.execute('DROP TABLE IF EXISTS scores')
    db.executescript(dump)
    db.close()


def dump_handler(args):
    if os.path.exists(args.filename):
        print('File "' + args.filename + '" already exists')
        return

    db = sqlite3.connect(settings.DATABASE)

    try:
        dump_file = open(args.filename, 'w')
    except OSError:
        print('Could not open the dump file')
        return

    for line in db.iterdump():
        dump_file.write('%s\n' % line)
    dump_file.close()

    db.close()


if __name__ == "__main__":
    root_parser = argparse.ArgumentParser()
    root_subparsers = root_parser.add_subparsers(help='sub-command help', dest='cmd')

    # init
    init_parser = root_subparsers.add_parser('init', help='Create new database')

    # load
    load_parser = root_subparsers.add_parser('load', help='Load database dump')
    load_parser.add_argument('filename', action='store', metavar='filename', help='Dump for load')

    # dump
    dump_parser = root_subparsers.add_parser('dump', help='Dump database into file')
    dump_parser.add_argument('filename', action='store', metavar='filename', help='Dump filename')

    # clear
    clear_parser = root_subparsers.add_parser('clear', help='Clear data')

    args = root_parser.parse_args()

    if args.cmd == 'init':
        init_handler()
    elif args.cmd == 'load':
        load_handler(args)
    elif args.cmd == 'dump':
        dump_handler(args)
    elif args.cmd == 'clear':
        init_handler()
    else:
        print('Unknown command:', args.cmd)
