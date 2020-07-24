#!/bin/bash

MMP=$1
WAV=${MMP%%.*}.wav
LMMS=${HOME}/Work/apps/lmms-1.2.2-linux-x86_64.AppImage

${LMMS} -l -f wav -r $1 -o ${WAV}

play ${WAV}


