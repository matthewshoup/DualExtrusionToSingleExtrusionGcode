# DualExtrusionToSingleExtrusionGcode
Convert Gcode from dual extrusion to single extruder and also ouput Gcode for serial filament splices.

Turn your 3d prints from dual extrusion into a single extruder gcode file. Also outputs gcode to make a filament splice to create a single roll of filament via splices/joins.

Example usage:

python3 D2SgcodeConvert.py lulzbot_taz_flexydually_keychain.gcode

Outputs two files:
1. single extruder gcode
2. serial filament splicing lengths

