import os
from pipelines.orchestrator import Orchestrator

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = os.path.join(PROJECT_PATH, 'input/')
OUTPUT_PATH = os.path.join(PROJECT_PATH, 'output/')
PROJECT_NAME = 'fp'


def main():
    o = Orchestrator(PROJECT_NAME, INPUT_PATH, OUTPUT_PATH)
    o.execute()


if __name__ == "__main__":
    main()
