## 1. Assignment 1: Finding the Best Threshold

### 1.1 Explanation
Identifying the best threshold for a binary classification model based on recall and F1 score. The process involves the following steps:

1. **Find the Upper Bound of Threshold Meeting Recall >= 0.9**:
   - Use binary search to find the highest threshold where recall is greater than or equal to 0.9.

2. **Calculate F1 Score for These Thresholds**:
   - For all thresholds that satisfy the recall condition, calculate the F1 score.

3. **Identify the Best Threshold with the Highest F1 Score**:
   - After calculating the F1 scores for all the valid thresholds, the threshold that provides the highest F1 score will be selected as the "best threshold."

### 1.2 Usage
To run the program, use the following command:

```bash
python best_threshold.py --data_file_path <path-you-data-file.json>
```

### 1.3 Testing
To run the tests for this assignment, use the following command:

```bash
pytest test.py
```

### 1.4 Data Example
Here is an example of how the data in the JSON file should be structured:

```json
{
    "1": {
        "threshold": 0.1,
        "TP": 100,
        "FP": 80,
        "TN": 20,
        "FN": 0
    },
    "2": {
        "threshold": 0.2,
        "TP": 100,
        "FP": 75,
        "TN": 25,
        "FN": 0
    },
    "3": {
        "threshold": 0.3,
        "TP": 98,
        "FP": 50,
        "TN": 50,
        "FN": 2
    },
    "4": {
        "threshold": 0.4,
        "TP": 95,
        "FP": 35,
        "TN": 65,
        "FN": 5
    },
    "5": {
        "threshold": 0.5,
        "TP": 92,
        "FP": 40,
        "TN": 60,
        "FN": 8
    },
    "6": {
        "threshold": 0.6,
        "TP": 91,
        "FP": 10,
        "TN": 90,
        "FN": 9
    },
    "7": {
        "threshold": 0.7,
        "TP": 90,
        "FP": 10,
        "TN": 90,
        "FN": 10
    },
    "8": {
        "threshold": 0.8,
        "TP": 80,
        "FP": 5,
        "TN": 95,
        "FN": 20
    },
    "9": {
        "threshold": 0.9,
        "TP": 55,
        "FP": 0,
        "TN": 100,
        "FN": 45
    }
}
```

## 2. Assignment 2: FSM

### 2.1 Explanation


### 2.2 Usage
To run the program, use the following command:

```bash
python finit_state_machine.py --input <your-binary-number>
```

### 2.3 Testing
To run the tests for this assignment, use the following command:

```bash
pytest test_fsm.py```
```