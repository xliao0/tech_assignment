import argparse
import json
from typing import Dict
from collections import defaultdict
import logging

logging.basicConfig(
    level=logging.WARNING,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ThresholdFinder:
    def __init__(self, target_recall: float = 0.9):
        """
        Initilization
        :param data_file_path:
        :param target_recall: Traget Recall, 0.9 as default
        """
        self.target_recall = target_recall
        self.data = {}
        self.upper_threshold = None
        self.best_threshold = None

    def load_data_from_json(self, data_file_path) -> "ThresholdFinder":
        # Load data from json file
        try:
            with open(data_file_path, "r") as f:
                data = json.load(f)
                self.data = defaultdict(dict)
                for _, entry in data.items():
                    for k in ["TP", "FP", "TN", "FN"]:
                        self.data[entry["threshold"]][k] = entry[k]
                logging.info(f"Data successfully loaded from {data_file_path}")
        except FileNotFoundError:
            logging.error(f"File {data_file_path} not found")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file {data_file_path}: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading the file: {e}")
            raise

    def cal_recall(self, threshold: float) -> float:
        # Calculate traget recall
        tp, fn = self.data[threshold]["TP"], self.data[threshold]["FN"]
        if tp + fn == 0:
            logging.warning(
                f"Recall calculation: TP + FN is 0 for threshold {threshold}"
            )
            return 0.0

        return tp / (tp + fn)

    def find_upper_threshold(self) -> "ThresholdFinder":
        # Find highest threshold w/ binary search
        thresholds = sorted(self.data.keys(), reverse=True)
        l, r = 0, len(thresholds) - 1
        while l < r:
            mid = (l + r) // 2
            recall = self.cal_recall(thresholds[mid])
            logging.debug(f"Checking recall {recall} at threshold {thresholds[mid]}")
            if recall >= self.target_recall:
                r = mid
            else:
                l = mid + 1
        self.upper_threshold = thresholds[l]
        logging.info(
            f"Upper threshold for Recall >= {self.target_recall}: {self.upper_threshold}"
        )
        return self

    def calculate_f1_score(self, threshold: float) -> float:
        # Calcaulte f1
        tp, fp = (
            self.data[threshold]["TP"],
            self.data[threshold]["FP"],
        )
        if tp + fp == 0:
            logging.warning(f"F1 calculation: TP + FP is 0 for threshold {threshold}")
            return 0.0

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = self.cal_recall(threshold)
        if precision + recall == 0:
            logging.warning(
                f"F1 calculation: precision + recall is 0 for threshold {threshold}"
            )
            return 0.0

        f1 = 2 * (precision * recall) / (precision + recall)
        return f1

    def find_best_threshold(self) -> "ThresholdFinder":
        # Find threshlod w/ best f1
        if self.upper_threshold is None:
            logging.error(
                "Upper threshold not found. Run find_upper_threshold() first."
            )
            return self

        candidates = [k for k in self.data.keys() if k <= self.upper_threshold]
        best_f1_score = -1

        for threshold in candidates:
            f1_score = self.calculate_f1_score(threshold)
            logging.debug(f"F1 score at threshold {threshold}: {f1_score}")

            if f1_score > best_f1_score:
                best_f1_score = f1_score
                self.best_threshold = threshold

        logging.info(f"Best threshold with max F1 score: {self.best_threshold}")
        return self

    def process(self, data_file_path) -> float:
        self.load_data_from_json(data_file_path)
        self.find_upper_threshold()
        self.find_best_threshold()
        return float(self.best_threshold)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the best threshold based on target recall."
    )
    parser.add_argument(
        "--data_file_path", type=str, required=True, help="Path to the JSON data file."
    )
    parser.add_argument(
        "--target_recall",
        type=float,
        default=0.9,
        help="Target recall value (default: 0.9).",
    )

    args = parser.parse_args()

    finder = ThresholdFinder(target_recall=args.target_recall)
    best_threshold = finder.process(args.data_file_path)

    if best_threshold is not None:
        print(best_threshold)
        logging.info(f"The best threshold is: {best_threshold}")
    else:
        logging.error("Failed to determine the best threshold.")
