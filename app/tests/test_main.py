import unittest
import threading
from app.histogram import Histogram

class TestHistogram(unittest.TestCase):
    def test_invalid_intervals(self):
        # Test that erroneous inputs in the Histogram definition are flagged
        intervals = [(100, 99), (8.5, 8.7), (4, 4.5), (0, 1.1), (31.5, 41.27)]
        histogram = Histogram(intervals)
        try:
            histogram.insert_samples([2.0, 5.0, 10.0])  # Insert some samples
            self.fail("ValueError not raised")
        except ValueError as e:
            self.assertEqual(str(e), "Internal server error. Invalid intervals found. Please correct the intervals in intervals.txt file.")
    
    def test_overlapping_intervals(self):
        # Test that overlapping intervals in the Histogram definition are flagged
        intervals = [(3, 4.1), (8.5, 8.7), (4, 4.5), (0, 1.1), (3.5, 5)] # Intentionally include an overlapping interval
        histogram = Histogram(intervals)
        try:
            histogram.calculate_statistics()
            self.fail("ValueError not raised")
        except ValueError as e:
            self.assertEqual(str(e), "Internal server error. Overlapping intervals found. Please correct the intervals in intervals.txt file.")

    def test_thread_safety(self):
        # Test thread-safety with multiple threads inserting samples
        intervals = [(3, 4.1), (8.5, 8.7), (4.3, 4.5), (0, 2), (31.5, 41.27)]
        histogram = Histogram(intervals)
        num_threads = 5
        samples_per_thread = 100

        def insert_samples_thread(samples):
            for _ in range(samples):
                histogram.insert_samples([1])  # Insert a dummy sample

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=insert_samples_thread, args=(samples_per_thread,))
            threads.append(thread)

        try:
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            # Check that the total count matches the expected count
            expected_count = num_threads * samples_per_thread
            total_count = sum(histogram.counts.values())
            self.assertEqual(total_count, expected_count)
        except Exception as e:
            self.fail(f"Exception occurred: {e}")


if __name__ == '__main__':
    unittest.main()
