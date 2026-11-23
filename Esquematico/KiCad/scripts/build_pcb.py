#!/usr/bin/env python3
"""Genera el PCB de DK Energy (KiCad) desde el netlist verificado del esquematico.
Reproducible: python build_pcb.py  (requiere kiutils).
Coloca huellas, asigna redes por pad, contorno 120x90mm, agujeros M3 y zona GND.
Las pistas de senal quedan para rutear en KiCad (netlist listo)."""
import os, uuid, copy
from kiutils.board import Board
from kiutils.footprint import Footprint
from kiutils.items.common import Position, Net
from kiutils.items.gritems import GrLine
from kiutils.items.zones import Zone, ZonePolygon
from kiutils.schematic import Schematic

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Esquematico/KiCad
FPDIR = os.path.join(HERE, "DK_Energy.pretty")
def U(): return str(uuid.uuid4())

s = Schematic.from_file(os.path.join(HERE, "DK_Energy.kicad_sch")); sch_uuid = s.uuid
ref2uuid = {}
for ss in s.schematicSymbols:
    r = next((p.value for p in ss.properties if p.key == "Reference"), None)
    if r and ss.libraryNickname == "DK_Energy" and not r.startswith("#"): ref2uuid[r] = ss.uuid

INST = {"SP1":"Solar_Panel_5V","D1":"Schottky_3A","U1":"TP4056_Module","BT1":"Battery_18650","U2":"MT3608_Module",
 "C1":"C","J1":"USB_A_Female","U3":"PIC16F887","X1":"Crystal_32kHz","C2":"C","C3":"C","C4":"C","C5":"C",
 "J2":"LCD_16x2","RV1":"Pot_10k","SW1":"SW_Push","SW2":"SW_Push","SW3":"SW_Push","R1":"R","R2":"R","R3":"R",
 "D2":"LED","R4":"R","Q1":"BC547","R5":"R","R6":"R","R7":"R","C6":"C","R8":"R","R9":"R","C7":"C","R10":"R",
 "U4":"LM393","R11":"R","R12":"R","R13":"R","J3":"Conn_ICSP"}
VAL = {"SP1":"Panel_5V_2W","D1":"1N5822","U1":"TP4056","BT1":"18650","U2":"MT3608","C1":"100uF","J1":"USB_A",
 "U3":"PIC16F887","X1":"32.768kHz","C2":"15pF","C3":"15pF","C4":"100nF","C5":"100nF","J2":"LCD_16x2","RV1":"10k",
 "SW1":"B.A","SW2":"B.M","SW3":"B.C","R1":"3.3k","R2":"3.3k","R3":"3.3k","D2":"LED_Green","R4":"330","Q1":"BC547",
 "R5":"1k","R6":"10k","R7":"10k","C6":"100nF","R8":"10k","R9":"10k","C7":"100nF","R10":"0.1","U4":"LM393",
 "R11":"10k","R12":"470k","R13":"1k","J3":"ICSP"}
SN2FP = {"Solar_Panel_5V":"USB_Micro_B_Female","Schottky_3A":"DO-214AA_SMB","TP4056_Module":"TP4056_Module",
 "Battery_18650":"18650_Holder","MT3608_Module":"MT3608_Module","C":"C_0805","USB_A_Female":"USB_A_Female",
 "PIC16F887":"DIP-40_W7.62mm","Crystal_32kHz":"Crystal_32kHz","LCD_16x2":"LCD_16x2_Header","Pot_10k":"Potentiometer_THT",
 "SW_Push":"Tactile_6x6","R":"R_0805","LED":"LED_3mm","BC547":"TO-92","LM393":"SOIC-8","Conn_ICSP":"Header_1x06_2.54mm"}
