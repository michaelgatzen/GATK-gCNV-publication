from callset import CallsetMatrixView, Callset, GCNVCallset, TruthCallset
from interval_collection import IntervalCollection
from interval import Interval
from event import EventType
import pandas as pd
import pyranges as pr
import numpy as np

pd.set_option("display.max_rows", None, "display.max_columns", None)

# analyzed intervals original
ANALYZED_INTERVALS_ORIGINAL = "./test_files/analyzed_intervals.interval_list"

# analyzed intervals random
ANALYZED_INTERVALS_RANDOM = "./test_files/analyzed_intervals.not.subset.interval_list"

# gCNV test callset resources
GCNV_CALLSET_SAMPLE_0_TEST_VCF = "./test_files/GCNV_SAMPLE_0.vcf"
GCNV_CALLSET_SAMPLE_1_TEST_VCF = "./test_files/GCNV_SAMPLE_1.vcf"
GCNV_CALLSET_SAMPLE_2_TEST_VCF = "./test_files/GCNV_SAMPLE_2.vcf"
GCNV_CALLSET_SAMPLE_3_TEST_VCF = "./test_files/GCNV_SAMPLE_3.vcf"
GCNV_CALLSET_SAMPLE_1_TEST_VALUES = [('1', 1001, 3000, EventType.DEL, 2, 60, 0),
                                     ('2', 4001, 5000, EventType.DUP, 1, 100, 0)]

GCNV_CALLSET_SAMPLE_0_SAMPLE_NAME = "SAMPLE_0"
GCNV_CALLSET_SAMPLE_1_SAMPLE_NAME = "SAMPLE_1"
GCNV_CALLSET_SAMPLE_2_SAMPLE_NAME = "SAMPLE_2"
GCNV_CALLSET_SAMPLE_3_SAMPLE_NAME = "SAMPLE_3"
GCNV_CALLSET_TEST_DF = pd.DataFrame(GCNV_CALLSET_SAMPLE_1_TEST_VALUES, columns=Callset.CALLSET_COLUMNS)
GCNV_CALLSET_TEST_DF = GCNV_CALLSET_TEST_DF.astype(Callset.CALLSET_COLUMN_TYPES)
GCNV_CALLSET_TEST_PYRANGE_EXPECTED = pr.PyRanges(GCNV_CALLSET_TEST_DF)

GCNV_FULL_CALLSET_INTERVAL_TO_TARGET_MAP_EXPECTED = {Interval("1", 1001, 3000): {'1:400-1400', '1:2500-2501'},
                                                     Interval("1", 2001, 4000): {'1:2500-2501', '1:3500-5500'},
                                                     Interval("1", 5001, 6000): {'1:3500-5500'}}

# Truth test callset resources
TRUTH_CALLSET_TEST_BED = "./test_files/truth.bed"
TRUTH_CALLSET_VALUES = [('1', 501, 4500, 'DEL_chr1_1', EventType.DEL, frozenset(['SAMPLE_0', 'SAMPLE_1', 'SAMPLE_2']), 1.0, 3),
                        ('1', 7001, 10000, 'DEL_chr1_2', EventType.DEL, frozenset(['SAMPLE_0']), 1./3, 2),
                        ('2', 1001, 3000, 'DUP_chr2_1', EventType.DUP, frozenset(['SAMPLE_0']), 1./3, 0),
                        ('2', 4001, 7000, 'DUP_chr2_2', EventType.DUP, frozenset(['SAMPLE_0', 'SAMPLE_1']), 2./3, 2),
                        ('2', 11001, 12000, 'DUP_chr_2_3', EventType.DUP, frozenset(['SAMPLE_0', 'SAMPLE_2']), 2./3, 1),
                        ('2', 13001, 16000, 'DEL_chr_2_4', EventType.DEL, frozenset(['SAMPLE_2']), 1./3, 1)]

SAMPLES_TO_KEEP = {'SAMPLE_0', 'SAMPLE_1', 'SAMPLE_2'}
TRUTH_CALLSET_TEST_DF = pd.DataFrame(TRUTH_CALLSET_VALUES, columns=TruthCallset.JOINT_CALLSET_COLUMNS)
TRUTH_CALLSET_TEST_DF = TRUTH_CALLSET_TEST_DF.astype(TruthCallset.JOINT_CALLSET_COLUMN_TYPES)
TRUTH_CALLSET_TEST_PYRANGE_EXPECTED = pr.PyRanges(TRUTH_CALLSET_TEST_DF)
TRUTH_CALLSET_TEST_FILTERED_PYRANGE_EXPECTED = pr.PyRanges(TRUTH_CALLSET_TEST_DF.iloc[[0, 1, 3, 4, 5]])

