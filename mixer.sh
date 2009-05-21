#!/bin/sh
# simple OSD script for adjusting volume, for xfce, etc
# usage: mixer.sh up/down
# You will probably need to adjust the lines with Mono: in them...


OP=$1
CURRENT=`amixer sget DAC|grep "Mono:"|sed 's/  Mono: \(.*\) \[.*\] \[.*\]/\1/'`

if [ "$OP" = "up" ];then
    NEW=$((${CURRENT}+2))
else
    NEW=$((${CURRENT}-2))
fi

PER=`amixer sset DAC,0 ${NEW} |grep Mono:|sed 's/  Mono: .* \[\(.*\)%\] \[.*\]/\1/'`
amixer sset DAC,1 ${NEW}>/dev/null

killall -9 osd_cat 2>/dev/null

osd_cat --font="-adobe-helvetica-bold-*-*-*-34-*-*-*-*-*-*-*" --shadow=2 -l 1 -c green -d 1 -b percentage -A center -p middle -T Volume -P ${PER}
