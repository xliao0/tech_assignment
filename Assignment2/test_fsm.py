import pytest
from finit_state_machine import FSM, Mode3FSM


def test_fsm_base_class():
    # Test base FSM class with a simple binary counter
    state_map = {
        "A": {"0": "A", "1": "B"},
        "B": {"0": "A", "1": "B"}
    }
    output_map = {"A": 0, "B": 1}
    fsm = FSM(state_map, output_map, "A")
    
    assert fsm.process("0") == 0
    assert fsm.process("1") == 1
    assert fsm.process("000001") == 1

def test_mode3fsm_extended():
    fsm = Mode3FSM()
    
    # Test empty input
    assert fsm.process("") == 0
    
    # Test single digits
    assert fsm.process("0") == 0
    assert fsm.process("1") == 1
    
    # Test multiple digits
    assert fsm.process("10") == 2
    assert fsm.process("11") == 0
    
    # Test longer sequences
    assert fsm.process("1101") == 1
    assert fsm.process("1110") == 2
    assert fsm.process("1111") == 0
    
    # Test error cases
    with pytest.raises(ValueError):
        fsm.process("12")
    with pytest.raises(ValueError):
        fsm.process("a")

def test_fsm_state_transitions():
    fsm = Mode3FSM()
    
    # Test internal state transitions
    fsm.process("1")  # Should end in S1
    assert fsm.state == "S0"  # Should be reset
    
    # Test reset functionality
    fsm.process("101")
    fsm.reset()
    assert fsm.state == "S0"