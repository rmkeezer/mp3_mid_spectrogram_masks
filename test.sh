#!/bin/bash
for f in midis/mp3/*.mp3
do
    f=$(echo "${f%.mp3}")
    f=$(echo "${f#midis/}")
    echo $f
    length=$(ffprobe -v error -show_entries format=duration   -of default=noprint_wrappers=1:nokey=1 midis/"$f".mp3)
    len=$(echo ${length%.*})
    for i in `seq 0 1 $len`
    do 
        out=$(echo 1secmids/"$f"_$i.wav)
        if [ -e out ]
        then
            in=$(echo midis/"$f".mp3)
            ffmpeg -ss $i -i "$in" -f wav -t 1 "$out"
        fi
    done
done