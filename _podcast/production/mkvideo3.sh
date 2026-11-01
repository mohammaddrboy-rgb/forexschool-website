#!/bin/bash
# mkvideo3.sh BG AUDIO OUT WAVE_X WAVE_Y WAVE_W WAVE_H BAR_X BAR_Y BAR_W FPS  (env: CRF, ABR)
BG=$1; AUD=$2; OUT=$3; WX=$4; WY=$5; WW=$6; WH=$7; BX=$8; BY=$9; BW=${10}; FPS=${11}
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
python3.13 "$(dirname "$0")/bars.py" "$AUD" $FPS $WW $WH | \
ffmpeg -hide_banner -loglevel error -y -loop 1 -framerate $FPS -i "$BG" -i "$AUD" \
 -f lavfi -i "color=c=0xFA9939:s=${BW}x9:r=$FPS:d=$D" \
 -f rawvideo -pix_fmt rgba -s ${WW}x${WH} -framerate $FPS -i pipe:0 -filter_complex "
 [0:v]split[bg][bgc];[bgc]crop=$BX:9:0:$BY,setpts=PTS-STARTPTS[lm];
 [3:v]format=rgba,split[w1][w2];[w2]gblur=sigma=5,colorchannelmixer=aa=0.55[glow];
 [bg][glow]overlay=$WX:$WY[b1];[b1][w1]overlay=$WX:$WY[b2];
 [b2][2:v]overlay=x='$BX-$BW+$BW*t/$D':y=$BY:eval=frame[b3];
 [b3][lm]overlay=0:$BY,format=yuv420p[v]" \
 -map "[v]" -map 1:a -t $D -c:v libx264 -preset veryslow -crf ${CRF:-24} -g 900 -r $FPS \
 -c:a aac -b:a ${ABR:-128k} -ar 48000 -movflags +faststart "$OUT"
