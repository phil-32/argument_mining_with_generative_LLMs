# -*- coding: utf-8 -*-
# Source:
# https://www.kaggle.com/code/robikscube/student-writing-competition-twitch-stream?scriptVersionId=83303421

import numpy as np
import logging
import pandas as pd
from argument_mining_persuade import utils
import os

log = logging.getLogger('main_logger')


def calc_overlap(row):
    """
    Calculates the overlap between prediction and
    ground truth and overlap percentages used for determining
    true positives.
    """
    set_pred = set(row.predictionstring_pred.split(" "))
    set_gt = set(row.predictionstring_gt.split(" "))
    # Length of each and intersection
    len_gt = len(set_gt)
    len_pred = len(set_pred)
    inter = len(set_gt.intersection(set_pred))
    overlap_1 = inter / len_gt
    overlap_2 = inter / len_pred
    return [overlap_1, overlap_2]


def score_feedback_comp_micro(pred_df, gt_df):
    """
    A function that scores for the kaggle
        Student Writing Competition

    Uses the steps in the evaluation page here:
        https://www.kaggle.com/c/feedback-prize-2021/overview/evaluation
    """
    gt_df = (
        gt_df[["essay_id", "discourse_type", "predictionstring"]]
        .reset_index(drop=True)
        .copy()
    )
    pred_df = pred_df[
        ["essay_id", "discourse_type", "predictionstring"]].reset_index(
        drop=True).copy()
    pred_df["pred_id"] = pred_df.index
    gt_df["gt_id"] = gt_df.index
    # Step 1. all ground truths and predictions for a given class are compared.
    joined = pred_df.merge(
        gt_df,
        left_on=["essay_id", "discourse_type"],
        right_on=["essay_id", "discourse_type"],
        how="outer",
        suffixes=("_pred", "_gt"),
    )
    joined["predictionstring_gt"] = joined["predictionstring_gt"].fillna(" ")
    joined["predictionstring_pred"] = joined[
        "predictionstring_pred"].fillna(" ")

    joined["overlaps"] = joined.apply(calc_overlap, axis=1)

    # 2. If the overlap between the ground truth and prediction is >= 0.5,
    # and the overlap between the prediction and the ground truth >= 0.5,
    # the prediction is a match and considered a true positive.
    # If multiple matches exist, the match with the highest pair of overlaps
    # is taken.
    joined["overlap1"] = joined["overlaps"].apply(lambda x: eval(str(x))[0])
    joined["overlap2"] = joined["overlaps"].apply(lambda x: eval(str(x))[1])

    joined["potential_TP"] = (
        joined["overlap1"] >= 0.5) & (joined["overlap2"] >= 0.5)
    joined["max_overlap"] = joined[["overlap1", "overlap2"]].max(axis=1)
    tp_pred_ids = (
        joined.query("potential_TP")
        .sort_values("max_overlap", ascending=False)
        .groupby(["essay_id", "predictionstring_gt"])
        .first()["pred_id"]
        .values
    )

    # 3. Any unmatched ground truths are false negatives
    # and any unmatched predictions are false positives.
    fp_pred_ids = [
        p for p in joined["pred_id"].unique() if p not in tp_pred_ids]

    matched_gt_ids = joined.query("potential_TP")["gt_id"].unique()
    unmatched_gt_ids = [c for c in joined["gt_id"].unique()
                        if c not in matched_gt_ids]

    # Get numbers of each type
    TP = len(tp_pred_ids)
    FP = len(fp_pred_ids)
    FN = len(unmatched_gt_ids)
    # calc microf1
    my_f1_score = TP / (TP + 0.5 * (FP + FN))
    return my_f1_score


def score_feedback_comp(pred_df, gt_df, return_class_scores=False):
    class_scores = {}
    pred_df = pred_df[[
        "essay_id", "discourse_type", "predictionstring"]].reset_index(
        drop=True).copy()
    for discourse_type, gt_subset in gt_df.groupby("discourse_type"):
        pred_subset = (
            pred_df.loc[pred_df["discourse_type"] == discourse_type]
            .reset_index(drop=True)
            .copy()
        )
        class_score = score_feedback_comp_micro(pred_subset, gt_subset)
        class_scores[discourse_type] = class_score
    f1 = np.mean([v for v in class_scores.values()])
    if return_class_scores:
        return f1, class_scores
    return f1


def get_span_and_word_metrics(gt_df, result_df, output_dir=""):
    if len(result_df) == 0:
        return log.warning("Result data frame is empty. Results cannot be "
                           "evaluated.")
    # Span-based metrics
    prediction_df_span = utils.add_predictionstring_span(
        result_df, "original_essay_text", "discourse_start", "discourse_end")
    prediction_gt_df_span = utils.add_predictionstring_span(
        gt_df, "full_text_clean", "discourse_start", "discourse_end")
    f1_span, class_scores_span = score_feedback_comp(
        prediction_df_span, prediction_gt_df_span, return_class_scores=True)
    all_scores_span = class_scores_span.copy()
    all_scores_span["All"] = f1_span
    # Word-based metrics
    prediction_df_word = utils.build_predictionstring_df_word(
        result_df, "original_essay_text", "discourse_start", "discourse_end",
        "essay_id", "discourse_type")
    prediction_gt_df_word = utils.build_predictionstring_df_word(
        gt_df, "full_text_clean", "discourse_start", "discourse_end",
        "essay_id", "discourse_type")
    f1_word, class_scores_word = score_feedback_comp(
        prediction_df_word, prediction_gt_df_word, return_class_scores=True)
    all_scores_word = class_scores_word.copy()
    all_scores_word["All"] = f1_word

    # Construct data frame with result metrics
    metrics_df = pd.concat([pd.DataFrame(all_scores_span, index=["F1_span"]),
                            pd.DataFrame(all_scores_word, index=["F1_word"])])
    if output_dir:
        metrics_df.to_csv(os.path.join(output_dir, "metrics_df.csv"))

    log.info(f"F1_scores:\n{metrics_df.transpose().to_string()}\n")

    return metrics_df
