import os
from pyprint.ConsolePrinter import ConsolePrinter

from coalib.parsing.Globbing import glob
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section
from coalib.settings.ConfigurationGathering import get_config_directory


def main(log_printer=None, section: Section=None):
    start_path = get_config_directory(section)
    log_printer = log_printer or LogPrinter(ConsolePrinter())

    if start_path is None:
        log_printer.err("Can only delete .orig files if .coafile is found")
        return 255

    orig_files = glob(os.path.abspath(os.path.join(start_path, '**', '*.orig')))

    not_deleted = 0
    for ofile in orig_files:
        log_printer.info("Deleting old backup file... "
                         + os.path.relpath(ofile))
        try:
            os.remove(ofile)
        except:
            not_deleted += 1
            log_printer.warn("Couldn't delete... " + os.path.relpath(ofile))

    if not_deleted:
        log_printer.warn(not_deleted + " .orig backup files could not be"
                         " deleted, possibly because you lack the permission"
                         " to do so. coala may not be able to create"
                         " backup files when patches are applied.")
    return 0
