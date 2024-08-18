# -*- coding: utf-8 -*-
import unittest
import pandas as pd
import fuzzysearch
from difflib import SequenceMatcher
from argument_mining_persuade import utils
from argument_mining_persuade import metrics
from argument_mining_persuade import prompt_generation


class Test_parse_discourse_type(unittest.TestCase):
    def test1(self):
        self.assertEqual(utils.parse_discourse_type("concludingstatement"),
                         "Concluding Statement")

    def test2(self):
        self.assertEqual(utils.parse_discourse_type("concluding statement"),
                         "Concluding Statement")

    def test3(self):
        self.assertEqual(utils.parse_discourse_type("Concludingstatement"),
                         "Concluding Statement")

    def test4(self):
        self.assertEqual(utils.parse_discourse_type("Concluding Statement"),
                         "Concluding Statement")

    def test5(self):
        self.assertEqual(utils.parse_discourse_type("CONCLUDING STATEMENT"),
                         "Concluding Statement")

    def test6(self):
        self.assertEqual(utils.parse_discourse_type("something else"),
                         None)

    def test7(self):
        self.assertEqual(utils.parse_discourse_type("lead"),
                         "Lead")

    def test8(self):
        self.assertEqual(utils.parse_discourse_type("COUNTER CLAIM"),
                         "Counterclaim")

    def test9(self):
        self.assertEqual(utils.parse_discourse_type("counter claim"),
                         "Counterclaim")


class Test_start_and_end_word_idx(unittest.TestCase):
    def test1(self):
        self.assertEqual(utils._get_start_and_end_word_idx(
            "word1 wor'd2.  word3 word4, word5.", 0, 4), "0")

    def test2(self):
        self.assertEqual(utils._get_start_and_end_word_idx(
            "word1 wor'd2.  word3 word4, word5.", 15, 33), "2 3 4")
        #    0123456789012345678901234567890123


class Test_word_based_predictionstring(unittest.TestCase):
    def test_word_1(self):
        df = pd.DataFrame({"essay_id": "1",
                           "discourse_type": "Claim",
                           "full_text": "word1 wor'd2.  word3 word4, word5.",
                           "discourse_start": 15,
                           "discourse_end": 33
                           }, index=[0])
        result_df = utils.build_predictionstring_df_word(
            df, "full_text", "discourse_start", "discourse_end", "essay_id",
            "discourse_type")
        self.assertEqual(result_df.predictionstring.iloc[0], "2")
        self.assertEqual(result_df.predictionstring.iloc[1], "3")
        self.assertEqual(result_df.predictionstring.iloc[2], "4")


class Test_metrics(unittest.TestCase):
    def test_span_1(self):
        df_gt = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1 2 3"]
             })
        df_pred = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1 2 3"]
             })

        self.assertEqual(metrics.score_feedback_comp(
            df_pred, df_gt, return_class_scores=False),
            1)

    def test_span_2(self):
        df_gt = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1"]
             })
        df_pred = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1 2 3"]
             })

        self.assertEqual(metrics.score_feedback_comp(
            df_pred, df_gt, return_class_scores=False),
            1)

    def test_span_3(self):
        df_gt = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0"]
             })
        df_pred = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1 2 3"]
             })

        self.assertEqual(metrics.score_feedback_comp(
            df_pred, df_gt, return_class_scores=False),
            0)

    def test_span_4(self):
        df_gt = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Claim"],
             "predictionstring": ["0 1 2 3"]
             })
        df_pred = pd.DataFrame(
            {"essay_id": ["0"],
             "discourse_type": ["Concluding Statement"],
             "predictionstring": ["0 1 2 3"]
             })

        self.assertEqual(metrics.score_feedback_comp(
            df_pred, df_gt, return_class_scores=False),
            0)


class Test_overlap(unittest.TestCase):
    def test1(self):
        self.assertEqual(utils.check_overlap(0, 4, 1, 3), (1, 3))
        self.assertEqual(utils.check_overlap(0, 4, 4, 10), None)
        self.assertEqual(utils.check_overlap(0, 4, 2, 7), (2, 4))
        self.assertEqual(utils.check_overlap(0, 4, 5, 7), None)
        self.assertEqual(utils.check_overlap(1, 4, 1, 4), (1, 4))


class Test_parser_formatter_(unittest.TestCase):
    """
    Test the different formatters and parsers by applying both of them
    sequencially to a test df containing one essay and checking if the same
    (or almost the same output) is generatated. Very small differences might
    occur due to the handling of characters like " or '.

    Returns
    -------
    None.

    """

    def test_python_dict(self):
        df = pd.read_csv("example_essay_1_shot_A5DB60716E91.csv", index_col=0)
        df.reset_index(drop=True, inplace=True)
        formated_essay = prompt_generation.formatExampleEssayPythonDict(
            df, "", "")
        formated_essay = formated_essay.split('"""')[-1]
        output_dict = utils.parser_python_dict(formated_essay)
        dict_as_tuples = list(output_dict.items())
        self.assertEqual(len(dict_as_tuples), len(df))
        for i, row in df.iterrows():
            ratio = SequenceMatcher(None, dict_as_tuples[i][0],
                                    row.discourse_text_clean).ratio()
            self.assertTrue(ratio > 0.95)
            self.assertEqual(dict_as_tuples[i][1], row.discourse_type)

    def test_XML(self):
        df = pd.read_csv("example_essay_1_shot_A5DB60716E91.csv", index_col=0)
        df.reset_index(drop=True, inplace=True)
        formated_essay = prompt_generation.formatExampleEssayXML(df, "", "")
        # formated_essay = formated_essay.split('"""')[-1]
        output_dict = utils.parser_XML(formated_essay)
        dict_as_tuples = list(output_dict.items())
        self.assertEqual(len(dict_as_tuples), len(df))
        for i, row in df.iterrows():
            ratio = SequenceMatcher(None, dict_as_tuples[i][0],
                                    row.discourse_text_clean).ratio()
            self.assertTrue(ratio > 0.95)
            self.assertEqual(dict_as_tuples[i][1], row.discourse_type)

    def test_TANL(self):
        df = pd.read_csv("example_essay_1_shot_A5DB60716E91.csv", index_col=0)
        df.reset_index(drop=True, inplace=True)
        formated_essay = prompt_generation.formatExampleEssayTANL(df, "", "")
        # formated_essay = formated_essay.split('"""')[-1]
        output_dict = utils.parser_TANL(formated_essay)
        dict_as_tuples = list(output_dict.items())
        self.assertEqual(len(dict_as_tuples), len(df))
        for i, row in df.iterrows():
            ratio = SequenceMatcher(None, dict_as_tuples[i][0],
                                    row.discourse_text_clean).ratio()
            self.assertTrue(ratio > 0.95)
            self.assertEqual(dict_as_tuples[i][1], row.discourse_type)


if __name__ == "__main__":
    unittest.main()
