#!/bin/sh
# v19 GATE, chained session-proof: waits for the summit probe to finish,
# then runs the interrupted-twice gate (v19 parallel root vs v18) with the
# machine to itself. One command, survives session restarts.
while pgrep -f "summit_probe.py" > /dev/null; do sleep 60; done
cd "/Users/mettamazza/Desktop/Smithian Fold Theory/tools"
python3 h2h_gate.py /tmp/fold_bot_v18 > /tmp/v19_gate_result.log 2>&1
