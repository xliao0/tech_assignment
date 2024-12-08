from typing import Dict
import logging
import argparse

logging.basicConfig(
    level=logging.WARNING,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FSM:
    def __init__(self, state_map: Dict, output_map: Dict, initial_state):
        """
        Generic FSM implementation.

        Provides a base implementation for any FSM with:
        - Discrete states
        - State transitions based on input symbols
        - Output values associated with states

        Attributes:
            state_map (Dict): Maps (state, input) pairs to next states
            output_map (Dict): Maps states to output values
            initial_state: The starting state of the FSM
            state: Current state of the FSM
        """
        self.state_map = state_map
        self.output_map = output_map
        self.initial_state = initial_state
        self.state = initial_state

    def reset(self):
        self.state = self.initial_state

    def get_output(self, state):
        return self.output_map[state]

    def process(self, s: str):
        """
        Process a string of input symbols through the FSM.
        Args: s (str): Input string to process
        Returns: Any: Output value associated with the final state
        Raises: ValueError: If an invalid input symbol is encountered
        """
        for c in s:
            if c not in self.state_map[self.state]:
                logging.error(f"Invalid input: {c} for state: {self.state}")
                raise ValueError(f"Invalid input '{c}' for state '{self.state}'")
            self.state = self.state_map[self.state][c]
        out = self.get_output(self.state)
        self.reset()
        return out


class Mode3FSM(FSM):
    def __init__(self):
        three_mode_state_map = {
            "S0": {"0": "S0", "1": "S1"},
            "S1": {"0": "S2", "1": "S0"},
            "S2": {"0": "S1", "1": "S2"},
        }
        output_map = {"S0": 0, "S1": 1, "S2": 2}
        initial_state = "S0"
        super().__init__(three_mode_state_map, output_map, initial_state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mode 3 FSM: Process a binary string to get the result."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="A binary number presented as a string"
    )

    args = parser.parse_args()

    fsm = Mode3FSM()
    try:
        result = fsm.process(args.input)
        logging.info(f"The result for the input is: {result}")
    except ValueError as e:
        logging.error(f"Error occurred: {e}")
