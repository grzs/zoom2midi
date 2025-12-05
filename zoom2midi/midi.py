from mido import Message, MidiFile, MidiTrack
from zoom2midi.seq import Duration, Note, Sequence


class ZoomMidiFile(MidiFile):
    def __init__(self, note_offset=0, sequence=None):
        super().__init__(type=0)  # single track MIDI file
        self.tick_duration_ratio = self.ticks_per_beat / Duration.QUARTER
        self.tracks.append(MidiTrack())
        self.tracks[-1].name = "ZOOM sequence"
        self.note_offset = note_offset
        self.seq = sequence if isinstance(sequence, Sequence) else Sequence()

    def duration2ticks(self, duration: int):
        return int(duration * self.tick_duration_ratio)

    def ticks2duration(self, ticks: int):
        return int(ticks / self.tick_duration_ratio)

    def from_sequence(self, seq=None):
        if not isinstance(seq, Sequence):
            seq = self.seq

        track = self.tracks[0]
        position = 0
        for msg in seq.to_messages(note_offset=self.note_offset):
            msg["time"] = self.duration2ticks(msg["position"] - position)  # delta
            position = msg.pop("position")
            track.append(Message(**msg))

    def to_sequence(self, seq=None):
        if not isinstance(seq, Sequence):
            seq = self.seq

        track = self.tracks[0]
        channels = [[], [], [], [], [], [], [], []]
        position = 0
        for msg in track.messages:
            if msg.type.startswitth("note_"):
                channel_nr = msg.note - self.note_offset
                channel = channels[channel_nr]

                # close previous note
                if len(channel) > 0:
                    prev_note = channel[-1]
                    if msg.type == "note_off" or prev_note.length == 1:
                        prev_note.length = position - channel[-1].start

                if msg.type == "note_on":
                    note = Note(channel=channel_nr, start=position, length=1)
                    channel.append(note)
                    seq.notes.append(note)

            delta = self.ticks2duration(msg.time)
            if delta > 0:
                seq.notes.append(Note(start=position, length=delta))
                position += delta

        return seq.trim_and_close()