TRUTH_CALLSET_SAMPLE_TO_PYRANGE_MAP = {'SAMPLE_0': [('1', 501, 4500, EventType.DEL, 3, 0, 1.0),
                                                    ('1', 7001, 10000, EventType.DEL, 2, 0, 1./3),
                                                    ('2', 4001, 7000, EventType.DUP, 2, 0, 2./3),
                                                    ('2', 11001, 12000, EventType.DUP, 1, 0, 2./3)],
                                       'SAMPLE_1': [('1', 501, 4500, EventType.DEL, 3, 0, 1.0),
                                                    ('2', 4001, 7000, EventType.DUP, 2, 0, 2./3)],
                                       'SAMPLE_2': [('1', 501, 4500, EventType.DEL, 3, 0, 1.0),
                                                    ('2', 11001, 12000, EventType.DUP, 1, 0, 2./3),
                                                    ('2', 13001, 16000, EventType.DEL, 1, 0, 1./3)]}
for s in TRUTH_CALLSET_SAMPLE_TO_PYRANGE_MAP.keys():
    TRUTH_CALLSET_SAMPLE_TO_PYRANGE_MAP[s] = pr.PyRanges(pd.DataFrame(TRUTH_CALLSET_SAMPLE_TO_PYRANGE_MAP[s],
                                                                      columns=Callset.CALLSET_COLUMNS)
                                                         .astype(Callset.CALLSET_COLUMN_TYPES))

TRUTH_CALLSET_CALLSET_MATRIX_VIEW_SAMPLES = ['SAMPLE_0', 'SAMPLE_1', 'SAMPLE_2']
TRUTH_CALLSET_CALLSET_MATRIX_VIEW_GENOTYPES = np.array([[1, 1, 1, 0, 1, 1, 2, 2, 2],
                                                        [1, 1, 1, 0, 0, 0, 2, 2, 0],
                                                        [1, 1, 1, 0, 0, 0, 0, 0, 1]])
TRUTH_CALLSET_CALLSET_MATRIX_VIEW_QUALITIES = np.zeros(shape=TRUTH_CALLSET_CALLSET_MATRIX_VIEW_GENOTYPES.shape)
TRUTH_CALLSET_CALLSET_MATRIX_VIEW_EXPECTED = CallsetMatrixView(TRUTH_CALLSET_CALLSET_MATRIX_VIEW_SAMPLES,
                                                               TRUTH_CALLSET_CALLSET_MATRIX_VIEW_GENOTYPES,
                                                               TRUTH_CALLSET_CALLSET_MATRIX_VIEW_QUALITIES)
TRUTH_CALLSET_RARE_INTERVALS_SUBSET_VALUES = [('1', 5001, 6000),
                                              ('1', 7001, 8000),
                                              ('1', 9001, 10000),
                                              ('2', 10001, 15000)]
TRUTH_CALLSET_RARE_INTERVALS_SUBSET_DF = pd.DataFrame(TRUTH_CALLSET_RARE_INTERVALS_SUBSET_VALUES,
                                                      columns=IntervalCollection.INTERVAL_COLLECTION_COLUMNS)
TRUTH_CALLSET_RARE_INTERVALS_SUBSET_DF = TRUTH_CALLSET_RARE_INTERVALS_SUBSET_DF.astype(IntervalCollection.INTERVAL_COLLECTION_COLUMN_TYPES)

TRUTH_CALLSET_RARE_INTERVALS_SUBSET_PYRANGE_EXPECTED = pr.PyRanges(TRUTH_CALLSET_RARE_INTERVALS_SUBSET_DF)

GCNV_CALLSET_MATRIX_TEST_VCF = "./test_files/GCNV_SAMPLE_0.vcf"
GCNV_CALLSET_MATRIX_VIEW_SAMPLES = ['SAMPLE_0']
GCNV_CALLSET_MATRIX_VIEW_GENOTYPES = np.array([[0, 1, 1, 1, 2, 2, 0, 0, 2]])
GCNV_CALLSET_MATRIX_VIEW_QUALITIES = np.array([[20, 60, 60, 10, 20, 20, 100, 100, 0]])
GCNV_CALLSET_MATRIX_VIEW_EXPECTED = CallsetMatrixView(GCNV_CALLSET_MATRIX_VIEW_SAMPLES,
                                                      GCNV_CALLSET_MATRIX_VIEW_GENOTYPES,
                                                      GCNV_CALLSET_MATRIX_VIEW_QUALITIES)


def test_gcnv_callset():
    interval_collection = IntervalCollection.read_interval_list(ANALYZED_INTERVALS_ORIGINAL)
    gcnv_callset_actual = GCNVCallset.read_in_callset(gcnv_segment_vcfs=[GCNV_CALLSET_SAMPLE_0_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_1_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_2_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_3_TEST_VCF],
                                                      gcnv_joint_vcf=None,
                                                      interval_collection=interval_collection)

    print(gcnv_callset_actual.sample_to_pyrange_map[GCNV_CALLSET_SAMPLE_1_SAMPLE_NAME].df)
    #assert gcnv_callset_actual.sample_to_pyrange_map[GCNV_CALLSET_SAMPLE_1_SAMPLE_NAME].df.equals(GCNV_CALLSET_TEST_PYRANGE_EXPECTED.df)


