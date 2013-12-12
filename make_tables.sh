#!/bin/bash

echo Init table
./jsonify-table.py tables/small_state/0M  init_table
echo Short table
./jsonify-table.py tables/small_state/5M  short_table
echo Medium table
./jsonify-table.py tables/small_state/10M medium_table
echo Long Table
./jsonify-table.py tables/small_state/15M long_table 
