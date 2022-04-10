import logging
import os

import click
import magic

from .modules.auto import ParserFactory

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level="ERROR",
)


@click.group()
def cli():
    pass


@cli.command("detect")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=True, resolve_path=False),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
def detect_file(file, verbose, debug):
    """detect the file type"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    if os.path.isdir(file):
        logging.info(f"{file} is a directory")
        for root, _, files in os.walk(file):
            for file in files:
                path = os.path.join(root, file)
                mime = magic.from_file(path, mime=True)
                print(f"{path}: {mime}")
    else:
        mime = magic.from_file(file, mime=True)
        print(f"{file}: {mime}")


@cli.command("fields")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
def list_fields(file, verbose, debug):
    """list all fields in the file"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    parser_cls = ParserFactory.get_parser_for_file(file)
    if parser_cls is None:
        raise Exception("Cannot find parser for file")
    parser = parser_cls()
    parser.parse(file)
    for field in parser.get_fields():
        print(field)


@cli.command("set")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
@click.argument("field")
@click.argument("value")
def set_field(file, verbose, debug, field, value):
    """set FIELD VALUE"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    if os.path.isdir(file):
        for root, _, files in os.walk(file):
            for file in files:
                path = os.path.join(root, file)
                parser_cls = ParserFactory.get_parser_for_file(path)
                if parser_cls is None:
                    logging.info(f"Skipping {file} as no parser have been found")
                    continue
                parser = parser_cls()
                parser.parse(path)
                try:
                    parser.set_field(field, value)
                except KeyError:
                    logging.warn(f"Field {field} not present in {file}")
                print(f"Updating {file}")
                parser.write()
    else:
        parser_cls = ParserFactory.get_parser_for_file(file)
        if parser_cls is None:
            raise Exception("Cannot find parser for file")
        parser = parser_cls()
        parser.parse(file)
        parser.set_field(field, value)
        parser.write()


@cli.command("delete")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
@click.argument("field")
def delete_field(file, verbose, debug, field):
    """delete FIELD"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    if os.path.isdir(file):
        for root, _, files in os.walk(file):
            for file in files:
                path = os.path.join(root, file)
                parser_cls = ParserFactory.get_parser_for_file(path)
                if parser_cls is None:
                    logging.info(f"Skipping {file} as no parser have been found")
                    continue
                parser = parser_cls()
                parser.parse(path)
                try:
                    parser.delete_field(field)
                except KeyError:
                    logging.warn(f"Field {field} not present in {file}")
                print(f"Updating {file}")
                parser.write()
    else:
        parser_cls = ParserFactory.get_parser_for_file(file)
        if parser_cls is None:
            raise Exception("Cannot find parser for file")
        parser = parser_cls()
        parser.parse(file)
        parser.delete_field(field)
        parser.write()


@cli.command("delete-all")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
def delete_all_fields(file, verbose, debug):
    """delete all fields"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    if os.path.isdir(file):
        for root, _, files in os.walk(file):
            for file in files:
                path = os.path.join(root, file)
                parser_cls = ParserFactory.get_parser_for_file(path)
                if parser_cls is None:
                    logging.info(f"Skipping {file} as no parser have been found")
                    continue
                parser = parser_cls()
                parser.parse(path)
                parser.clear()
                print(f"Updating {file}")
                parser.write()
    else:
        parser_cls = ParserFactory.get_parser_for_file(file)
        if parser_cls is None:
            raise Exception("Cannot find parser for file")
        parser = parser_cls()
        parser.parse(file)
        parser.clear()
        parser.write()


@cli.command("print")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
    help="path to the file/directory for parsing",
    required=True,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="print info messages",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="print debug messages",
)
def print_file(file, verbose, debug):
    """print the file"""
    if verbose:
        logging.getLogger().setLevel("INFO")
    if debug:
        logging.getLogger().setLevel("DEBUG")

    if os.path.isdir(file):
        for root, _, files in os.walk(file):
            for file in files:
                path = os.path.join(root, file)
                parser_cls = ParserFactory.get_parser_for_file(path)
                if parser_cls is None:
                    logging.info(f"Skipping {file} as no parser have been found")
                    continue
                parser = parser_cls()
                parser.parse(path)
                print(f"{file}:")
                parser.print()
                print()
    else:
        parser_cls = ParserFactory.get_parser_for_file(file)
        if parser_cls is None:
            raise Exception("Cannot find parser for file")
        parser = parser_cls()
        parser.parse(file)
        parser.print()


def entry_point():
    try:
        cli()
    except Exception:
        logging.critical("", exc_info=True)