NET = {
 "SP1":{"1":"PANEL","5":"GND"},"D1":{"1":"PANEL","2":"PANEL_IN"},
 "U1":{"1":"PANEL_IN","2":"GND","3":"VBAT","4":"VBAT_NEG","5":"VBAT_PROT","6":"GND"},
 "BT1":{"1":"VBAT","2":"VBAT_NEG"},"U2":{"1":"VBAT_PROT","2":"GND","3":"GND","4":"+5V"},
 "C1":{"1":"+5V","2":"GND"},"J1":{"1":"+5V","4":"SHUNT_HI","5":"GND","6":"GND"},
 "U3":{"2":"ADC_BAT","3":"ADC_PANEL","4":"ADC_CURR","14":"OSC2","13":"OSC1","1":"MCLR","33":"BTN_PWR",
       "39":"PGC","40":"PGD","15":"RC0_IND","16":"BTN_MENU","17":"BTN_PHONE","19":"LCD_E","20":"LCD_RS",
       "21":"LCD_RW","27":"LCD_D4","28":"LCD_D5","29":"LCD_D6","30":"LCD_D7","11":"+5V","32":"+5V","12":"GND","31":"GND"},
 "X1":{"1":"OSC2","2":"OSC1"},"C2":{"1":"OSC1","2":"GND"},"C3":{"1":"OSC2","2":"GND"},
 "C4":{"1":"+5V","2":"GND"},"C5":{"1":"+5V","2":"GND"},
 "J2":{"1":"GND","2":"+5V","3":"LCD_VO","4":"LCD_RS","5":"LCD_RW","6":"LCD_E","11":"LCD_D4","12":"LCD_D5",
       "13":"LCD_D6","14":"LCD_D7","15":"+5V","16":"LCD_K"},
 "RV1":{"1":"+5V","2":"LCD_VO","3":"GND"},
 "SW1":{"1":"BTN_PWR","2":"GND","3":"BTN_PWR","4":"GND"},"SW2":{"1":"BTN_MENU","2":"GND","3":"BTN_MENU","4":"GND"},
 "SW3":{"1":"BTN_PHONE","2":"GND","3":"BTN_PHONE","4":"GND"},
 "R1":{"1":"+5V","2":"BTN_PWR"},"R2":{"1":"+5V","2":"BTN_MENU"},"R3":{"1":"+5V","2":"BTN_PHONE"},
 "D2":{"1":"LED_A","2":"GND"},"R4":{"1":"RC0_IND","2":"LED_A"},"R5":{"1":"RC0_IND","2":"BL_BASE"},
 "Q1":{"1":"GND","2":"BL_BASE","3":"LCD_K"},
 "R6":{"1":"VBAT","2":"ADC_BAT"},"R7":{"1":"ADC_BAT","2":"GND"},"C6":{"1":"ADC_BAT","2":"GND"},
 "R8":{"1":"PANEL_IN","2":"ADC_PANEL"},"R9":{"1":"ADC_PANEL","2":"GND"},"C7":{"1":"ADC_PANEL","2":"GND"},
 "R10":{"1":"SHUNT_HI","2":"GND"},
 "U4":{"3":"SHUNT_HI","2":"AMP_FB","1":"ADC_CURR","8":"+5V","4":"GND","5":"GND","6":"GND"},
 "R11":{"1":"AMP_FB","2":"GND"},"R12":{"1":"AMP_FB","2":"ADC_CURR"},"R13":{"1":"+5V","2":"ADC_CURR"},
 "J3":{"1":"MCLR","2":"+5V","3":"GND","4":"PGD","5":"PGC"},
}
POS = {"SP1":(8,85),"D1":(20,85),"U1":(45,80),"U2":(80,80),"C1":(100,80),"J1":(112,80),"BT1":(15,12),
 "U3":(25,55),"X1":(15,60),"C2":(12,52),"C3":(12,45),"C4":(35,60),"C5":(40,60),"J2":(95,55),"RV1":(80,42),
 "SW1":(78,28),"SW2":(90,28),"SW3":(100,28),"R1":(78,38),"R2":(90,38),"R3":(100,38),"D2":(113,42),"R4":(113,35),
 "Q1":(113,27),"R5":(107,27),"R6":(50,40),"R7":(50,48),"C6":(57,48),"R8":(64,40),"R9":(64,48),"C7":(71,48),
 "R10":(50,30),"U4":(57,33),"R11":(50,26),"R12":(64,28),"R13":(70,28),"J3":(80,65)}

