""" Picard Parser takes a picard file or content and collects the info into
four attributes:
1) arguments, an unordered dict of the arguments given to the picard run that
produced this input, mapping arg names to values.
2) module_name, a string with the name of the picard module that was run to make input
3) metrics, an ordered dict for the METRICS section, mapping metric names to values
4) histogram, an ordered dict for the HISTOGRAM section mapping bins to values

Works with any of CollectInsertSizeMetrics, MarkDuplicates, 
MeanQualityByCycle and CollectAlignmentSummaryMetrics. 
For the MeanQualityByCycle and CollectAlignmentSummaryMetrics inputs,
the former doesn't have metrics and the latter doesn't have a histogram,
so those attributes will be None, respectively. """
# Max Peterson
# December 29 2014

import re
import StringIO
from collections import OrderedDict

METRICS_KEYWORD = 'METRICS CLASS'
HISTOGRAM_KEYWORD = 'HISTOGRAM'
SUMMARY_FILE = 'picard.analysis.CollectAlignmentSummaryMetrics'
QUALITY_FILE = 'picard.analysis.MeanQualityByCycle'
class PicardParser(object):

    def _check_not_found(self, obj, descriptor="some"):
        """ raises ValueError if obj is false
        descriptor is a string for the error message """
        if not obj:
            raise ValueError("Failed to find " + descriptor + " in input.")

    def _skip_ahead_to_keyword(self, keyword):
        """ skips through input until a line matching keyword is found.
        Stops at first matching line & discards that line. """

        line = self.input.readline()
        while line and re.search(keyword, line) is None:
            line = self.input.readline()

    def _get_picard_module_name(self, line):
        """ gets the picard module name from line 
        module name in input must & be of the form picard.[word].[word].
        raises ValueError if module name not found"""

        match = re.search("(picard\.\w+\.\w+)", line)
        self._check_not_found(match, 'Picard module name')
        return match.group(1)

    def _collect_arguments(self, line):
        """ line is the second line of a picard input, with the names & values of
        all the arguments given to the picard program. If no = signs present
        (i.e. "line" is the wrong line), raises ValueError.
        Returns unordered dict mapping each picard argument name to its value. """

        match = re.search("(\w+=.*)", line)
        self._check_not_found(match, 'Picard module arguments')
        args_list = match.group(1).split()
        args_dict = dict()
        for arg in args_list:
            name, val = arg.split('=')
            args_dict[name] = val
        return args_dict

    def _collect_metrics(self):
        """ returns an OrderedDict mapping the name of each metric to its value.
        assumes input currently at line with metric names """

        metric_names = self.input.readline().split("\t")
        metric_values = self.input.readline().split("\t")
        metrics = OrderedDict(zip(metric_names, metric_values))
        self._check_not_found(metrics, METRICS_KEYWORD)
        return metrics

    def _collect_histogram(self):
        """ assumes input currently at line just before histogram values.
        histogram values must be the last things in input, else raises
        ValueError.
        returns an OrderedDict mapping bins to values from 
        the histogram info from input """

        self.header = self.input.readline()
        histogram = OrderedDict()
        line = self.input.readline().strip()
        while line:
            bucket, freq = line.split()
            try:
                float(bucket), float(freq)
            except ValueError:
                raise ValueError("found non-numeric histogram bin or value.\n" +\
                                 "Are histogram bins & vals the last things " +\
                                 "in input (they should be)?\n" +\
                                 "Problem line: " + line)
            bucket = int(bucket) if bucket.isdigit() else float(bucket)
            freq = int(freq) if freq.isdigit() else float(freq)
            histogram[bucket] = freq
            line = self.input.readline().strip()
        self._check_not_found(histogram, HISTOGRAM_KEYWORD)
        return histogram

    def __init__(self, filename = None, content = None):
        if filename:
            self.input = open(filename, 'r')
        elif content:
            self.input = StringIO.StringIO(content)
        else:
            raise ValueError('PicardParser requires a filename or content')

        self.input.readline() # first info we want is on 2nd line, so burn first line
        second_line = self.input.readline()
        self.module_name = self._get_picard_module_name(second_line)
        self.metrics, self.histogram, self.arguments = None, None, None
        # Summary file doesn't have a picard arguments, so skip if we're using that input
        if not self.module_name == SUMMARY_FILE:
            self.arguments = self._collect_arguments(second_line)
        # Quality file doesn't have metrics
        if not self.module_name == QUALITY_FILE:
            self._skip_ahead_to_keyword(METRICS_KEYWORD)
            self.metrics = self._collect_metrics()
        # Summary file doesn't have a histogram
        if not self.module_name == SUMMARY_FILE:
            self._skip_ahead_to_keyword(HISTOGRAM_KEYWORD)
            self.histogram = self._collect_histogram()
        self.input.close()
