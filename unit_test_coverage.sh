#!/bin/bash

poetry run coverage erase

poetry run coverage run -p --source=planar_graph --branch -m pytest -s src/tests/test_planar_graph_unit.py

poetry run coverage run -p --source=condition --branch -m pytest -s src/tests/test_condition_unit.py

poetry run coverage run -p --source=edge --branch -m pytest -s src/tests/test_edge_unit.py

poetry run coverage combine

poetry run coverage report
