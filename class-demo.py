#!/usr/bin/env python

# Two types sequences:
# - reads
# - references
# The reads need to:
# - Store their source
# - Keep track of the reference asignment
# - Store their sequence
# And the references need to
# - Store their taxa/label
# - Store their sequence
# - Needs to compute the score

import argparse


class Sequence:
    def __init__(self, seq: str):
        self._sequence = seq

    def score(self, other):
        score = 0
        for i, j in zip(self._sequence, other._sequence):
            if i == j:
                score += 1

        return score


class Read(Sequence):
    def __init__(self, source: str, seq: str):
        self._reference = None
        self._source = source

        super().__init__(seq)

    def assign(self, reference_ass):
        if self._reference < reference_ass:
            self._reference = reference_ass


class Reference(Sequence):
    def __init__(self, label: str, seq: str):
        self._label = label
        super().__init__(seq)

    def score(self, other):
        score = 0
        for i, j in zip(self._sequence, other._sequence):
            if i == j:
                score += 1

        return ReferenceAssigment(self, score)


class ReferenceAssigment:
    """Class that holds a refernce, and an associated score"""

    def __init__(self, ref, score):
        self._reference = ref
        self._score = score

    def __lt__(self, other):
        return self._score < other._score


def score(read, ref):
    score = 0
    for i, j in zip(read, ref):
        if i == j:
            score += 1
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--reads", required=True)

    args = parser.parse_args()

    references = []
    with open(args.reference) as reffile:
        for line in reffile:
            lsplit = line.split()
            references.append({"label": lsplit[0], "sequence": lsplit[1]})

    reads = []
    with open(args.reads) as readfile:
        for line in readfile:
            lsplit = line.split()
            reads.append({"label": lsplit[0], "sequence": lsplit[1]})

    for r in reads:
        for ref in references:
            score = score(r["sequence"], ref["sequence"])

            if "assignment" not in r:
                r["assignment"] = None

            if "score" not in r:
                r["score"] = float("-inf")

            if r["score"] < score:
                r["assignment"] = ref
                r["score"] = score

    # if __name__ == "__main__":
    #    parser = argparse.ArgumentParser()
    #    parser.add_argument("--reference", required=True)
    #    parser.add_argument("--reads", required=True)
    #
    #    args = parser.parse_args()
    #
    #    with open(args.reference) as reffile:
    #        references = [Reference(*line.split()) for line in reffile]
    #    with open(args.reads) as readfile:
    #        reads = [Read(*line.split()) for line in readfile]
    #
    #    for r in reads:
    #        for ref in references:
    #            score = ref.score(r)
    #            r.assign(ref, score)
