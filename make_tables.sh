#!/bin/bash

echo Init table
./jsonify-table.py tables/small_state/initial_table  init_table
echo Short table
./jsonify-table.py tables/small_state/table_9  short_table
echo Medium table
./jsonify-table.py tables/small_state/table_60 medium_table
echo Long Table
./jsonify-table.py tables/small_state/table    long_table 
