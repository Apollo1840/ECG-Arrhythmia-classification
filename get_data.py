from glob import glob
import numpy as np
import wfdb


def get_records():
    """ Get paths for data in data/mit/ directory """
    # Download if doesn't exist
    
    # There are 3 files for each record
    # *.atr is one of them
    paths = glob('/path/to/MITDB/dataset/*.atr')

    # Get rid of the extension, [:-4] to remove '.atr'
    paths = [path[:-4] for path in paths]
    paths.sort()

    return paths


def beat_annotations(annotation, beat_type="N"):
    """
        Get rid of non specific beat markers

    :param: annotation, wfdb.annotation type.
        annotation.symbol is the annotation of the beats(peak).
        annotation.sample is the index of the beats(peak)
    :param: beat_type: str.
        'N' for normal beats.
        'L' for left bundle branch block beats.
        'R' for right bundle branch block beats.
        'A' for Atrial premature contraction.
        'V' for ventricular premature contraction.
        '/' for paced beat.
        'E' for Ventricular escape beat.

    :return: beat index of specific beat_type
    """

    # annotation
    ids = np.in1d(annotation.symbol, [beat_type])

    # We want to know only the positions
    beats = annotation.sample[ids]

    return beats


def get_beats(records, beat_type="N"):
    """

    :param records: List[str], each item is a wfdb readable record, like (/path/to/the/record)
    :param beat_type: str.
        'N' for normal beats.
        'L' for left bundle branch block beats.
        'R' for right bundle branch block beats.
        'A' for Atrial premature contraction.
        'V' for ventricular premature contraction.
        '/' for paced beat.
        'E' for Ventricular escape beat.

    :return: List[np.array], list of wanted beats
    """

    beats = []
    for record in records:

        # notice: here we pick the first appear channel, it is NOT necessary to be lead-1.
        signals, fields = wfdb.rdsamp(record, channels=[0])
        ann = wfdb.rdann(record, 'atr')

        # indexes of the beats
        beats = (ann.sample)

        # indexes of normal beats
        imp_beats = beat_annotations(ann, beat_type)

        beats = list(beats)
        for i in imp_beats:

            # the index of normal beats in all beats
            j = beats.index(i)
            if j != 0 and j != (len(beats)-1):
                beat_start_index = beats[j] + abs(beats[j-1] - beats[j])//2
                beat_end_index = beats[j] + abs(beats[j+1] - beats[j])//2
                beats.append(signals[beat_start_index: beat_end_index, 0])
    return beats

