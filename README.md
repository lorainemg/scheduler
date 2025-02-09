# CPU Scheduling Simulator

## Overview
This project is a CPU Scheduling Simulator that implements various scheduling algorithms, including:

- First-Come, First-Served (FIFO)
- Shortest Job First (SJF)
- Shortest Time to Completion First (STCF)
- Round Robin (RR)
  
The simulator processes jobs with different arrival times, execution times, and potential interruptions. It calculates metrics such as turnaround time and response time to compare scheduling strategies.

## Features
- Job Handling: Models job execution with arrival times, execution times, and I/O interruptions.
- Multiple Scheduling Algorithms: FIFO, SJF, STCF, and Round Robin scheduling.
- Performance Analysis: Calculates turnaround time, response time, and maximum completion time.
- Configurable Quantum Time: For Round Robin scheduling.

## Installation
### Prerequisites
- Python 3.x
- NumPy

## Setup

### Clone this repository:
```sh
git clone <repo-url>
cd <project-folder>
```

### Install dependencies:
```sh
pip install numpy
```

## Usage
Run the main script:

```sh
python main.py
```

The program will execute scheduling algorithms and output performance metrics.

### Project Structure
```bash
│── main.py            # Entry point for the simulation  
│── operating_sys.py   # Defines Operating System and Job classes  
│── scheluder.py       # Implements scheduling algorithms  
└── README.md          # Project documentation
```

### License
This project is released under the MIT License.
