#!/usr/bin/env python3
import sys
import os
import argparse
from zoom2midi import ZoomMidiFile


def parse_args(mode):
    if mode == "zoom2midi":
        description = "Converts a ZOOM sequence file to MIDI file."
    elif mode == "midi2zoom":
        description = "Converts a MIDI file to a ZOOM sequence file."

    parser = argparse.ArgumentParser(
        prog="zoom2midi",
        description=description,
    )
    parser.add_argument(
        "--midifile",
        default="zoom.mid",
        help="MIDI file path (default: %(default)s)",
    )
    parser.add_argument(
        "--zoomfile",
        default="SMPLSEQ.ZDT",
        help="ZOOM sequence file path (default: %(default)s)",
    )
    parser.add_argument(
        "--offset",
        default=0,
        help="MIDI note nr mapped to ZOOM track #1 (default: %(default)i)",
    )
    parser.add_argument(
        "--midi_track",
        default=0,
        help="MIDI track to parse (default: %(default)i)",
    )
    parser.add_argument(
        "--multiply",
        type=int,
        help="If set, ZOOM sequence is multiplied for the give times. (0 or less means filling the whole sequence)",
    )
    return parser.parse_args()


def main(mode):
    args = parse_args(mode)

    # check files
    midifile = args.midifile
    zoomfile = args.zoomfile
    if mode == "zoom2midi" and not os.path.isfile(args.midifile):
        midifile = None
    elif mode == "midi2zoom" and not os.path.isfile(args.zoomfile):
        zoomfile = None

    mid = ZoomMidiFile(
        filename=midifile,
        sequence_file=zoomfile,
        note_offset=args.offset,
        zoom_track_nr=args.midi_track,
    )
    if args.multiply is not None:
        multiply_times = args.multiply if args.multiply > 0 else None
        mid.seq.multiply_notes(times=multiply_times)

    try:
        if mode == "zoom2midi":
            mid.from_sequence()
            mid.save(args.midifile)
            print("MIDI file {:s} has been written succesfully.".format(args.midifile))
        elif mode == "midi2zoom":
            mid.seq.write_file(args.zoomfile)
            print(
                "ZOOM sequence file {:s} has been written succesfully.".format(
                    args.zoomfile
                )
            )
    except FileNotFoundError as e:
        print("%s: %s" % (e.strerror, e.filename))
        print("Run %s --help" % sys.argv[0])
        sys.exit(e.errno)


if __name__ == "__main__":
    mode = (
        "midi2zoom"
        if os.path.split(sys.argv[0])[-1].startswith("midi2zoom")
        else "zoom2midi"
    )
    main(mode)
