#!/bin/bash

for FILE in $(ls examples/0*)
  do
  python $FILE
done