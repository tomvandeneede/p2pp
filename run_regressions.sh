#!/bin/bash

mkdir -p tests/output
rm tests/output/*

python ./p2pp.py -g -i tests/TestFirmware.gcode -d tests/output/TestFirmware.mcf.gcode
python ./p2pp.py -g -i tests/TestSoftware.gcode -d tests/output/TestSoftware.mcf.gcode
diff -i -b -w -B -a --normal tests/TestFirmwareBaseline.mcf.gcode tests/output/TestFirmware.mcf.gcode > tests/output/TestFirmware.diff
diff -i -b -w -B -a --normal tests/TestSoftwareBaseline.mcf.gcode tests/output/TestSoftware.mcf.gcode > tests/output/TestSoftware.diff