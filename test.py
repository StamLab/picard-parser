""" Tests for PicardParser (in picard_parser.py).
So far only "it-works!" tests are present, aren't any tests
for checking failures when failures should happen. """

import unittest
import logging
import sys

from picard_parser import PicardParser
from collections import OrderedDict

class TestBasicParsing(unittest.TestCase):
    
    def setUp(self):
        self.file = "examples/CollectInsertSizeMetrics.test.picard"
        self.parser = PicardParser(filename = self.file)

    def test_names_and_values_of_metrics_are_correct_and_match(self):
        metrics = self.parser.metrics
        self.assertIsNotNone(metrics)
        expected_names = ['MEDIAN_INSERT_SIZE', 'MEDIAN_ABSOLUTE_DEVIATION',
                        'MIN_INSERT_SIZE', 'MAX_INSERT_SIZE', 'MEAN_INSERT_SIZE',
                        'STANDARD_DEVIATION', 'READ_PAIRS', 'PAIR_ORIENTATION',
                        'WIDTH_OF_10_PERCENT', 'WIDTH_OF_20_PERCENT', 'WIDTH_OF_30_PERCENT', 
                        'WIDTH_OF_40_PERCENT', 'WIDTH_OF_50_PERCENT', 'WIDTH_OF_60_PERCENT', 
                        'WIDTH_OF_70_PERCENT', 'WIDTH_OF_80_PERCENT', 'WIDTH_OF_90_PERCENT',
                        'WIDTH_OF_99_PERCENT', 'SAMPLE', 'LIBRARY', 'READ_GROUP']
        expected_values = map(str,
                              [79, 26, 28, 380, 89.600433, 41.83386, 199599385, 
                               'FR', 11, 21, 31, 43, 53, 65, 75, 91, 147, 255])
        expected_metrics = OrderedDict(zip(expected_names, expected_values))
        self.assertEqual(self.parser.metrics, expected_metrics)

    def test_names_and_values_of_picard_args_are_correct_and_match(self):
        arguments = self.parser.arguments
        self.assertIsNotNone(arguments)
        expected_names = ['HISTOGRAM_FILE', 'INPUT', 'OUTPUT', 'ASSUME_SORTED', 
                          'VALIDATION_STRINGENCY', 'DEVIATIONS', 'MINIMUM_PCT', 
                          'METRIC_ACCUMULATION_LEVEL', 'STOP_AFTER', 'VERBOSITY', 
                          'QUIET', 'COMPRESSION_LEVEL', 'MAX_RECORDS_IN_RAM',
                          'CREATE_INDEX', 'CREATE_MD5_FILE']
        expected_vals = ['EXAMPLE_GATTAC_L002.CollectInsertSizeMetrics.picard.pdf',
                         'EXAMPLE_GATTAC_L002.uniques.sorted.bam', 
                         'EXAMPLE_GATTAC_L002.CollectInsertSizeMetrics.picard',
                         'true', 'LENIENT', '10.0', '0.05', '[ALL_READS]',
                         '0', 'INFO', 'false', '5', '500000', 'false', 'false']
        expected_arguments = dict(zip(expected_names, expected_vals))
        self.assertEqual(arguments, expected_arguments)

    def test_picard_module_name(self):
        self.assertEqual('picard.analysis.CollectInsertSizeMetrics', self.parser.module_name)

    def test_histogram_bins_and_values_are_correct_and_match(self):
        histogram = self.parser.histogram
        self.assertIsNotNone(histogram)
        expected_bins = range(28, 39)
        expected_values = [4, 1, 3, 11, 9, 446, 3477, 132444, 3264532, 2094, 22]
        expected_histogram = OrderedDict(zip(expected_bins, expected_values))
        self.assertEqual(histogram, expected_histogram)

class TestContentParsing(TestBasicParsing):
    """
    Run the same tests as above, except on passed content instead of a file loaded.
    """

    def setUp(self):
        self.file = "examples/CollectInsertSizeMetrics.test.picard"
        content = open(self.file, 'r').read()
        self.parser = PicardParser(content = content) 

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "picard_parser" ).setLevel( logging.DEBUG )
    unittest.main()
