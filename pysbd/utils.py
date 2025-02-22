#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Rule(object):

    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def __repr__(self):
        return '<{} pattern="{}" and replacement="{}">'.format(
            self.__class__.__name__, self.pattern, self.replacement)


class Text(str):
    """Extending str functionality to apply regex rules

    https://stackoverflow.com/questions/4698493/can-i-add-custom-methods-attributes-to-built-in-python-types

    Parameters
    ----------
    str : str
        string content

    Returns
    -------
    str
        input as it is if rule pattern doesnt match
        else replacing found pattern with replacement chars
    """
    def apply(self, *rules):
        for each_r in rules:
            self = re.sub(each_r.pattern, each_r.replacement, self)
        return self


class TextSpan(object):

    def __init__(self, sent, start, end):
        """
        Sentence text and its start & end character offsets within original text

        Parameters
        ----------
        sent : str
            Sentence text
        start : int
            start character offset of a sentence in original text
        end : int
            end character offset of a sentence in original text
        """
        self.sent = sent
        self.start = start
        self.end = end

    def __repr__(self):
        return "{0}(sent='{1}', start={2}, end={3})".format(
            self.__class__.__name__, self.sent, self.start, self.end)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.sent == other.sent and self.start == other.start and self.end == self.end
        return False


if __name__ == "__main__":
    SubstituteListPeriodRule = Rule('♨', '∯')
    StdRule = Rule(r'∯', r'∯♨')
    more_rules = [Rule(r'∯♨', r'∯∯∯∯'), Rule(r'∯∯∯∯', '♨♨')]
    sample_text = Text("I. abcd ♨ acnjfe")
    output = sample_text.apply(SubstituteListPeriodRule, StdRule, *more_rules)
    print(output)
