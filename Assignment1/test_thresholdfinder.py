import pytest
import json
from best_threshold import ThresholdFinder


def test_thresholdfinder():
    finder = ThresholdFinder()
    data_path = "data.json"
    assert finder.process(data_path) == pytest.approx(0.6)


def test_edge_cases():
    finder = ThresholdFinder()

    # Test empty data
    with pytest.raises(FileNotFoundError):
        finder.process("nonexistent.json")

    # Test invalid JSON
    with pytest.raises(json.JSONDecodeError):
        finder.process("invalid.json")

    # Test different target recalls
    finder = ThresholdFinder(target_recall=0.95)
    assert finder.process("data.json") < 0.6


def test_calculation_methods():
    finder = ThresholdFinder()
    finder.load_data_from_json("data.json")

    # Test recall calculation
    assert finder.cal_recall(0.1) == 1.0

    # Test F1 score calculation
    assert 0 <= finder.calculate_f1_score(0.6) <= 1
