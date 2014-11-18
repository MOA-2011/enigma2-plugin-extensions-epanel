#!/bin/sh
#DESCRIPTION=This script shows the ecm-, pid.info for some emu's
FIN="================================="
echo $FIN
echo "ecm.info:"
echo $FIN
if [ -e /tmp/ecm.info ]; then
    cat /tmp/ecm.info
else
    echo "No ecm.info found."
fi
echo ""
echo $FIN
echo "pid.info:"
echo $FIN
if [ -e /tmp/pid.info ]; then
    cat /tmp/pid.info
else
    echo "No pid.info found."
fi
echo ""
echo $FIN
echo ""
exit 0