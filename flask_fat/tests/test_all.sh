#!/bin/bash
# MOCK_DIR="$( cd "$(dirname "$0")" ; pwd -P )/mock/"
TEST_FILE="$( cd "$(dirname "$0")" ; pwd -P )/test_target.sh"

test_files=$(find . -name 'test_*.py')

for i in $test_files; do
  $i
done

# mock_targets=$(ls $MOCK_DIR)

# for i in $mock_targets; do
#     $TEST_FILE $i -q -c
# done