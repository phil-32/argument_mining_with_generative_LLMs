# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, WORD, Toplevel
import pandas as pd
from dataclasses import dataclass
from typing import Any
from argument_mining_persuade import utils
from argument_mining_persuade import metrics
from argument_mining_persuade import config


LEGEND_COLOR_DICT = {
    "Lead": "#d2da00",
    "Position": "#ff9fe9",
    "Claim": "#00e862",
    "Counterclaim": "#ffa35f",
    "Rebuttal": "#01bdd6",
    "Evidence": "#a99534",
    "Concluding Statement": "#a2fff0",
    "Overlap": "#ff0000",
    }

DEFAULT_GT_DF = config.TEST_DATASET_PATH
DEFAULT_PRED_DF = ""


class EssayViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Essay Viewer")
        master.geometry("1400x800")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gt_load_button = tk.Button(
            master, text="Load File with ground truth", height=2,
            command=self.file_open_and_load_gt_file)
        self.gt_load_button.grid(row=0, column=2, columnspan=1, sticky="wens")

        self.pred_load_button = tk.Button(
            master, text="Load File with LLM preditions", height=2,
            command=self.file_open_and_load_pred_file)
        self.pred_load_button.grid(row=0, column=3, columnspan=1,
                                   sticky="wens")

        self.gt_file_label = tk.Label(master, text="No file selected",
                                      wraplength=500)
        self.gt_file_label.grid(row=1, column=2, columnspan=1)

        self.pred_file_label = tk.Label(master, text="No file selected",
                                        wraplength=500)
        self.pred_file_label.grid(row=1, column=3, columnspan=1)

        self.show_next_button = tk.Button(
            master, text="Show next essay >", height=2,
            command=self.show_next_essay)
        self.show_next_button.grid(row=0, column=0, columnspan=2,
                                   sticky="wens")
        self.show_previous_button = tk.Button(
            master, text="< Show previous essay", height=2,
            command=self.show_previous_essay)
        self.show_previous_button.grid(row=1, column=0, columnspan=2,
                                       sticky="wens")

        self.index_label = tk.Label(master, text="Enter row index:")
        self.index_label.grid(row=2, column=0, sticky="w")
        self.index_entry = tk.Entry(master)
        self.index_entry.grid(row=2, column=1, sticky="w")
        self.show_button_index = tk.Button(
            master, text="Show essay at index",
            command=lambda: self.show_essay("index"))
        self.show_button_index.grid(row=3, column=0, columnspan=2,
                                    sticky="wens")

        self.essay_id_label = tk.Label(master, text="Enter essay ID:")
        self.essay_id_label.grid(row=4, column=0, sticky="w")
        self.essay_id_entry = tk.Entry(master)
        self.essay_id_entry.grid(row=4, column=1)
        self.show_button_id = tk.Button(
            master, text="Show essay with essay ID",
            command=lambda: self.show_essay("essay_id"))
        self.show_button_id.grid(row=5, column=0, columnspan=2, sticky="wens")

        master.grid_columnconfigure(0, minsize=20)
        master.grid_columnconfigure(1, minsize=20)
        master.grid_columnconfigure(2, weight=3)
        master.grid_columnconfigure(3, weight=3)
        master.grid_rowconfigure(0, weight=1, minsize=20)
        master.grid_rowconfigure(1, weight=1, minsize=20)
        master.grid_rowconfigure(2, weight=1, minsize=20)
        master.grid_rowconfigure(3, weight=1, minsize=20)
        master.grid_rowconfigure(4, weight=1, minsize=20)
        master.grid_rowconfigure(5, weight=1, minsize=20)
        master.grid_rowconfigure(6, weight=1, minsize=20)

        @dataclass
        class AddtionalRow():
            col_name: str
            label_name: str
            grid_row: int
            label_obj: Any
            entry_obj: Any

        # Add addtional information from df
        self.additional_rows = {
            'holistic_essay_score': "Holistic essay score",
            'prompt_name': "Prompt name",
            'task': "Task type",
            'grade_level': "Grade level",
            'ell_status': "English learner status",
            'essay_word_count': "Official word count",
            'word_count_clean': "Corrected word count",
            'token_count_cleaned_text': "Token count (GPT 3.5)",
            'ratio_token_to_words': "Ratio token/words",
            }
        current_row = 6  # start row (self.master.grid_size()[0] does not work)

        for col_name, label_name in self.additional_rows.items():
            label = tk.Label(master, text=label_name)
            label.grid(row=current_row, column=0, sticky="w")
            entry = tk.Entry(master)
            entry.grid(row=current_row, column=1)
            master.grid_rowconfigure(current_row, weight=1, minsize=20)
            self.additional_rows[col_name] = AddtionalRow(
                col_name, label_name, current_row, label, entry)
            current_row += 1

        # Show f1 scores for this essay
        self.show_f1_scores_button = tk.Button(
            master, text="Show essay F1 scores", height=2,
            command=self.showF1Scores)
        self.show_f1_scores_button.grid(row=current_row, column=0,
                                        columnspan=2, sticky="wens")

        # Text widgets
        self.legend_text = tk.Text(master, wrap=WORD, height=2,
                                   font=("Times New Roman", 14))
        self.legend_text.grid(row=2, column=2, columnspan=2, sticky="nwes")
        self.gt_text = tk.Text(master, wrap=WORD,
                               font=("Times New Roman", 14))
        self.gt_text.grid(row=3, column=2, rowspan=20, sticky="nwes")
        self.pred_text = tk.Text(master, wrap=WORD,
                                 font=("Times New Roman", 14))
        self.pred_text.grid(row=3, column=3, rowspan=20, sticky="nwes")
        self.fillLegend()

        # Definition of shortcuts
        self.master.bind("<Right>", self.right_key_press)
        self.master.bind("<Left>", self.left_key_press)

        # Set default value
        self.index_entry.insert(0, "0")
        self.load_gt_file(DEFAULT_GT_DF)
        self.load_pred_file(DEFAULT_PRED_DF)
        self.show_essay("index")

    def file_open_and_load_gt_file(self):
        self.load_gt_file(filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]))

    def file_open_and_load_pred_file(self):
        self.load_pred_file(filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]))

    def load_gt_file(self, file_path):
        if file_path:
            self.df = pd.read_csv(file_path, index_col=0)
            self.gt_file_label.config(text="File: " + file_path)
            # to_del = [
            #     'discourse_id', 'discourse_text', 'discourse_text_clean',
            #     'discourse_type', 'discourse_start',
            #     'discourse_end', 'discourse_start_clean',
            #     'discourse_end_clean', 'discourse_type_num',
            #     'similarity_ratio', 'discourse_effectiveness']
            # for column_name in to_del:
            #     if column_name in self.essay_df.columns:
            #         self.essay_df.drop(column_name, axis=1, inplace=True)
            self.essay_df = self.df.drop_duplicates(
                "essay_id", ignore_index=True, keep='first')
            self.essay_df.reset_index(inplace=True, drop=True)

    def load_pred_file(self, file_path):
        if file_path:
            self.pred_df = pd.read_csv(file_path, index_col=0)
            self.pred_file_label.config(text="File: " + file_path)
        else:
            self.pred_df = None

    def right_key_press(self, event):
        self.show_next_essay()

    def left_key_press(self, event):
        self.show_previous_essay()

    def show_next_essay(self):
        s = self.index_entry.get()
        current_index = int(s)
        if current_index < len(self.essay_df) - 1:
            self.index_entry.delete(0, tk.END)
            self.index_entry.insert(0, str(current_index + 1))
        self.show_essay("index")

    def show_previous_essay(self):
        current_index = int(self.index_entry.get())
        if current_index > 0:
            self.index_entry.delete(0, tk.END)
            self.index_entry.insert(0, str(current_index - 1))
        self.show_essay("index")

    def show_essay(self, mode):
        row_index_input = self.index_entry.get()
        if mode == "index":
            row_index = int(row_index_input)
            essay_text = self.essay_df.loc[row_index, 'full_text_clean']
            # Update essay_id entry
            essay_id = self.essay_df.loc[row_index, 'essay_id']
            self.essay_id_entry.delete(0, tk.END)
            self.essay_id_entry.insert(0, essay_id)
            self.setAddtionalColumnValues(self.essay_df.iloc[row_index])
            # Write text to text widget
            self.printTextAndTagDiscourseUnits(
                essay_text, essay_id, self.gt_text, self.df,
                "discourse_start_clean", "discourse_end_clean")

        elif mode == "essay_id":
            essay_id = self.essay_id_entry.get()
            essay_row = self.essay_df[
                self.essay_df.essay_id == essay_id]
            essay_text = essay_row['full_text_clean']
            self.index_entry.delete(0, tk.END)
            self.index_entry.insert(0, essay_row.index[0])
            self.setAddtionalColumnValues(
                self.essay_df.iloc[essay_row.index[0]])
            self.printTextAndTagDiscourseUnits(
                essay_row.full_text_clean.iloc[0], essay_id, self.gt_text,
                self.df, "discourse_start_clean", "discourse_end_clean")

        # Show corresponding prediction essay if predictions exist for that
        # essay
        if not (self.pred_df is None):
            if essay_id in self.pred_df.essay_id.values:
                self.printTextAndTagDiscourseUnits(
                    essay_text, essay_id, self.pred_text, self.pred_df,
                    "discourse_start", "discourse_end")
            else:
                self.pred_text.delete(1.0, tk.END)
                self.pred_text.insert(
                    tk.END, "No predictions found for this essay")
        else:
            self.pred_text.delete(1.0, tk.END)
            self.pred_text.insert(
                tk.END, "No prediction data frame loaded")

    def setAddtionalColumnValues(self, df_row):
        for col_name, obj in self.additional_rows.items():
            val = df_row[col_name]
            obj.entry_obj.delete(0, tk.END)
            obj.entry_obj.insert(0, val)

    def fillLegend(self):
        for discourse_type, color in LEGEND_COLOR_DICT.items():
            # Remove spaces in discourse type because they are not allowed in
            # tags
            self.legend_text.tag_configure(discourse_type.replace(" ", ""),
                                           background=color)
            # Create the same tags in the output window too
            self.gt_text.tag_configure(discourse_type.replace(" ", ""),
                                       background=color)
            self.pred_text.tag_configure(discourse_type.replace(" ", ""),
                                         background=color)
            self.legend_text.insert(tk.END, discourse_type,
                                    discourse_type.replace(" ", ""))
            self.legend_text.insert(tk.END, "  ")

    def printTextAndTagDiscourseUnits(
            self, essay_text, essay_id, text_widget, df, discourse_start_col,
            discourse_end_col):
        text_widget.delete(1.0, tk.END)
        essay_du_df = df[df["essay_id"] == essay_id].sort_values(
            discourse_start_col)
        # Get discourse units for essay
        cursor_pos = 0
        overlap_list = []
        for i, discourse_row in essay_du_df.iterrows():
            start = discourse_row[discourse_start_col]
            end = discourse_row[discourse_end_col]
            # Check of overlaps in discourse units
            for j, discourse2_row in essay_du_df.iterrows():
                # exclude overlap calculation for the same discourse unit
                if i != j:
                    overlap = utils.check_overlap(
                        start, end, discourse2_row[discourse_start_col],
                        discourse2_row[discourse_end_col])
                    if overlap:
                        overlap_list.append(overlap)
            # Add non argument section before current discourse unit if there
            # is one.
            if cursor_pos < start:
                text_widget.insert(
                    tk.END, essay_text[cursor_pos:start])
            
            # In case of overlap with the previous discourse unit: add only the
            # part that is not overlapping (the overlap will be tagged later)
            if cursor_pos > start:
                text_widget.insert(
                    tk.END, essay_text[cursor_pos:end],
                    discourse_row.discourse_type.replace(" ", ""))
            # Add the discourse unit text with tag if curser postion is equal
            # to start
            else:
                text_widget.insert(
                    tk.END, essay_text[start:end],
                    discourse_row.discourse_type.replace(" ", ""))
            # Only set new cursor position if the end is behind the current
            # cursor positon (is might be before in case of small overlapping)
            # predicitons
            if end > cursor_pos:
                cursor_pos = end

        # Add no-argument section at the end of the text if there is one
        if cursor_pos < len(essay_text):
            text_widget.insert(tk.END, essay_text[cursor_pos:])

        # Tag overlap sequences:
        for i, (start, end) in enumerate(set(overlap_list)):
            text_widget.tag_add("Overlap",
                                self.convertIndex(essay_text, start),
                                self.convertIndex(essay_text, end))

    def convertIndex(self, text, index):
        # Line breaks count as one character but in the slices are counted as 2
        num_of_line_breaks = text[:index].count(r"\n")
        return f"1.0+{index - num_of_line_breaks}c"

    def showF1Scores(self):
        gt_df = self.df[self.df["essay_id"] == self.essay_id_entry.get()]
        pred_df = self.pred_df[
            self.pred_df["essay_id"] == self.essay_id_entry.get()]
        if len(gt_df) > 0 and len(pred_df) > 0:
            metrics_df = metrics.get_span_and_word_metrics(gt_df, pred_df)
            output = metrics_df.transpose().to_string()
        else:
            output = "No predictions or ground truth for this essay!"

        metrics_window = Toplevel(self.master)
        metrics_window.title("Essay F1 scores")
        results = tk.Label(metrics_window,
                           text=output, justify=tk.LEFT,
                           foreground="black", font=("Courier", 14))
        results.grid(row=0, column=0, columnspan=3)

    def on_closing(self):
        self.master.quit()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EssayViewerApp(root)
    root.mainloop()
