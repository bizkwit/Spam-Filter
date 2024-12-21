# Spam-Filter

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A simple spam filter implemented in Python.** This project demonstrates a Naive Bayes classifier for identifying spam emails.  It allows for experimentation with stop word filtering and word length filtering to optimize performance.


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
- [Examples](#examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)


## Overview

This Python-based spam filter utilizes a Naive Bayes approach to classify emails as either spam or ham (non-spam). The model is trained on a dataset of emails and then used to classify new, unseen emails. The project includes options to experiment with stop word filtering and word length filtering to improve accuracy.


## Features

- **Naive Bayes Classification:**  Implements a multinomial Naive Bayes classifier for email classification.
- **Stop Word Filtering:** Option to filter out common words (stop words) that don't contribute significantly to classification accuracy.
- **Word Length Filtering:** Option to filter words based on their length, potentially removing noise.
- **Model Persistence:** Saves and loads the trained model to a file.
- **Performance Metrics:** Calculates and displays accuracy, precision, recall, and F1-score.
- **Experimentation:** Allows for running experiments with different filtering techniques.


## Technologies

- [Python](https://www.python.org/)
- [Regular Expressions (re)](https://docs.python.org/3/library/re.html)
- [Enum](https://docs.python.org/3/library/enum.html)


## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- Required Python libraries (`math`, `enum`, `re`, `os`). These are typically included with standard Python installations, but you may need to install them explicitly if not.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bizkwit/Spam-Filter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Spam-Filter
   ```

### Usage

1. **Prepare your data:**  The project expects two folders, "train" and "test", in the same directory as the Python script.  The "train" folder should contain the training emails (spam and ham separated by filenames), and the "test" folder should contain the test emails.  You'll also need a file named "English-Stop-Words.txt" containing a list of stop words (one word per line).  You can create this file manually or find a suitable list online.


2. **Run the script:** Execute the `model.py` script. The script presents a menu-driven interface to select tasks:
    - **Task 1:** Builds the model and saves it to 'model.txt'.
    - **Task 2:** Builds the model, tests it on the test set, and prints the baseline performance metrics. Results are saved to 'baseline-result.txt'.
    - **Task 3:** Allows you to perform experiments with stop word filtering and word length filtering, saving results to 'stopword-result.txt' and 'wordlength-result.txt' respectively.

The script will guide you through the process.


## Examples

After running Task 2, the `baseline-result.txt` file will contain the classification results for each test email.  Similarly, `stopword-result.txt` and `wordlength-result.txt` will contain results for the respective experiments in Task 3.


## Roadmap

- [x] Implement Naive Bayes classifier
- [x] Implement stop word filtering
- [x] Implement word length filtering
- [x] Create menu-driven interface for task selection
- [x] Save and load model
- [x] Calculate and display performance metrics (accuracy, precision, recall, F1-score)
- [x] Write comprehensive README


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
