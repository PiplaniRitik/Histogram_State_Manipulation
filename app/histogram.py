import threading
from typing import List, Tuple

class Histogram:
    def __init__(self, intervals: List[Tuple[float, float]]):
        self.lock = threading.Lock() # to ensure thread saftey
        self.intervals = sorted(intervals, key=lambda x: x[0]) # to read intervals defined in environment variable
        self.counts = {tuple(interval): 0 for interval in self.intervals} # hash to store frequency intervals wise
        self.valid_samples_total_sum = 0 # total sum of valid samples
        self.valid_samples_total_count = 0 # total count of valid samples
        self.valid_samples_square_sum = 0 # squared sum of valid samples
        self.mean = 0.0 # mean of valid samples
        self.variance = 0.0 # variance of valid samples
        self.outliers = [] # list to store outliers 
        self.isInvalidInterval = self.check_valid_intervals() # bool to check invalid intervals existence
        self.isOverlappingInterval = self.check_overlapping_intervals() # bool to check overlapping intervals

    def check_valid_intervals(self):
        for interval in self.intervals:
            if interval[0] >= interval[1]:
                return True
        return False

    def check_overlapping_intervals(self):
        for i in range(len(self.intervals) - 1):
            if self.intervals[i][1] > self.intervals[i + 1][0]:
                return True
        return False

    def binary_search_interval(self, sample):
        low, high = 0, len(self.intervals) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.intervals[mid][0] <= sample < self.intervals[mid][1]:
                return mid
            elif sample < self.intervals[mid][0]:
                high = mid - 1
            else:
                low = mid + 1
        return None

    def insert_samples(self, samples):
        if self.isInvalidInterval:
            raise ValueError("Internal server error. Invalid intervals found. Please correct the intervals in intervals.txt file.")
        if self.isOverlappingInterval:
            raise ValueError("Internal server error. Overlapping intervals found. Please correct the intervals in intervals.txt file.")

        for sample in samples:
            index = self.binary_search_interval(sample)
            if index is not None:
                self.counts[tuple(self.intervals[index])] += 1 # to increase the frequency
                self.valid_samples_total_sum += sample # to update sum of valid samples
                self.valid_samples_square_sum += sample * sample # to update square sum of valid samples
                self.valid_samples_total_count += 1 # to update total count
            else:
                self.outliers.append(sample) # to update outliers list
        if not self.valid_samples_total_count == 0:
            self.mean = self.valid_samples_total_sum / self.valid_samples_total_count # to store mean
            self.variance = (self.valid_samples_square_sum / self.valid_samples_total_count) - (self.mean * self.mean) # to store variance

    def calculate_statistics(self):
        if self.isInvalidInterval :
            raise ValueError("Internal server error. Invalid intervals found. Please correct the intervals in intervals.txt file.")
        if self.isOverlappingInterval :
            raise ValueError("Internal server error. Overlapping intervals found. Please correct the intervals in intervals.txt file.")

        metrics_data = {} # json data to be sent as response
        for interval, count in self.counts.items():
            metrics_data[str(interval).replace('(', '[')] = count

        metrics_data["sample mean"] = round(self.mean, 3)
        metrics_data["sample variance"] = round(self.variance, 3)
        metrics_data["outliers"] = self.outliers

        return metrics_data
