#!/bin/bash
for f in in/songswithmidsALL/wavs/*.wav
do
    fin=$f
    length=$(ffprobe -v error -show_entries format=duration   -of default=noprint_wrappers=1:nokey=1 "$fin")
    f=$(echo "${f%.wav}")
    f=$(echo "${f#in/songswithmidsALL/wavs/}")
    echo $f
    echo $fin
    len=$(echo ${length%.*})
    for i in `seq 0 6 $len`
    do 
        out=$(echo out/songparts/6secALL/"$f"_$i.wav)
        if [ ! -f $out ]
        then
            ffmpeg -ss $i -i "$fin" -f wav -t 6 "$out"
        fi
    done
done