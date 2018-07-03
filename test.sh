#!/bin/bash
for f in in/songswithmids/mp3s/*.mp3
do
    fin=$f
    length=$(ffprobe -v error -show_entries format=duration   -of default=noprint_wrappers=1:nokey=1 "$fin")
    f=$(echo "${f%.mp3}")
    f=$(echo "${f#in/songswithmids/mp3s/}")
    echo $f
    echo $fin
    len=$(echo ${length%.*})
    for i in `seq 0 1 $len`
    do 
        out=$(echo out/songparts/"$f"_$i.wav)
        if [ ! -f $out ]
        then
            ffmpeg -ss $i -i "$fin" -f wav -t 1 "$out"
        fi
    done
done