def test_truth_callset():
    interval_collection = IntervalCollection.read_interval_list(ANALYZED_INTERVALS_ORIGINAL)
    # Test callset parsing
    truth_callset_actual = TruthCallset.read_in_callset(truth_callset_bed_file=TRUTH_CALLSET_TEST_BED,
                                                        interval_collection=interval_collection,
                                                        samples_to_keep=SAMPLES_TO_KEEP)
    from interval import Interval
    from collections import defaultdict
    interval_to_target_map = defaultdict(lambda: set())

    # joined_intervals = truth_callset_actual.truth_callset_pyrange.join(interval_collection.pyrange)
    # print(joined_intervals.df)
    # for k, df in joined_intervals:
    #     for index, event in df.iterrows():
    #         interval = Interval(event['Chromosome'], event['Start'], event['End'])
    #         interval_to_target_map[interval].add(str(Interval(event['Chromosome'], event['Start_b'], event['End_b'])))
    # [print(str(i) + ":" + str(interval_to_target_map[i])) for i in interval_to_target_map.keys()]

    assert truth_callset_actual.truth_callset_pyrange.df.equals(TRUTH_CALLSET_TEST_PYRANGE_EXPECTED.df)

    # Test filtering
    truth_callset_actual.filter_out_uncovered_events_from_joint_callset(interval_collection, min_overlap_fraction=0.3)
    assert truth_callset_actual.truth_callset_pyrange.df.equals(TRUTH_CALLSET_TEST_FILTERED_PYRANGE_EXPECTED.df)

    for s in truth_callset_actual.sample_set:
        assert truth_callset_actual.sample_to_pyrange_map[s].df.equals(TRUTH_CALLSET_SAMPLE_TO_PYRANGE_MAP[s].df)

    joined_sample_level_callsets_df = pd.concat([truth_callset_actual.sample_to_pyrange_map[s].df for s in truth_callset_actual.sample_set], ignore_index=True)
    joined_sample_level_callset_pr = pr.PyRanges(joined_sample_level_callsets_df)
    #print(joined_sample_level_callsets_df)
    #print(joined_sample_level_callsets_df.groupby(["Chromosome", "Start", "End"]).apply(lambda group: sum(group['NumBins'])))
    rare_intervals_subset_actual = truth_callset_actual.subset_intervals_to_rare_regions(interval_collection,
                                                                                         max_allelic_fraction=0.5)
    assert rare_intervals_subset_actual.pyrange.df.equals(TRUTH_CALLSET_RARE_INTERVALS_SUBSET_PYRANGE_EXPECTED.df)


def test_target_caching():
    interval_collection = IntervalCollection.read_interval_list(ANALYZED_INTERVALS_RANDOM)
    gcnv_callset_actual = GCNVCallset.read_in_callset(gcnv_segment_vcfs=[GCNV_CALLSET_SAMPLE_0_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_1_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_2_TEST_VCF,
                                                                         GCNV_CALLSET_SAMPLE_3_TEST_VCF],
                                                      gcnv_joint_vcf=None,
                                                      interval_collection=interval_collection)
    assert GCNV_FULL_CALLSET_INTERVAL_TO_TARGET_MAP_EXPECTED == gcnv_callset_actual.cached_interval_to_targets_map


def test_sample_by_interval_matrix():
    interval_collection = IntervalCollection.read_interval_list(ANALYZED_INTERVALS_ORIGINAL)
    # Test callset parsing
    truth_callset = TruthCallset.read_in_callset(truth_callset_bed_file=TRUTH_CALLSET_TEST_BED,
                                                 interval_collection=interval_collection,
                                                 samples_to_keep=SAMPLES_TO_KEEP)
    callset_matrix_view_actual = truth_callset.get_callset_matrix_view(interval_collection, list(truth_callset.sample_set))
    print(callset_matrix_view_actual.samples_by_intervals_quality_matrix)
    assert callset_matrix_view_actual == TRUTH_CALLSET_CALLSET_MATRIX_VIEW_EXPECTED

    gcnv_callset = GCNVCallset.read_in_callset(gcnv_segment_vcfs=[GCNV_CALLSET_MATRIX_TEST_VCF])
    gcnv_callset_matrix_view_actual = gcnv_callset.get_callset_matrix_view(interval_collection, list(gcnv_callset.sample_set))
    print(gcnv_callset_matrix_view_actual.samples_by_intervals_quality_matrix)
    assert gcnv_callset_matrix_view_actual == GCNV_CALLSET_MATRIX_VIEW_EXPECTED


def main():
    test_gcnv_callset()
    #test_truth_callset()
    #test_target_caching()
    #test_sample_by_interval_matrix()


if __name__ == '__main__':
    main()
