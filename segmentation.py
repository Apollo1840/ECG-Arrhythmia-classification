import numpy as np
import biosppy


def split_by_peaks(csv_data):
    """

    :param csv_data: List[float], the list of amplitude
    :return: List[List[float]]. list of beats
    """

    data = np.array(csv_data)
    signals = []
    count = 1
    peaks = biosppy.signals.ecg.christov_segmenter(signal=data, sampling_rate=200)[0]
    for i in (peaks[1:-1]):
        beat_start_index = peaks[count] + abs(peaks[count - 1] - i) // 2
        beat_end_index = peaks[count] + abs(peaks[count + 1] - i) // 2
        signals.append(data[beat_start_index:beat_end_index])
        count += 1
    return signals
