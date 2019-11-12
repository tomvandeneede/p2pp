#!/bin/bash

mkdir -p tests/output
rm tests/output/*

python ./p2pp.py -g -i tests/gcodes/TestFirmware.gcode -d tests/output/TestFirmware.mcf.gcode
python ./p2pp.py -g -i tests/gcodes/TestSoftware.gcode -d tests/output/TestSoftware.mcf.gcode
diff -i -b -w -B -a --normal tests/gcodes/TestFirmwareBaseline.mcf.gcode tests/output/TestFirmware.mcf.gcode > tests/output/TestFirmware.diff
diff -i -b -w -B -a --normal tests/gcodes/TestSoftwareBaseline.mcf.gcode tests/output/TestSoftware.mcf.gcode > tests/output/TestSoftware.diff

