#!/bin/bash

for f in ./*.png; do
    echo $f
    convert "$f" "${f%.png}.webp"
done