netnames = sorted({n for d in NET.values() for n in d.values()})
netnum = {name: i+1 for i, name in enumerate(netnames)}
b = Board.create_new(); b.version = 20211014; b.generator = "kiutils"; b.general.thickness = 1.6
b.nets = [Net(number=0, name="")] + [Net(number=netnum[n], name=n) for n in netnames]
W, H = 120, 90
for (x1,y1,x2,y2) in [(0,0,W,0),(W,0,W,H),(W,H,0,H),(0,H,0,0)]:
    b.graphicItems.append(GrLine(start=Position(X=x1,Y=y1), end=Position(X=x2,Y=y2), layer="Edge.Cuts", width=0.1, tstamp=U()))
fpcache = {}
def get_fp(name):
    if name not in fpcache: fpcache[name] = Footprint.from_file(os.path.join(FPDIR, name+".kicad_mod"))
    return copy.deepcopy(fpcache[name])
boxes = {}
for ref, sn in INST.items():
    fpname = "CP_Radial_D6.3_P2.50mm" if ref == "C1" else SN2FP[sn]
    fp = get_fp(fpname); x, y = POS[ref]; fp.position = Position(X=x, Y=y, angle=0)
    fp.libraryNickname = "DK_Energy"; fp.entryName = fpname; fp.tstamp = U()
    fp.path = "/" + sch_uuid + "/" + ref2uuid.get(ref, U())
    fp.properties = {"Reference": ref, "Value": VAL[ref]}
    for pad in fp.pads:
        nn = NET.get(ref, {}).get(pad.number)
        if nn: pad.net = Net(number=netnum[nn], name=nn)
    b.footprints.append(fp)
    xs = [p.position.X for p in fp.pads]; ys = [p.position.Y for p in fp.pads]
    if xs: boxes[ref] = (x+min(xs)-1, y+min(ys)-1, x+max(xs)+1, y+max(ys)+1)
for i, (mx,my) in enumerate([(5,5),(W-5,5),(5,H-5),(W-5,H-5)], 1):
    fp = get_fp("MountingHole_3.2mm_M3"); fp.position = Position(X=mx, Y=my, angle=0)
    fp.libraryNickname = "DK_Energy"; fp.entryName = "MountingHole_3.2mm_M3"; fp.tstamp = U()
    fp.properties = {"Reference": f"MH{i}", "Value": "M3"}
    b.footprints.append(fp)
gnd = Zone(net=netnum["GND"], netName="GND", layers=["B.Cu"], tstamp=U(), name="GND", connectPads="thru_hole_only",
           clearance=0.3, minThickness=0.25,
           polygons=[ZonePolygon(coordinates=[Position(X=1,Y=1),Position(X=W-1,Y=1),Position(X=W-1,Y=H-1),Position(X=1,Y=H-1)])])
b.zones.append(gnd)
pcbpath = os.path.join(HERE, "DK_Energy.kicad_pcb"); b.to_file(pcbpath)
print("PCB written. footprints:", len(b.footprints), "nets:", len(b.nets), "bytes:", os.path.getsize(pcbpath))
def overlap(a, bx): return not (a[2]<bx[0] or bx[2]<a[0] or a[3]<bx[1] or bx[3]<a[1])
ov = []; keys = list(boxes)
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        if overlap(boxes[keys[i]], boxes[keys[j]]): ov.append((keys[i], keys[j]))
print("pad-bbox overlaps:", ov)