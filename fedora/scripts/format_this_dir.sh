#!/usr/bin/env sh

for i in ./*.py
do
   black $i
done
