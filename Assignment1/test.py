import pytest
from best_threshold import ThresholdFinder
from finit_state_machine import Mode3FSM


def test_thresholdfinder():
    finder = ThresholdFinder()
    data_path = "data.json"
    assert finder.process(data_path) == pytest.approx(0.6)


def test_fsm():
    fsm = Mode3FSM()
    assert fsm.process("1101") == 1
    assert fsm.process("1110") == 2
    assert fsm.process("1111") == 0

    # empty input
    fsm.reset()
    assert fsm.process("") == 0

    # invalid input
    with pytest.raises(ValueError):
        fsm.process("1021")


test_fsm()
