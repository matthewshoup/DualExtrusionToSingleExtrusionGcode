#!/usr/bin/python

import sys

if (len(sys.argv)<=1):
    print("usage: python3 D2SgcodeConvert.py <your_filename.gcode>")
    sys.exit
    quit()
try:    
    f = open(sys.argv[1],"r")
except ValueError:
    sys.exit
    quit()
    
lines = f.readlines()
whichT = 'T0'
extrudeAmount = float(0)
gcodeOut = ";CONVERTED DUAL EXTRUSION GCODE TO SINGLE EXTRUSION GCODE;\n\n"
extrusionLengths = ";EXTRUDE FILAMENT AND MAKE CUTS;\n\n";
for i in range(len(lines)):
    str = lines[i].rstrip('\n') + ' '
    
    if ('T0' in str and whichT=="T1" and extrudeAmount>0): 
        extrusionLengths = extrusionLengths + whichT+"; SWITCH EXTRUDER\nG1 E"+"{0:.5f}".format(extrudeAmount)+";\nM380; MAKE CUT\nM381; END CUT\nM400; WAIT FOR COMMANDS TO FINISH\n\n"
        extrudeAmount = float(0);
        whichT = 'T0'
    
    if ('T1' in str and whichT=="T0" and extrudeAmount>0):
        extrusionLengths = extrusionLengths + whichT+"; SWITCH EXTRUDER\nG1 E"+"{0:.5f}".format(extrudeAmount)+";\nM380; MAKE CUT\nM381; END CUT\nM400; WAIT FOR COMMANDS TO FINISH\n\n"
        extrudeAmount = float(0);
        whichT = 'T1'
    
    if (str.startswith('G1') or str.startswith('G0')):
        extrude = str.split(' E')
        
        if len(extrude)>=2:
            try:
                extrudeAmount = extrudeAmount + float(extrude[1].replace(" ","").strip())
            except ValueError:
                doNothing = True
    
    if (str.startswith('T1')==False and str.startswith('M104 T1')==False and str.startswith('M109 T1')==False and str.startswith(';M109 T1')==False and str.startswith(';M104 T1')==False):
        gcodeOut = gcodeOut + str+"\n"

if (extrudeAmount>0):
    extrusionLengths = extrusionLengths + whichT+"; SWITCH EXTRUDER\nG1 E"+repr(extrudeAmount)+";\nM380; MAKE CUT\nM381; END CUT\nM400; WAIT FOR COMMANDS TO FINISH\n\n"

extrusionLengths = extrusionLengths+"M84; END GAME\n"

with open(sys.argv[1].replace('.gcode','')+'_single_extruder.gcode', 'w') as f:
    f.write(gcodeOut)
f.close()

with open(sys.argv[1].replace('.gcode','')+'_filament_lengths.gcode', 'w') as f:
    f.write(extrusionLengths)
f.close()

print(extrusionLengths)
