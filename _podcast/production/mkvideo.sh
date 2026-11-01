#!/bin/bash
# mkvideo.sh BG AUDIO OUT WAVE_X WAVE_Y WAVE_W WAVE_H BAR_X BAR_Y BAR_W FPS
BG=$1; AUD=$2; OUT=$3; WX=$4; WY=$5; WW=$6; WH=$7; BX=$8; BY=$9; BW=${10}; FPS=${11}
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
ffmpeg -hide_banner -loglevel error -y -loop 1 -framerate $FPS -i "$BG" -i "$AUD" \
 -f lavfi -i "color=c=0xFA9939:s=${BW}x9:r=$FPS:d=$D" -filter_complex "
 [0:v]split[bg][bgc];[bgc]crop=$BX:9:0:$BY,setpts=PTS-STARTPTS[lm];
 [1:a]aformat=channel_layouts=mono,showwaves=s=${WW}x${WH}:mode=cline:rate=$FPS:scale=sqrt:draw=full:colors=0xFA9939,format=rgba,split[w1][w2];
 [w2]gblur=sigma=6,colorchannelmixer=aa=0.7[glow];
 [bg][glow]overlay=$WX:$WY[b1];[b1][w1]overlay=$WX:$WY[b2];
 [b2][2:v]overlay=x='$BX-$BW+$BW*t/$D':y=$BY:eval=frame[b3];
 [b3][lm]overlay=0:$BY,format=yuv420p[v]" \
 -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 24 -r $FPS -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
