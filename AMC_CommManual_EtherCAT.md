# ADVANCED Motion Controls EtherCAT Communication Manual

Converted from AMC_CommManual_EtherCAT.pdf for text-based reading.



---
## Page 1

Everything’s possible.
DigiFlex® Performance™ Servo Drives
EtherCAT® Communication
Reference Manual
www.a-m-c.com 
MNCMECRF-07

---
## Page 2

MNCMECRF-07 i
Preface
ADVANCED Motion Controls constantly strives to improve all of its products. We review the information in 
this document regularly and we welcome any suggestions for improvement. We reserve the right to modify 
equipment and documentation without prior notice.
For the most recent software, the latest revisions of this manual, and copies of compliance and 
declarations of conformity, visit the company’s website at www.a-m-c.com. Otherwise, contact the 
company directly at:
ADVANCED Motion Controls  3805 Calle Tecate Camarillo, CA  93012-5068 USA
Agency Compliances
The company holds original documents for the following:
• UL 508c, file number E140173
• Electromagnetic Compatibility, EMC Directive - 2014/30/EU
EN61000-6-2:2005
EN61000-6-4:2007/A1:2011
• Electrical Safety, Low Voltage Directive - 2014/35/EU
EN 60204-1:2006/A1:2009
• Reduction of Hazardous Substances (RoHS II), 2011/65/EU
Trademarks
ADVANCED Motion Controls®, the combined isosceles trapezoid/right triangle logo, DIGIFLEX®, 
DIGIFLEX® Performance™ and DriveWare® are either registered trademarks or trademarks of ADVANCED 
Motion Controls in the United States and/or other countries. EtherCAT® is a registered trademark and 
patented technology, licensed by Beckhoff Automation GmbH, Germany. All other trademarks are the 
property of their respective owners.
Related Documentation
• Product datasheet specific for your drive, available for download at www.a-m-c.com.

---
## Page 3

MNCMECRF-07 ii
 / 
Attention Symbols
The following symbols are used throughout this document to draw attention to important operating 
information, special instructions, and cautionary warnings. The section below outlines the overall directive 
of each symbol and what type of information the accompanying text is relaying.
Note - Pertinent information that clarifies a process, operation, or ease-
of-use preparations regarding the product.
Notice - Required instruction necessary to ensure successful completion 
of a task or procedure.
Caution - Instructs and directs you to avoid damaging equipment.
Warning - Instructs and directs you to avoid harming yourself.
Danger - Presents information you must heed to avoid serious injury or 
death.
Note

---
## Page 4

MNCMECRF-07 iii
 / 
Revision History
© 2018 ADVANCED Motion Controls. All rights reserved.
Document ID Revision # Date Changes
MNCMECRF-01 5.16.9 11/2011 - First Release
MNCMECRF-02 7.0 8/2012
- Added sub-indices 2010.12h and 2010.13h in 2010h: Current Values
- Added sub-indices 2011.06h and 2011.07h in 2011h: Velocity Values
- Added sub-indices 2012.05h, 2012.06h, and 2012.07h in 2012h: Position Values
- Added sub-index 201E.02h in 201Eh: Auxiliary Encoder Value
- Added sub-index 2034.29h in 2034h: Current Loop & Commutation Control Parameters
- Updated sub-indices 203C.01h to 203C.0Eh in 203Ch: Command Limiter Parameters
- Updated definition for KMS in Table A.2 on page 226
- Updated sub-indices 203D.01h to 203D.06h in 203Dh: Deadband Parameters
- Added object 203Eh: Jog Parameters
- Added unit type DA4 to Table A.1 on page 225
- Updated sub-indices 2044.01h to 2044.10h in 2044h: Analog Input Parameters
- Updated sub-indices 2046.01h to 2046.04h in 2046h: Auxiliary Input Parameters
- Added sub-indices 2058.1Dh to 2058.20h in 2058h: Digital Input Parameters
- Added sub-index 2062.05h to 2062h: Braking/Stop General Properties
- Updated sub-index 2032.08h in 2032h: Feedback Sensor Parameters
- Added object 20C8h: Motion Engine Configuration
- Added object 20C9h: Motion Engine Control
- Added object 2029h: Motion Engine Status
- Added sub-index 201A:05h to 201Ah: Analog Input Values
- Added object 2006h: Network Configuration
MNCMECRF-03 7.1 6/2013
- Added sub-indices 205A.61h, 205A.62h, and 205A63h in 205Ah: Digital Output Parameters
- Added sub-index 205B.60h in 205Bh: Programmable Status Parameters
- Updated object 203Eh: Jog Parameters
- Added sub-index 2058.22h in 2058h: Digital Input Parameters
- Added sub-index 20E6.01 in 20E6h: CANopen Parameters
- Added ojbect 20CAh: Dynamic Index Data
- Added unit type DA5 to Table A.1 on page 225
- Added conversion constant KDS to Table A.2 on page 226
MNCMECRF-04 7.2 2/2014
- Added object 2018h: Programmable Limit Switch Values
- Modified sub-index 2032.03h in 2032h: Feedback Sensor Parameters
- Added sub-indices 2032.11h and 2032.12h to 2032h: Feedback Sensor Parameters
- Added object 2040h: Programmable Limit Switch Parameters
- Modified sub-index 205A.55h in 205Ah: Digital Output Parameters
- Added sub-indices 205A.64h and 205A.65h to 205Ah: Digital Output Parameters
- Modified sub-index 205B.54h in 205Bh: Programmable Status Parameters
MNCMECRF-05 7.3 10/2015
- Removed Motion Engine Reset from object 2058h: Digital Input Parameters
- Shifted sub-indices 2058.1F - 2058.22 to 2058.1E - 2058.21
- Added sub-index 205A.66 in 205Ah: Digital Output Parameters
- Added sub-index 205B.61 in 205Bh: Programmable Status Parameters
- Added sub index 2068.2B in 2068h: Event Maximum Recoveries Parameters
MNCMECRF-06 7.4 10/2017
- Added object 2022h: Analog Input ADC Raw Values
- Added sub-indices 1018.02h - 1018.04h to 1018h: Identity Object
-Updated instances of “current overshoot” definitions to “over current”
MNCMECRF-07 7.4 7/2026 -Updated sub-index 2029.04h table.

---
## Page 5

MNCMECRF-07 iv
Contents
 1 Communication Manual 1
1.1 Introduction  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.1.1 Purpose of this manual  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.1.2 Differences between this manual and ETG.1000 & ETG.6010  . 1
1.2 CANopen Objects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
1.2.1 Object Dictionary Structure  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
Data Type Objects (Registers) 0x0000 - 0x0FFF  . . . . . . . . . . . . . . . 2
CoE Communication Objects 1000h – 1FFFh . . . . . . . . . . . . . . . . . 2
Manufacturer Specific Objects 2000h – 5FFFh . . . . . . . . . . . . . . . . 2
Standard Servo Drive Objects 6000h – 9FFFh . . . . . . . . . . . . . . . . . 2
1.2.2 Object Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.3 EtherCAT State Machine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.4 Watchdog . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.4.1 Sync Manager Watchdog  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.4.2 PDO Watchdog . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.5 SDO vs. PDO Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.5.1 SDO Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.5.2 PDO Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
Transmit Process Data Object (TPDO)  . . . . . . . . . . . . . . . . . . . . . . 6
Receive Process Data Object (RPDO) . . . . . . . . . . . . . . . . . . . . . . 6
PDO Configuration  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Mapping Parameter Object  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
EtherCAT PDO Assignments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
PDO Mappable Objects  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
1.6 Control State Machine  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
1.6.1 State Machine Overview  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
1.6.2 Drive States . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
1.6.3 ControlWord (6040h) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
1.6.4 StatusWord (6041h)  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

---
## Page 6

MNCMECRF-07 v
 / 
1.7 Homing  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.7.1 Home Offset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.7.2 Homing Speeds  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.7.3 Homing Acceleration  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.7.4 Homing Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
Method 1: Homing on the Negative Limit Switch  . . . . . . . . . . . . 17
Method 2: Homing on the Positive Limit Switch . . . . . . . . . . . . . . 17
Methods 3 and 4: Homing on the Positive Home Switch  . . . . . . 18
Methods 5 and 6: Homing on the Negative Home Switch  . . . . 18
Methods 7-14: Homing on the Home Switch . . . . . . . . . . . . . . . . 19
Methods 17-30: Homing without an Index Pulse  . . . . . . . . . . . . . 21
Methods 33 and 34: Homing on the Index Pulse . . . . . . . . . . . . . 21
Method 35  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
1.8 Modes of Operation  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
1.8.1 Profile Modes  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Profile Position Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
Profile Velocity Mode  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Profile Current Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
1.8.2 Homing Mode  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
1.8.3 Cyclic Synchronous Modes  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Cyclic Synchronous Position Mode . . . . . . . . . . . . . . . . . . . . . . . . 26
Cyclic Synchronous Velocity Mode  . . . . . . . . . . . . . . . . . . . . . . . 27
Cyclic Synchronous Current Mode . . . . . . . . . . . . . . . . . . . . . . . . 28
1.8.4 Custom Defined Modes Of Operation  . . . . . . . . . . . . . . . . . . . 28
1.9 Connecting to an AMC EtherCAT Drive  . . . . . . . . . . . . . . . . . . . . . . 29
1.9.1 USB Interface Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
1.9.2 EtherCAT Interface Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
Node Addressing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
1.10 Hardware Requirements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
 2 Object Dictionary 30
2.1 Dictionary Table Format  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
2.2 Configuration Objects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
2.2.1 Administrative Objects  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
2009h: Load EEPROM Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
200Ah: AMC Store Drive Parameters  . . . . . . . . . . . . . . . . . . . . . . 31
2.3 Communication Settings . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
2.3.1 General Settings  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32

---
## Page 7

MNCMECRF-07 vi
 / 
1000h: Device Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
1018h: Identity Object  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
1C00h: Sync Manager Communication Type . . . . . . . . . . . . . . . 33
20E6h: CANopen Parameters  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
2006h: Network Configuration . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
2.3.2 PDO Configuration  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
1600h: Receive PDO Mapping  . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
1A00h: Transmit PDO Mapping  . . . . . . . . . . . . . . . . . . . . . . . . . . . 38
2.4 Drive Configuration  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41
2.4.1 Motion Control Profile  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41
20D0h: Control Loop Configuration Parameters . . . . . . . . . . . . . 41
2032h: Feedback Sensor Parameters . . . . . . . . . . . . . . . . . . . . . . 42
2046h: Auxiliary Input Parameters . . . . . . . . . . . . . . . . . . . . . . . . . 47
2034h: Current Loop & Commutation Control Parameters  . . . . 47
2036h: Velocity Loop Control Parameters  . . . . . . . . . . . . . . . . . . 55
2037h: Velocity Limits  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
2038h: Position Loop Control Parameters . . . . . . . . . . . . . . . . . . . 60
2039h: Position Limits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63
6065h: Position Following Error Window  . . . . . . . . . . . . . . . . . . . . 65
6066h: Position Following Error Time Out . . . . . . . . . . . . . . . . . . . . 65
60F4h: Position Following Error Actual Value  . . . . . . . . . . . . . . . . 66
6098h: Homing Method  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
6099h: Homing Speeds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
609Ah: Homing Acceleration  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
607Ch: Home Offset  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
6086h: Motion Profile Type  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
6088h: Torque Profile Type  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
203Ch: Command Limiter Parameters . . . . . . . . . . . . . . . . . . . . . 67
60C2h: Interpolation Time Period  . . . . . . . . . . . . . . . . . . . . . . . . . 70
2.4.2 Hardware Profile  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 71
200Bh: Stored User Parameters  . . . . . . . . . . . . . . . . . . . . . . . . . . . 71
2008h: Drive Initialization Parameters  . . . . . . . . . . . . . . . . . . . . . . 71
20C8h: Motion Engine Configuration  . . . . . . . . . . . . . . . . . . . . . . 72
2033h: User Voltage Protection Parameters  . . . . . . . . . . . . . . . . 72
2054h: Drive Temperature Parameters . . . . . . . . . . . . . . . . . . . . . 74
2043h: Capture Configuration Parameters  . . . . . . . . . . . . . . . . . 75
2058h: Digital Input Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . 78
205Ah: Digital Output Parameters . . . . . . . . . . . . . . . . . . . . . . . . . 84
2044h: Analog Input Parameters . . . . . . . . . . . . . . . . . . . . . . . . . 101
205Ch: Analog Output Parameters  . . . . . . . . . . . . . . . . . . . . . . 109
2040h: Programmable Limit Switch Parameters  . . . . . . . . . . . . 111

---
## Page 8

MNCMECRF-07 vii
 / 
203Dh: Deadband Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . 114
203Eh: Jog Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 115
2062h: Braking/Stop General Properties . . . . . . . . . . . . . . . . . . . 116
2064h: Event Response Time Parameters . . . . . . . . . . . . . . . . . . 117
2065h: Event Action Parameters . . . . . . . . . . . . . . . . . . . . . . . . . 124
2066h: Event Recovery Time Parameters . . . . . . . . . . . . . . . . . . 135
2067h: Event Time-Out Window Parameters  . . . . . . . . . . . . . . . 140
2068h: Event Maximum Recoveries Parameters  . . . . . . . . . . . . 147
205Bh: Programmable Status Parameters  . . . . . . . . . . . . . . . . . 157
208Ch: Product Information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 173
208Dh: Firmware Information . . . . . . . . . . . . . . . . . . . . . . . . . . . . 174
20D8h: Power Board Information  . . . . . . . . . . . . . . . . . . . . . . . . 174
2.5 Drive Operation Objects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180
2.5.1 Control Objects  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 181
6040h: ControlWord  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 181
2001h: Control Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 182
6060h: Modes Of Operation  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
2.5.2 Command Objects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
6071h: Target Current . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
60FFh: Target Velocity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
607Ah: Target Position . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 185
60B1h: Velocity Offset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 185
60B2h: Current Offset  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 185
2045h: Interface Inputs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 185
2.5.3 Motion Engine Command Objects . . . . . . . . . . . . . . . . . . . . . 187
20C9h: Motion Engine Control . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
20CAh: Dynamic Index Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
2.5.4 Monitor Objects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 190
6041h: StatusWord . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 190
2002h: Drive Status  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
2003h: Drive Status History  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194
2029h: Motion Engine Status  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 195
6061h: Modes Of Operation Display . . . . . . . . . . . . . . . . . . . . . . 197
200Eh: Feedback Sensor Values  . . . . . . . . . . . . . . . . . . . . . . . . . 197
2027h: Feedback Hardware Diagnostics . . . . . . . . . . . . . . . . . . 198
201Ch: Gearing Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 200
201Eh: Auxiliary Encoder Value . . . . . . . . . . . . . . . . . . . . . . . . . . 200
6077h: Actual Current . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
2010h: Current Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
606Bh: Velocity Demand  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 204
606Ch: Actual Velocity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205

---
## Page 9

MNCMECRF-07 viii
 / 
606Dh: Velocity Window  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205
606Eh: Velocity Window Time  . . . . . . . . . . . . . . . . . . . . . . . . . . . 205
6069h: Velocity Sensor Actual Value  . . . . . . . . . . . . . . . . . . . . . 205
2011h: Velocity Values  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 206
6064h: Actual Position . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 207
2012h: Position Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 207
2014h: Command Limiter Input . . . . . . . . . . . . . . . . . . . . . . . . . . 208
200Fh: Power Bridge Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 209
2021h: Drive Temperature Values  . . . . . . . . . . . . . . . . . . . . . . . . 210
2019h: Capture Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 210
2023h: Digital Input Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 211
2024h: Digital Output Values . . . . . . . . . . . . . . . . . . . . . . . . . . . . 212
201Ah: Analog Input Values  . . . . . . . . . . . . . . . . . . . . . . . . . . . . 212
2022h: Analog Input ADC Raw Values . . . . . . . . . . . . . . . . . . . . 213
2025h: Analog Output Values  . . . . . . . . . . . . . . . . . . . . . . . . . . . 214
2015h: Deadband Input Value  . . . . . . . . . . . . . . . . . . . . . . . . . . 214
2018h: Programmable Limit Switch Values . . . . . . . . . . . . . . . . . 214
201Bh: PWM and Direction Input Values  . . . . . . . . . . . . . . . . . . 215
2028h: Fault Log Counter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 215
 A Appendix 225
A.1 Appendix A - Units . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 225
A.1.1 Conversion Example 1  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 226
A.1.2 Conversion Example 2  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 226
A.1.3 Conversion Example 3  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 227
A.2 Appendix B - Current Limiting Algorithm . . . . . . . . . . . . . . . . . . . . . 228
A.2.1 Time-Based Peak Current Limiting . . . . . . . . . . . . . . . . . . . . . . 229
A.2.2 Time-Based Non-Peak Current Limiting  . . . . . . . . . . . . . . . . . 230
A.2.3 Time-Based Current Recovery . . . . . . . . . . . . . . . . . . . . . . . . . 231
A.2.4 Charge-Based Peak Current Limiting . . . . . . . . . . . . . . . . . . . 232
A.2.5 Charge-Based Non-Peak Current Limiting . . . . . . . . . . . . . . . 233
A.2.6 Charge-Based Current Recovery . . . . . . . . . . . . . . . . . . . . . . 234
A.2.7 RMS Current Scaling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 235

---
## Page 10

MNCMECRF-07 ix
 / 
 B Appendix B 236
B.1 Appendix B - EtherCAT PDO Assignments . . . . . . . . . . . . . . . . . . . . 236
B.1.1 Modifying PDO Assignments in TwinCAT . . . . . . . . . . . . . . . . . 237
1 - Modify and Download the New Project File Settings Using 
DriveWare . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 237
2 - Modify the EtherCAT Device Description File . . . . . . . . . . . . 238
3 - Write the Device Description Data to the Drive Using the 
EtherCAT Host  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 240

---
## Page 11

MNCMECRF-07 1
 1 Communication Manual
1.1 Introduction
1.1.1 Purpose of this manual
This manual will provide all information necessary to communicate with and operate 
ADVANCED Motion Controls’ EtherCAT drives using CANopen over EtherCAT (CoE). Further 
information regarding the EtherCAT physicallayer and implementation of CoE is attainable 
through the ETG.1000 and ETG.6010 documentation.
The EtherCAT interface for ADVANCED Motion Controls’ digital drives follows the ETG.1000.6 
EtherCAT Application Layer protocol specification and the ETG.6010 Implementation 
guideline for CiA402 drive profile (device profile for drives and motion control). ETG 
(EtherCAT Technology Group) is the organization that governs the EtherCAT standard. They 
can be contacted at http://www.ethercat.org/.
1.1.2 Differences between this manual and ETG.1000 & ETG.6010
This manual provides all information necessary to properly communicate with the drive via 
the EtherCAT interface using a compatible host. The ETG.1000 and ETG.6010 documents are 
complimentary and can be used if more detailed information is required on specific standard 
EtherCAT features.

---
## Page 12

MNCMECRF-07 2
Communication Manual / CANopen Objects
1.2 CANopen Objects
Every AMC EtherCAT drive function is defined by groups of objects. An object is roughly 
equivalent to a memory location that holds a value. The values stored in the drive’s objects are 
used to perform the drive functions (current loop, velocity loop, position loop, I/O functions).
The drive has a unique object for every parameter that needs to be stored or used. Access to 
the objects varies depending on what the object is used for. Objects may be writable, readable, 
or both. Some objects are state dependant such that they may only be written to if the drive is 
in a certain state (e.g. disabled state). The list of objects that AMC EtherCAT servo drives use is 
found in the “Object Dictionary” on page 30. Each table in the object dictionary describes the 
important information regarding that object including: object index, sub-indices, units, and 
accessibility.
Each object is accessible with a 16-bit address called the object index. Some objects contain sub 
components with 8-bit addresses called sub-indices. Reading and writing to objects is 
accomplished via CANopen Messages. Specific types of messages are designed to access 
specific objects.
1.2.1 Object Dictionary Structure
There are 3 main object categories:
Data Type Objects (Registers) 0x0000 - 0x0FFF   The first 1000h bytes of the object 
dictionary are made up of registers, which are configured from an EtherCAT host, and 
generally not writeable from the application side. Registers may be monitored via a 
configuration tool such as TwinCAT .
CoE Communication Objects 1000h – 1FFFh   These objects relate to CoE 
communication; more specifically, they relate to objects defined by the ETG.1000 
communication profile. Objects in this range are used to configure CoE messages.
Manufacturer Specific Objects 2000h – 5FFFh   These objects are manufacturer 
specific. Detailed information about the AMC manufacturer specific objects can be found in the 
“Object Dictionary” on page 30.
Standard Servo Drive Objects 6000h – 9FFFh   These objects are the standardized 
device profile objects. Objects in this range relate to the device profile of the EtherCAT device. 
The applicable device profile for AMC EtherCAT drives is ETG.6010 (Implementation guideline 
for CiA402 drive profile). Detailed information about AMC supported DS402 objects can be 
found in the “Object Dictionary” on page 30.
Index (hex) Object Dictionary Area
0x0000-0x0FFF Data Type Objects (Registers)
0x1000-0x1FFF CoE Communication Objects
0x2000-0x5FFF Manufacturer Specific Objects
0x6000-0xFFFF Profile Objects

---
## Page 13

MNCMECRF-07 3
Communication Manual / EtherCAT State Machine
1.2.2 Object Data
Every object index - and sub-index if available - is an address pointer to a data location. The 16-
bit index and 8-bit sub index make it effectively a 24-bit address space. The data type can be 
any type typically found in digital systems, such as 8-bit, 16-bit, 32-bit, or string. The data type 
can also be a record (in the case of an index with sub-indices), with multiple record entries, 
and each entry can be of the above mentioned data type. Nested records are not allowed.
1.3 EtherCAT State Machine
The EtherCAT state machine defines the general communication states of the drive. The 
EtherCAT master controls the state by sending requests to the slave. Each state defines which 
types of communication are allowed. Each state allowance is defined below.
State Allowances
Init No communication on the application layer (no SDOs)
No process data communication is possible (no PDOs)
Pre-Operational SDO communication allowed
No process data communication is possible (no PDOs)
Safe-Operational SDO communication allowed
PDOs are sent, but only TPDOs (drive-to-host) are processed. RPDOs are ignored
Operational SDO communication allowed
PDO communication allowed
Init
Pre-Operational
Safe-Operational
Operational

---
## Page 14

MNCMECRF-07 4
Communication Manual / Watchdog
1.4 Watchdog
1.4.1 Sync Manager Watchdog
The Sync Manager (SM) watchdog monitors the RPDO rate while the drive is in Cyclic 
Synchronous mode and the EtherCAT state machine is in the Operational state. The watchdog 
time is configured using the EtherCAT host software. If cyclic RPDO information is missed, the 
watchdog timer will initiate. When no new PDOs are received within the configured watchdog 
time, the drive will report a Comm Channel Error. The behavior associated with this error is 
configurable via the setup software, or by writing to object 2065.21h. The error will become 
inactive if RPDOs recommence or if the EtherCAT state is transitioned to something other than 
Operational. While the SyncManager watchdog time can be configured to any time, total 
watchdog response times below 15ms cannot be guaranteed.
1.4.2 PDO Watchdog
The PDO watchdog monitors PDO messages while the drive is in the "Operational" state and in 
cyclic operation mode. For the PDO watchdog fault to trigger, the following three conditions 
must be met:
1. Drive must be in "Operational" state, and the number of PDOs must be non-zero.
2. Drive must be in cyclic operation mode.
3. Drive must have a valid period (the object 60C2.01h has a valid value in it).
When the above three conditions are met, the PDO watchdog is armed and will start its 
countdown after every valid PDO transfer. If no new PDO messages are received after 2-3 
cycles, the PDO watchdog fault will trigger a Comm Channel Error.
PDO watchdog behavior is shown below. The example also accounts for processing and 
hardware delays (<15ms) when the Comm Channel Error is assigned to an event action such 
as drive disable.
PDO Watchdog
Countdown Begin
PDO Watchdog
Triggered
Drive 
Disable
Red LED
LED State
PDO Received

---
## Page 15

MNCMECRF-07 5
Communication Manual / SDO vs. PDO Messages
1.5 SDO vs. PDO Messages
There are two methods for reading and writing data to objects: Service Data Object (SDO) and 
Process Data Object (PDO) messages. An SDO consists of an outgoing message from host to 
node and a reply message from node to host; this is called confirmed messaging. A PDO 
consists of 1 or more unconfirmed messages. PDOs are used for cyclic, time critical data 
exchange, while SDOs are used for non-time-critical communication and configuration. PDOs 
are the primary method for communication during run-time but they must be configured 
prior to being used. PDO transmission occurs only while the EtherCAT state machine is in the 
operational state (and limited transactions during safe operational state). SDO messages may 
be used any time after initialization but are less commonly used during actual drive operation.
1.5.1 SDO Messages
An SDO message can be used to read nearly every object in the object dictionary. Write access 
may be limited to certain objects or certain drive operation conditions. The EtherCAT host 
generally handles the message structure of an SDO. If writing to an object, it is required to 
specify the object index, sub-index, and the data (the size of the data may also be required). 
Below are examples of how different host programs handle reading and writing SDO messages 
during configuration.
TwinCAT can be configured to continuously poll every drive object. Writing data to an object is 
as simple as double-clicking on the object, entering the data, and clicking OK. If SDO is 
accepted, the table will update with the new value.


---
## Page 16

MNCMECRF-07 6
Communication Manual / SDO vs. PDO Messages
SOEM (Simple Open EtherCAT Master) software requires the index, sub-index, and data if 
writing to an object.
EtherCAT Master Sample software (Acontis Technologies) requires the size of the object in 
addition to the index, sub-index, and data.
1.5.2 PDO Messages
PDO messages exchange information between the host and nodes without the overhead of 
SDO messages. PDO messages have no reply, (i.e. they are unconfirmed messages) which 
allows for fast, efficient data transfer of up to 16 objects per PDO. PDO messages, unlike SDO 
messages, are configured prior to use. Once configured, PDOs are transmitted every EtherCAT 
cycle. There are two types of PDO messages: a transmit PDO (TPDO) message and a receive 
PDO (RPDO) message.
Transmit Process Data Object (TPDO)   The TPDO sends data from the slave to the host. 
Before data is transmitted by the TPDO, it must first have the desired read objects mapped to 
it. The TPDO does not alter any object data; it only transmits data to the host.
Receive Process Data Object (RPDO)   The host uses the RPDO to write data to objects in 
the slave. Before data is received by an RPDO, it must have the desired write objects mapped to 


---
## Page 17

MNCMECRF-07 7
Communication Manual / SDO vs. PDO Messages
it. Since the RPDO is used to write to object data, it is important to ensure that the data sent 
from the host is in agreement with the objects mapped to the PDO (PDO object mapping is 
discussed below).
PDO Configuration   PDO configuration is accomplished by writing the index, sub-index, and 
object length of the desired object to the appropriate sub-index of the PDO mapping object. 
Configuration of the PDO mapping objects must be done while the EtherCAT state machine is 
in the pre-operational state. With one or more objects mapped, PDO communication will begin 
once the EtherCAT state machine is transitioned to the operational state.
Mapping Parameter Object   The mapping parameter object contains information about 
each object mapped to the PDO. AMC EtherCAT drives have one RPDO mapping object (1600) 
and one TPDO mapping object (1A00), each with 16 sub-indices allowing up to 16 objects to 
be mapped. The total data for each must be less than or equal to 256 bits. This could be in the 
form of up to eight 32-bit objects, or sixteen 16-bit objects, or some other combination of 16 
and 32 bit objects. Sub-index zero is read/write in this case, and must be configured with the 
total number of objects mapped to the PDO. The table below shows the structure of the address 
information for the PDO mapping objects.
TABLE 1.1 Mapping Parameter bit descriptions
The three components that represent a mapped object are described below:
• Index: The index of the object mapped to the PDO (zero if no object is mapped).
• Sub-index: The sub-index of the mapped object(zero if the object has no sub-indices).
• Object Length: The bit length (in hex) of the data to be transmitted. For example, 20h = 32 
bits.
By placing information about an object in the Mapping Parameter, that object becomes 
mapped to the associated PDO. Mapping allows PDOs to know where they should read their 
data prior to transmission (in the case of a TPDO) or where they should write their data upon 
reception (in the case of an RPDO). 
EtherCAT PDO Assignments   AMC EtherCAT drives employ a user mappable PDO structure. 
By default, there are pre-mapped PDOs when drives are shipped from the factory, as shown in 
Table 1.2. TxPDOs are PDOs coming from the drive, and RxPDOs are data going to the drive. 
This default mapping may be changed or added to as the application requires.
Bits 31 – 16 Bits 15 – 8 Bits 7 – 0
Index Sub Index Object Length

---
## Page 18

MNCMECRF-07 8
Communication Manual / SDO vs. PDO Messages
TABLE 1.2 Default Pre-Mapped PDOs 
The list of PDOs may be modified or added to. It is not recommended to remove the pre-
mapped PDOs. See “Appendix B” on page 236 for an example of how to modify the PDO list 
using TwinCAT .
PDO Mappable Objects   Only a subset of objects in the object dictionary may be mapped to 
a TPDO or RPDO. Table 1.3 lists all PDO mappable objects. Data exchange with objects not 
listed in the table require an SDO.
TABLE 1.3 PDO Mappable Objects
TxPDOs RxPDOs
Status Word Control Word
Actual Position Target Position
Actual Velocity Target Velocity
Actual Current Target Current
Digital Inputs User Bits
Type Object Index Sub-Index Object Name Mapping Access PDO Allocation (bits)
Drive 
Operation
2001 03 User Bits RPDO/TPDO 16
6040 00 ControlWord RPDO/TPDO 16
Command 
Objects
6071 00 Target Current RPDO/TPDO 16
607A 00 Target Position RPDO/TPDO 32
60B1 00 Velocity Offset RPDO/TPDO 32
60B2 00 Current Offset RPDO/TPDO 16
60FF 00 Target Velocity RPDO/TPDO 32
Monitor 
Objects
2002 01 Drive Bridge Status TPDO Only 16
2002 02 Drive Protection Status TPDO Only 16
2002 03 System Protection Status TPDO Only 16
2002 04 Drive/System Status 1 TPDO Only 16
2002 05 Drive/System Status 2 TPDO Only 16
2002 06 Drive/System Status 3 TPDO Only 16
2002 07 Active Configuration Status TPDO Only 16
2003 01 Drive Bridge Status History TPDO Only 16
2003 02 Drive Protection Status History TPDO Only 16
2003 03 System Protection Status History TPDO Only 16
2003 04 Drive/System Status 1 History TPDO Only 16
2003 05 Drive/System Status 2 History TPDO Only 16
2003 06 Drive/System Status 3 History TPDO Only 16
200F 01 DC Bus Voltage TPDO Only 16
2010 02 Current Demand - Torque TPDO Only 16
2010 12 Torque Summation Input TPDO Only 32
2010 13 Torque Summation Offset TPDO Only 32
2011 05 Velocity Error TPDO Only 32
2011 06 Velocity Summation Input TPDO Only 32
2011 07 Velocity Summation Offset TPDO Only 32
2012 03 Position Demand TPDO Only 32
2012 05 Position Summation Input TPDO Only 32
2012 06 Position Summation Offset TPDO Only 32

---
## Page 19

MNCMECRF-07 9
Communication Manual / SDO vs. PDO Messages
Monitor 
Objects
2012 07 Position Index Capture Value TPDO Only 32
2018 01 PLS Input Value TPDO Only 32
2018 02 PLS 1 State TPDO Only 32
2018 03 PLS 2 State TPDO Only 32
2019 01 Capture ’A’ Value TPDO Only 32
2019 02 Capture ’B’ Value TPDO Only 32
2019 03 Capture ’C’ Value TPDO Only 32
201A 01 Analog Input 1 Value TPDO Only 16
201A 02 Analog Input 2 Value TPDO Only 16
201A 03 Analog Input 3 Value TPDO Only 16
201A 04 Analog Input 4 Value TPDO Only 16
201D 01 PVT Status Values TPDO Only 16
201E 01 Auxiliary Encoder Value TPDO Only 32
201E 02 Auxiliary Position Index Capture Value TPDO Only 32
2021 01 External Thermal Sense Value TPDO Only 32
2021 02 Thermistor Resistance TPDO Only 16
2022 01 Analog Input 1 ADC Raw Value TPDO Only 16
2022 02 Analog Input 2 ADC Raw Value TPDO Only 16
2022 03 Analog Input 3 ADC Raw Value TPDO Only 16
2022 04 Analog Input 4 ADC Raw Value TPDO Only 16
2023 01 Digital Input Values TPDO Only 16
2025 01 Analog Output 1 Value TPDO Only 16
2025 02 Analog Output 2 Value TPDO Only 16
6041 00 Status Word TPDO Only 16
6061 00 Modes of Operation Display TPDO Only 16
6064 00 Actual Position TPDO Only 32
606B 00 Velocity Demand TPDO Only 32
606C 00 Actual Velocity TPDO Only 32
6077 00 Actual Current TPDO Only 16
60F4 00 Position Error TPDO Only 32

---
## Page 20

MNCMECRF-07 10
Communication Manual / Control State Machine
1.6 Control State Machine
1.6.1 State Machine Overview
AMC EtherCAT drives operate based on a control state machine as defined by CANopen 
standards, where each state has a defined behavior (this is not to be confused with the 
EtherCAT state machine, which controls communication access). The drive can be controlled to 
transition from one state to another in a particular order using the ControlWord object 
(6040h). This is a write only object used specifically to transition the drive’s control state 
machine between states. Below is a graphical overview of the state machine. The grey boxes 
represent the states. The arrows represent the one-way path between states. The small text 
along the path of the arrow represents the command necessary to make each transition.
FIGURE 1.1 ControlWord State Machine Block Diagram
Upon power-up, the drive will automatically step through the ‘Start’ and ‘Not Ready to Switch 
On’ states, arriving at the ‘Switch On Disabled’ state. Further advancement to other states is 
accomplished by setting the ControlWord (Object index 6040h) to the proper value. The 
 
 
Ready to 
Switch On  
 
 
Operation 
Enabled
 
Quick Stop 
Active
 
Fault  
 
 
 
 
 
 
Switch On 
Disabled
Reset
Fault
Shut
Down
Disable
Voltage
Disable
Voltage Disable
Voltage
Disable
Voltage
Switch
On
Shut
Down
Enable
Operation
Shut
Down
Enable
Operation
Quick
Stop
Power
Disabled
Power
Enabled
Fault
Switch On
Not Ready to 
Start
Operation Disabled
(Switched On)
Switch
On
Initialization
Fault Reaction
Active

---
## Page 21

MNCMECRF-07 11
Communication Manual / Control State Machine
commands that cause the state transitions in the state machine correspond to certain bit 
settings within the ControlWord. For example, to transfer from the ‘Ready to Switch On’ state to 
the ‘Switched On State’ , one would use the Switch On command, by setting the ControlWord to 
the appropriate value (and hence bit pattern). The drive state may be queried by using 
StatusWord (Object index 6041h). If the drive senses a fault (any internal drive event which 
causes the bridge to be disabled), it will automatically move into the Fault Reaction Active 
state, then transition to the Fault state. The ControlWord can once again be used to move from 
the Fault state to the Switch On Disabled state.
1.6.2 Drive States
The following tables provide details on each of the CANopen states supported by AMC drives.
TABLE 1.4 
TABLE 1.5 
TABLE 1.6 
TABLE 1.7 
Not Ready to Switch On
Function Part of drive initialization
Status Logic Supply has been applied to the drive. The drive is being initialized. Drive functionality is disabled during this time.
Transitions Transition to ‘Switch On Disabled’ is automatic when initialization complete.
Switch On Disabled
Function Drive initialization is complete. If a fatal error exists, the processor executes a Reset Fault command automatically. The drive is still 
disabled.
Status Drive parameters have been set up. Only logic supply voltage is necessary at this time. Drive process monitoring may begin.
Transitions Transition to the Ready to Switch On state is possible by a Shut Down command.
Ready to Switch On
Function Last state before Bridge enabled
Status No energy is supplied to the motor. Control loops do not work. The drive function is still disabled. Bus power may be applied.
Transitions Transition to Operation Disabled (Switched ON) state is possible via the Switch On command. Transition back to the Switch On 
Disabled state is possible via the Disable Voltage command, or by a Quick Stop command.
Operation Disabled (Switched On)
Function The bridge is turned on and a mode-dependent zero command is issued.
Status The control loops are operational. Bus power is applied. The power section is switched on (if not already on). The target signal is not 
processed. The drive function is disabled. 
Transitions Transition to the Operation Enabled state is possible via the Enable Operation command. Transition back to the Ready to Switch On 
state is equally possible via the Shut Down command. Transition back to the Switch On Disabled state is possible via the Disable 
Voltage command or via a Quick Stop command.

---
## Page 22

MNCMECRF-07 12
Communication Manual / Control State Machine
TABLE 1.8 
TABLE 1.9 
TABLE 1.10 
TABLE 1.11 
Operation Enabled
Function This is the normal operation state of the drive.
Status Power is supplied to the motor. Control loops are operational and target signals are processed.
Transitions A Quick Stop command transfers the drive to the Quick Stop Active state. Transition back to the Ready to Switch On state is 
possible via the Shut Down command. Transition back to the Switch On Disabled state is possible via the Disable Voltage command 
or the Drive Enable Input. Transition back to the Operation Disabled state is possible via the Switch On command.
Quick Stop Active
Function The motor (shaft) is brought to a stop using the Stop Deceleration Limit.
Status Control loops are operational. Power is applied to the motor. The motor shaft is held in position in position mode or zero velocity in 
velocity mode.
Transitions Transition back to the Operation Enabled state is possible via the Enable Operation (7) command. Transition back to the Switch On 
Disabled state is possible via the Disable Voltage (4) command, or via the Drive Enable Input (2) (both include the “Power Disable 
Delay” process).
Fault Reaction Active
Function The event reaction for the incident fault state will occur.
Status Power is supplied to the motor. Control loops are operational and target signals are processed. 
Transitions Fault Reaction Active will automatically transition to the Fault state. Time in Fault Reaction Active state is dependent on background 
tasks, but could be anywhere between 100s and 2ms.
Fault
Function A fault has occurred and has not yet been reset
Status The power output stage is disabled; no energy is supplied to the motor.
Transitions Transition to the Switch On Disabled state is possible via the Reset Fault command.

---
## Page 23

MNCMECRF-07 13
Communication Manual / Control State Machine
1.6.3 ControlWord (6040h)
The following table shows the values used with object 6040h to cause transitions shown in 
Figure 1.1 above. An example hexadecimal value is provided on the right.
TABLE 1.12  ControlWord values
 
TABLE 1.13 Additional ControlWord values
For additional information on object 6040h, see “6040h: ControlWord” on page 181.
State Transition Command Bit 7 Bit 4 Bit 3 Bit 2 Bit 1 Bit 0 Example 
Value
Reset Fault 01 X X X X X XX 80
Disable Voltage 0 X X X 0 X XX 00
Shutdown 0 X X 1 1 0 XX 06
Switch On 0 X 0 1 1 1 XX 07
Enable Operation 0 X 1 1 1 1 XX 0F
Quick Stop 0 X X 0 1 X XX 02
Begin Homing 
(Homing mode only)
0 1 1 1 1 1 XX 1F
End Homing 
(Homing mode only)
0 0 1 1 1 1 XX 0F
0 = OFF, 1 = ON, X = don’t care
State Transition Command Bit 13 Bit 12 Description
Inhibit Negative Motion X 1 enable commanded * [negative stop OR negative torque inhibit]
Inhibit Positive Motion 1 X enable commanded * [positive stop OR positive torque inhibit]
0 = disable, 1 = enable, X = don’t care, * see Event Action Configuration command (2065h)

---
## Page 24

MNCMECRF-07 14
Communication Manual / Control State Machine
1.6.4 StatusWord (6041h)
The StatusWord reports exactly which state the drive is in. Table 1.14 defines each bit in the 
StatusWord and Table 1.15 shows how to interpret what state the drive is in via the 
combination of bits 0-3, 5 and 6. Each drive state is described in detail in “Drive States” on 
page 11.
TABLE 1.14  StatusWord bit descriptions
TABLE 1.15  StatusWord drive states
Bits Name Descriptions
0 Ready to Switch On See Table 1.15 to see how this bit relates to the control state machine.
1 Switched On See Table 1.15 to see how this bit relates to the control state machine
2 Operation Enabled See Table 1.15 to see how this bit relates to the control state machine
3 Fault See Table 1.15 to see how this bit relates to the control state machine
4 Voltage Enabled 1 when power is applied to the motor
5 Quick Stop See Table 1.15 to see how this bit relates to the control state machine
6 Switch On disabled See Table 1.15 to see how this bit relates to the control state machine
7 Warning Object 205B can be used to configure which internal drive events will set this bit.
8 Manufacture specific Object 205B can be used to configure which internal drive events will set this bit.
9 Remote 0 when read/write access has been seized by the service channel (i.e. configuration software).
1 when control over the network is allowed.
10 Target Reached 1 Under the following conditions:
- Home reached if the Can operational-mode is homing.
- Home reached if the Can operational-mode is custom and homing is active.
- At command for all other conditions.
11 Internal Limit Active Object 205B can be used to configure which internal drive events will set this bit.
12 Homing complete 1 when Homing completes, otherwise 0.
13 - -
14 - -
15 - -
Drive State Bit 6 Bit 5 Bit 4 Bit 3 Bit 2 Bit 1 Bit 0 StatusWord
Not Ready to 
Switch On
0 X X 0 0 0 0 xxxx xxxx x0xx 0000
Switch On 
Disabled
1 X X 0 0 0 0 xxxx xxxx x1xx 0000
Ready to Switch 
On
0 1 X 0 0 0 1 xxxx xxxx x01x 0001
Switched On 0 1 X 0 0 1 1 xxxx xxxx x01x 0011
Operation 
Enabled
0 1 X 0 1 1 1 xxxx xxxx x01x 0111
Fault Reaction 
Active
0 X X 1 1 1 1 xxxx xxxx x0xx 1111
Fault 0 X X 1 0 0 0 xxxx xxxx x0xx 1000
Quick Stop Active 0 0 X 0 1 1 1 xxxx xxxx x00x 0111
0 = OFF, 1 = ON, X = don’t care

---
## Page 25

MNCMECRF-07 15
Communication Manual / Homing
1.7 Homing
AMC EtherCAT drives support a wide variety of homing routines. These routines rely on 
signals such as limit switch, home switch, and encoder index signals to achieve precise starting 
positions. Four objects define the offset, speed, acceleration, and the particular homing method 
used. These objects are listed in the table below. 
TABLE 1.16 Homing Objects
1.7.1 Home Offset
The home offset specifies the difference between the home position and the zero position. The 
home position is the position of the motor when the home switch or encoder index is toggled 
during a homing routine. The zero position is the position defined to be zero as seen by the 
EtherCAT master. If the home offset is set to zero, the home position will be equal to the zero 
position.
1.7.2 Homing Speeds
There are two homing speeds to take into consideration: the speed during the search for home 
switch, and the speed during the search for the index. Typically, the speed during the search 
for the home switch is set to be faster than the speed during the search for the index.
1.7.3 Homing Acceleration
A single value is used to define the acceleration and deceleration of all moves during the 
homing routine.
1.7.4 Homing Methods
Homing methods depend on the presence of up to three different system components: an 
index pulse, a home switch, and a limit switch. The simplest homing methods require just one 
or none of these components, whereas the more complex methods require two or all of these 
components. All homing methods have been summarized in Table 1.17, along with their 
necessary components, and have been named according to [DSP402] which states that there 
are a total of 35 possible homing methods, some of which are reserved and not currently 
specified.
Object Index Description
607Ch Home Offset
6099h Homing Speeds
609Ah Homing Acceleration
6098h Homing Method

---
## Page 26

MNCMECRF-07 16
Communication Manual / Homing
TABLE 1.17  Homing Methods Summary
Because these homing methods can become fairly complex, they are best described visually. As 
a result, homing diagrams are utilized to illustrate the behavior of each method. Homing 
diagrams consist of multiple components each of which is described in Figure 1.2.
FIGURE 1.2 Homing Diagrams
Homing Method Index Pulse Home Switch Limit Switch
Methods 1 & 2  
Methods 3 to 6  
Methods 7 to 14   
Methods 15 & 16 Reserved
Methods 17 & 18 
Methods 19 to 22 
Methods 23 to 30  
Methods 31 & 32 Reserved
Methods 33 & 34 
Method 35
Load and physical limits
The square near the middle of the illustration shows the load object that is to be moved. The endpoints represent physical limitations or barriers, which 
the load cannot travel past. The left side is in the negative direction while the right side is in the positive direction.
Direction of travel
The vertical line on the right side represents the starting position. The load travels in the direction of the arrow. In the illustration shown, the load begins 
traveling in the negative direction and then switches directions to move in the positive direction. The circle represents the home position at which point 
the (actual) measured position is reset to zero. The small section of arrow following the circle represents the distance traveled, past the home position, 
during deceleration of the load. Lastly, the number in the circle represents the number designated to that particular homing method.
Index Pulse
Each vertical line represents one index pulse.
Limit/Home Switch
A label in the actual homing diagram will be used to label a switch as either a limit/home switch. As shown, there are only two 
positions for a switch: high (active) or low (inactive).
Break
Represents a break in the diagram. This is used for representing a length of distance too large to properly scale on the 
diagram.
1

---
## Page 27

MNCMECRF-07 17
Communication Manual / Homing
Method 1: Homing on the Negative Limit Switch    This method uses the negative 
limit switch and index to home the load. If the negative limit switch is off, the motor moves in 
the negative direction. Once the limit switch toggles, the motor changes direction and moves 
until the next encoder index. Homing is complete at this point. Figure 1.3 illustrates the 
homing diagram for this method.
FIGURE 1.3 Homing on the Negative Limit Switch 
Method 2: Homing on the Positive Limit Switch   This method uses the positive limit 
switch and index to home the load. If the positive limit switch is off, the motor moves in the 
positive direction. Once the limit switch toggles, the motor changes direction and moves until 
the next encoder index. Homing is complete at this point. Figure 1.4 illustrates the homing 
diagram for this method.
FIGURE 1.4 Homing on the Positive Limit Switch
1
Index Pulse
Negative Limit Switch
Index Pulse
Positive Limit Switch
2

---
## Page 28

MNCMECRF-07 18
Communication Manual / Homing
Methods 3 and 4: Homing on the Positive Home Switch   These methods use the 
positive home switch and index to home the load. The initial direction of movement for a given 
routine method is dependent on the home switch position. However, the final position is 
always in the same direction. Homing methods 3 and four perform the same operations, but in 
opposite directions with opposite home switch polarity. Figure 1.5 illustrates the homing 
diagram for these methods.
FIGURE 1.5 Homing on the Positive Home Switch
Methods 5 and 6: Homing on the Negative Home Switch   This is literally a 
mirror image of the homing routines used by methods 3 and 4. Figure 1.6 illustrates the 
homing diagram for these methods.
FIGURE 1.6 Homing on the Negative Home Switch
4
Homing Switch
3
3
4
Index Pulse
6
Homing Switch
5
5
6
Index Pulse

---
## Page 29

MNCMECRF-07 19
Communication Manual / Homing
Methods 7-14: Homing on the Home Switch   These methods use all three possible 
homing components (index pulse, home switch, and limit switch) with the index pulse to the 
nearest right or left of the home switch always being the sought after home position. Methods 
7 to 10 use a positive limit switch and if the starting position is outside the active home switch 
region the initial direction of travel is always positive. For cases where the starting position is 
inside the active home switch region the initial direction will depend upon the index pulse 
being sought after: methods 7 & 8 home towards the left home switch edge so the initial 
direction will be left, whereas methods 9 & 10 home towards the right home switch edge so the 
initial direction will be right. Note that the only difference between methods 7 & 8 is that one 
homes to the index pulse left of the home switch edge whereas the other homes to the index 
pulse to the right; the same difference holds true for methods 9 & 10. Figure 1.7 illustrates the 
homing diagram for methods 7 to 10.
FIGURE 1.7
Homing Switch
7
7
Index Pulse
7
Positive Limit Switch
8
8
8
9
9
9
10
10
10

---
## Page 30

MNCMECRF-07 20
Communication Manual / Homing
Methods 11 to 14 use a negative limit switch instead of a positive limit switch. As a result, the 
initial direction will be left, instead of right, whenever the starting point is outside of the active 
home switch region. Outside of this difference, methods 11 to 14 are identical to methods 7 to 
10. Figure 1.8 illustrates the homing diagram for methods 11 to 14.
FIGURE 1.8
Homing Switch
Index Pulse
Positive Limit Switch
14
14
14
11
11
11
12
12
12
13
13
13

---
## Page 31

MNCMECRF-07 21
Communication Manual / Homing
Methods 17-30: Homing without an Index Pulse   These homing routines use the 
same methods as 1 to 14, except the index pulse is not used. Instead, the home position is 
dependant on the edge of the relevant home or limit switch. To illustrate this difference, 
Figure 1.9 shows the homing diagram for methods 19 and 20, which are equivalent to 
methods 3 and 4 without the index pulse.
FIGURE 1.9
Methods 33 and 34: Homing on the Index Pulse   These homing methods home to 
the nearest index pulse. Method 33 homes in the negative directions and method 34 homes in 
the positive direction.
FIGURE 1.10
Method 35   This homing method requires no index pulse or switches and involves nothing more 
than setting the current measured position equal to the home position value, which can be 
accomplised in object 2039.02h “Home Position Value” on page 63.
Homing Switch
19
19
20
20
34
33
Index Pulse

---
## Page 32

MNCMECRF-07 22
Communication Manual / Modes of Operation
1.8 Modes of Operation
AMC EtherCAT drives close position, velocity, and torque (current) loops that are configurable 
via CoE. There are 8 modes of operation available with object 6060h. Other modes of operation 
are achievable using DriveWare. When changing loop configurations using object 6060h, 
velocity and position loop feedback sources are not touched. This means changing loop 
configurations assumes the feedback wiring and project parameters are configured properly 
for both the present loop and the one the drive is moving to.
More information on object 6060h is found in the “Object Dictionary” on page 30.
TABLE 1.18 Modes of Operation
1.8.1 Profile Modes
In a profile mode of operation, the trajectory is limited by the drive. Profile modes use the 
command limiter values (object 203C) to limit the maximum command rate. If the host sends 
a large command step, the drive spreads the demand over some period of time to stay equal to 
or below the maximum defined rate. The command limiter is configurable to supply up to 4 
different slopes depending on the input, as shown in Figure 1.11 below.
Modes of Operation
Profile Position Mode
Profile Velocity Mode
Profile Torque Mode (current mode)
Homing Mode
Cyclic Synchronous Position Mode
Cyclic Synchronous Velocity Mode
Cyclic Synchronous Torque Mode
Custom Configured Modes

---
## Page 33

MNCMECRF-07 23
Communication Manual / Modes of Operation
FIGURE 1.11  
Profile Position Mode   The AMC Position control loop is a fully de-coupled PID with velocity and 
acceleration feedforward terms. In Profile Position Mode, the drive closes three control loops, 
position, velocity, and current. The velocity loop provides additional “stiffness,” keeping the 
dynamic position errors minimal because the drive now reacts not only to position errors, but 
also to velocity errors (which can be interpreted as position error changes). The Command 
Limiter is enabled in this mode. The Profiler sets limits on the rate of change of the target 
position command, otherwise called velocity. When commanding point-to-point moves, the 
velocity between points is limited to the maximum value set in the profiler. When tuning the 
position loop for profile position mode, proportional gain is typically all that is needed. It is 
important, however, to start with a stable, yet responsive velocity loop. Feedforward gain can 
be added to improve tracking performance, if needed. More information on tuning is found in 
the DriveWare application help files.
The following objects define how the drive will behave in Position mode.


---
## Page 34

MNCMECRF-07 24
Communication Manual / Modes of Operation
TABLE 1.19 
Profile Velocity Mode   The AMC Velocity control loop is a fully de-coupled PID with an 
acceleration feedforward term, and a low speed estimator. In Profile Velocity Mode, the drive 
closes two control loops, velocity, and current. Velocity feedback may be derived from a motor 
mounted encoder or analog source with a 10V maximum. The low speed estimator is most 
useful when necessarily tight velocity loops can cause audible noise during low speed moves 
(less than 1 count per velocity update).
The Command Limiter is enabled in this mode. The Limiter sets limits on the rate of change of 
the velocity command. When commanding large velocity transients, the resulting acceleration 
between points is limited to the maximum value set in the profiler.
When tuning the velocity loop it is important to start with a stable, yet responsive current loop. 
Feedforward gain can be added to improve tracking performance, if needed. More information 
on tuning is found in the DriveWare help files.
TABLE 1.20 
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation.
203Ch Command Limiter Parameters Sets the values used by the command limiter to limit the target command. 
6086h Motion Profile Type Sets profiling to linear ramp. Currently this is fixed and read only.
2038h Position Loop Control Parameters Sets the tuning values associated with the position loop
2039h Position Limits Sets the trip points for various position events such as Max Measured Position Limit.
2012h Position Values Read instantaneous values such as Position demand and Position Target. This object is 
read only.
6064h Actual Position Same as 2012.01h, reads measured position value.
607Ah Target Position Sets the target position command.
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation.
203Ch Command Limiter Parameters Sets the values used by the command limiter to limit the target command. 
6086h Motion Profile Type Sets profiling to linear ramp. Currently this is fixed and read only.
2037h Velocity Limits Sets the trip points for various velocity events such as Over Speed.
2036h Velocity Loop Control Parameters Sets the tuning values associated with the velocity loop
2011h Velocity Values Read instantaneous values such as Velocity demand and Velocity Target. This object is 
read only.
6069h Velocity Sensor Actual Value Same as 2011.01h, reads pre-filtered measured velocity value.
606Bh Velocity Demand Same as 2011.04h, reads Velocity Demand value.
606Ch Actual Velocity Same as 2011.02h, reads post-filtered measured velocity value.
60FFh Target Velocity Sets the target velocity command.

---
## Page 35

MNCMECRF-07 25
Communication Manual / Modes of Operation
Profile Current Mode   Profile Current Mode, also referred to as Profile Torque Mode, configures 
the drive to respond to target current commands. The drive’s current loop consists of a PI loop. 
Because torque is merely a constant Kt multiplied by a magnitude of current, it is the 
programmer’s responsibility to convert current values into torque values in the software 
environment.
The Command Limiter is enabled in this mode and sets limits on the rate of change of the 
current command. During a step acceleration command, the change in commanded torque, 
known as Jerk, is limited to the maximum value set in the profiler.
Tune this loop according to “current loop tuning” instructions in the DriveWare Software 
Guide. The following objects are used to setup and operate the Current Mode:
TABLE 1.21 
1.8.2 Homing Mode
See “Homing” on page 15 for detailed information about methods and hardware involved in 
homing.
1.8.3 Cyclic Synchronous Modes
Cyclic Synchronous Modes give responsibility of trajectory control to the host. There is no 
command limiter. Instead, the drive interpolates between command points, defining the rate 
by dividing the change in command by the interpolation time period (object 60C2). This 
allows the drive to respond smoothly to each step in command. Figure 1.12 below shows how 
the drive interpolates different commands, with T representing the interpolation time. In each 
case, the drive arrives at the commanded value at precisely T seconds after the command 
changed.
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation
203Ch Command Limiter Parameters Sets the values used by the command limiter to limit the target command.
6086h Motion Profile Type Sets profiling to linear ramp. Currently this is fixed and read only.
2010h Current Values Read instantaneous values such as Current Demand and Current Target. This object is read 
only.
2034h Current Loop and Commutation Values Sets the tuning and commutation values associated with the current loop.
6071h Target Current Sets the target current command.
6077h Actual Current Reads the actual motor current (in case of 3-phase motors, this is a composite, equivalent 
single phase current).

---
## Page 36

MNCMECRF-07 26
Communication Manual / Modes of Operation
FIGURE 1.12
Cyclic Synchronous Position Mode   In Cyclic Synchronous Position Mode, the drive 
closes three control loops: position, velocity, and current. The host can send target position, 
velocity feedforward, and current feedforward values to the drive. This allows for gain 
compensation in applications with varying loads.The Command Limiter is disabled in this 
mode, giving the host more control over the motion profile. The drive interpolates linearly 
between EtherCAT updates to maintain consistent targets between commands. The 
interpolation time period value should be equal to the EtherCAT cycle time for proper 
functionality.
The following objects define how the drive will behave in Cyclic Synchronous Position Mode.
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation.
60B1h Velocity Offset Contains the input value for velocity feed forward.
60B2h Current Offset Contains the input value for current feed forward.
60C2h Interpolation Time Period Value Contatins the period used for the linear interpolation algorithm. Used with Cyclic 
synchronous modes of operation.
2038h Position Loop Control Parameters Sets the tuning values associated with the position loop.
2039h Position Limits Sets the trip points for various position events such as Max Measured Position Limit.
2012h Position Values Reads instantaneous values such as Position demand and Position Target. This object is 
read only.
6064h Actual Position Same as 2012.01h, reads measured position value.
607Ah Target Position Sets the target position command.
TimeTTTTTT
Input into Fixed-Time 
Linear Interpolator
New Command 
arrives early
T
Output of the Fixed-
Time Linear Interpolator

---
## Page 37

MNCMECRF-07 27
Communication Manual / Modes of Operation
Cyclic Synchronous Velocity Mode   In Cyclic Synchronous Velocity Mode, the drive 
closes the velocity loop around the current loop. The host can send target velocity, velocity 
offset, and current feedforward values to the drive. This allows for gain compensation in 
applications with varying loads.The Command Limiter is disabled in this mode, giving the host 
more control over the motion profile. The drive interpolates linearly between EtherCAT 
updates to maintain consistent targets between commands. The interpolation time period 
value should be equal to the EtherCAT cycle time for proper functionality.
The following objects define how the drive will behave in Cyclic Synchronous Velocity Mode.
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation.
60B1h Velocity Offset Contains the input value for velocity feed forward.
60B2h Current Offset Contains the input value for current feed forward.
60C2h Interpolation Time Period Value Contatins the period used for the linear interpolation algorithm. Used with Cyclic 
synchronous modes of operation.
2036h Velocity Loop Control Parameters Sets the tuning values associated with the velocity loop.
2037h Velocity Limits Sets the trip points for various velocity events such as Over Speed.
2011h Velocity Values Read instantaneous values such as Velocity Demand and Velocity Target. This object is 
read only.
6069h Velocity Sensor Actual Value Same as 2011.01h, reads pre-filtered measured velocity value.
606Bh Velocity Demand Same as 2011.04h, reads Velocity Demand value.
606Ch Actual Velocity Same as 2011.02h, reads post-filtered measured velocity value.
60FFh Target Velocity Sets the target velocity command.

---
## Page 38

MNCMECRF-07 28
Communication Manual / Modes of Operation
Cyclic Synchronous Current Mode   In Cyclic Synchronous Current Mode, the drive closes 
the current loop. The host can send target current and current offset values to the drive.The 
Command Limiter is disabled in this mode, giving the host more control over the motion 
profile. The drive interpolates linearly between EtherCAT updates to maintain consistent 
targets between commands. The interpolation time period value should be equal to the 
EtherCAT cycle time for proper functionality.
The following objects define how the drive will behave in Cyclic Synchronous Current Mode.
1.8.4 Custom Defined Modes Of Operation
ADVANCED Motion Controls digital servo drives provide flexibility beyond the CANopen 
defined standard modes of operation. For a case where a drive configuration is desired that is 
not available via object 6060h, contact ADVANCED Motion Controls directly for technical 
support.
Object 
index Name Description
6060h Modes Of Operation Sends a request to change the drive’s mode of operation.
6061h Modes of Operation Display Displays the actual mode of operation.
60B2h Current Offset Contains the input value for current offset.
60C2h Interpolation Time Period Value Contatins the period used for the linear interpolation algorithm. Used with Cyclic 
synchronous modes of operation.
2010h Current Values Reads instantaneous values such as Current Demand and Current Target. This object is 
read only.
2034h Current Loop & Commutation Control 
Parameters
Sets the tuning values and commutation values associated with the current loop.
6071h Target Current Sets the target current command.
6077h Actual Current Reads the actual motor current (in case of 3-phase motors, this is a composite, equivalent 
single phase current)

---
## Page 39

MNCMECRF-07 29
Communication Manual / Connecting to an AMC EtherCAT Drive
1.9 Connecting to an AMC EtherCAT Drive
Connecting to an ADVANCED Motion Controls’ EtherCAT drive is possible via two 
communication interfaces on the drive. One interface is the EtherCAT communication 
interface, which is used after the drive is configured for proper operation. The other interface 
is an USB serial communication interface. This is used when first configuring a drive project 
file according to the application needs and storing it to the drive’s Non Volatile Memory.
1.9.1 USB Interface Setup
All that is needed is a USB cable connected from the drive USB port to a computer.Refer to the 
hardware manual and software configuration manual for more information about connecting 
to the USB interface.
1.9.2 EtherCAT Interface Setup
Node Addressing   Typically, the EtherCAT host automatically configures the address according 
to proximity, so no user configuration is required. However, it is possible to override this 
addressing by setting a station alias. Refer to the hardware manual and software configuration 
manual for more information.
1.10 Hardware Requirements
No special hardware is required to operate EtherCAT drives. They use standard 100BASE- TX 
cables, connected to an available network card running EtherCAT host software. For more 
information, refer to the hardware installation manual.

---
## Page 40

MNCMECRF-07 30
 2 Object Dictionary
2.1 Dictionary Table Format
The object dictionary provides one entry for each existing object. Since objects may or may not 
have sub-indices, the following convention is used for each entry:
FIGURE 2.1 Object Table Convention
In the example of Figure 2.1 the object index and sub-index is referenced via the dot (.). 2002h 
is the object index and .01h is the sub-index. Objects without sub-indices will be referenced 
without the dot (.). Furthermore, each entry has the following attributes:
• Data Type: This field specifies the data type of the object. Data types can be 8-bit, 16-bit, 
32-bit, or string.
• Range: This field specifies the usable range of the values this object can contain.
• Units: This field specifies the units that apply to the value stored in this object. If the value 
contained in this object has no units, the field will contain “N/A” . The appropriate physical 
unit is only supplied if there is a one-to-one relationship between the physical unit and 
the drive data type or if a generic scaling factor is used. If a generic scaling factor is used, 
its abbreviation will be supplied in brackets beside the units (as shown in Figure 2.1). For 
units that require specific scaling between a physical unit and the drive data type, an 
abbreviation for a drive unit is supplied. All scaling factors and drive units are described in 
“Appendix” on page 225 according to their abbreviation.
• Accessibility: This field specifies whether the object can be read or written to. If there is a 
* in this box, then the object may only be accessible in certain modes. See the Description 
box for more information about mode dependencies.
• Stored to NVM: This field specifies whether or not the object can be stored to Non Volatile 
Memory such that it is recalled on power up.
• Description: This field contains detailed information on the object and what it is used for.
2002.01h Sub Index Name
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(15)-1] N/A (SF1) Read / Write* No
Description:
Detailed description of what this object does and how to use it.
* This indicates a note about conditions.

---
## Page 41

MNCMECRF-07 31
Object Dictionary / Configuration Objects
2.2 Configuration Objects
Although the following objects are used predominately during drive setup and initialization, 
they are not restricted to use only during setup. Configuration objects can be divided into the 
following three categories.
• Administrative Objects: These objects are used for administrative operations such as 
loading or restoring parameters from non-volatile memory.
• Communication Objects: These objects determine the CANopen communication settings 
of the drive.
• Drive Objects: These objects define the drive configuration and are largely determined by 
the DriveWare setup and configuration software. Objects which contain general drive 
information are also available.
2.2.1 Administrative Objects
2009h: Load EEPROM Values   
200Ah: AMC Store Drive Parameters   
2009.01h Load EEPROM Values
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 See Table N/A Write Only No
Description:
Defines which parameters will be loaded from the drive’s non-volatile memory to the drive’s RAM.
200A.01h AMC Store Drive Parameters
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 See Table N/A Write Only Yes
Description:
Defines which parameters will be stored to the drive’s non-volatile memory.
Key (Hex) Description
165B Load CANopen communication parameters
1CAE Load RS232 communication parameters
7405 Load non-axis parameters
8137 Load axis parameters
Key (Hex) Description
165B Store CANopen communication parameters
1CAE Store RS232 communication parameters
7405 Store non-axis parameters
8137 Store axis parameters

---
## Page 42

MNCMECRF-07 32
Object Dictionary / Communication Settings
2.3 Communication Settings
2.3.1 General Settings
1000h: Device Type   
1018h: Identity Object   
1000h Device Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – [2(32) –1] N/A Read Only No
Description:
Contains information about the device type. This 32-bit object is split into two 16-bit fields. Bits 0-15 describe the device profile and bits 16-
31 supply additional optional information about the device. AMC drives fit under device profile number 402 (Drives and Motion Control), 
which is represented by 0192h in the first 16-bit field. Servo drives are designated by setting the second bit of the second field (bit 17) to 1.
1018.01h Vendor ID
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read Only No
Description:
A unique vendor identifier. Always BDh for ADVANCED Motion Controls’ drives.
1018.02h Product Code
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read Only No
Description:
Contains the product code. ADVANCED Motion Controls’ DigiFlex Performance series products use a fixed product code of 12C.
1018.03h Revision Number
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read Only No
Description:
Contains the drive revision number.
Bit 0-15 Device Profile Number = 0192h (402 - Drives and Motion Controllers)
Bit 16-23 Type = 02h (Servo Drive
Bit 24-31 Reserved = 00

---
## Page 43

MNCMECRF-07 33
Object Dictionary / Communication Settings
1C00h: Sync Manager Communication Type   The Sync Manager Communication 
Type object holds the configuration in which messages are sent and received. A specific 
configuration is required for EtherCAT drives.
1018.04h Serial Number
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read Only No
Description:
Contains the drive serial number.
1C00.00h Number of Sync Manager Channels
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 4 - 32 N/A Read Only Yes
Description:
Number of Sync Manager channels. Default = 4.
1C00.01h Communication Type Sync Manager 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 0 - 4 N/A Read Only Yes
Description:
Communication Type Sync Manager 0. Default value = 1, mailbox receive (master to slave).
1C00.02h Communication Type Sync Manager 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 0 - 4 N/A Read Only Yes
Description:
Communication Type Sync Manager 1. Default value = 2, mailbox send (slave to master).
1C00.03h Communication Type Sync Manager 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 0 - 4 N/A Read Only Yes
Description:
Communication Type Sync Manager 2. Default value = 3, process data output (master to slave).

---
## Page 44

MNCMECRF-07 34
Object Dictionary / Communication Settings
20E6h: CANopen Parameters   
1C00.04h Communication Type Sync Manager 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 0 - 4 N/A Read Only Yes
Description:
Communication Type Sync Manager 3. Default value = 4, process data input (slave to master).
20E6.01h Startup Mode of Operation
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31) –1] N/A Read / Write Yes
Description:
Contains the initial mode of operation when the drive is powered on. Requires power cycle to activate.
20E6.02h CAN options
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write No
Description:
Configuration settings for CANopen functionality. This is the mechanism to switch COB ID filtering on and off.
Note: A reset node or power cycle is needed before the changes will take effect.
Bit Assignment (1 = assigned, 0 = not assigned)
1 Profile Position Mode
2 Profile Velocity Mode
4 Profile Torque Mode (current mode)
6 Homing Mode
8 Cyclic Synchronous Position Mode
9 Cyclic Synchronous Velocity Mode
A Cyclic Synchronous Torque Mode (current mode)
9E Config 0
DE Config 1
FF None (Use active configuration settings)
Bit Assignment (1 = assigned, 0 = not assigned)
0
State Machine Autosequence - When assigned, 
the drive will automatically sequence to the 
enabled state when configured to do so.
1
Inhibit COB ID filtering - When assigned, COB ID 
filtering will be turned off. It is recommended to 
leave this bit unassigned.
2-15 Reserved

---
## Page 45

MNCMECRF-07 35
Object Dictionary / Communication Settings
2006h: Network Configuration   
2.3.2 PDO Configuration
1600h: Receive PDO Mapping   Holds the RPDO mappings 
2006.01h IP Address
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – (231-1) N/A Read/Write Yes
Description:
Contains the IP address. Each byte represents one octet of the IP address.
Example: C0 A8 64 01 = 192.168.100.1
2006.02h Subnet Mask
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – (231-1) N/A Read/Write Yes
Description:
Contains the Subnet Mask. Each byte represents one octet of the subnet mask.
Example: FF FF FF 00 = 255.255.255.0
2006.03h Default Gateway
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – (231-1) N/A Read/Write Yes
Description:
Contains the default gateway. Each byte represents one octet of the gateway.
Example: C0 A8 64 64 = 192.168.100.100
1600.00h Number of objects in this PDO
Data Type Data Range Units Accessibility Stored to NVM
Unsigned8 0 - 16 N/A Read / Write No
Description:
Holds the number of RPDO mappings.

---
## Page 46

MNCMECRF-07 36
Object Dictionary / Communication Settings
1600.01h PDO Mapping for the 1st Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 1st offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.02h PDO Mapping for the 2nd Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 2nd offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.03h PDO Mapping for the 3rd Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 3rd offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.04h PDO Mapping for the 4th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 4th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.05h PDO Mapping for the 5th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 5th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.06h PDO Mapping for the 6th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 6th offset of RPDO1. A value of zero means no object is mapped to this offset.

---
## Page 47

MNCMECRF-07 37
Object Dictionary / Communication Settings
1600.07h PDO Mapping for the 7th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 7th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.08h PDO Mapping for the 8th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 8th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.09h PDO Mapping for the 9th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 9th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.0Ah PDO Mapping for the 10th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 10th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.0Bh PDO Mapping for the 11th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 11th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.0Ch PDO Mapping for the 12th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 12th offset of RPDO1. A value of zero means no object is mapped to this offset.

---
## Page 48

MNCMECRF-07 38
Object Dictionary / Communication Settings
1A00h: Transmit PDO Mapping    Holds the TPDO mappings.
1600.0Dh PDO Mapping for the 13th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 13th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.0Eh PDO Mapping for the 14th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 14th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.0Fh PDO Mapping for the 15th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 15th offset of RPDO1. A value of zero means no object is mapped to this offset.
1600.10h PDO Mapping for the 16th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read/Write Yes
Description:
Holds the COB-ID of the object mapped to the 16th offset of RPDO1. A value of zero means no object is mapped to this offset.
1A00.00h Number of objects in this PDO
Data Type Data Range Units Accessibility Stored to NVM
Unsigned8 0 - 16 N/A Read / Write Yes
Description:
Holds the number of TPDO mappings.

---
## Page 49

MNCMECRF-07 39
Object Dictionary / Communication Settings
1A00.01h PDO Mapping for the 1st Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 1st offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.02h PDO Mapping for the 2nd Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 2nd offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.03h PDO Mapping for the 3rd Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 3rd offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.04h PDO Mapping for the 4th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 4th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.05h PDO Mapping for the 5th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 5th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.06h PDO Mapping for the 6th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 6th offset of TPDO1. A value of zero means no object is mapped to this offset.

---
## Page 50

MNCMECRF-07 40
Object Dictionary / Communication Settings
1A00.07h PDO Mapping for the 7th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 7th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.08h PDO Mapping for the 8th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 8th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.09h PDO Mapping for the 9th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 9th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.0Ah PDO Mapping for the 10th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 10th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.0Bh PDO Mapping for the 11th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 11th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.0Ch PDO Mapping for the 12th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 12th offset of TPDO1. A value of zero means no object is mapped to this offset.

---
## Page 51

MNCMECRF-07 41
Object Dictionary / Drive Configuration
2.4 Drive Configuration
2.4.1 Motion Control Profile
20D0h: Control Loop Configuration Parameters   
1A00.0Dh PDO Mapping for the 13th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 13th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.0Eh PDO Mapping for the 14th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 14th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.0Fh PDO Mapping for the 15th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 15th offset of TPDO1. A value of zero means no object is mapped to this offset.
1A00.10h PDO Mapping for the 16th Application Object
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - 232 N/A Read / Write Yes
Description:
Holds the COB-ID of the object mapped to the 16th offset of TPDO1. A value of zero means no object is mapped to this offset.
20D0.01h Control Loop Configuration
Data Type Data Range Units Accessibility Stored to NVM
N/A N/A N/A Read / Write Yes
Description:
Control loop configuration. Drive setup and configuration software will determine the values in this parameter. For systems that do not load 
parameter values from non-volatile memory but rather download parameters to the drive upon each system initialization, this parameter 
should be read from the drive upon completion of setup and configuration and saved with all other relevant drive parameters.

---
## Page 52

MNCMECRF-07 42
Object Dictionary / Drive Configuration
2032h: Feedback Sensor Parameters   
2032.01h Encoder Wiring Polarity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the encoder wiring polarity.
2032.02h Maximum Phase Detection Current
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] DC2 Read / Write Yes
Description:
Contains a value corresponding to the maximum phase detection current that is allowed during a phase detect. See “Appendix” on page 225 
for units conversion.
2032.03h Phase Detect Settling Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(31) –1] N/A Read / Write Yes
Description:
Contains the delay after a phase detect, before the commutation angle value is assigned. This delay should be set greater than the time it 
takes for the load to settle after phase detection. The value to be written to the drive is calculated as follows:
(desired phase detect settling time in milliseconds) x f
where f = the switching frequency of the drive in kHz.
Examples:
For a drive with a switching frequency of 20 kHz, to achieve a phase detect settling time of 500ms, the value written to the drive is:
500 x 20 = 10000
For a drive with a switching frequency of 14 kHz, to achieve a phase detect settling time of 500ms, the value written to the drive is:
500 x 14 = 7000 
2032.04h Maximum Phase Detection Brake Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – [2(32) –1] milliseconds (ms) Read / Write Yes
Description:
Contains a value corresponding to the maximum phase detection brake time.

---
## Page 53

MNCMECRF-07 43
Object Dictionary / Drive Configuration
2032.05h Maximum Phase Detection Motion
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] DG1 Read / Write Yes
Description:
Contains a value corresponding to the maximum phase detection motion that is allowed during a phase detect. See “Appendix” on page 225 
for unit conversion details.
2032.06h Resolver Resolution
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 1 N/A Read / Write Yes
Description:
Contains a value corresponding to the resolver resolution.
2032.07h Serial Encoder Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the serial encoder type:
Value Resolver Resolution*
0 Low  (12 bit = 4096 counts/resolver cycle standard)
1 High (14 bit = 16384 counts/resolver cycle standard)
*Refer to the drive datasheet for the specific resolution values supported by the drive.
Value Serial Encoder Type
0 Not Assigned
1 Hiperface
2 EnDat 2.1
3 BiSS
4 EnDat 2.2

---
## Page 54

MNCMECRF-07 44
Object Dictionary / Drive Configuration
2032.08h Position Interpolation / Velocity Divider
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
For Sin/Cos encoder interpolation, contains a value corresponding to the position interpolation. The number of position counts per Sin/Cos 
cycle is equal to 4 multiplied by the interpolation value. This only applies to position. The measured velocity is unaffected by the interpolation.
For digital encoder feedback (BiSS, EnDat 2.2) contains a value corresponding to the Velocity Divider parameter. The Velocity Divider is 
used to scale down the feedback going to the velocity gains when very high resolution encoders are used. This prevents saturation of the 
velocity loop. For incremental encoder feedback, the Interpolation Value is 1.
2032.09h Encoder Steps Per Encoder Sine Period
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the encoder steps per encoder sine period.
2032.0Ah Secondary Encoder Position Interpolation
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the secondary encoder position interpolation.
Sin/Cos Encoder Digital Encoder
Value Interpolation Velocity Divider
0 1x 1
1 2x 2
2 4x 4
3 8x 8
4 16x 16
5 32x 32
6 64x 64
7 128x 128
8 256x 256
9 512x 512

---
## Page 55

MNCMECRF-07 45
Object Dictionary / Drive Configuration
2032.0Bh Low Speed Smoothing Constant
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the low speed smoothing constant.
2032.0Ch Encoder Emulation Divide By
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 1-20h N/A Read / Write Yes
Description:
Contains a value corresponding to the emulated encoder divide by amount. The drive will output an emulated encoder frequency equal to the 
drive’s interpreted encoder frequency divided by the divide amount. Allowable values are 1,2,4,8,16 and 32.
2032.0Dh Sin/Cos Error Window
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0000h – 4000h N/A (SF1) Read / Write Yes
Description:
Contains a value corresponding to the Sin/Cos error window for drives that support a 1V peak-to-peak encoder. The valid range in physical 
units is 0 to 1. The window determines whether or not a feedback sensor error should be activated according to the health of a Sin/Cos 
encoder (see object 2027.03h). If x is the error window entered in this object, then an error is activated when the health of the encoder is not 
within the range 1±x. See “Appendix” on page 225 for information on scaling.
2032.0Eh Emulation Output Mode
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0-1 N/A Read / Write Yes
Description:
This applies only to drives that support sin/cos encoder or absolute encoder feedback. Specifies whether the output encoder signal is 
buffered (0) or emulated (1).
2032.0Fh Position of Emulated Index
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(32)] – [2(31)-1] counts Read / Write Yes
Description:
This applies only to drives that support sin/cos encoder or absolute encoder feedback. Specifies the position of the emulated index in drive 
counts.

---
## Page 56

MNCMECRF-07 46
Object Dictionary / Drive Configuration
2032.10h Emulated Counts per Emulated Index
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read / Write Yes
Description:
This applies only to drive that support sin/cos encoder or absolute encoder feedback. Specifies the number of emulated counts per emulated 
index.
2032.11h Digital Absolute Only - Resolution Configuration Bitfield
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read / Write Yes
Description:
Contains the absolute encoder resolution. This parameter is used with BiSS encoders. The bits are separated into resolution per turn and 
resolution (turns).
2032.12h Digital Absolute Only - Data Format Configuration Bitfield
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read / Write Yes
Description:
Contains information about the data format used. This parameter is used with BiSS encoders. The bits are separated into data width and 
justification for single turn data and multi turn data.
Bit Description
0...7 Number of bits per turn. A value of decimal 16 represents 
216 counts per turn.
8...15 Number of bits whole turns. A value of decimal 16 
represents 216 turns.
Bit Description
0...6 Single turn data width. A value of decimal 16 represents 16 
bits.
7 1 when bits/turn data is left justified, and 0 when bits/turn 
data is right justified.
8...14 Multi turn data width. A value of decimal 16 represents 16 
bits.
15 1 when turns data is left justified, and 0 when turns data is 
right justified.

---
## Page 57

MNCMECRF-07 47
Object Dictionary / Drive Configuration
2046h: Auxiliary Input Parameters   
2034h: Current Loop & Commutation Control Parameters   
2046.01h Auxiliary Input - Input Counts: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 1 - [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the number of input counts in the input/output ratio used for Encoder following and Step and Direction 
modes in Configuration 0. 
2046.02h Auxiliary Input - Output Counts: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 -[2(16) –1] - [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the output in the input/output ratio used for Encoder following and Step and Direction modes in 
Configuration 0. Encoder following mode can be used only when the position loop is closed. However, Step and Direction can be used to 
control position, velocity or current. Therefore, the scaling value used is mode dependent. 
2046.03h Auxiliary Input - Input Counts: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 1 - [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the number of input counts in the input/output ratio used for Encoder following and Step and Direction 
modes in Configuration 1. 
2046.04h Auxiliary Input - Output Counts: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 -[2(16) –1] - [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the output in the input/output ratio used for Encoder following and Step and Direction modes in 
Configuration 1. Encoder following mode can be used only when the position loop is closed. However, Step and Direction can be used to 
control position, velocity or current. Therefore, the scaling value used is mode dependent. 
2034.01h Torque Current Loop Proportional Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] N/A Read / Write Yes
Description:
Contains the value of proportional gain for the current loop. This value is calculated from the gain value as follows: 
 Gain 29 Value to the drive=

---
## Page 58

MNCMECRF-07 48
Object Dictionary / Drive Configuration
2034.02h Torque Current Loop Integral Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] N/A Read / Write Yes
Description:
Contains the value of integral gain for the current loop. This value is calculated from the gain value as follows: 
2034.03h Torque Current Target Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read / Write Yes
Description:
Contains a value corresponding to the torque current target offset 
2034.04h Peak Current Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] DC1 Read / Write Yes
Description:
Contains a value corresponding to the peak current limit set in the drive. See “Appendix” on page 225 for unit conversion.
2034.05h Peak Current Hold Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
Contains a value corresponding to the peak current time set in the drive.
2034.06h Continuous Current Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] DC1 Read / Write Yes
Description:
Contains a value corresponding to the continuous current limit set in the drive. See “Appendix” on page 225 for unit conversion.
2034.07h Peak to Continuous Current Transition Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
Contains a value corresponding to the peak to continuous current transition time set in the drive.
Gain 29 Value to the drive=

---
## Page 59

MNCMECRF-07 49
Object Dictionary / Drive Configuration
2034.08h Flux Current Reference Loop Proportional Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the flex current reference loop proportional gain. The flux current loop is only used for AC induction 
motors. This value can be calculated from the gain value as follows:
(Flux Current Reference Loop Proportional Gain) x 10000h, where ( 0  Gain  32767 )
2034.09h Flux Current Reference Loop Integral Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the flex current reference loop integral gain. The flux current loop is only used for AC induction motors. 
This value can be calculated from the gain value as follows:
(Flux Current Reference Loop Integral Gain) x 400000h, where ( 0  Gain  512 )
2034.0Ah Rated Peak Line Current
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the rated peak line current allowed when using an AC induction motor.
2034.0Bh No Load Peak Magnetization Current
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the no-load peak magnetization current allowed when using an AC induction motor.
2034.0Ch Rated Frequency
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the rated frequency.

---
## Page 60

MNCMECRF-07 50
Object Dictionary / Drive Configuration
2034.0Dh Rated Rotor No Load Base Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] RPM Read / Write Yes
Description:
Contains a value corresponding to the rated rotor no-load base speed. This parameter is only used with an AC induction motor.
2034.0Eh FW Threshold Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the field weakening threshold speed. This parameter is used for AC induction motors only.
2034.0Fh Motor Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 - N/A Read / Write Yes
Description:
Contains a value corresponding to the type of motor connected to the drive.
2034.10h Auxiliary Commutation Mode
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 - N/A Read / Write Yes
Description:
Contains a value corresponding to the auxiliary commutation mode. Auxiliary commutation only occurs if the drive is connected to a brushed 
motor. Brushed motors commutate the motor internally and therefore do not require the drive to commutate the motor. The drive supplies 
current over two phases. This remains fixed for a brushed drive.
2034.11h Encoder Direction
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 3 N/A Read / Write Yes
Description:
Contains a value corresponding to the direction of the encoder feedback.
Data Value Rotation Direction Primary Feedback Polarity
0 Inverted Inverted
1 Inverted Standard
2 Standard Inverted
3 Standard Standard

---
## Page 61

MNCMECRF-07 51
Object Dictionary / Drive Configuration
2034.12h Synchronization Mode
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 - N/A Read / Write Yes
Description:
Contains a value corresponding to the current commutation method.
2034.13h Encoder Counts Per Electrical Cycle
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] counts Read / Write Yes
Description:
Contains the number of encoder counts per electrical cycle.
2034.14h NTHS Angle 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the NTHS angle 1.
2034.15h NTHS Angle 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the NTHS angle 2.
2034.16h NTIS Angle 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the NTIS angle 1.
2034.17h NTIS Angle 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the NTIS angle 2.

---
## Page 62

MNCMECRF-07 52
Object Dictionary / Drive Configuration
2034.18h NTA-EZ Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the NTA-EZ position.
2034.19h Max SPA Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the max SPA error.
2034.1Ah Max SPA Adjustment
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the max SPA adjustment.
2034.1Bh EC Adjust Count
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the EC adjust count.
2034.1Ch ECC Adjust Amount
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the ECC adjust amount.
2034.1Dh Valid HS Mask
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the valid HS mask.

---
## Page 63

MNCMECRF-07 53
Object Dictionary / Drive Configuration
2034.1Eh Hall Parameter 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 1.
2034.1Fh Hall Parameter 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 2.
2034.20h Hall Parameter 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 3.
2034.21h Hall Parameter 4
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 4.
2034.22h Hall Parameter 5
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 5.
2034.23h Hall Parameter 6
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 6.

---
## Page 64

MNCMECRF-07 54
Object Dictionary / Drive Configuration
2034.24h Hall Parameter 7
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 7.
2034.25h Hall Parameter 8
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to Hall Parameter 8.
2034.26h Phase Detect Control
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the Phase Detect Control options:
2034.27h Phase Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DG1 Read / Write Yes
Description:
Contains a value corresponding to the Phase Advance feature.
2034.28h Current Limiting Algorithm
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0-2 N/A Read / Write Yes
Description:
This enum selects from one of three current limiting algorithms. See “Appendix B - Current Limiting Algorithm” on page 228 for more details.
Data Value Description
0 Normal Phase Detect Operation
1 Ignore User Positive Limit Event
2 Ignore User Negative Limit Event
3 Ignore both User Positive and Negative Limit Events
Data Value Description
0 Time Based (Default)
1 Charge Based with RMS Scaling
2 Charge Based

---
## Page 65

MNCMECRF-07 55
Object Dictionary / Drive Configuration
2036h: Velocity Loop Control Parameters   
2034.29h Torque At Command Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31) –1] DC2 Read / Write Yes
Description:
Contains a value for an At Command window around the current error. While in current mode, when the current error is within this window, 
the At Command event will be active.
2036.01h Velocity Feedback Direction
Data Type Data Range Units Accessibility Stored to NVM
Integer16 - N/A Read / Write Yes
Description:
Contains a value corresponding to the feedback polarity of an auxiliary encoder used for velocity feedback.
2036.02h Velocity Feedback Filter Coefficient
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(30)] N/A Read / Write Yes
Description:
Contains a value that corresponds to the velocity feedback filter coefficient. To convert between the value entered into DriveWare and the 
value sent to the drive, use the following functions:
DriveWare to drive:
where a = [value entered into DriveWare] x (-6.283185307x10-4) and P = [value sent to drive]
Drive to DriveWare:
where P = [value in drive]
230 e– a 1 +  P=
1 P
230- - - - - - -– 
 ln
6.283185307– 10 4–
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - [value seen in DriveWare (Hz)]=

---
## Page 66

MNCMECRF-07 56
Object Dictionary / Drive Configuration
2036.03h Velocity Loop Proportional Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the proportional loop gain of the velocity loop for Gain Set 0. This value can be calculated from the gain 
value as follows:
(Velocity Loop Proportional Gain) x ((216 * Vvel * Rppv) / (2 * Cpk)), where:
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current
2036.04h Velocity Loop Integral Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the integral loop gain of the velocity loop for Gain Set 0. This value can be calculated from the gain 
value as follows:
(Velocity Loop Integral Gain) x (232 * Rppv) / (2 * Cpk), where
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current
2036.05h Velocity Loop Derivative Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the derivative loop gain of the velocity loop for Gain Set 0. This value can be calculated from the gain 
value as follows:
(Velocity Loop Derivative Gain) x ((216 * (Vvel)2 * Rppv) / (2 * Cpk)), where
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current

---
## Page 67

MNCMECRF-07 57
Object Dictionary / Drive Configuration
2036.06h Velocity Loop Acceleration Feed Forward Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the velocity loop acceleration feed forward gain for Gain Set 0. This value can be calculated from the 
gain value as follows:
(Velocity Loop Acceleration Feed Forward Gain) x ((216 * (Vvel)2 * Rppv) / (2 * Cpk)), where
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current
2036.07h Velocity Loop Integrator Decay Rate
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to a percentage of the velocity loop integrator decay rate. The value can be calculated from the velocity 
loop integrator decay rate as follows:
(% of Integrator Gain) * (216 / 100 )
2036.08h Velocity Loop Proportional Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the proportional loop gain of the velocity loop for Gain Set 1. This value can be calculated from the gain 
value as follows:
(Velocity Loop Proportional Gain) x ((216 * Vvel * Rppv) / (2 * Cpk)), where:
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current

---
## Page 68

MNCMECRF-07 58
Object Dictionary / Drive Configuration
2036.09h Velocity Loop Integral Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the integral loop gain of the velocity loop for Gain Set 1. This value can be calculated from the gain 
value as follows:
(Velocity Loop Integral Gain) x (232 * Rppv) / (2 * Cpk), where
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current
2036.0Ah Velocity Loop Derivative Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the derivative loop gain of the velocity loop for Gain Set 1. This value can be calculated from the gain 
value as follows:
(Velocity Loop Derivative Gain) x ((216 * (Vvel)2 * Rppv) / (2 * Cpk)), where
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current
2036.0Bh Velocity Loop Acceleration Feed Forward Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the velocity loop acceleration feed forward gain for Gain Set 1. This value can be calculated from the 
gain value as follows:
(Velocity Loop Acceleration Feed Forward Gain) x ((216 * (Vvel)2 * Rppv) / (2 * Cpk)), where
Vvel = (Switching Frequency / 2)
Rppv = Interpolation Value (see object 2032.08h for a reference table to locate the actual interpolation value using the stored enum)
Cpk = Peak Current

---
## Page 69

MNCMECRF-07 59
Object Dictionary / Drive Configuration
2037h: Velocity Limits   
2037.01h Motor Over Speed Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] DS1 Read / Write Yes
Description:
Contains a value corresponding to the motor over speed limit set in the drive. When the velocity of the motor meets or exceeds this value, 
the drive will indicate a motor over speed condition is present. See “Appendix” on page 225 for unit conversion.
2037.02h Zero Speed Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] DS1 Read / Write Yes
Description:
Contains a value corresponding to the motor zero speed limit set in the drive. When the velocity of the motor reaches this value or LOWER, 
the drive will indicate that it has reached a zero speed condition. See “Appendix” on page 225 for unit conversion.
2037.03h At Velocity Window
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – [2(31)-1] DS4 Read / Write Yes
Description:
Contains a value for an At Velocity tolerance window around the target velocity. The At Velocity Window functions like a tolerance value for 
the velocity error. When the velocity error is within this window either above or below the target velocity, the drive will indicate that it is At 
Command. See “Appendix” on page 225 for unit conversion.
2037.04h Velocity Loop Following Error Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – [2(31)-1] DS1 Read / Write Yes
Description:
Contains a value corresponding to the velocity at speed limit set in the drive. If the measured velocity meets or exceeds this value, the drive 
will perceive this as a velocity following error. See “Appendix” on page 225 for unit conversion.
2037.05h Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] DS1 Read / Write Yes
Description:
Contains a value corresponding to the positive velocity limit set in the drive. When the speed set by this value is met or exceeded, the drive 
will indicate that the positive limit was reached. See “Appendix” on page 225 for unit conversion.

---
## Page 70

MNCMECRF-07 60
Object Dictionary / Drive Configuration
2038h: Position Loop Control Parameters   
2037.06h Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] DS1 Read / Write Yes
Description:
Contains a value corresponding to the negative velocity limit set in the drive. When the speed set by this value is met or exceeded, the drive 
will indicate that the negative limit was reached. See “Appendix” on page 225 for unit conversion.
2037.07h Velocity Loop Integrator Decay Active Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value that corresponds to the velocity loop integrator decay active window.
2038.01h Position Loop Proportional Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop proportional gain for Gain Set 0. This value can be calculated from the gain value using 
the following formula:
(Position Loop Proportional Gain) x 232, where
2038.02h Position Loop Integral Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop integral gain for Gain Set 0. This value can be calculated from the gain value using the 
following formula:
(Position Loop Integral Gain) x (241 / Vpos), where
Vpos = (Switching Frequency / 2)

---
## Page 71

MNCMECRF-07 61
Object Dictionary / Drive Configuration
2038.03h Position Loop Derivative Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop derivative gain for Gain Set 0. This value can be calculated from the gain value using the 
following formula:
(Position Loop Derivative Gain) x (228 * Vpos), where
Vpos = (Switching Frequency / 2)
2038.04h Position Loop Velocity Feed Forward Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop velocity feed forward gain for Gain Set 0. This value can be calculated from the gain 
value using the following formula:
(Position Loop Velocity Feed Forward Gain) x (228 * Vpos), where
Vpos = (Switching Frequency / 2)
2038.05h Position Loop Acceleration Feed Forward Gain: Gain Set 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop acceleration feed forward gain for Gain Set 0. This value can be calculated from the gain 
value using the following formula:
(Position Loop Acceleration Feed Forward Gain) x (228 * (Vpos)2), where
Vpos = (Switching Frequency / 2)
2038.06h Position Feedback Direction
Data Type Data Range Units Accessibility Stored to NVM
Integer16 - N/A Read / Write Yes
Description:
Contains a value corresponding to the feedback polarity of an auxiliary encoder used for position feedback.

---
## Page 72

MNCMECRF-07 62
Object Dictionary / Drive Configuration
2038.07h Position Loop Integrator Decay Rate
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] % Read / Write Yes
Description:
Contains a value that corresponds to the position loop integrator decay rate. The value is in percentage of the position loop Integrator Gain.
2038.08h Position Loop Proportional Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop proportional gain for Gain Set 1. This value can be calculated from the gain value using 
the following formula:
(Position Loop Proportional Gain) x 232, where
2038.09h Position Loop Integral Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop integral gain for Gain Set 1. This value can be calculated from the gain value using the 
following formula:
(Position Loop Integral Gain) x (241 / Vpos), where
Vpos = (Switching Frequency / 2)
2038.0Ah Position Loop Derivative Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop derivative gain for Gain Set 1. This value can be calculated from the gain value using the 
following formula:
(Position Loop Derivative Gain) x (228 * Vpos), where
Vpos = (Switching Frequency / 2)

---
## Page 73

MNCMECRF-07 63
Object Dictionary / Drive Configuration
2039h: Position Limits   
2038.0Bh Position Loop Velocity Feed Forward Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop velocity feed forward gain for Gain Set 1. This value can be calculated from the gain 
value using the following formula:
(Position Loop Velocity Feed Forward Gain) x (228 * Vpos), where
Vpos = (Switching Frequency / 2)
2038.0Ch Position Loop Acceleration Feed Forward Gain: Gain Set 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] N/A Read / Write Yes
Description:
Contains a value corresponding to the position loop acceleration feed forward gain for Gain Set 1. This value can be calculated from the gain 
value using the following formula:
(Position Loop Acceleration Feed Forward Gain) x (228 * (Vpos)2), where
Vpos = (Switching Frequency / 2)
2039.01h Measured Position Value 
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Replacement value for the measured position when the Set Position event is triggered. This allows you to redefine the current measured 
position (e.g. reset to zero).
2039.02h Home Position Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Position value of the home position. When the measured position reaches this position, within the In-Home Position Window, the At-Home 
event becomes active.

---
## Page 74

MNCMECRF-07 64
Object Dictionary / Drive Configuration
2039.03h Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Maximum allowed measured position. The Max Measured Position event will become active if the measured position exceeds this value.
2039.04h Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Minimum allowed measured position. The Min Measured Position event will become active if the measured position exceeds this value.
2039.05h At Home Position Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Defines a window around the Home Position Value, such that when the measured position is within this window, the At-Home event will be 
active.
2039.06h In Position Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] counts Read / Write Yes
Description:
Defines a window around the target position, such that when the position error is within this window, the At Command event will be active.
2039.07h Position Following Error Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] counts Read / Write Yes
Description:
The maximum allowed position error (difference between target position and measured position), prior to setting the “Position Following 
Error” event (active in position mode only). This parameter is equivalent to the “Position Following Error Limit” of DSP402 (object 6065h).
2039.08h Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Maximum allowed target position. The Max Target Position event will become active if the target position exceeds this value.

---
## Page 75

MNCMECRF-07 65
Object Dictionary / Drive Configuration
6065h: Position Following Error Window   
6066h: Position Following Error Time Out   
2039.09h Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] counts Read / Write Yes
Description:
Minimum allowed target position. The Min Target Position event will become active if the target position exceeds this value.
2039.0Ah Position Limits Control
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 - N/A Read / Write Yes
Description:
Defines if the position limits are enabled or not. 3 = Enable Limits, 0 = Disable Limits.
2039.0Bh Position Loop Integrator Decay Active Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] counts Read / Write Yes
Description:
Contains a value that corresponds to the position loop integrator decay active window.
6065h Position Following Error Window
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] counts Read / Write Yes
Description:
The maximum allowed position error (difference between target and measured position), prior to setting the “Position Following Error” event 
(active in position mode only).
6066h Position Following Error Time Out
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 2 - [2(15)-1] ms Read / Write Yes
Description:
The time delay after the occurrence of Position Following Error before its Event Action (2065h) is executed. The functionality of this object is 
identical to that of the manufacturer-specific object 2064.16h.

---
## Page 76

MNCMECRF-07 66
Object Dictionary / Drive Configuration
60F4h: Position Following Error Actual Value   
6098h: Homing Method   
6099h: Homing Speeds   
609Ah: Homing Acceleration   
60F4h Position Following Error Actual Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-232] - [2(32) –1] counts Read Only Yes
Description:
Provides the actual value of the position following error, defined as the difference between target and measured position.
6098h Homing Method
Data Type Data Range Units Accessibility Stored to NVM
Integer8 1 – 35 N/A Read / Write Yes
Description:
There are almost 35 homing methods supported by AMC servo drives. See “Homing” on page 15 for details on each homing method.
6099.01h Speed During Search For Switch
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – (232-1) DS4 Read / Write Yes
Description:
Sets the speed during the first stage of Homing algorithms. See “Appendix” on page 225 for unit conversion.
6099.02h Speed During Search For Zero
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – (232-1) DS4 Read / Write Yes
Description:
Sets the speed during the search for zero. This is usually after the search for switch has completed and is set much slower for accuracy. See 
“Appendix” on page 225 for unit conversion.
609Ah Homing Acceleration
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 – (232-1) DA1 Read / Write Yes
Description:
Sets the accelerations and decelerations used by the drive’s homing routine. See “Appendix” on page 225 for unit conversion details.

---
## Page 77

MNCMECRF-07 67
Object Dictionary / Drive Configuration
607Ch: Home Offset   
6086h: Motion Profile Type   
6088h: Torque Profile Type   
203Ch: Command Limiter Parameters   The Command Limiter limits the slope of the 
target command in any mode. It is broken into four components, where each component is 
assigned to one sub-index. To remove any effects of the command limiter, maximize all limiter 
parameters. Some limiter parameters have units that change with the operating mode of the 
drive. For these parameters, refer to Table 2.1 to make the correct unit selection.
607Ch Home Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) counts Read / Write Yes
Description:
When the homing routine is complete, the zero position found by the drive is given an offset equal to the value stored in this object. All moves 
are interpreted relative to this new zero position. When homing completes, the equation for the drive’s current position is “Current position = 
0 – Home Offset value”.
6086.00h Motion Profile Type
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 2 N/A Read / Write No
Description:
Specifies the type of profile to be used for profiled position mode (see object 6060 for setting modes). The default profile type is linear 
(trapezoidal), but accel/decel may be selected. This value is not stored to NVM. Specific values for either profile can be configured using 
object 203C.
6088.00h Torque Profile Type
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 N/A Read Only No
Description:
Specifies the type of profile to be used for profiled torque mode (see object 6060 for setting modes). The value is fixed equal to 0 which 
specifies a linear (trapezoidal) profile.
Value Input Method
0 (default) Linear Ramp (trapezoidal profile)
2 Accel/Decel (jerk-free ramp)

---
## Page 78

MNCMECRF-07 68
Object Dictionary / Drive Configuration
TABLE 2.1 Command Limiter Units
Drive Operation Mode Units
Current (Torque) DJ1
Velocity DA2
Position (Around Velocity Or Current) DS2
203C.01h Linear Ramp Positive Target Positive Change: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum positive change in positive command used with the command limiter in Configuration 0. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.02h Linear Ramp Positive Target Negative Change: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum negative change in positive command used with the command limiter in Configuration 0. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.03h Linear Ramp Negative Target Negative Change: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum negative change in negative command used with the command limiter in Configuration 0. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.04h Linear Ramp Negative Target Positive Change: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum positive change in negative command used with the command limiter in Configuration 0. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.

---
## Page 79

MNCMECRF-07 69
Object Dictionary / Drive Configuration
203C.05h Linear Ramp Positive Target Positive Change: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum positive change in positive command used with the command limiter in Configuration 1. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.06h Linear Ramp Positive Target Negative Change: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum negative change in positive command used with the command limiter in Configuration 1. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.07h Linear Ramp Negative Target Negative Change: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum negative change in negative command used with the command limiter in Configuration 1. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.08h Linear Ramp Negative Target Positive Change: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 - [2(48) –1] See Table 2.1 Read / Write Yes
Description:
Defines the maximum positive change in negative command used with the command limiter in Configuration 1. Units are mode dependant. 
See “Appendix” on page 225 for unit conversions.
203C.09h Controlled Accel/Decel Maximum Speed: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer64 0 - [2(64) –1] DS3 Read / Write Yes
Description:
Sets the maximum speed for a profile in Configuration 0. See “Appendix” on page 225 for unit conversions.

---
## Page 80

MNCMECRF-07 70
Object Dictionary / Drive Configuration
60C2h: Interpolation Time Period   This object is used only for synchronous cyclic modes of 
operation (see “6060h: Modes Of Operation” on page 184). The interpolation time period 
defines the rate in which target commands are sent by the host to the drive. When a periodic 
target command is sent to the drive at a rate slower than the loop update rate, there is 
potential for the loop gains to spike with each new target command. Defining the interpolation 
time period allows the target to follow a linear ramp between target commands. The 
interpolation time period is made up of two values as follows:
203C.0Ah Controlled Accel/Decel Maximum Acceleration: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] DA3 Read / Write Yes
Description:
Defines the maximum acceleration used with the command limiter in Configuration 0. See “Appendix” on page 225 for unit conversions.
203C.0Bh Controlled Accel/Decel Maximum Deceleration: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] DA3 Read / Write Yes
Description:
Defines the maximum deceleration used with the command limiter in Configuration 0. See “Appendix” on page 225 for unit conversions.
203C.0Ch Controlled Accel/Decel Maximum Speed: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer64 0 - [2(64) –1] DS3 Read / Write Yes
Description:
Sets the maximum speed for a profile in Configuration 1. See “Appendix” on page 225 for unit conversions.
203C.0Dh Controlled Accel/Decel Maximum Acceleration: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] DA3 Read / Write Yes
Description:
Defines the maximum acceleration used with the command limiter in Configuration 1. See “Appendix” on page 225 for unit conversions.
203C.0Eh Controlled Accel/Decel Maximum Deceleration: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] DA3 Read / Write Yes
Description:
Defines the maximum deceleration used with the command limiter in Configuration 1. See “Appendix” on page 225 for unit conversions.

---
## Page 81

MNCMECRF-07 71
Object Dictionary / Drive Configuration
Interpolation Time Period = [interpolation time period value] x 10(interpolation time index) 
seconds
The drive will support an interpolation time period between 0 and 1 second. If the value is not 
a multiple of the loop update rate, it will be truncated to the next lowest multiple.
2.4.2 Hardware Profile
200Bh: Stored User Parameters   
2008h: Drive Initialization Parameters   
60C2.01h Interpolation Time Period Value
Data Type Data Range Units Accessibility Stored to NVM
Unsigned 8 0 - 255 N/A Read / Write Yes
Description:
Defines the mantissa of the interpolation time period.
60C2.02h Interpolation Time Index
Data Type Data Range Units Accessibility Stored to NVM
Integer 8 -6 to 0 N/A Read / Write Yes
Description:
Defines the exponent of the interpolation time period.
200B.01h User Defined Drive Name
Data Type Data Range Units Accessibility Stored to NVM
String256 ASCII Values N/A Read / Write Yes
Description:
Contains a user specified drive name for the drive. The characters in the string are stored as ASCII values. For the drive name “AMC”, the 
digits stored are: 41h, 4Dh, 43h 
2008.01h Start-Up Sequence Control
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Defines how the drive will behave when power is first applied.
Bit Drive Initialization Parameters
0 Disable Bridge
1 Load Config 1
2 Phase Detect
3 Set Position
4 Enable Motion Engine After Startup Sequence
5...15 Reserved

---
## Page 82

MNCMECRF-07 72
Object Dictionary / Drive Configuration
20C8h: Motion Engine Configuration   
2033h: User Voltage Protection Parameters   
2008.02h Start-Up Phase Detect Configuration
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read / Write Yes
Description:
Defines how the Phase Detect feature will behave when power is first applied.
20C8.01h Start-Up Motion Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 1FFFh N/A Read / Write Yes
Description:
Defines the startup behavior when running a motion engine index upon power-up. The bit values are broken up as defined below.
Bits 0:2
0: Indexer Mode
1-7: Reserved
Bits 3:4
0: Motion initiated via digital inputs
1: Motion initiated via Network commands
Bits 5:8
Defines the index number to load on power-up
Bits 9:15
0: Motion will not immediately start.
1: Motion will automatically start if the Motion Engine is configured to be enabled on power-up.
2-7: Reserved
2033.01h Over-Voltage Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DV1 Read / Write Yes
Description:
Contains the over voltage limit specified for the drive. It must be set lower than the drive over-voltage hardware shutdown point and greater 
than the Nominal DC Bus Voltage. See “Appendix” on page 225 for unit conversion.
Value Description
0 Phase Detect Immediately upon power-up
1 Phase Detect after the first bridge enable upon power-up

---
## Page 83

MNCMECRF-07 73
Object Dictionary / Drive Configuration
2033.02h Under-Voltage Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DV1 Read / Write Yes
Description:
Contains the under voltage limit specified for the drive. It must be set above the drive under-voltage hardware shutdown point and less than 
the Nominal DC Bus Voltage. See “Appendix” on page 225 for unit conversion.
2033.03h Shunt Regulator Enable Threshold
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] DV1 Read / Write Yes
Description:
Contains a value corresponding to the shunt regulator enable threshold voltage. When the bus reaches this voltage, built in shut regulator 
will turn on allow excess energy to be dissipated across an external shunt resistor. Not all drives have built in shunt regulators. See 
“Appendix” on page 225 for unit conversion.
2033.04h Shunt Regulator Configuration
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 See Table N/A Read / Write Yes
Description:
Contains a value corresponding to the current state of the shunt regulator.
2033.05h External Shunt Resistance
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] ohms (Ω) Read / Write Yes
Description:
Contains a value corresponding to the resistance of the external shunt resistor.
2033.06h External Shunt Power
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] watts (W) Read / Write Yes
Description:
Contains a value corresponding to the amount of power the external shunt resistor is allowed to dissipate.
Value (Hex) Description
00 Disable Shunt Regulator
02 Enable Shunt Regulator

---
## Page 84

MNCMECRF-07 74
Object Dictionary / Drive Configuration
2054h: Drive Temperature Parameters   
2033.07h External Shunt Inductance
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] microhenrys (μH) Read / Write Yes
Description:
Contains a value corresponding to the inductance of the external shunt resistor.
2054.01h External Analog Temperature Disable Level
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] DT1 Read / Write Yes
Description:
Contains a value corresponding to the temperature disable level for an analog over temperature event. See “Appendix” on page 225 for unit 
conversion.
2054.02h External Analog Temperature Enable Level
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] DT1 Read / Write Yes
Description:
Contains a value corresponding to the temperature re-enable level after the analog over temperature event has been activated. See 
“Appendix” on page 225 for unit conversion.
2054.03h Thermistor Disable Resistance
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] Ohms Read / Write Yes
Description:
If supported by the hardware, this value represents the value of the thermistor resistance (ohms) in which the Motor Over Temperature Event 
is to trip. For a Positive Thermal Coefficient (PTC), the disable resistance will be greater than or equal to the enable value. For a Negative 
Thermal Coefficient (NTC), the disable resistance will be less than the enable value.
2054.04h Thermistor Enable Resistance
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] Ohms Read / Write Yes
Description:
If supported by the hardware, this value represents the value of the thermistor resistance (ohms) in which the Motor Over Temperature Event 
is to release. For a Positive Thermal Coefficient (PTC), the disable resistance will be greater than or equal to the enable value. For a 
Negative Thermal Coefficient (NTC), the disable resistance will be less than the enable value.

---
## Page 85

MNCMECRF-07 75
Object Dictionary / Drive Configuration
2043h: Capture Configuration Parameters   The following tables are used by the sub-
indices of this object.
TABLE 2.2 Capture Edge Configuration
TABLE 2.3  Capture Trigger Type
2054.05h Thermal Monitor Configuration
Data Type Data Range Units Accessibility Stored to NVM
N/A N/A - Read / Write Yes
Description:
If supported by the hardware, configures the operation of the thermistor/thermal cutoff switch.
Value Description
0 None / Off
1 Rising Edge
2 Falling Edge
3 Both Rising and Falling Edges
Value Description
0 Single Trigger: Captures one value at a time. Need to reset Capture before capturing another.
1 Continuous Trigger: Captures a new value each time Capture input is triggered without having to reset.
Valid Values
0 Disabled
1 Thermistor Active
2 Thermal Cutoff Switch Active Closed
3 Thermal Cutoff Switch Active High

---
## Page 86

MNCMECRF-07 76
Object Dictionary / Drive Configuration
TABLE 2.4  Capture Source High/Low Values
Signal Source Low Value High Value
Velocity Feedback 16 17
Velocity Measured 18 19
Velocity Target 20 21
Velocity Demand 22 23
Velocity Error 24 25
Position Measured 26 27
Position Target 28 29
Position Demand 30 31
Position Error 32 33
Auxiliary Position Input 34 35
Phase Angle 15 87
Stator Angle 86 87
2043.01h Capture ‘A’ Edge Configuration
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 3 N/A Read / Write Yes
Description:
Selects the edge(s) that will trigger Capture A to capture the pre-selected signal source. See Table 2.2 for a list of allowable values.
2043.02h Capture ‘A’ Trigger
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 1 N/A Read / Write Yes
Description:
Selects whether a value should be captured only once, upon the first applicable edge that is encountered, or every time an edge is 
encountered. See Table 2.3 for a list of allowable values.
2043.03h Capture ‘A’ Source – Low Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the next to select the signal source to capture. See Table 2.4 for a list of allowable values. 

---
## Page 87

MNCMECRF-07 77
Object Dictionary / Drive Configuration
2043.04h Capture ‘A’ Source – High Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the previous to select the signal source to capture. See Table 2.4 for a list of allowable values. 
2043.05h Capture ‘B’ Edge Configuration
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 3 N/A Read / Write Yes
Description:
Selects the edge(s) that will trigger Capture B to capture the pre-selected signal source. See Table 2.2 for a list of allowable values.
2043.06h Capture ‘B’ Trigger
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 1 N/A Read / Write Yes
Description:
Selects whether a value should be captured only once, upon the first applicable edge that is encountered, or every time an edge is 
encountered. See Table 2.3 for a list of allowable values.
2043.07h Capture ‘B’ Source – Low Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the next to select the signal source to capture. See Table 2.4 for a list of allowable values. 
2043.08h Capture ‘B’ Source – High Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the previous to select the signal source to capture. See Table 2.4 for a list of allowable values. 
2043.09h Capture ‘C’ Edge Configuration
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 3 N/A Read / Write Yes
Description:
Selects the edge(s) that will trigger Capture C to capture the pre-selected signal source. See Table 2.2 for a list of allowable values.

---
## Page 88

MNCMECRF-07 78
Object Dictionary / Drive Configuration
2058h: Digital Input Parameters   
TABLE 2.5  Object 2058 Mapping
* Number of actual inputs depends on drive model
2043.0Ah Capture ‘C’ Trigger
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 1 N/A Read / Write Yes
Description:
Selects whether a value should be captured only once, upon the first applicable edge that is encountered, or every time an edge is 
encountered. See Table 2.3 for a list of allowable values.
2043.0Bh Capture ‘C’ Source – Low Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the next to select the signal source to capture. See Table 2.4 for a list of allowable values. 
2043.0Ch Capture ‘C’ Source – High Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 See Table 2.4 N/A Read / Write Yes
Description:
This sub-index is used together with the previous to select the signal source to capture. See Table 2.4 for a list of allowable values. 
Bit Digital Input Mask*
0 Digital Input 1
1 Digital Input 2
2 Digital Input 3
3 Digital Input 4
4 Digital Input 5
5 Digital Input 6
6 Digital Input 7
7 Digital Input 8
8…15 Reserved

---
## Page 89

MNCMECRF-07 79
Object Dictionary / Drive Configuration
2058.01h  Digital Input Mask: Active Level
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Determines which digital inputs are active high and which are active low. See Table 2.5 above for mapping structure.
2058.02h  Digital Input Mask: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to User Disable. See Table 2.5 above for mapping structure.
2058.03h  Digital Input Mask: Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the positive limit. See Table 2.5 above for mapping structure.
2058.04h  Digital Input Mask: Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to negative limit. See Table 2.5 above for mapping structure.
2058.05h  Digital Input Mask: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to activate Motor Over Temperature. See Table 2.5 above for mapping structure.
2058.06h  Digital Input Mask: Phase Detection
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to activate Phase Detection. See Table 2.5 above for mapping structure.

---
## Page 90

MNCMECRF-07 80
Object Dictionary / Drive Configuration
2058.07h  Digital Input Mask: Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to activate the Auxiliary Disable. See Table 2.5 above for mapping structure.
2058.08h  Digital Input Mask: Set Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to activate the Set Position event. See Table 2.5 above for mapping structure.
2058.09h  Digital Input Mask: Start Homing
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to activate the Start Homing event. See Table 2.5 above for mapping structure.
2058.0Ah  Digital Input Mask: Home Switch
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Home Switch. See Table 2.5 above for mapping structure.
2058.0Bh  Digital Input Mask: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Stop event. See Table 2.5 above for mapping structure.
2058.0Ch  Digital Input Mask: Set / Reset Capture A
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Set / Reset Capture A event. See Table 2.5 above for mapping structure.

---
## Page 91

MNCMECRF-07 81
Object Dictionary / Drive Configuration
2058.0Dh  Digital Input Mask: Set / Reset Capture B
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Set / Reset Capture B event. See Table 2.5 above for mapping structure.
2058.0Eh  Digital Input Mask: Set / Reset Capture C
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Set / Reset Capture C event. See Table 2.5 above for mapping structure.
2058.0Fh  Digital Input Mask: Reset Event History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Reset Event History event. See Table 2.5 above for mapping structure.
2058.10h  Digital Input Mask: Configuration Select 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Configuration Select 0 event. See Table 2.5 above for mapping structure.
2058.11h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write Yes
2058.12h  Digital Input Mask: Gain Select 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Gain Select 0 event. See Table 2.5 above for mapping structure.

---
## Page 92

MNCMECRF-07 82
Object Dictionary / Drive Configuration
2058.13h  Digital Input Mask: Zero Position Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Zero Position Error event. See Table 2.5 above for mapping structure.
2058.14h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write Yes
2058.15h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write Yes
2058.16h  Digital Input Mask: Motion Engine Mode
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Engine Mode event. See Table 2.5 above for mapping structure.
2058.17h  Digital Input Mask: Motion Engine Enable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Enable Enable event. See Table 2.5 above for mapping structure.
2058.18h  Digital Input Mask: Motion Execute
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Execute event. See Table 2.5 above for mapping structure.

---
## Page 93

MNCMECRF-07 83
Object Dictionary / Drive Configuration
2058.19h  Digital Input Mask: Motion Select 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Select 0 event. See Table 2.5 above for mapping structure.
2058.1Ah  Digital Input Mask: Motion Select 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Select 1 event. See Table 2.5 above for mapping structure.
2058.1Bh  Digital Input Mask: Motion Select 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Select 2 event. See Table 2.5 above for mapping structure.
2058.1Ch  Digital Input Mask: Motion Select 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Select 3 event. See Table 2.5 above for mapping structure.
2058.1Dh  Digital Input Mask: Motion Engine Abort
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Motion Engine Abort event. See Table 2.5 above for mapping structure.
2058.1Eh  Digital Input Mask: Jog Plus
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Jog Plus event. See Table 2.5 above for mapping structure.

---
## Page 94

MNCMECRF-07 84
Object Dictionary / Drive Configuration
205Ah: Digital Output Parameters   
TABLE 2.6  Object 205A Mapping
2058.1Fh  Digital Input Mask: Jog Minus
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Jog Minus event. See Table 2.5 above for mapping structure.
2058.20h  Digital Input Mask: Jog 0 Select
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Jog 0 Select event. See Table 2.5 above for mapping structure.
2058.21h  Digital Input Mask: Jog 1 Select
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital inputs, if any, are assigned to the Jog 1 Select event. See Table 2.5 above for mapping structure.
Bit Digital Output Mask
0 Digital Output 1
1 Digital Output 2
2 Digital Output 3
3 Digital Output 4
4…15 Reserved
205A.01h Digital Output Mask: Active Level
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs are active high and which are active low. See Table 2.6 above for mapping structure.

---
## Page 95

MNCMECRF-07 85
Object Dictionary / Drive Configuration
205A.02h Digital Output Mask: Drive Reset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Drive Reset event. See Table 2.6 above for mapping structure.
205A.03h Digital Output Mask: Drive Internal Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Drive Internal Error event. See Table 2.6 above for mapping structure.
205A.04h Digital Output Mask: Short Circuit Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Short Circuit Fault event. See Table 2.6 above for mapping structure.
205A.05h Digital Output Mask: Over-Current Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Over-Current event. See Table 2.6 above for mapping structure.
205A.06h Digital Output Mask: Hardware Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Hardware Under Voltage event. See Table 2.6 above for mapping structure.
205A.07h Digital Output Mask: Hardware Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Hardware Over Voltage event. See Table 2.6 above for mapping structure.

---
## Page 96

MNCMECRF-07 86
Object Dictionary / Drive Configuration
205A.08h Digital Output Mask: Drive Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Drive Over Temperature event. See Table 2.6 above for mapping structure.
205A.09h Digital Output Mask: Parameter Restore Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Parameter Restore Error event. See Table 2.6 above for mapping structure.
205A.0Ah Digital Output Mask: Parameter Store Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Parameter Store Error event. See Table 2.6 above for mapping structure.
205A.0Bh Digital Output Mask: Invalid Hall State
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Invalid Hall State event. See Table 2.6 above for mapping structure.
205A.0Ch Digital Output Mask: Phase Synchronization Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Phase Synchronization Error event. See Table 2.6 above for mapping structure.
205A.0Dh Digital Output Mask: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Motor Over Temperature event. See Table 2.6 above for mapping structure.

---
## Page 97

MNCMECRF-07 87
Object Dictionary / Drive Configuration
205A.0Eh Digital Output Mask: Phase Detection Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Phase Detection Fault event. See Table 2.6 above for mapping structure.
205A.0Fh Digital Output Mask: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Feedback Sensor Error event. See Table 2.6 above for mapping structure.
205A.10h Digital Output Mask: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Log Entry Missed event. See Table 2.6 above for mapping structure.
205A.11h Digital Output Mask: Software Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Software Disable event. See Table 2.6 above for mapping structure.
205A.12h Digital Output Mask: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the User Disable event. See Table 2.6 above for mapping structure.
205A.13h Digital Output Mask: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Positive Limit event. See Table 2.6 above for mapping structure.

---
## Page 98

MNCMECRF-07 88
Object Dictionary / Drive Configuration
205A.14h Digital Output Mask: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Negative Limit event. See Table 2.6 above for mapping structure.
205A.15h Digital Output Mask: Current Limiting (Foldback)
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Current Limiting event. See Table 2.6 above for mapping structure.
205A.16h Digital Output Mask: Continuous Current Limit Reached
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Continuous Current Limit Reached event. See Table 2.6 above for mapping 
structure.
205A.17h Digital Output Mask: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Current Loop Saturated event. See Table 2.6 above for mapping structure.
205A.18h Digital Output Mask: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the User Under Voltage event. See Table 2.6 above for mapping structure.
205A.19h Digital Output Mask: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the User Over Voltage event. See Table 2.6 above for mapping structure.

---
## Page 99

MNCMECRF-07 89
Object Dictionary / Drive Configuration
205A.1Ah Digital Output Mask: Non-Sinusoidal Commutation
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Non-Sinusoidal Commutation. See Table 2.6 above for mapping structure.
205A.1Bh Digital Output Mask: Phase Detection
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Phase Detection event. See Table 2.6 above for mapping structure.
205A.1Ch Digital Output Mask: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the User Auxiliary Disable event. See Table 2.6 above for mapping structure.
205A.1Dh Digital Output Mask: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Shunt Regulator event. See Table 2.6 above for mapping structure.
205A.1Eh Digital Output Mask: Phase Detection Complete
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Phase Detection Complete event. See Table 2.6 above for mapping structure.
205A.1Fh Digital Output Mask: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Command Limiter Active event. See Table 2.6 above for mapping structure.

---
## Page 100

MNCMECRF-07 90
Object Dictionary / Drive Configuration
205A.20h Digital Output Mask: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Motor Over Speed event. See Table 2.6 above for mapping structure.
205A.21h Digital Output Mask: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the At Command event. See Table 2.6 above for mapping structure.
205A.22h Digital Output Mask: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Zero Velocity event. See Table 2.6 above for mapping structure.
205A.23h Digital Output Mask: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Velocity Following Error event. See Table 2.6 above for mapping structure.
205A.24h Digital Output Mask: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Positive Velocity Limit event. See Table 2.6 above for mapping structure.
205A.25h Digital Output Mask: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Negative Velocity Limit event. See Table 2.6 above for mapping structure.

---
## Page 101

MNCMECRF-07 91
Object Dictionary / Drive Configuration
205A.26h Digital Output Mask: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Max Measured Position event. See Table 2.6 above for mapping structure.
205A.27h Digital Output Mask: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Min Measured Position event. See Table 2.6 above for mapping structure.
205A.28h Digital Output Mask: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the At Home Position event. See Table 2.6 above for mapping structure.
205A.29h Digital Output Mask: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Position Following Error event. See Table 2.6 above for mapping structure.
205A.2Ah Digital Output Mask: Max Target position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Max Target Position Limit event. See Table 2.6 above for mapping structure.
205A.2Bh Digital Output Mask: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Min Target Position Limit event. See Table 2.6 above for mapping structure.

---
## Page 102

MNCMECRF-07 92
Object Dictionary / Drive Configuration
205A.2Ch Digital Output Mask: Set Measured Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Set Measured Position event. See Table 2.6 above for mapping structure.
205A.2Dh Digital Output Mask: Homing Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Homing Active event. See Table 2.6 above for mapping structure.
205A.2Eh Digital Output Mask: Apply Brake
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 ‘0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Apply Brake event. See Table 2.6 above for mapping structure.
205A.2Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205A.30h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205A.31h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205A.32h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205A.33h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 103

MNCMECRF-07 93
Object Dictionary / Drive Configuration
205A.34h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205A.35h Digital Output Mask: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Communication Error event. See Table 2.6 above for mapping structure.
205A.36h Digital Output Mask: Homing Complete
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Homing Complete event. See Table 2.6 above for mapping structure.
205A.37h Digital Output Mask: Commanded Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Commanded Stop event. See Table 2.6 above for mapping structure.
205A.38h Digital Output Mask: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the User Stop event. See Table 2.6 above for mapping structure.
205A.39h Digital Output Mask: Bridge Enabled
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Bridge Enabled status. See Table 2.6 above for mapping structure.

---
## Page 104

MNCMECRF-07 94
Object Dictionary / Drive Configuration
205A.3Ah Digital Output Mask: Dynamic Brake Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Dynamic Brake Active event. See Table 2.6 above for mapping structure.
205A.3Bh Digital Output Mask: Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Stop Active event. See Table 2.6 above for mapping structure.
205A.3Ch Digital Output Mask: Positive Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Positive Stop Active event. See Table 2.6 above for mapping structure.
205A.3Dh Digital Output Mask: Negative Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Negative Stop Active event. See Table 2.6 above for mapping structure.
205A.3Eh Digital Output Mask: Positive Inhibit Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Positive Inhibit Active event. See Table 2.6 above for mapping structure.
205A.3Fh Digital Output Mask: Negative Inhibit Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to the Negative Inhibit Active event. See Table 2.6 above for mapping structure.

---
## Page 105

MNCMECRF-07 95
Object Dictionary / Drive Configuration
205A.40h Digital Output Mask: User Bit 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 0. See Table 2.6 above for mapping structure.
205A.41h Digital Output Mask: User Bit 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 1. See Table 2.6 above for mapping structure.
205A.42h Digital Output Mask: User Bit 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 2. See Table 2.6 above for mapping structure.
205A.43h Digital Output Mask: User Bit 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 3. See Table 2.6 above for mapping structure.
205A.44h Digital Output Mask: User Bit 4
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 4. See Table 2.6 above for mapping structure.
205A.45h Digital Output Mask: User Bit 5
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 5. See Table 2.6 above for mapping structure.

---
## Page 106

MNCMECRF-07 96
Object Dictionary / Drive Configuration
205A.46h Digital Output Mask: User Bit 6
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 6. See Table 2.6 above for mapping structure.
205A.47h Digital Output Mask: User Bit 7
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 7. See Table 2.6 above for mapping structure.
205A.48h Digital Output Mask: User Bit 8
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 8 See Table 2.6 above for mapping structure.
205A.49h Digital Output Mask: User Bit 9
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 9. See Table 2.6 above for mapping structure.
205A.4Ah Digital Output Mask: User Bit 10
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 10. See Table 2.6 above for mapping structure.
205A.4Bh Digital Output Mask: User Bit 11
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 11. See Table 2.6 above for mapping structure.

---
## Page 107

MNCMECRF-07 97
Object Dictionary / Drive Configuration
205A.4Ch Digital Output Mask: User Bit 12
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 12. See Table 2.6 above for mapping structure.
205A.4Dh Digital Output Mask: User Bit 13
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 13. See Table 2.6 above for mapping structure.
205A.4Eh Digital Output Mask: User Bit 14
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 14. See Table 2.6 above for mapping structure.
205A.4Fh Digital Output Mask: User Bit 15
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to User Bit 15. See Table 2.6 above for mapping structure.
205A.50h Digital Output Mask: Capture A
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Capture A. See Table 2.6 above for mapping structure.
205A.51h Digital Output Mask: Capture B
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Capture B. See Table 2.6 above for mapping structure.

---
## Page 108

MNCMECRF-07 98
Object Dictionary / Drive Configuration
205A.52h Digital Output Mask: Capture C
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Capture C. See Table 2.6 above for mapping structure.
205A.53h Digital Output Mask: Commanded Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Commanded Positive Limit. See Table 2.6 above for mapping structure.
205A.54h Digital Output Mask: Commanded Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Commanded Negative Limit. See Table 2.6 above for mapping structure.
205A.55h Digital Output Mask: Safe Torque Off Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Safe Torque Off Active. See Table 2.6 above for mapping structure.
205A.56h Digital Output Mask: Zero Position Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Zero Position Error. See Table 2.6 above for mapping structure.
205A.57h Digital Output Mask: Motion Engine Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Motion Engine Error. See Table 2.6 above for mapping structure.

---
## Page 109

MNCMECRF-07 99
Object Dictionary / Drive Configuration
205A.58h Digital Output Mask: Motion Engine Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Motion Engine Active. See Table 2.6 above for mapping structure.
205A.59h Digital Output Mask: Active Motion Busy
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Busy. See Table 2.6 above for mapping structure.
205A.5Ah Digital Output Mask: Active Motion Done
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Done. See Table 2.6 above for mapping structure.
205A.5Bh Digital Output Mask: Active Motion Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Error. See Table 2.6 above for mapping structure.
205A.5Ch Digital Output Mask: Active Motion Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Active. See Table 2.6 above for mapping structure.
205A.5Dh Digital Output Mask: Active Motion Aborted
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Aborted. See Table 2.6 above for mapping structure.

---
## Page 110

MNCMECRF-07 100
Object Dictionary / Drive Configuration
205A.5Eh Digital Output Mask: Active Motion Execute
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion Execute. See Table 2.6 above for mapping structure.
205A.5Fh Digital Output Mask: Active Motion MotionDone
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion MotionDone. See Table 2.6 above for mapping structure.
205A.60h Digital Output Mask: Active Motion SequenceDone
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Active Motion SequenceDone. See Table 2.6 above for mapping structure.
205A.61h Digital Output Mask: Absolute Position Valid
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Absolute Position Valid See Table 2.6 above for mapping structure.
205A.62h Digital Output Mask: Jog Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Jog Active. See Table 2.6 above for mapping structure.
205A.63h Digital Output Mask: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to PWM and Direction Broken Wire. See Table 2.6 above for mapping structure.

---
## Page 111

MNCMECRF-07 101
Object Dictionary / Drive Configuration
2044h: Analog Input Parameters   
205A.64h Digital Output Mask: PLS Pulse 1 Post Active Level Output
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to PLS Pulse 1 Post Active Level. See Table 2.6 above for mapping structure.
205A.65h Digital Output Mask: PLS Pulse 2 Post Active Level Output
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to PLS Pulse 2 Post Active Level. See Table 2.6 above for mapping structure.
205A.66h Digital Output Mask: Motion Engine Abort
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines which digital outputs, if any, are assigned to Motion Engine Abort. See Table 2.6 above for mapping structure.
2044.01h Analog Input 1 Offset: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 1 Offset in Configuration 0. 
To convert the desired Offset Voltage to the appropriate do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 112

MNCMECRF-07 102
Object Dictionary / Drive Configuration
2044.02h Analog Input 1 Scale Factor: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 1 in Configuration 0. The values contained are mode dependent and 
require a different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.03h Analog Input 2 Offset: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 2 Offset in Configuration 0. 
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 113

MNCMECRF-07 103
Object Dictionary / Drive Configuration
2044.04h Analog Input 2 Scale Factor: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 2 in Configuration 0. This value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.05h Analog Input 3 Offset: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 3 Offset in Configuration 0. 
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 114

MNCMECRF-07 104
Object Dictionary / Drive Configuration
2044.06h Analog Input 3 Scale Factor: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 3 in Configuration 0. The value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.07h Analog Input 4 Offset: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 4 Offset in Configuration 0. 
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 115

MNCMECRF-07 105
Object Dictionary / Drive Configuration
2044.08h Analog Input 4 Scale Factor: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 4 in Configuration 0. The value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.09h Analog Input 1 Offset: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 1 Offset in Configuration 1. 
To convert the desired Offset Voltage to the appropriate do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 116

MNCMECRF-07 106
Object Dictionary / Drive Configuration
2044.0Ah Analog Input 1 Scale Factor: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 1 in Configuration 1. The values contained are mode dependent and 
require a different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.0Bh Analog Input 2 Offset: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 2 Offset in Configuration 1. 
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 117

MNCMECRF-07 107
Object Dictionary / Drive Configuration
2044.0Ch Analog Input 2 Scale Factor: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 2 in Configuration 1. This value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.0Dh Analog Input 3 Offset: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 3 Offset in Configuration 1. 
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 118

MNCMECRF-07 108
Object Dictionary / Drive Configuration
2044.0Eh Analog Input 3 Scale Factor: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 3 in Configuration 1. The value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
2044.0Fh Analog Input 4 Offset: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] DAI Read / Write Yes
Description:
Contains a value corresponding to the Analog Input 4 Offset in Configuration 1.
To convert the desired Offset Voltage to the appropriate value do the following:
Multiply Voltage (in decimal) by 819.2 and ignore any resulting fractional part. Now convert this decimal value to hexadecimal.

---
## Page 119

MNCMECRF-07 109
Object Dictionary / Drive Configuration
205Ch: Analog Output Parameters   
2044.10h Analog Input 4 Scale Factor: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Contains a value corresponding to the scale factor for analog input 4 in Configuration 1. The value is mode dependent and requires a 
different algorithm to calculate for each mode.
•Assigned to Current Loop Example: Desired scale factor = (X Amps / 1 Volt)
(X Amps * 10 * 2^18) / Drive Peak Current = Value in decimal; convert to hex.
•Assigned to Velocity Loop Example: Desired Scale factor = (X cnts/sec  / 1 Volt)
Convert X cnts/sec  Y cnts/100us by dividing by 10000. 
Now multiply: Ycnts * 20 * 2^18 = Value in Decimal; convert to hex.
•Assigned to Position Loop Example: Desired Scale Factor = (X cnts / 1 Volt)
Now Multiply: X cnts * 80 = Value in Decimal; convert to hex.
•Assigned to Current Limit Example: Desired Scale Factor = (X% of drive peak / 1 Volt)
Cannot achieve a value higher than 20% / 1 Volt.
Now Multiply X * 2^18 / 5 = Value in Decimal; convert to hex.
•Assigned to External Temperature: Desired Scale Factor = (X degrees C / 1 Volt)
Now multiply X *20 *2^18 = Value in Decimal; convert to hex
205C.01h Analog Output 1 Signal Select A
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Together with Signal Select B determines which internal drive parameter is assigned to analog output 1.
205C.02h Analog Output 1 Signal Select B
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Together with Signal Select A determines which internal drive parameter is assigned to analog output 1.
205C.03h Analog Output 1 Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] N/A Read / Write Yes
Description:
Analog output 1 offset.

---
## Page 120

MNCMECRF-07 110
Object Dictionary / Drive Configuration
205C.04h Analog Output 1 Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Analog output 1 gain.
205C.05h Analog Output 1 Operator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Analog output 1 operator.
205C.06h Analog Output 2 Signal Select A
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Together with Signal Select B determines which internal drive parameter is assigned to analog output 2.
205C.07h Analog Output 2 Signal Select B
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Together with Signal Select B determines which internal drive parameter is assigned to analog output 2.
205C.08h Analog Output 2 Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] - [2(15) –1] N/A Read / Write Yes
Description:
Analog output 2 offset.
205C.09h Analog Output 2 Gain
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] N/A Read / Write Yes
Description:
Analog output 2 gain.

---
## Page 121

MNCMECRF-07 111
Object Dictionary / Drive Configuration
2040h: Programmable Limit Switch Parameters   
205C.0Ah Analog Output 2 Operator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Analog output 2 operator.
2040.01h Programmable Limit Switch Configuration
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Defines the PLS mode and the signal that is monitored by PLS 1 and PLS 2.
2040.02h Programmable Limit Rollover Count
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] N/A Read / Write Yes
Description:
Contains the maximum value of the PLS position counter before rollover to zero.
Bit Description
0...4 PLS input select bits. 0 = No Source, 1 = Measured Position, 
2 = Demand Position
5...14 Reserved
15 A value of 1 enables linear mode. A value of 0 enables rotary 
mode.

---
## Page 122

MNCMECRF-07 112
Object Dictionary / Drive Configuration
2040.03h PLS 1 Configuration
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Contains the limits and settings for PLS 1.
2040.04h PLS 1 Lower Position Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the value of the lower PLS 1 pulse edge.
For rotary mode: Lower Position Value ≥ 0
For linear mode: Any 32 bit value
2040.05h PLS 1 Upper Position Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the value of the upper PLS 1 pulse edge. Upper Position ≥ Lower Position
2040.06h PLS 1 Repeat Delta Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the number of counts between repeating pulses. Repeat Delta Value > (Upper Position - Lower Position)
Bit Description
0 PLS enable. 0 = disable, 1 = enable
1 Output active level. 0 = active low, 1 = active high.
2 Repeat control. 0 = repeat count enabled, 1 = repeat count 
disabled (infinite repeat)
3 Pulse width control. 0 = pulse width based on position,
1 = pulse width based on time.
4-5 Pulse direction control. 0 = level sensitive / both directions,
1 = rising edge forward, 2 = falling edge reverse
6-7 Reserved. Write as 0.
8...15 Pulse repeat count. Total number of pulses in the pulse train 
= 1 + repeat count.

---
## Page 123

MNCMECRF-07 113
Object Dictionary / Drive Configuration
2040.07h PLS 1 Pulse Width Time Window
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - [2(16) –1] - Read / Write Yes
Description:
Used with time-based PLS. Contains the pulse width of PLS 1 in terms of time.
Measured in number of position loop samples (or switching frequency/2)
2040.08h PLS 2 Configuration
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Contains the limits and settings for PLS 2.
2040.09h PLS 2 Lower Position Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the value of the lower PLS 2 pulse edge.
For rotary mode: Lower Position Value ≥ 0
For linear mode: Any 32 bit value
2040.0Ah PLS 2 Upper Position Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the value of the upper PLS 2 pulse edge. Upper Position ≥ Lower Position
Bit Description
0 PLS enable. 0 = disable, 1 = enable
1 Output active level. 0 = active low, 1 = active high.
2 Repeat control. 0 = repeat count enabled, 1 = repeat count 
disabled (infinite repeat)
3 Pulse width control. 0 = pulse width based on position,
1 = pulse width based on time.
4-5 Pulse direction control. 0 = level sensitive / both directions,
1 = rising edge forward, 2 = falling edge reverse
6-7 Reserved. Write as 0.
8...15 Pulse repeat count. Total number of pulses in the pulse train 
= 1 + repeat count.

---
## Page 124

MNCMECRF-07 114
Object Dictionary / Drive Configuration
203Dh: Deadband Parameters   Some deadband parameters have units that vary with the 
operating mode of the drive. For these parameters, refer to Table 2.7 for the correct unit 
selection.
TABLE 2.7  Deadband Units
2040.0Bh PLS 2 Repeat Delta Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 - [2(32) –1] Counts Read / Write Yes
Description:
Contains the number of counts between repeating pulses. Repeat Delta Value > (Upper Position - Lower Position)
2040.0Ch PLS 2 Pulse Width Time Window
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - [2(16) –1] - Read / Write Yes
Description:
Used with time-based PLS. Contains the pulse width of PLS 2 in terms of time.
Measured in number of position loop samples (or switching frequency/2)
Drive Operation Mode Units
Current (Torque) DC2
Velocity DS1
Position (Around Velocity Or Current) counts
203D.01h Deadband Type: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 1 N/A Read / Write Yes
Description: 
Deadband Type for Configuration 0.
203D.02h Deadband Width: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] See Table 2.7 Read / Write Yes
Description:
The width from the midpoint to one end of the deadband in Configuration 0. Therefore, the total width is 2X this value.
Value Description
0 Non-linear (starts smoothly after reaching end of deadband)
1 Linear (jumps to command after reaching end of deadband)

---
## Page 125

MNCMECRF-07 115
Object Dictionary / Drive Configuration
203Eh: Jog Parameters   
203D.03h Deadband Set Point: Config 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] See Table 2.7 Read / Write Yes
Description:
Midpoint of the Deadband in Configuration 0.
203D.04h Deadband Type: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 - 1 N/A Read / Write Yes
Description: 
Deadband Type for Configuration 1.
203D.05h Deadband Width: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 0 – [2(31)-1] See Table 2.7 Read / Write Yes
Description:
The width from the midpoint to one end of the deadband in Configuration 1. Therefore, the total width is 2X this value.
203D.06h Deadband Set Point: Config 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] See Table 2.7 Read / Write Yes
Description:
Midpoint of the Deadband in Configuration 1.
203E.01h Max Acceleration
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DA4 Read / Write Yes
Description:
Sets the maximum acceleration for the selected Jog.
Value Description
0 Non-linear (starts smoothly after reaching end of deadband)
1 Linear (jumps to command after reaching end of deadband)

---
## Page 126

MNCMECRF-07 116
Object Dictionary / Drive Configuration
2062h: Braking/Stop General Properties   
203E.02h Max Deceleration
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DA4 Read / Write Yes
Description:
Sets the maximum deceleration for the selected Jog.
203E.03h Jog Speed 0
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DS1 Read / Write Yes
Description:
Sets the target speed for Jog 0.
203E.04h Jog Speed 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DS1 Read / Write Yes
Description:
Sets the target speed for Jog 1.
203E.05h Jog Speed 2
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DS1 Read / Write Yes
Description:
Sets the target speed for Jog 2.
203E.06h Jog Speed 3
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 – [2(31)-1] DS1 Read / Write Yes
Description:
Sets the target speed for Jog 3.
2062.01h Braking: Delay After Applying Brake
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
Specifies the delay, in milliseconds, after applying the external brake before disabling the power bridge or dynamic braking.

---
## Page 127

MNCMECRF-07 117
Object Dictionary / Drive Configuration
2064h: Event Response Time Parameters   
2062.02h Braking: Delay Before Disengaging Brake
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
Specifies the delay, in milliseconds, before releasing the external brake after enabling the power bridge or discontinuing dynamic braking.
2062.03h Stop Deceleration Limit - Position Mode
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 - [2(31) –1] DA1 Read / Write Yes
Description:
Specifies the maximum position mode deceleration during a controlled Stop event. See “Appendix” on page 225 for unit conversion details.
2062.04h Stop Deceleration Limit - Velocity Mode
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 - [2(31) –1] DA1 Read / Write Yes
Description:
Specifies the maximum velocity mode acceleration during a controlled Stop event. See “Appendix” on page 225 for unit conversion details.
2062.05h Stop Jerk Limit - Current Mode
Data Type Data Range Units Accessibility Stored to NVM
Integer32 1 - [2(31) –1] DJ1 Read / Write Yes
Description:
Sets the rate at which the target current ramps down during a Stop event. Only valid for current mode. See “Appendix” on page 225 for unit 
conversion details.
2064.01h Event Response Time: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Motor Over Temperature before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 128

MNCMECRF-07 118
Object Dictionary / Drive Configuration
2064.02h Event Response Time: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a Feedback Sensor Error before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.03h Event Response Time: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a Log Entry Missed before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.04h Event Response Time: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a User Disable before the power bridge is disabled.
The event action is disabled when bit 15 is set to 1.
2064.05h Event Response Time: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a User Positive Limit input before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.06h Event Response Time: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a User Negative Limit input before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 129

MNCMECRF-07 119
Object Dictionary / Drive Configuration
2064.07h Event Response Time: Current Limit Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] Milliseconds Read / Write Yes
Description:
The time delay after the occurrence of Current Limit Active before its Event Action (2065h) is executed.
2064.08h Event Response Time: Continuous Current Foldback
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of reaching the Continuous Current Foldback setting before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.09h Event Response Time: Current Limit Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Current Limit Saturated before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.0Ah Event Response Time: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of User Under Voltage before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.0Bh Event Response Time: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a user-specified Over Voltage level before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 130

MNCMECRF-07 120
Object Dictionary / Drive Configuration
2064.0Ch Event Response Time: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Motor Over Speed before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.0Dh Event Response Time: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a User Auxiliary Disable input before dynamic braking is applied.
The event action is disabled when bit 15 is set to 1.
2064.0Eh Event Response Time: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Shunt Regulator activity before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.0Fh Event Response Time: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Command Limiter Active before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.10h Event Response Time: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of At Command before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 131

MNCMECRF-07 121
Object Dictionary / Drive Configuration
2064.11h Event Response Time: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Zero Velocity before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.12h Event Response Time: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Velocity Following Error before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.13h Event Response Time: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Positive Velocity Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.14h Event Response Time: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Negative Velocity Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.15h Event Response Time: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of At Home Position before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 132

MNCMECRF-07 122
Object Dictionary / Drive Configuration
2064.16h Event Response Time: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Position Following Error before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.17h Event Response Time: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Max Target Position Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.18h Event Response Time: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Min Target Position Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.19h Event Response Time: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Maximum Measured Position Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.1Ah Event Response Time: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Minimum Measured Position Limit before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.

---
## Page 133

MNCMECRF-07 123
Object Dictionary / Drive Configuration
2064.1Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.1Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.1Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.1Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.20h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2064.21h Event Response Time: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of Communication Error before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2064.22h Event Response Time: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of a User Stop command before stopping the motor.
The event action is disabled when bit 15 is set to 1.

---
## Page 134

MNCMECRF-07 124
Object Dictionary / Drive Configuration
2065h: Event Action Parameters   
2064.23h Event Response Time: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after the occurrence of PWM and Direction Broken Wire before its Event Action (2065h) is executed.
The event action is disabled when bit 15 is set to 1.
2065.01h Event Action: Parameter Restore Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Parameter Restore Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.02h Event Action: Parameter Store Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Parameter Store Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.03h Event Action: Invalid Hall State
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after an Invalid Hall State. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.04h Event Action: Phase Synch Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Phase Synch Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 135

MNCMECRF-07 125
Object Dictionary / Drive Configuration
2065.05h Event Action: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Motor Over Temperature. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.06h Event Action: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Feedback Sensor Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.07h Event Action: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Log Entry Missed. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.08h Event Action: Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Current Limiting. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.09h Event Action: Continuous Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Continuous Current. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 136

MNCMECRF-07 126
Object Dictionary / Drive Configuration
2065.0Ah Event Action: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after Current Loop Saturated. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.0Bh Event Action: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Under Voltage. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.0Ch Event Action: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Over Voltage. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.0Dh Event Action: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after Shunt Regulator active. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.0Eh Event Action: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after Command Limiter Active. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 137

MNCMECRF-07 127
Object Dictionary / Drive Configuration
2065.0Fh Event Action: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Motor Over Speed. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.10h Event Action: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after an At Command state. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.11h Event Action: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Zero Velocity state. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.12h Event Action: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Velocity Following Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.13h Event Action: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Positive Velocity Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 138

MNCMECRF-07 128
Object Dictionary / Drive Configuration
2065.14h Event Action: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Negative Velocity Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.15h Event Action: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Max Measured Position Limit. Refer to Table 2.8 below for the valid event actions and their 
respective values.
2065.16h Event Action: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Min Measured Position Limit. Refer to Table 2.8 below for the valid event actions and their 
respective values.
2065.17h Event Action: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after an At Home Position state. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.18h Event Action: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Position Following Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 139

MNCMECRF-07 129
Object Dictionary / Drive Configuration
2065.19h Event Action: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Max Target Position Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.1Ah Event Action: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Min Target Position Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.1Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2065.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2065.1Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2065.1Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2065.1Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2065.20h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 140

MNCMECRF-07 130
Object Dictionary / Drive Configuration
2065.21h Event Action: Comm Channel Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Comm Channel Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.22h Event Action: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Positive Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.23h Event Action: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Negative Limit. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.24h Event Action: Drive Reset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Drive Reset. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.25h Event Action: Drive Internal Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Drive Internal Error. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 141

MNCMECRF-07 131
Object Dictionary / Drive Configuration
2065.26h Event Action: Short Circuit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Short Circuit. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.27h Event Action: Over Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Over Current. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.28h Event Action: Hardware Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Hardware Under Voltage. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.29h Event Action: Hardware Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Hardware Over Voltage. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.2Ah Event Action: Drive Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Drive Over Temperature. Refer to Table 2.8 below for the valid event actions and their respective 
values.

---
## Page 142

MNCMECRF-07 132
Object Dictionary / Drive Configuration
2065.2Bh Event Action: Software Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Software Disable. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.2Ch Event Action: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Disable. Refer to Table 2.8 below for the valid event actions and their respective values.
2065.2Dh Event Action: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a User Auxiliary Disable. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.2Eh Event Action: Phase Detection Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Phase Detection Fault. Refer to Table 2.8 below for the valid event actions and their respective 
values.
2065.2Fh Event Action: Commanded Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Commanded Positive Limit. Refer to Table 2.8 below for the valid event actions and their 
respective values.

---
## Page 143

MNCMECRF-07 133
Object Dictionary / Drive Configuration
TABLE 2.8 Event Action Options
2065.30h Event Action: Commanded Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 15 N/A Read / Write Yes
Description: 
The action of the drive immediately after a Commanded Negative Limit. Refer to Table 2.8 below for the valid event actions and their 
respective values.
2065.31h Event Action: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] N/A Read / Write Yes
Description: 
The action of the drive immediately after a PWM and Direction Broken Wire. Refer to Table 2.8 below for the valid event actions and their 
respective values.
Sub 
Index Event Valid Event Action Values (refer to Table 2.9 for value defini-
tions)
01h Parameter Restore Error - 1 - - 4 - - - 8 9 10 11
02h Parameter Store Error - 1 - - 4 - - - 8 9 10 11
03h Invalid Hall State - 1 - - 4 - - - 8 9 10 11
04h Phase Synch Error 0 1 - - 4 - - - 8 9 10 11
05h Motor Over Temperature 0 1 2 3 4 5 6 7 8 9 10 11
06h Feedback Sensor Error 0 1 2 3 4 5 6 7 8 9 10 11
07h Log Entry Missed 0 1 2 3 4 5 6 7 8 9 10 11
08h Current Limiting 0 1 2 3 4 5 6 7 8 9 10 11
09h Continuous Current 0 1 2 3 4 5 6 7 8 9 10 11
0Ah Current Loop Saturated 0 1 2 3 4 5 6 7 8 9 10 11
0Bh User Under Voltage 0 1 2 3 4 5 6 7 8 9 10 11
0Ch User Over Voltage 0 1 2 3 4 5 6 7 8 9 10 11
0Dh Shunt Regulator 0 1 - - 4 - - - 8 9 10 11
0Eh Command Limiter Active 0 - - - - - - - - - - -
0Fh Motor Over Speed 0 1 2 3 4 5 6 7 8 9 10 11
10h At Command 0 1 2 3 4 5 6 7 8 9 10 11
11h Zero Velocity 0 - - - - - - - - - - -
12h Velocity Following Error 0 1 2 3 4 5 6 7 8 9 10 11
13h Positive Velocity Limit 0 1 2 3 4 5 6 7 8 9 10 11
14h Negative Velocity Limit 0 1 2 3 4 5 6 7 8 9 10 11
15h Max Measured Position Limit 0 1 2 3 4 5 6 7 8 9 10 11
16h Min Measured Position Limit 0 1 2 3 4 5 6 7 8 9 10 11
17h At Home Position 0 - - - - - - - - - - -

---
## Page 144

MNCMECRF-07 134
Object Dictionary / Drive Configuration
TABLE 2.9 Event Action Values Definition
18h Position Following Error 0 1 2 3 4 5 6 7 8 9 10 11
19h Max Target Position Limit 0 1 2 3 4 5 6 7 8 9 10 11
1Ah Min Target Position Limit 0 1 2 3 4 5 6 7 8 9 10 11
1Bh Reserved 0 1 2 3 4 5 6 7 8 9 10 11
1Ch Reserved 0 1 2 3 4 5 6 7 8 9 10 11
1Dh Reserved 0 1 2 3 4 5 6 7 8 9 10 11
1Eh Reserved 0 1 2 3 4 5 6 7 8 9 10 11
1Fh Reserved 0 1 2 3 4 5 6 7 8 9 10 11
20h Reserved 0 1 2 3 4 - - - 8 9 10 11
21h Comm Channel Error 0 1 2 3 4 5 6 7 8 9 10 11
22h User Positive Limit - - 2 - - 5 - - - - - -
23h User Negative Limit - - - 3 - - 6 - - - - -
24h Drive Reset - 1 - - - - - - - - 10 -
25h Drive Internal Error - 1 - - - - - - - - 10 -
26h Short Circuit - 1 - - - - - - - - 10 -
27h Over Current - 1 - - - - - - - - 10 -
28h Hardware Under Voltage - 1 - - 4 - - - - - 10 -
29h Hardware Over Voltage - 1 - - - - - - - - 10 -
2Ah Drive Over Temperature - 1 - - - - - - - - 10 -
2Bh Software Disable - 1 - - - - - - 8 - 10 -
2Ch User Disable - 1 - - - - - - 8 - 10 -
2Dh User Auxiliary Disable - 1 - - 4 - - - 8 9 10 11
2Eh Phase Detection Fault - 1 - - - - - - 8 - 10 -
2Fh Commanded Positive Limit - - 2 - - 5 - - - - - -
30h Commanded Negative Limit - - - 3 - - 6 - - - - -
31h PWM and Dir Broken Wire 0 1 2 3 4 5 6 7 - - - -
Event Action Values Hex Values Event Actions
0 00h No Action
1 01h Disable Power Bridge
2 02h Disable Positive Direction
3 03h Disable Negative Direction
4 04h Dynamic Brake
5 05h Positive Stop
6 06h Negative Stop
7 07h Stop
8 08h Apply Brake then Disable Bridge
9 09h Apply Brake then Dynamic Brake
10 0Ah Apply Brake and Disable Bridge
11 0Bh Apply Brake and Dynamic Brake

---
## Page 145

MNCMECRF-07 135
Object Dictionary / Drive Configuration
2066h: Event Recovery Time Parameters   
2066.01h Event Recovery Time: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Motor Over Temperature is no longer true before its Event Action (2065h) is removed.
2066.02h Event Recovery Time: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Feedback Sensor Error is no longer true before its Event Action (2065h) is removed.
2066.03h Event Recovery Time: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Log Entry Missed is no longer true before its Event Action (2065h) is removed.
2066.04h Event Recovery Time: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after User Disable is no longer true before its Event Action (2065h) is removed.
2066.05h Event Recovery Time: Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Positive Limit is no longer true before its Event Action (2065h) is removed.
2066.06h Event Recovery Time: Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Negative Limit is no longer true before its Event Action (2065h) is removed.

---
## Page 146

MNCMECRF-07 136
Object Dictionary / Drive Configuration
2066.07h Event Recovery Time: Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Current Limiting is no longer true before its Event Action (2065h) is removed.
2066.08h Event Recovery Time: Continuous Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Continuous Current Limiting is no longer true before its Event Action (2065h) is removed.
2066.09h Event Recovery Time: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Current Loop Saturated status is no longer true before its Event Action (2065h) is removed.
2066.0Ah Event Recovery Time: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after User Under Voltage is no longer true before its Event Action (2065h) is removed.
2066.0Bh Event Recovery Time: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after User Over Voltage is no longer true before its Event Action (2065h) is removed.
2066.0Ch Event Recovery Time: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after User Auxiliary Disable is no longer true before its Event Action (2065h) is removed.

---
## Page 147

MNCMECRF-07 137
Object Dictionary / Drive Configuration
2066.0Dh Event Recovery Time: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Shunt Regulator active is no longer true before its Event Action (2065h) is removed.
2066.0Eh Event Recovery Time: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Command Limiter Active is no longer true before its Event Action (2065h) is removed.
2066.0Fh Event Recovery Time: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Motor Over Speed is no longer true before its Event Action (2065h) is removed.
2066.10h Event Recovery Time: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after At Command is no longer true before its Event Action (2065h) is removed.
2066.11h Event Recovery Time: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Zero Velocity is no longer true before its Event Action (2065h) is removed.
2066.12h Event Recovery Time: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Velocity Following Error is no longer true before its Event Action (2065h) is removed.

---
## Page 148

MNCMECRF-07 138
Object Dictionary / Drive Configuration
2066.13h Event Recovery Time: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Positive Velocity Limit is no longer true before its Event Action (2065h) is removed.
2066.14h Event Recovery Time: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Negative Velocity Limit is no longer true before its Event Action (2065h) is removed.
2066.15h Event Recovery Time: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Max Measured Position Limit status is no longer true before its Event Action (2065h) is removed.
2066.16h Event Recovery Time: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Min Measured Position Limit status is no longer true before its Event Action (2065h) is removed.
2066.17h Event Recovery Time: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after no longer At Home Position before its Event Action (2065h) is removed.
2066.18h Event Recovery Time: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Position Following Error is no longer true before its Event Action (2065h) is removed.

---
## Page 149

MNCMECRF-07 139
Object Dictionary / Drive Configuration
2066.19h Event Recovery Time: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Max Target Position Limit is no longer true before its Event Action (2065h) is removed.
2066.1Ah Event Recovery Time: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Min Target Position Limit is no longer true before its Event Action (2065h) is removed.
2066.1Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2066.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2066.1Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2066.1Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2066.1Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2066.20h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 150

MNCMECRF-07 140
Object Dictionary / Drive Configuration
2067h: Event Time-Out Window Parameters   
2066.21h Event Recovery Time: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after Communication Error is no longer true before its Event Action (2065h) is removed.
2066.22h Event Recovery Time: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after User Stop is no longer true before it is considered no longer active.
2066.23h Event Recovery Time: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time delay after PWM and Direction Broken Wire is no longer true before it is considered no longer active.
2067.01h Event Time-Out Window: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Motor Over Temperature as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.02h Event Time-Out Window: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Feedback Sensor Error as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.

---
## Page 151

MNCMECRF-07 141
Object Dictionary / Drive Configuration
2067.03h Event Time-Out Window: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a User Disable as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.04h Event Time-Out Window: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Positive Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.05h Event Time-Out Window: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Negative Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.06h Event Time-Out Window: Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Current Limiting as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.07h Event Time-Out Window: Continuous Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Continuous Current as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.

---
## Page 152

MNCMECRF-07 142
Object Dictionary / Drive Configuration
2067.08h Event Time-Out Window: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Current Loop Saturated as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.09h Event Time-Out Window: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a User Under Voltage as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.0Ah Event Time-Out Window: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a User Over Voltage as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.0Bh Event Time-Out Window: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a User Auxiliary Disable as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.0Ch Event Time-Out Window: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Shunt Regulator as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.

---
## Page 153

MNCMECRF-07 143
Object Dictionary / Drive Configuration
2067.0Dh Event Time-Out Window: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Command Limiter Active as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.0Eh Event Time-Out Window: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Motor Over Speed as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.0Fh Event Time-Out Window: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of At Command as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.10h Event Time-Out Window: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Zero Velocity as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.

---
## Page 154

MNCMECRF-07 144
Object Dictionary / Drive Configuration
2067.11h Event Time-Out Window: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Velocity Following Error as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.12h Event Time-Out Window: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Positive Velocity Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.13h Event Time-Out Window: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Negative Velocity Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.14h Event Time-Out Window: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Max Measured Position Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.

---
## Page 155

MNCMECRF-07 145
Object Dictionary / Drive Configuration
2067.15h Event Time-Out Window: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Min Measured Position Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.16h Event Time-Out Window: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of At Home Position as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.17h Event Time-Out Window: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Position Following Error as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.18h Event Time-Out Window: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Max Target Position Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.

---
## Page 156

MNCMECRF-07 146
Object Dictionary / Drive Configuration
2067.19h Event Time-Out Window: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of Min Target Position Limit as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur 
within this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) 
attribute.
2067.1Ah Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.1Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.1Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.1Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.1Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2067.20h Event Time-Out Window: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a Communication Error as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within 
this window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.

---
## Page 157

MNCMECRF-07 147
Object Dictionary / Drive Configuration
2068h: Event Maximum Recoveries Parameters   
2067.21h Event Time-Out Window: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of a User Stop as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2067.22h Event Time-Out Window: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] milliseconds (ms) Read / Write Yes
Description:
The time, after the Recovery Time (2066h) and subsequent removal of the event action, during which the drive will NOT consider an 
occurrence of PWM and Direction as a new occurrence. The Event Action (2065h) will still be applied in case an event does occur within this 
window. However, that occurrence will not be counted as a new occurrence with regard to the Maximum Recoveries (2068h) attribute.
2068.01h Event Maximum Recoveries: Short Circuit 
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Short Circuit performs the action assigned to this event. Each time the event is removed for longer than the addition of 
the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the maximum 
recovery count allowed before the Short Circuit event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.02h Event Maximum Recoveries: Hardware Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Hardware Under Voltage performs the action assigned to this event. Each time the event is removed for longer than 
the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets 
the maximum recovery count allowed before the Hardware Under Voltage event latches and must be actively reset in order to enable the 
bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 158

MNCMECRF-07 148
Object Dictionary / Drive Configuration
2068.03h Event Maximum Recoveries: Hardware Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Hardware Over Voltage performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Hardware Over Voltage event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.04h Event Maximum Recoveries: Drive Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Drive Over Temperature performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Drive Over Temperature event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.05h Event Maximum Recoveries: Invalid Hall State
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of an Invalid Hall State performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Invalid Hall State event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.
2068.06h Event Maximum Recoveries: Phase Synchronization Error 
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Phase Synchronization Error performs the action assigned to this event. Each time the event is removed for longer 
than the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object 
sets the maximum recovery count allowed before the Phase Synchronization Error event latches and must be actively reset in order to 
enable the bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. 
For more information on event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 159

MNCMECRF-07 149
Object Dictionary / Drive Configuration
2068.07h Event Maximum Recoveries: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Motor Over Temperature performs the action assigned to this event. Each time the event is removed for longer than 
the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets 
the maximum recovery count allowed before the Motor Over Temperature event latches and must be actively reset in order to enable the 
bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.08h Event Maximum Recoveries: Phase Detection Failure
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Phase Detection Failure performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Phase Detection Failure event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.09h Event Maximum Recoveries: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Feedback Sensor Error performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Feedback Sensor Error event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.0Ah Event Maximum Recoveries: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Log Entry Missed performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Log Entry Missed event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 160

MNCMECRF-07 150
Object Dictionary / Drive Configuration
2068.0Bh Event Maximum Recoveries: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a User Disable performs the action assigned to this event. Each time the event is removed for longer than the addition of 
the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the maximum 
recovery count allowed before the User Disable event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.0Ch Event Maximum Recoveries: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Positive Limit performs the action assigned to this event. Each time the event is removed for longer than the addition of 
the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the maximum 
recovery count allowed before the Positive Limit event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.0Dh Event Maximum Recoveries: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Negative Limit performs the action assigned to this event. Each time the event is removed for longer than the addition 
of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Negative Limit event latches and must be actively reset in order to enable the bridge. Re-setting 
the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.0Eh Event Maximum Recoveries: Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Current Limiting performs the action assigned to this event. Each time the event is removed for longer than the addition 
of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Current Limiting event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 161

MNCMECRF-07 151
Object Dictionary / Drive Configuration
2068.0Fh Event Maximum Recoveries: Continuous Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Continuous Current Limiting performs the action assigned to this event. Each time the event is removed for longer than 
the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets 
the maximum recovery count allowed before the Continuous Current Limiting event latches and must be actively reset in order to enable the 
bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.10h Event Maximum Recoveries: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Current Loop Saturated performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Current Loop Saturated event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.11h Event Maximum Recoveries: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a User Under Voltage performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the User Under Voltage event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information 
on event handling, see the Help file associated with the AMC drive configuration software.
2068.12h Event Maximum Recoveries: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a User Over Voltage performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the User Over Voltage event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information 
on event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 162

MNCMECRF-07 152
Object Dictionary / Drive Configuration
2068.13h Event Maximum Recoveries: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a User Auxiliary Disable performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the User Auxiliary Disable event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.14h Event Maximum Recoveries: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Shunt Regulator performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Shunt Regulator event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.
2068.15h Event Maximum Recoveries: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Command Limiter Active performs the action assigned to this event. Each time the event is removed for longer than 
the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets 
the maximum recovery count allowed before the Command Limiter Active event latches and must be actively reset in order to enable the 
bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.16h Event Maximum Recoveries: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of a Motor Over Speed performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Motor Over Speed event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 163

MNCMECRF-07 153
Object Dictionary / Drive Configuration
2068.17h Event Maximum Recoveries: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of At Command performs the action assigned to this event. Each time the event is removed for longer than the addition of 
the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the maximum 
recovery count allowed before the At Command event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.18h Event Maximum Recoveries: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Zero Velocity performs the action assigned to this event. Each time the event is removed for longer than the addition of 
the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the maximum 
recovery count allowed before the Zero Velocity event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.19h Event Maximum Recoveries: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Velocity Following Error performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Velocity Following Error event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.1Ah Event Maximum Recoveries: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Positive Velocity Limit performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Positive Velocity Limit event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 164

MNCMECRF-07 154
Object Dictionary / Drive Configuration
2068.1Bh Event Maximum Recoveries: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Negative Velocity Limit performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Negative Velocity Limit event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.1Ch Event Maximum Recoveries: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Max Measured Position performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Max Measured Position event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.1Dh Event Maximum Recoveries: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Min Measured Position performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Min Measured Position event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.1Eh Event Maximum Recoveries: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of At Home Position performs the action assigned to this event. Each time the event is removed for longer than the addition 
of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the At Home Position event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 165

MNCMECRF-07 155
Object Dictionary / Drive Configuration
2068.1Fh Event Maximum Recoveries: Position Following Errors
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Position Following Errors performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Position Following Errors event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.20h Event Maximum Recoveries: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Max Target Position performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Max Target Position event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information 
on event handling, see the Help file associated with the AMC drive configuration software.
2068.21h Event Maximum Recoveries: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Min Target Position performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Min Target Position event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on 
event handling, see the Help file associated with the AMC drive configuration software.
2068.22h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2068.23h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2068.24h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 166

MNCMECRF-07 156
Object Dictionary / Drive Configuration
2068.25h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2068.26h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2068.27h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
2068.28h Event Maximum Recoveries: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Communication Error performs the action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Communication Error event latches and must be actively reset in order to enable the bridge. 
Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more 
information on event handling, see the Help file associated with the AMC drive configuration software.
2068.29h Event Maximum Recoveries: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of User Stop performs the event action assigned to this event. Each time the event is removed for longer than the addition 
of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the User Stop event latches and must be actively reset in order to enable the bridge. Re-setting the 
recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information on event 
handling, see the Help file associated with the AMC drive configuration software.
2068.2Ah Event Maximum Recoveries: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of PWM and Direction Broken Wire performs the event action assigned to this event. Each time the event is removed for 
longer than the addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This 
object sets the maximum recovery count allowed before the PWM and Direction Broken Wire event latches and must be actively reset in 
order to enable the bridge. Re-setting the recovery counter requires a connection to the AMC drive configuration software appropriate for 
this drive. For more information on event handling, see the Help file associated with the AMC drive configuration software.

---
## Page 167

MNCMECRF-07 157
Object Dictionary / Drive Configuration
205Bh: Programmable Status Parameters   Determines which events will be mapped to 
the StatusWord (6041h) bits, indicated below. When multiple events are mapped to a single bit, 
they will be logically OR-ed.
TABLE 2.10 Programmable Status Mapping
2068.2Bh Event Maximum Recoveries: Motion Engine Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 65535 N/A Read / Write Yes
Description:
Each occurrence of Motion Engine Error performs the event action assigned to this event. Each time the event is removed for longer than the 
addition of the values in the Time-Out Window (2067h) and Recovery Time (2066h), a recovery counter is incremented. This object sets the 
maximum recovery count allowed before the Motion Engine Error event latches and must be actively reset in order to enable the bridge. Re-
setting the recovery counter requires a connection to the AMC drive configuration software appropriate for this drive. For more information 
on event handling, see the Help file associated with the AMC drive configuration software.
Programmable Status 
Mask Description
Bit 9 Bit 11 (Internal Limit Active) in 6041h (StatusWord)
Bit 10...13 Reserved
Bit 14 Bit 7 (Warning) in 6041h (StatusWord)
Bit 15 Bit 8 (manufacturer specific) in 6041h (StatusWord)
205B.01h Programmable Status Mask: Drive Reset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Drive Reset event. See Table 2.10 above for mapping structure.
205B.02h Programmable Status Mask: Drive Internal Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Drive Internal Error event. See Table 2.10 above for mapping structure.

---
## Page 168

MNCMECRF-07 158
Object Dictionary / Drive Configuration
205B.03h Programmable Status Mask: Short Circuit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Short Circuit event. See Table 2.10 above for mapping structure.
205B.04h Programmable Status Mask: Over Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Over Current event. See Table 2.10 above for mapping structure.
205B.05h Programmable Status Mask: Hardware Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Hardware Under Voltage event. See Table 2.10 above for mapping structure.
205B.06h Programmable Status Mask: Hardware Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Hardware Over Voltage event. See Table 2.10 above for mapping structure.
205B.07h Programmable Status Mask: Drive Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Drive Over Temperature event. See Table 2.10 above for mapping structure.
205B.08h Programmable Status Mask: Parameter Restore Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Parameter Restore Error event. See Table 2.10 above for mapping structure.

---
## Page 169

MNCMECRF-07 159
Object Dictionary / Drive Configuration
205B.09h Programmable Status Mask: Parameter Store Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Parameter Store Error event. See Table 2.10 above for mapping structure.
205B.0Ah Programmable Status Mask: Invalid Hall State
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Invalid Hall State event. See Table 2.10 above for mapping structure.
205B.0Bh Programmable Status Mask: Phase Synchronization Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A                                                 Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Phase Synchronization Error event. See Table 2.10 above for mapping structure.
205B.0Ch Programmable Status Mask: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Motor Over Temperature event. See Table 2.10 above for mapping structure.
205B.0Dh Programmable Status Mask: Phase Detection Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Phase Detection Fault event. See Table 2.10 above for mapping structure.
205B.0Eh Programmable Status Mask: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Feedback Sensor Error event. See Table 2.10 above for mapping structure.

---
## Page 170

MNCMECRF-07 160
Object Dictionary / Drive Configuration
205B.0Fh Programmable Status Mask: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Log Entry Missed event. See Table 2.10 above for mapping structure.
205B.10h Programmable Status Mask: Software Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Software Disable Event. See Table 2.10 above for mapping structure.
205B.11h Programmable Status Mask: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Disable Event. See Table 2.10 above for mapping structure.
205B.12h Programmable Status Mask: Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Positive Limit event. See Table 2.10 above for mapping structure.
205B.13h Programmable Status Mask: Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Negative Limit event. See Table 2.10 above for mapping structure.
205B.14h Programmable Status Mask: Current Limiting (Foldback)
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Current Limiting event. See Table 2.10 above for mapping structure.

---
## Page 171

MNCMECRF-07 161
Object Dictionary / Drive Configuration
205B.15h Programmable Status Mask: Continuous Current Limit Reached
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Continuous Current Limit Reached event. See Table 2.10 above for mapping 
structure.
205B.16h Programmable Status Mask: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to Current Loop Saturated event. See Table 2.10 above for mapping structure.
205B.17h Programmable Status Mask: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Under Voltage event. See Table 2.10 above for mapping structure.
205B.18h Programmable Status Mask: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Over Voltage event. See Table 2.10 above for mapping structure.
205B.19h Programmable Status Mask: Non-sinusoidal Commutation
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Non-sinusoidal Commutation event. See Table 2.10 above for mapping structure.
205B.1Ah Programmable Status Mask: Phase Detection
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Phase Detection event. See Table 2.10 above for mapping structure.

---
## Page 172

MNCMECRF-07 162
Object Dictionary / Drive Configuration
205B.1Bh Programmable Status Mask: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Auxiliary Disable event. See Table 2.10 above for mapping structure.
205B.1Ch Programmable Status Mask: Shunt Regulator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Shunt Regulator event. See Table 2.10 above for mapping structure.
205B.1Dh Programmable Status Mask: Phase Detection Complete
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Phase Detection Complete event. See Table 2.10 above for mapping structure.
205B.1Eh Programmable Status Mask: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Command Limiter Active event. See Table 2.10 above for mapping structure.
205B.1Fh Programmable Status Mask: Motor Over Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Motor Over Speed event. See Table 2.10 above for mapping structure.
205B.20h Programmable Status Mask: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the At Command event. See Table 2.10 above for mapping structure.

---
## Page 173

MNCMECRF-07 163
Object Dictionary / Drive Configuration
205B.21h Programmable Status Mask: Zero Velocity
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Zero Velocity event. See Table 2.10 above for mapping structure.
205B.22h Programmable Status Mask: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Velocity Following Error event. See Table 2.10 above for mapping structure.
205B.23h Programmable Status Mask: Positive Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Positive Velocity Limit event. See Table 2.10 above for mapping structure.
205B.24h Programmable Status Mask: Negative Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Negative Velocity Limit event. See Table 2.10 above for mapping structure.
205B.25h Programmable Status Mask: Max Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Max Measured Position event. See Table 2.10 above for mapping structure.
205B.26h Programmable Status Mask: Min Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Min Measured Position Limit event. See Table 2.10 above for mapping structure.

---
## Page 174

MNCMECRF-07 164
Object Dictionary / Drive Configuration
205B.27h Programmable Status Mask: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the At Home Position event. See Table 2.10 above for mapping structure.
205B.28h Programmable Status Mask: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Position Following Error event. See Table 2.10 above for mapping structure.
205B.29h Programmable Status Mask: Max Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Max Target Position Limit event. See Table 2.10 above for mapping structure.
205B.2Ah Programmable Status Mask: Min Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Min Target Position Limit event. See Table 2.10 above for mapping structure.
205B.2Bh Programmable Status Mask: Set Measured Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Set Measured Position event. See Table 2.10 above for mapping structure.
205B.2Ch Programmable Status Mask: Homing Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Homing Active event. See Table 2.10 above for mapping structure.

---
## Page 175

MNCMECRF-07 165
Object Dictionary / Drive Configuration
205B.2Dh Programmable Status Mask: Apply Brake
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Apply Brake event. See Table 2.10 above for mapping structure.
205B.2Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.2Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.30h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.31h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.32h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.33h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
205B.34h Programmable Status Mask: Communication Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Communication Error Mask event. See Table 2.10 above for mapping structure.

---
## Page 176

MNCMECRF-07 166
Object Dictionary / Drive Configuration
205B.35h Programmable Status Mask: Homing Complete
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Homing Complete event. See Table 2.10 above for mapping structure.
205B.36h Programmable Status Mask: Commanded Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Commanded Stop event. See Table 2.10 above for mapping structure.
205B.37h Programmable Status Mask: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Stop event. See Table 2.10 above for mapping structure.
205B.38h Programmable Status Mask: Bridge Enabled
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Bridge Enabled event. See Table 2.10 above for mapping structure.
205B.39h Programmable Status Mask: Dynamic Brake Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Dynamic Brake Active event. See Table 2.10 above for mapping structure.
205B.3Ah Programmable Status Mask: Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Stop Active event. See Table 2.10 above for mapping structure.

---
## Page 177

MNCMECRF-07 167
Object Dictionary / Drive Configuration
205B.3Bh Programmable Status Mask: Positive Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Positive Stop Active event. See Table 2.10 above for mapping structure.
205B.3Ch Programmable Status Mask: Negative Stop Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Negative Stop Active event. See Table 2.10 above for mapping structure.
205B.3Dh Programmable Status Mask: Positive Inhibit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Positive Inhibit event. See Table 2.10 above for mapping structure.
205B.3Eh Programmable Status Mask: Negative Inhibit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Negative Inhibit event. See Table 2.10 above for mapping structure.
205B.3Fh Programmable Status Mask: User Bit 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 0 event. See Table 2.10 above for mapping structure.
205B.40h Programmable Status Mask: User Bit 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 1 event. See Table 2.10 above for mapping structure.

---
## Page 178

MNCMECRF-07 168
Object Dictionary / Drive Configuration
205B.41h Programmable Status Mask: User Bit 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 2 event. See Table 2.10 above for mapping structure.
205B.42h Programmable Status Mask: User Bit 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 3 event. See Table 2.10 above for mapping structure.
205B.43h Programmable Status Mask: User Bit 4
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 4 event. See Table 2.10 above for mapping structure.
205B.44h Programmable Status Mask: User Bit 5
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 5 event. See Table 2.10 above for mapping structure.
205B.45h Programmable Status Mask: User Bit 6
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 6 event. See Table 2.10 above for mapping structure.
205B.46h Programmable Status Mask: User Bit 7
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 7 event. See Table 2.10 above for mapping structure.

---
## Page 179

MNCMECRF-07 169
Object Dictionary / Drive Configuration
205B.47h Programmable Status Mask: User Bit 8
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 8 event. See Table 2.10 above for mapping structure.
205B.48h Programmable Status Mask: User Bit 9
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 9 event. See Table 2.10 above for mapping structure.
205B.49h Programmable Status Mask: User Bit 10
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 10 event. See Table 2.10 above for mapping structure.
205B.4Ah Programmable Status Mask: User Bit 11
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 11 event. See Table 2.10 above for mapping structure.
205B.4Bh Programmable Status Mask: User Bit 12
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 12 event. See Table 2.10 above for mapping structure.
205B.4Ch Programmable Status Mask: User Bit 13
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 13 event. See Table 2.10 above for mapping structure.

---
## Page 180

MNCMECRF-07 170
Object Dictionary / Drive Configuration
205B.4Dh Programmable Status Mask: User Bit 14
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 14 event. See Table 2.10 above for mapping structure.
205B.4Eh Programmable Status Mask: User Bit 15
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the User Bit 15 event. See Table 2.10 above for mapping structure.
205B.4Fh Programmable Status Mask: Capture 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Capture 1 event. See Table 2.10 above for mapping structure.
205B.50h Programmable Status Mask: Capture 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Capture 2 event. See Table 2.10 above for mapping structure.
205B.51h Programmable Status Mask: Capture 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Capture 3 event. See Table 2.10 above for mapping structure.
205B.52h Programmable Status Mask: Commanded Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Commanded Positive Limit event. See Table 2.10 above for mapping structure.

---
## Page 181

MNCMECRF-07 171
Object Dictionary / Drive Configuration
205B.53h Programmable Status Mask: Commanded Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Commanded Negative Limit event. See Table 2.10 above for mapping structure.
205B.54h Programmable Status Mask: Safe Torque Off Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Safe Torque Off Active event. See Table 2.10 above for mapping structure.
205B.55h Programmable Status Mask: Zero Position Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Zero Position Error event. See Table 2.10 above for mapping structure.
205B.56h Programmable Status Mask: Motion Engine Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Motion Engine Error event. See Table 2.10 above for mapping structure.
205B.57h Programmable Status Mask: Motion Engine Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Motion Engine Active event. See Table 2.10 above for mapping structure.
205B.58h Programmable Status Mask: Active Motion Execute
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Execute event. See Table 2.10 above for mapping structure.

---
## Page 182

MNCMECRF-07 172
Object Dictionary / Drive Configuration
205B.59h Programmable Status Mask: Active Motion Busy
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Busy event. See Table 2.10 above for mapping structure.
205B.5Ah Programmable Status Mask: Active Motion Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Active event. See Table 2.10 above for mapping structure.
205B.5Bh Programmable Status Mask: Active Motion MotionDone
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion MotionDone event. See Table 2.10 above for mapping structure.
205B.5Ch Programmable Status Mask: Active Motion SequenceDone
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion SequenceDone event. See Table 2.10 above for mapping structure.
205B.5Dh Programmable Status Mask: Active Motion Done
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Done event. See Table 2.10 above for mapping structure.
205B.5Eh Programmable Status Mask: Active Motion Aborted
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Aborted event. See Table 2.10 above for mapping structure.

---
## Page 183

MNCMECRF-07 173
Object Dictionary / Drive Configuration
208Ch: Product Information   
205B.5Fh Programmable Status Mask: Active Motion Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Active Motion Error event. See Table 2.10 above for mapping structure.
205B.60h Programmable Status Mask: PWM and Direction Broken Wire
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the PWM and Direction Broken Wire event. See Table 2.10 above for mapping 
structure.
205B.61h Programmable Status Mask: Motion Engine Abort
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] N/A Read / Write Yes
Description:
Specifies which StatusWord bit, if any, is assigned to the Motion Engine Abort event. See Table 2.10 above for mapping structure.
208C.01h Hardware Information
Data Type Data Range Units Accessibility Stored to NVM
String(352) ASCII N/A Read Only Yes
Description:
Provides all the drive information in a single 384-byte string. The meaning of each byte in the string is divided into sections according to the 
following table. Bytes 2 through 33 provide the “Control Board Name” for example. 
Byte Definitions Description
0...1 Reserved
2...33 Control Board Name
34...65 Control Board Version
66...97 Control Board Serial Number
98...129 Control Board Build Date
130...161 Control Board Build Time
162...191 Reserved
192...223 Product Part Number (including revision letter)
224...255 Product Version
256...287 Product Serial Number
288...319 Product Build Date
320...351 Product Build Time
352...383 Reserved

---
## Page 184

MNCMECRF-07 174
Object Dictionary / Drive Configuration
208Dh: Firmware Information   
20D8h: Power Board Information   
208D.01h Firmware Version
Data Type Data Range Units Accessibility Stored to NVM
String(32) ASCII N/A Read Only Yes
Description:
Returns a 32-byte string containing the firmware version that is currently running on the drive.
208D.02h Bootloader Version
Data Type Data Range Units Accessibility Stored to NVM
String(32) ASCII N/A Read Only Yes
Description:
Returns a 32-byte string containing the bootloader version that is currently running on the drive.
208D.03h FPGA-Image Version
Data Type Data Range Units Accessibility Stored to NVM
String(32) ASCII N/A Read Only Yes
Description:
Returns a 32-byte string containing the FPGA-image version that is currently running on the drive.
20D8.01h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.02h Name
Data Type Data Range Units Accessibility Stored to NVM
String(32) N/A N/A Read Only Yes
20D8.03h Version
Data Type Data Range Units Accessibility Stored to NVM
String(32) N/A N/A Read Only Yes

---
## Page 185

MNCMECRF-07 175
Object Dictionary / Drive Configuration
20D8.04h Serial Number
Data Type Data Range Units Accessibility Stored to NVM
String(32) N/A N/A Read Only Yes
20D8.05h Build Date
Data Type Data Range Units Accessibility Stored to NVM
String(32) N/A N/A Read Only Yes
20D8.06h Build Time
Data Type Data Range Units Accessibility Stored to NVM
String(32) N/A N/A Read Only Yes
20D8.07h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.08h DC Bus Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBV Read Only Yes
20D8.09h DC Bus Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBV Read Only Yes
20D8.0Ah Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read Only Yes
20D8.0Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Integer32 N/A N/A Read Only Yes

---
## Page 186

MNCMECRF-07 176
Object Dictionary / Drive Configuration
20D8.0Ch Maximum Peak Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBC Read Only Yes
20D8.0Dh Maximum Continuous Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBC Read Only Yes
20D8.0Eh Maximum Peak Current Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBT Read Only Yes
20D8.0Fh Maximum Peak To Continuous Current Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] PBT Read Only Yes
20D8.10h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.11h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.12h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.13h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.14h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 187

MNCMECRF-07 177
Object Dictionary / Drive Configuration
20D8.15h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.16h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.17h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.18h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.19h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Ah Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.1Fh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 188

MNCMECRF-07 178
Object Dictionary / Drive Configuration
20D8.20h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Integer16 N/A N/A Read Only Yes
20D8.21h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.22h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.23h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.24h Switching Frequency
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A PBF Read Only Yes
20D8.25h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.26h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.27h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.28h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.29h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 189

MNCMECRF-07 179
Object Dictionary / Drive Configuration
20D8.2Ah Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.2Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.2Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes
20D8.2Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only Yes

---
## Page 190

MNCMECRF-07 180
Object Dictionary / Drive Operation Objects
2.5 Drive Operation Objects
The following objects are typically used during operation. They are either used to perform 
specific tasks or to obtain information from the drive. These objects have been divided into the 
following three categories: Control Objects, Command Objects, and Monitor Objects.

---
## Page 191

MNCMECRF-07 181
Object Dictionary / Drive Operation Objects
2.5.1 Control Objects
6040h: ControlWord   
6040h ControlWord
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - 65535 N/A Read / Write No
Description:
The ControlWord object sets the control state machine in the drive. “State Machine Overview” on page 10 explains each drive state and how 
to use the ControlWord to move the drive to that state. Below is a table providing the basic ControlWord commands and bit field definitions.
See “ControlWord (6040h)” on page 13 for more information on this subject.
Value (Hex) Command Description
80 Reset Fault On any transition to "1" of bit 7 causes a Reset Fault
04 Disable Voltage Drive in "Switch On Disabled" state
06 Shutdown Drive in "Ready to Switch On" state
07 Switch On Drive in "Switched On" state
0F Enable Operation Drive in "Operation Enabled" state
02 Stop Drive in "Stop Active" state
1F Start Homing Starts Homing (when in homing mode)
0F End Homing Ends Homing
Bit Name Description
0 Switch On A transition from 0 to 1 commands the state machine into the Switched On state.
1 Disable Voltage A transition from 0 to 1 commands the state machine into the Switch On Disabled State.
2 Quick Stop A value of 0 activates a commanded stop.
3 Enable Operation A transition from 0 to 1 commands the state machine into Operation Enabled state.
4 Mode Specific 1 In Jog Mode, Jog Select 0: Writing a 1 sets bit 0 of the Jog Speed Select. Writing a 0 clears it.
In Homing, Home Execute: Writing a 1 causes the homing routine to be active. Writing a 0 ends it.
5 Mode Specific 2 In Jog Mode, Jog Plus: Writing a 1 asserts Jog Plus. Writing a 0 deasserts Jog Plus.
6 Mode Specific 3 In Jog Mode, Jog Minus: Writing a 1 asserts Jog Minus. Writing a 0 deasserts Jog Minus.
7 Reset Fault A transition from 0 to 1 activates a fault reset.
8 Reserved Read as zero / write as zero.
9 Mode Specific 4 In Jog Mode, Jog Select 1: Writing a 1 sets bit 1 of the Jog Speed Select. Writing a 0 clears it.
10 Reserved Read as zero / write as zero.
11 Dynamic Brake Activates the Dynamic Brake
12 Commanded Negative Limit Activates negative limiting.
13 Commanded Positive Limit Activates positive limiting.
14-15 Reserved Read as zero / write as zero.

---
## Page 192

MNCMECRF-07 182
Object Dictionary / Drive Operation Objects
2001h: Control Parameters   
2001.01h Drive Control Word 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 1FFFh N/A Read/Write* No
Description:
This bit field enables/disables certain drive functions according to the table below.
2001.02h Drive Control Word 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 1FFFh N/A Read/Write* No
Description:
This bit field enables/disables certain drive functions according to the table below.
Bit Name Description
0 Reserved Read as zero / write as zero.
1 Zero Position Error Sets the target position equal to the measured position.
2 Phase Detect Activates the phase detection routine.
3 Set Position Causes the position counter to be loaded with the preset position value.
4 Reserved Read as zero / write as zero.
5 Reserved Read as zero / write as zero.
6 Reserved Read as zero / write as zero.
7 Capture 1 Arm A change from 0 to 1 arms/rearms Capture unit 1. A change from 1 to 0 Disarms it.
8 Capture 2 Arm A change from 0 to 1 arms/rearms Capture unit 2. A change from 1 to 0 Disarms it.
9 Capture 3 Arm A change from 0 to 1 arms/rearms Capture unit 3. A change from 1 to 0 Disarms it.
10 Reserved Read as zero / write as zero.
11 Reserved Read as zero / write as zero.
12 Reset Events Resets all but the following events: Over Current, Parameter Restore Error, Parameter Store Error, 
Phase Detection Failure, Software Disable
13-15 Reserved Read as zero / write as zero.
Bit Name Description
0 Gain Parameters Set A change from 0 to 1 selects Gain Set 1. A change from 1 to 0 selects Gain Set 0.
1 Command Limiter Parameters Set A change from 0 to 1 selects Command Limiter Set 1. A change from 1 to 0 selects Command 
Limiter Set 0.
2 Command Source Modifier Set A change from 0 to 1 selects Source Modifier Set 1. A change from 1 to 0 selects Source Modifier 
Set 0.
3-15 Reserved Read as zero / write as zero.

---
## Page 193

MNCMECRF-07 183
Object Dictionary / Drive Operation Objects
2001.03h User Bit Control
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – FFFFh N/A Read / Write No
Description:
Toggles the User Bits on or off by assigning a 1 or 0 to the appropriate bit. See the table below for bit assignment. Note that User Bits can be 
mapped to digital outputs through the configuration software or by directly configuring command 2024h.
Bit Assignment (1 = asserted, 0 = not asserted)
0 User Bit 0
1 User Bit 1
2 User Bit 2
3 User Bit 3
4 User Bit 4
5 User Bit 5
6 User Bit 6
7 User Bit 7
8 User Bit 8
9 User Bit 9
10 User Bit 10
11 User Bit 11
12 User Bit 12
13 User Bit 13
14 User Bit 14
15 User Bit 15

---
## Page 194

MNCMECRF-07 184
Object Dictionary / Drive Operation Objects
6060h: Modes Of Operation   
2.5.2 Command Objects
6071h: Target Current   
60FFh: Target Velocity   
6060h Modes Of Operation
Data Type Data Range Units Accessibility Stored to NVM
Integer8 0 - 255 N/A Read / Write No
Description:
This object indicates the requested mode of operation. This may differ from the actual mode of operation if the mode change is not yet 
possible (for example, if the mode change is requested while the drive is in the operation enabled state). The actual mode of operation can 
be found using the read-only object 6061. “Modes of Operation” on page 22 explains the valid control loop configurations for an AMC servo 
drive.
6071h Target Current
Data Type Data Range Units Accessibility Stored to NVM
Integer16 -215 – (215-1) DC2 Read / Write No
Description:
Sets the Target Current while in Current Mode (set by object 6060h). See “Appendix” on page 225 for units conversion.
60FFh Target Velocity
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) DS1 Read / Write No
Description:
Use this object to set the Target Velocity when the drive is in Velocity mode. See “Appendix” on page 225 for unit conversion.
Value Operation Mode
1 Profile Position Mode
3 Profile Velocity Mode
4 Profile Torque Mode (current mode)
6 Homing Mode
7 Interpolated Position Mode (PVT)
8 Cyclic Synchronous Position Mode
9 Cyclic Synchronous Velocity Mode
A Cyclic Synchronous Torque Mode (current mode)
8C Jog Mode
9E Config 0
DE Config 1
EC Motion Engine Mode
FF None (Use active configuration settings)

---
## Page 195

MNCMECRF-07 185
Object Dictionary / Drive Operation Objects
607Ah: Target Position   
60B1h: Velocity Offset   
60B2h: Current Offset   
2045h: Interface Inputs   Interface inputs can be used in place of analog inputs for any function 
that can be assigned to an analog input. Examples of this include command source, feedback 
source, and motor temperature source. The units for interface inputs are dependent upon the 
function the interface input is assigned to as given in Table 2.11. For details on unit conversion 
see “Appendix” on page 225.
607Ah Target Position
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) counts Read / Write No
Description:
Sets the Target Position value while in position mode (set by object 6060h). This is the target position before limiting and profiling is applied. 
Position error is derived from demanded position, which is this signal after limiting and profiling is applied.
60B1h Velocity Offset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 -231 – (231-1) DS1 Read / Write No
Description:
Contains a value corresponding to offset for the target velocity value. Used with cyclic synchronous position and cyclic synchronous velocity 
modes. In cyclic synchronous position mode, this object contains the input value for velocity feed forward. In cyclic synchronous velocity 
mode it contains the commanded velocity offset.
60B2h Current Offset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 -214 – (214-1) DC2 Read / Write No
Description:
Contains a value corresponding to offset for the target current value. Used with cyclic synchronous modes of operation. In cyclic 
synchronous position mode and cyclic synchronous velocity mode, this object contains the input value for current feed forward. In cyclic 
synchronous torque mode it contains the commanded current offset.

---
## Page 196

MNCMECRF-07 186
Object Dictionary / Drive Operation Objects
TABLE 2.11 Interface Input Units
Interface Input Function Units
Position Command Source counts
Velocity Command Source DS1
Torque/Current Command Source DC2
Position Feedback Source counts
Velocity Feedback Source DS1
Motor Temperature Source DT1
2045.01h Interface Input 1
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.11 Read / Write No
Description:
Defines the value used with interface input 1.
2045.02h Interface Input 2
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.11 Read / Write No
Description:
Defines the value used with interface input 2.
2045.03h Interface Input 3
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.11 Read / Write No
Description:
Defines the value used with interface input 3.
2045.04h Interface Input 4
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.11 Read / Write No
Description:
Defines the value used with interface input 4.

---
## Page 197

MNCMECRF-07 187
Object Dictionary / Drive Operation Objects
2.5.3 Motion Engine Command Objects
20C9h: Motion Engine Control   
20CAh: Dynamic Index Data   
20C9.01h Start-Up Motion Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 N/A N/A Read / Write Yes
Description:
Defines the startup behavior when running a motion engine index upon power-up. The bit values are broken up as defined below.
Bits 0:15 - Enumerated values
0: Select Motion (This enum is only used when motion is initiated via a digital input.)
1: Initiate Selected Motion (Run the index or sequence specified in the Motion Engine Control Data)
2: Abort Active Motion (No fault, Motion Engine will return to ready for motion start)
3: Reserved. Write zero.
4: Initiate Dynamic Index
5: Set Motion Select Source
6: Indexer / Sequencer Select
7-15: Reserved
Bits 16:31 - This is the data that is associated with each of the action enums above. The allowable values for each enum are as 
follows
0: Select Index - When the communication channel is the motion select source, the valid range is [0,15], otherwise it is an error
1: Initiate Selected Motion - When the communication channel is the motion select source, this value will be the motion that is initiated. 
Otherwise it will be ignored.
2: Abort Active Motion - Values are ignored
3: Reserved. Write zero.
4: Initiate Dynamic Index - Values are ignored
5: Set Motion Select Source - 0:Hardware, 1:Communication Channel - all other values are invalid
6: Indexer / Sequencer Select - When the communication channel is the motion select source, this value will be the motion type that is 
selected. Valid values are 0: Indexer, 1: Sequencer - all other values are invalid
7-15: Reserved
20CA.01h Move Index
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh - Read / Write No
Description:
When defining a dynamic index, this value should be set to 0x0020.

---
## Page 198

MNCMECRF-07 188
Object Dictionary / Drive Operation Objects
20CA.02h Move Type
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh - Read / Write No
Description:
Defines the type of move. 
20CA.03h Repeat Count
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh - Read / Write No
Description:
Specifies the number of times to repeat the move. Only valid for relative moves.
20CA.04h Dwell Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh milliseconds (ms) Read / Write No
Description:
Specifies the time after the move is complete before the Index Done status becomes active.
20CA.05h Position Target - Word 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh counts Read / Write No
Description:
The least significant word in the 2-word (32-bit) position command. Depending on the assigned move type, will apply to an absolute or 
relative position target.
20CA.06h Position Target - Word 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh counts Read / Write No
Description:
The most significant word in the 2-word (32-bit) position command. Depending on the assigned move type, will apply to an absolute or 
relative position target.
Value Move Type
0x0008 Absolute
0x0018 Relative

---
## Page 199

MNCMECRF-07 189
Object Dictionary / Drive Operation Objects
20CA.07h Max Velocity - Word 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DS3 Read / Write No
Description:
The least significant word in the 4-word (64-bit) maximum velocity value. See “Appendix” on page 225 for unit conversion.
20CA.08h Max Velocity - Word 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DS3 Read / Write No
Description:
The second word in the 4-word (64-bit) maximum velocity value. See “Appendix” on page 225 for unit conversion.
20CA.09h Max Velocity - Word 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DS3 Read / Write No
Description:
The third word in the 4-word (64-bit) maximum velocity value. See “Appendix” on page 225 for unit conversion.
20CA.0Ah Max Velocity - Word 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DS3 Read / Write No
Description:
The most significant word in the 4-word (64-bit) maximum velocity value. See “Appendix” on page 225 for unit conversion.
20CA.0Bh Max Acceleration - Word 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DA5 Read / Write No
Description:
The least significant word in the 2-word (32-bit) maximum acceleration value. See “Appendix” on page 225 for unit conversion.
20CA.0Ch Max Acceleration - Word 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DA5 Read / Write No
Description:
The most significant word in the 2-word (32-bit) maximum acceleration value. See “Appendix” on page 225 for unit conversion.

---
## Page 200

MNCMECRF-07 190
Object Dictionary / Drive Operation Objects
2.5.4 Monitor Objects
6041h: StatusWord   
20CA.0Dh Max Deceleration - Word 0
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DA5 Read / Write No
Description:
The least significant word in the 2-word (32-bit) maximum deceleration value. See “Appendix” on page 225 for unit conversion.
20CA.0Eh Max Deceleration - Word 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - FFFFh DA5 Read / Write No
Description:
The most significant word in the 2-word (32-bit) maximum deceleration value. See “Appendix” on page 225 for unit conversion.
20CA.0Fh - 
20CA.1Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 - - - No
6041h StatusWord
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - 655535 N/A Read Only No
Description:
The StatusWord is used to determine which state the drive is in. “Drive States” on page 11 explains each drive’s state and the StatusWord bit 
definitions. Below is a table of the hex values for each state.
Value State Description
xxxx xxxx x0xx 0000 Not Ready to Switch On Drive is initializing, drive is disabled
xxxx xxxx x1xx 0000 Switch On Disabled Drive completed initialization, drive is 
disabled
xxxx xxxx x01x 0001 Ready to Switch On Bus power may be applied, drive is 
disabled
xxxx xxxx x01x 0011 Switched On Bus power is applied, drive is disabled
xxxx xxxx x01x 0111 Operation Enabled Drive is enabled
xxxx xxxx x0xx 1111 Fault Reaction Active Drive will execute fault reaction event
xxxx xxxx x0xx 1000 Fault Drive is in the fault state
xxxx xxxx x00x 0111 Stop Active  Stop received from host and now in 
this state

---
## Page 201

MNCMECRF-07 191
Object Dictionary / Drive Operation Objects
2002h: Drive Status   
2002.01h Drive Bridge Status
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.
2002.02h Drive Protection Status
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.
2002.03h System Protection Status
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.
2002.04h Drive/System Status 1
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.
2002.05h Drive/System Status 2
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.

---
## Page 202

MNCMECRF-07 192
Object Dictionary / Drive Operation Objects
2002.06h Drive/System Status 3
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.
2002.07h Active Configuration Status
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
Description:
The function of each bit is given in Table 2.12 below.

---
## Page 203

MNCMECRF-07 193
Object Dictionary / Drive Operation Objects
TABLE 2.12 Drive Status bit-field definitions
Bit
Drive 
Bridge 
Status
Drive 
Protection 
Status
System 
Protection 
Status
Drive
System 
Status 1
Drive
System
Status 2
Drive
System 
Status 3
Active
Configuration
Status
0 Bridge 
Enabled
Drive Reset Parameter 
Restore Error
Log Entry 
Missed
Zero Velocity Reserved Absolute Position 
Valid
1 Dynamic 
Brake 
Enabled
Drive 
Internal Error
Parameter 
Store Error
Software 
Disable
At Command Reserved Positive Stop 
Active
2 Stop Enabled Short Circuit Invalid Hall 
State
User Disable Velocity 
Following Error
Reserved Negative Stop 
Active
3 Positive Stop 
Enabled
Over Current Phase Sync. 
Error
User Positive 
Inhibit
Positive Target 
Velocity Limit
Reserved Reserved
4 Negative 
Stop Enabled
Under 
Voltage
Motor Over 
Temperature
User 
Negative 
Inhibit
Negative Target 
Velocity Limit
Reserved Reserved
5 Positive 
Torque Inhibit 
Active
Over Voltage Phase 
Detection 
Fault
Current 
Limiting
Command 
Limiter Active
Reserved Reserved
6 Negative 
Torque Inhibit 
Active
Drive Over 
Temperature
Feedback 
Sensor Error
Continuous 
Current 
Foldback
In Home Position Commanded 
Stop
Reserved
7 External 
Brake Active
Reserved Motor Over 
Speed
Current Loop 
Saturated
Position 
Following Error
User Stop Reserved
8 Reserved Reserved Max 
Measured 
Position
User Under 
Voltage
Max Target 
Position Limit
Capture 1 
Active
Reserved
9 Reserved Reserved Min 
Measured 
Position
User Over 
Voltage
Min Target 
Position Limit
Capture 2 
Active
Reserved
10 Reserved Reserved Comm. Error 
(Node 
Guarding)
Non-
sinusoidal 
Commutation
Set Position Capture 3 
Active
Reserved
11 Reserved Reserved PWM Input 
Broken Wire
Phase Detect 
Active
Reserved Commanded 
Positive Limit
Reserved
12 Reserved Reserved Motion 
Engine Error
Motion 
Engine Active
Homing Active Commanded 
Negative Limit
Reserved
13 Reserved Reserved Motion 
Engine Abort
User 
Auxiliary 
Disable
Safe Torque Off 
Status
Reserved Reserved
14 Reserved Reserved Reserved Shunt 
Regulator
Homing 
Complete
Reserved Reserved
15 Reserved Reserved Reserved Phase Detect 
Done
Zero Position 
Error
Reserved Reserved

---
## Page 204

MNCMECRF-07 194
Object Dictionary / Drive Operation Objects
2003h: Drive Status History   
2003.01h Drive Bridge Status History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.
2003.02h Drive Protection Status History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.
2003.03h System Protection Status History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.
2003.04h Drive/System Status 1 History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.

---
## Page 205

MNCMECRF-07 195
Object Dictionary / Drive Operation Objects
2029h: Motion Engine Status   
2003.05h Drive/System Status 2 History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.
2003.06h Drive/System Status 3 History
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only* No
Description:
If an event becomes active and then becomes inactive, Drive Status History will mark the event with a history bit. If a bit is 1, that event has 
occurred sometime in the past; 0 indicates the event has never occurred since power-up. The function of each bit is given in Table 2.12 of 
object 2002h.
 *Features a Read / Write function, in that any history bit can be cleared by writing a 1 to that bit.
2029.01h Active Sequence
Data Type Data Range Units Accessibility Stored to NVM
N/A -2 - 15 N/A Read Only No
Description:
Displays the active sequence number when using motion engine sequencing.
Bits 0:7
0-15 for index 0 to 15
FE: Dynamic Index
FF: No Invalid Index
Bits 8:15
Reserved
2029.02h Reserved
Data Type Data Range Units Accessibility Stored to NVM
N/A Read Only No

---
## Page 206

MNCMECRF-07 196
Object Dictionary / Drive Operation Objects
2029.03h Reserved
Data Type Data Range Units Accessibility Stored to NVM
N/A Read Only No
2029.04h Motion Engine Status
Data Type Data Range Units Accessibility Stored to NVM
N/A 0 - 9 N/A Read Only No
Description:
Defines the present state of the motion engine. 
Bits Value Motion Engine State
0 - 7
0 Inactive
1 Waiting for Motion Start (Motion Engine is enabled and ready for an index)
2 Executing Motion (Index is currently running)
3 Program Load in Progress (Motion Engine is not ready for commanded index)
4 Program Load Failure - CRC Error (Problem loading Index. Must reset Motion Engine to continue)
5 Halt Asserted (Motion has been interrupted)
6 Single Step Active
7 Break Point Active
8 - 15
0 No Errors
1 Invalid Data Parameter (Problem loading Index. Must reset Motion Engine to continue)
2 Invalid Op-Code (Problem loading Index. Must reset Motion Engine to continue)
3 Invalid Op-code for Dynamic Motion (Problem with index parameters)
4 Invalid Reference Frame (Problem with index parameters)
5 Invalid Bridge State (Bridge must be enabled to begin indexed motion)
6 User Defined Fault

---
## Page 207

MNCMECRF-07 197
Object Dictionary / Drive Operation Objects
6061h: Modes Of Operation Display   
200Eh: Feedback Sensor Values   
6061h Modes Of Operation Display
Data Type Data Range Units Accessibility Stored to NVM
Integer8 0 - 255 N/A Read Only No
Description:
A “Mode Of Operation” refers to how the drive’s internal control loops are configured. “Modes of Operation” on page 22 explains the valid 
control loop configurations for an AMC CANopen servo drive.
200E.01h Primary Encoder Counts
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the current number of encoder counts from the primary encoder. It is an absolute value in that it does not depend on the current 
load measured position or home values.
200E.02h Latched Encoder/Resolver Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned32 0 - [2(32) –1] counts Read Only No
Description:
Contains a value corresponding to the latched encoder/resolver position.
200E.03h Commutation Synchronization Counts
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains a value corresponding to the commutation synchronization counts.
Value Operation Mode
1 Profile Position Mode
3 Profile Velocity Mode
4 Profile Torque Mode (current mode)
6 Homing Mode
8 Cyclic Synchronous Position Mode
9 Cyclic Synchronous Velocity Mode
A Cyclic Synchronous Torque Mode
FF Custom Configured Modes

---
## Page 208

MNCMECRF-07 198
Object Dictionary / Drive Operation Objects
2027h: Feedback Hardware Diagnostics   
200E.04h Hall Sensor Values
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] N/A Read Only No
Description:
Contains a value corresponding to the Hall sensor values.
2027.01h Sin/Cos Encoder Sine
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] Volts (SF1) Read Only No
Description:
Represents the differential voltage of the +/- sine input of a 1V peak-to-peak encoder. Only applicable to drives that support Sin/Cos 
encoders. See “Appendix” on page 225 for information on scaling.
2027.02h Sin/Cos Encoder Cosine
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] Volts (SF1) Read Only No
Description:
Represents the differential voltage of the +/- cosine input of a 1V peak-to-peak encoder. Only applicable to drives that support Sin/Cos 
encoders. See “Appendix” on page 225 for information on scaling.
2027.03h Sin/Cos Encoder Health
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] Volts (SF1) Read Only No
Description:
Represents the health of the Sin/Cos encoder inputs according the formula below, where a value closer to 1 is healthy and a value closer to 
0 is unhealthy. See “Appendix” on page 225 for information on scaling.
Encoder Health = Sin2 + Cos2

---
## Page 209

MNCMECRF-07 199
Object Dictionary / Drive Operation Objects
2027.04h Absolute Encoder Fault Word
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(16) –1] N/A Read Only No
Description:
Contains a value that corresponds to an absolute encoder fault code. Fault codes are listed below by encoder type. The drive checks for 
faults and attempts to clear them during a phase detection routine. If a fault cannot be cleared, the appropriate fault code will be given by this 
sub-index and the drive will activate a feedback sensor error.
Hiperface (Stegmann):
EnDat (Heidenhein):
Status Value Status Name
00h No Error
01h Analog signals outside of specification
02h Internal angle offset erroneous
03h Data field partition destroyed
04h Analog limit is not available
05h Internal I^2C is not serviceable
06h Internal checksum error
07h Encoder reset occurred
08h Counter overflow
09h Parity error
0Ah Checksum of transmitted data is wrong
0Bh Unknown command code
0Ch Number of data transmitted is wrong
0Dh Command argument transmitted is impermissible
0Eh Data may not be written to the data field selected
0Fh Wrong access code
10h Size of specified data field cannot be changed
11h Specified word address outside data field
12h Access to non-existent data field
1Ch Monitoring the magnitude of the analog signals
1Dh Critical encoder current
1Eh Critical encoder temperature
1Fh Speed too high, position information not possible
20h Position of single turn impermissible
21h Position error, multi-turn
22h Position error, multi-turn
23h Position error, multi-turn
28h Error absolute value formation linear measuring system
Bit Fault Name
0 Light Source
1 Signal Amplitude
2 Position Value
3 Over Voltage
4 Under Voltage
5 Over Current
6 Battery
7-15 RFU

---
## Page 210

MNCMECRF-07 200
Object Dictionary / Drive Operation Objects
201Ch: Gearing Values   
201Eh: Auxiliary Encoder Value   
2027.05h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(16) –1] N/A Read Only No
2027.06h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(16) –1] N/A Read Only No
201C.01h Gear Input
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] Counts Read Only No
Description:
Contains a value corresponding to the number of encoder counts sent to the gearing module.
201C.02h Present Gear Input Counts
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Value corresponding to the denominator of the gear ratio.
201C.03h Present Gear Output Counts
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Value corresponding to the numerator of the gear ratio.
201E.01h Auxiliary Encoder Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) Counts Read Only No
Description:
Contains the raw number of counts seen on the auxiliary encoder input. This value resets to zero when the drive is power-cycled.

---
## Page 211

MNCMECRF-07 201
Object Dictionary / Drive Operation Objects
6077h: Actual Current   
2010h: Current Values   
201E.02h Auxiliary Position Index Capture Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) counts Read Only No
Description:
Contains the position of the last auxiliary encoder index captured by the drive. Requires auxiliary encoder with index.
6077h Actual Current
Data Type Data Range Units Accessibility Stored to NVM
Integer16 -215 – (215-1) DC1 Read Only No
Description:
Contains the instantaneous current applied to the motor. See “Appendix” on page 225 for units conversion.
2010.01h Current Target - Torque
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2 Read Only No
Description:
Contains the value of the target current (torque-producing). See “Appendix” on page 225 for unit conversion.
2010.02h Current Demand - Torque
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the value of the demand current (torque-producing). See “Appendix” on page 225 for unit conversion.
2010.03h Current Measured - Torque
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the value of the measured current (torque-producing). See “Appendix” on page 225 for unit conversion.

---
## Page 212

MNCMECRF-07 202
Object Dictionary / Drive Operation Objects
2010.04h Current Error - Torque
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the error between the target current and the measured current (torque-producing). This is equivalent to: demand current minus 
measured current. When the demand current is reached, the current error is zero. See “Appendix” on page 225 for unit conversion.
2010.05h Current Target - Flux
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2 Read Only No
Description:
Contains the value of the target current (flux-producing). See “Appendix” on page 225 for unit conversion.
2010.06h Current Demand - Flux
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the value of the demand current (flux-producing). See “Appendix” on page 225 for unit conversion.
2010.07h Current Measured - Flux
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the value of the measured current (flux-producing). See “Appendix” on page 225 for unit conversion.
2010.08h Current Error - Flux
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains the value of the Current error (flux-producing). See “Appendix” on page 225 for unit conversion.
2010.09h Current Target - Flux Reference
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2 Read Only No
Description:
Contains a value corresponding to the Current target flux reference. See “Appendix” on page 225 for unit conversion.

---
## Page 213

MNCMECRF-07 203
Object Dictionary / Drive Operation Objects
2010.0Ah Current Demand - Flux Reference
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read Only No
Description:
Contains a value corresponding to the current demand flux reference.
2010.0Bh Current Measured - Flux Reference
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read Only No
Description:
Contains a value corresponding to the current measured flux reference.
2010.0Ch Current Error - Flux Reference
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] N/A Read Only No
Description:
Contains a value corresponding to the current error flux reference.
2010.0Dh Current Limit
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] N/A Read Only No
Description:
Contains a value corresponding to the current limit.
2010.0Eh Current Measured - Phase A
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains a value corresponding to the current measured in phase A. See “Appendix” on page 225 for unit conversion.
2010.0Fh Current Measured - Phase B
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DC1 Read Only No
Description:
Contains a value corresponding to the current measured in phase B. See “Appendix” on page 225 for unit conversion.

---
## Page 214

MNCMECRF-07 204
Object Dictionary / Drive Operation Objects
606Bh: Velocity Demand   
2010.10h Phase Angle - Rotor
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 359 DG1 Read Only No
Description:
Contains a value corresponding to the Phase Angle – Rotor. See “Appendix” on page 225 for unit conversion.
2010.11h Phase Angle - Stator
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – 359 DG1 Read Only No
Description:
Contains a value corresponding to the Phase Angle – Stator. See “Appendix” on page 225 for unit conversion.
2010.12h Torque Summation Input
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2 Read Only No
Description:
Contains the raw current command before filtering or an offset has been applied. See “Appendix” on page 225 for unit conversion.
2010.13h Torque Summation Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2 Read Only No
Description:
Contains the offset of the commanded current in the current loop. See “Appendix” on page 225 for unit conversion.
606Bh Velocity Demand
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) DS1 Read Only No
Description:
Velocity Demand is defined as the target velocity, after limits and profiling, which is applied to the signal. This is the signal used by the 
velocity loop to produce a velocity error signal. See “Appendix” on page 225 for unit conversion.

---
## Page 215

MNCMECRF-07 205
Object Dictionary / Drive Operation Objects
606Ch: Actual Velocity   
606Dh: Velocity Window   
606Eh: Velocity Window Time   
6069h: Velocity Sensor Actual Value   
606Ch Actual Velocity
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) DS1 Read Only No
Description:
Actual Velocity is defined as the measured velocity, after conditioning, used to close the drive’s velocity loop. See “Appendix” on page 225 for 
unit conversion.
606Dh Velocity Window
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16) –1] DS1 Read / Write No
Description:
The maximum allowed difference between the target velocity and the velocity actual value. Bit 10 of the statusword shall be set to 1 (target 
reached) when the difference between the target velocity and velocity actual value is within the velocity window longer than the velocity 
window time. See “Appendix” on page 225 for unit conversion.
606Eh Velocity Window Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(15) –1] ms Read / Write Yes
Description:
The time delay after the occurrence of Velocity Following Error before its Event Action (2065h) is executed. The functionality of this object is 
identical to that of manufacturer-specific object 2064.12h.
6069h Velocity Sensor Actual Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) DS1 Read Only No
Description:
The value read from this object is the velocity measured directly from the primary feedback device before filtering or conditioning is applied. 
To read the actual velocity value used by the velocity control loop, see “606Ch: Actual Velocity”. See “Appendix” on page 225 for unit 
conversion.

---
## Page 216

MNCMECRF-07 206
Object Dictionary / Drive Operation Objects
2011h: Velocity Values   
2011.01h Velocity Measured Pre-Filter
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the measured velocity before the feedback cutoff filter. See “Appendix” on page 225 for unit conversion.
2011.02h Velocity Measured Post-Filter
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the measured velocity after the feedback cutoff filter. See “Appendix” on page 225 for unit conversion.
2011.03h Velocity Target
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the current velocity target when the drive is in velocity mode. See “Appendix” on page 225 for unit conversion.
2011.04h Velocity Demand
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the current velocity demand when the drive is in velocity mode. See “Appendix” on page 225 for unit conversion.
2011.05h Velocity Loop Error
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the error between the target velocity and the measured velocity. This is equivalent to target velocity minus measured velocity. When 
the current commanded velocity is reached, the velocity loop error will be zero. See “Appendix” on page 225 for unit conversion.
2011.06h Velocity Summation Input
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the raw velocity command before filtering or an offset has been applied. See “Appendix” on page 225 for unit conversion.

---
## Page 217

MNCMECRF-07 207
Object Dictionary / Drive Operation Objects
6064h: Actual Position   
2012h: Position Values   
2011.07h Velocity Summation Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DS1 Read Only No
Description:
Contains the offset of the commanded velocity in the velocity loop. See “Appendix” on page 225 for unit conversion.
6064h Actual Position
Data Type Data Range Units Accessibility Stored to NVM
Integer32 -231 – (231-1) counts Read Only No
Description:
Position Actual Value contains the measured position of the primary feedback device. This is the actual value used to create position error in 
position mode.
2012.01h Position Measured
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the current measured position in counts.
2012.02h Position Target
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the current commanded position when the drive is used in the position mode.
2012.03h Position Demand
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the current position demand in counts.

---
## Page 218

MNCMECRF-07 208
Object Dictionary / Drive Operation Objects
2014h: Command Limiter Input   
2012.04h Position Loop Error
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the error between the target position (in counts) and the measured position (in counts). This is equivalent to target position (counts) 
minus measured position (counts). When the current commanded position is reached, the position loop error will be zero.
2012.05h Position Summation Input
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the raw position command before filtering or an offset has been applied.
2012.06h Position Summation Offset
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the offset of the commanded position in the position loop.
2012.07h Position Index Capture Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the position of the last encoder index captured by the drive. Requires encoder with index.
2014.01h Input Command
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] N/A Read Only No
Description:
Contains a value corresponding to the input of the command limiter.

---
## Page 219

MNCMECRF-07 209
Object Dictionary / Drive Operation Objects
200Fh: Power Bridge Values   
200F.01h DC Bus Voltage
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(15)-1] DV1 Read Only No
Description:
Contains a value corresponding to the DC Bus Voltage. See “Appendix” on page 225 for unit conversions.
200F.02h Phase A Output Voltage
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DPV Read Only No
Description:
Contains a value corresponding to the Phase A Output Voltage. See “Appendix” on page 225 for unit conversion details.
200F.03h Phase B Output Voltage
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DPV Read Only No
Description:
Contains a value corresponding to the Phase B Output Voltage. See “Appendix” on page 225 for unit conversion details.
200F.04h Phase C Output Voltage
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DPV Read Only No
Description:
Contains a value corresponding to the Phase C Output Voltage. See“Appendix” on page 225 for unit conversion details.
200F.05h Trap Mode Output Voltage
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DPV Read Only No
Description:
Contains a value corresponding to the trap mode output voltage. See “Appendix” on page 225 for unit conversion details.

---
## Page 220

MNCMECRF-07 210
Object Dictionary / Drive Operation Objects
2021h: Drive Temperature Values   
2019h: Capture Values   The capture values have units that vary with the operating mode of 
the drive. For these parameters, refer to Table 2.13 for the correct unit selection.
TABLE 2.13 Capture Units
2021.01h External Thermal Sense Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] N/A Read Only No
Description:
Contains a value corresponding to the external thermal sense value. This value represents the motor temperature value detected by the 
drive. To determine the physical temperature, use the following formula:
(Thermal Sense Value) / 65536 = Temperature measured by drive (in °C)
Example: The reported External Thermal Sense Value is 1234567 (decimal). The temperature measured by the drive is therefore 
(1234567/65536) = 18.8 °C
2021.02h Thermistor Resistance
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] Ohms Read Only No
Description:
If supported by the hardware, this value represents the measured thermistor resistance value in ohms.
Drive Operation Mode Units
Current (Torque) DC2
Velocity DS1
Position (Around Velocity Or Current) counts
2019.01h Capture ‘A’ Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.13 Read Only No
Description:
Capture A captured value
2019.02h Capture ‘B’ Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.13 Read Only No
Description:
Capture B captured value

---
## Page 221

MNCMECRF-07 211
Object Dictionary / Drive Operation Objects
2023h: Digital Input Values   
2019.03h Capture ‘C’ Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] - [2(31) –1] See Table 2.13 Read Only No
Description:
Capture C captured value
2023.01h Digital Inputs (Post Active Level)
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 See Table N/A Read Only No
Description:
Bit field corresponding to the state of the digital inputs. Bit field definitions are given below.
*Number of actual inputs depends on drive model
Bit Digital Inputs*
0 Digital Input 1
1 Digital Input 2
2 Digital Input 3
3 Digital Input 4
4 Digital Input 5
5 Digital Input 6
6 Digital Input 7
7 Digital Input 8
8 Digital Input 9
9 Digital Input 10
10 Digital Input 11
11 Digital Input 12
12 Digital Input 13
13 Digital Input 14
14 Digital Input 15
15 Digital Input 16

---
## Page 222

MNCMECRF-07 212
Object Dictionary / Drive Operation Objects
2024h: Digital Output Values   
201Ah: Analog Input Values   
2024.01h Digital Outputs (Pre Active Level)
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 See Table N/A Read Only No
Description:
Bit field corresponding to the state of the digital inputs. Bit field definitions are given below.
*Number of actual outputs depends on drive model
201A.01h Analog Input 1 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAI Read Only No
Description:
Contains a value corresponding to the voltage present on analog input 1. See “Appendix” on page 225 for unit conversion details.
201A.02h Analog Input 2 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAI Read Only No
Description:
Contains a value corresponding to the voltage present on analog input 2. See “Appendix” on page 225 for unit conversion details.
Bit Digital Outputs*
0 Digital Output 1
1 Digital Output 2
2 Digital Output 3
3 Digital Output 4
4 Digital Output 5
5 Digital Output 6
6 Digital Output 7
7 Digital Output 8
8 Digital Output 9
9 Digital Output 10
10 Digital Output 11
11 Digital Output 12
12 Digital Output 13
13 Digital Output 14
14 Digital Output 15
15 Digital Output 16

---
## Page 223

MNCMECRF-07 213
Object Dictionary / Drive Operation Objects
2022h: Analog Input ADC Raw Values   
201A.03h Analog Input 3 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAI Read Only No
Description:
Contains a value corresponding to the voltage present on analog input 3. See “Appendix” on page 225 for unit conversion details.
201A.04h Analog Input 4 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAI Read Only No
Description:
Contains a value corresponding to the voltage present on analog input 4. See “Appendix” on page 225 for unit conversion details.
2022.01h Analog Input 1 ADC Raw Value
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Provides the full scale raw value of the ADC used for Analog Input 1.
2022.02h Analog Input 2 ADC Raw Value
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Provides the full scale raw value of the ADC used for Analog Input 2.
2022.03h Analog Input 3 ADC Raw Value
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Provides the full scale raw value of the ADC used for Analog Input 3.

---
## Page 224

MNCMECRF-07 214
Object Dictionary / Drive Operation Objects
2025h: Analog Output Values   
2015h: Deadband Input Value   
2018h: Programmable Limit Switch Values   
2022.04h Analog Input 4 ADC Raw Value
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 – [2(16)-1] N/A Read Only No
Description:
Provides the full scale raw value of the ADC used for Analog Input 4.
2025.01h Analog Output 1 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAO Read Only No
Description:
Contains a value corresponding to the value of analog output 1. The analog outputs have a range of 0 to 10 Volts. See “Appendix” on 
page 225 for unit conversion details.
2025.02h Analog Output 2 Value
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(15)] – [2(15)-1] DAO Read Only No
Description:
Contains a value corresponding to the value of analog output 2. The analog outputs have a range of 0 to 10 Volts. See “Appendix” on 
page 225 for unit conversion details.
2015.01h Deadband Input Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] DC2, DS1, counts Read Only No
Description:
Value of the command input to the Deadband function. Mode dependant units.
2018.01h PLS Input Value
Data Type Data Range Units Accessibility Stored to NVM
Integer32 [-2(31)] – [2(31)-1] counts Read Only No
Description:
Contains the value of the programmable limit switch position input. If a rollover value has been defined, this value will range between zero 
and the rollover value.

---
## Page 225

MNCMECRF-07 215
Object Dictionary / Drive Operation Objects
201Bh: PWM and Direction Input Values   
2028h: Fault Log Counter   
2018.02h PLS 1 State
Data Type Data Range Units Accessibility Stored to NVM
Bits 0-1 - Read Only No
Description:
Contains the current state of programmable limit switch 1. This bit is high when PLS 1 is active.
2018.03h PLS 2 State
Data Type Data Range Units Accessibility Stored to NVM
Bits 0-1 - Read Only No
Description:
Contains the current state of programmable limit switch 2. This bit is high when PLS 2 is active.
201B.01h Applied PWM Duty Cycle
Data Type Data Range Units Accessibility Stored to NVM
Integer16 [-2(13)] – [2(13)]
Fractional duty cycle * 
2(13) Read Only No
Description:
Contains the value of the input duty cycle expressed as a signed fraction when the drive is configured for PWM command input. This value 
represents the measured duty cycle after polarity and inversions applied.
201B.02h Input PWM Duty Cycle
Data Type Data Range Units Accessibility Stored to NVM
Integer16 0 – [2(13)] duty cycle * 2(31) Read Only No
Description:
Contains the value of the input duty cycle expressed as an unsigned fraction when the drive is configured for PWM command input. This 
value represents the measured duty cycle before polarity and inversions applied.
2028.01h Log Counter: Total Run Time
Data Type Data Range Units Accessibility Stored to NVM
Unsigned48 0 – 248 msec Read Only No
Description:
This object holds the total run time of the drive.

---
## Page 226

MNCMECRF-07 216
Object Dictionary / Drive Operation Objects
2028.02h Log Counter: Drive Reset
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Drive Reset occurred in the life of the drive.
2028.03h Log Counter: Drive Internal Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Drive Internal Error occurred in the life of the drive.
2028.04h Log Counter: Short Circuit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Short Circuit occurred in the life of the drive.
2028.05h Log Counter: Over Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Over Current occurred in the life of the drive.
2028.06h Log Counter: Hardware Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Hardware Under Voltage occurred in the life of the drive.
2028.07h Log Counter: Hardware Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Hardware Over Voltage occurred in the life of the drive.

---
## Page 227

MNCMECRF-07 217
Object Dictionary / Drive Operation Objects
2028.08h Log Counter: Drive Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Drive Over Temperature occurred in the life of the drive.
2028.09h Log Counter: Parameter Restore Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Parameter Restore Error occurred in the life of the drive.
2028.0Ah Log Counter: Parameter Store Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Parameter Store Error occurred in the life of the drive.
2028.0Bh Log Counter: Invalid Hall State
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Invalid Hall State occurred in the life of the drive.
2028.0Ch Log Counter: Phase Synchronization Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Phase Sync. Error occurred in the life of the drive.
2028.0Dh Log Counter: Motor Over Temperature
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Motor Over Temperature occurred in the life of the drive.

---
## Page 228

MNCMECRF-07 218
Object Dictionary / Drive Operation Objects
2028.0Eh Log Counter: Phase Detection Fault
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Phase Detection Fault occurred in the life of the drive.
2028.0Fh Log Counter: Feedback Sensor Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Feedback Sensor Error occurred in the life of the drive.
2028.10h Log Counter: Log Entry Missed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Log Entry Missed occurred in the life of the drive.
2028.11h Log Counter: Software Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Software Disable occurred in the life of the drive.
2028.12h Log Counter: User Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Disable occurred in the life of the drive.
2028.13h Log Counter: User Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Positive Limit occurred in the life of the drive.

---
## Page 229

MNCMECRF-07 219
Object Dictionary / Drive Operation Objects
2028.14h Log Counter: User Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Negative Limit occurred in the life of the drive.
2028.15h Log Counter: Current Limiting
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Current Limiting occurred in the life of the drive.
2028.16h Log Counter: Continuous Current
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Continuous Current occurred in the life of the drive.
2028.17h Log Counter: Current Loop Saturated
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Current Loop Saturated occurred in the life of the drive.
2028.18h Log Counter: User Under Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Under Voltage occurred in the life of the drive.
2028.19h Log Counter: User Over Voltage
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Over Voltage occurred in the life of the drive.

---
## Page 230

MNCMECRF-07 220
Object Dictionary / Drive Operation Objects
2028.1Ah Log Counter: User Auxiliary Disable
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Auxiliary Disable occurred in the life of the drive.
2028.1Bh Log Counter: Shunt Regulator Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Shunt Regulator Active occurred in the life of the drive.
2028.1Ch Log Counter: Command Limiter Active
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Command Limiter Active occurred in the life of the drive.
2028.1Dh Log Counter: Motor Overspeed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Motor Overspeed occurred in the life of the drive.
2028.1Eh Log Counter: At Command
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times At Command occurred in the life of the drive.
2028.1F0h Log Counter: Zero Speed
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Zero Speed occurred in the life of the drive.

---
## Page 231

MNCMECRF-07 221
Object Dictionary / Drive Operation Objects
2028.20h Log Counter: Velocity Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Velocity Following Error occurred in the life of the drive.
2028.21h Log Counter: Positive Target Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Positive Target Velocity Limit occurred in the life of the drive.
2028.22h Log Counter: Negative Target Velocity Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Negative Target Velocity Limit occurred in the life of the drive.
2028.23h Log Counter: Upper Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Upper Measured Position Limit occurred in the life of the drive.
2028.24h Log Counter: Lower Measured Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Lower Measured Position Limit occurred in the life of the drive.
2028.25h Log Counter: At Home Position
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times At Home Position occurred in the life of the drive.

---
## Page 232

MNCMECRF-07 222
Object Dictionary / Drive Operation Objects
2028.26h Log Counter: Position Following Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Position Following Error occurred in the life of the drive.
2028.27h Log Counter: Upper Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Upper Target Position Limit occurred in the life of the drive.
2028.28h Log Counter: Lower Target Position Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Lower Target Position Limit occurred in the life of the drive.
2028.29h Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
2028.2Ah Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
2028.2Bh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
2028.2Ch Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
2028.2Dh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No

---
## Page 233

MNCMECRF-07 223
Object Dictionary / Drive Operation Objects
2028.2Eh Reserved
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 N/A N/A Read Only No
2028.2Fh Log Counter: Communication Channel Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0- [2(16) –1] count Read Only No
Description:
Number of times Communication Channel Error occurred in the life of the drive.
2028.30h Log Counter: Commanded Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Commanded Stop occurred in the life of the drive.
2028.31h Log Counter: User Stop
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times User Stop occurred in the life of the drive.
2028.32h Log Counter: Commanded Positive Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Commanded Positive Limit occurred in the life of the drive.
2028.33h Log Counter: Commanded Negative Limit
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times Commanded Negative Limit occurred in the life of the drive.

---
## Page 234

MNCMECRF-07 224
Object Dictionary / Drive Operation Objects
2028.34h Log Counter: PWM and Direction Broken Wire Error
Data Type Data Range Units Accessibility Stored to NVM
Unsigned16 0 - [2(16) –1] count Read Only No
Description:
Number of times PWM and Direction Broken Wire Error occurred in the life of the drive.

---
## Page 235

MNCMECRF-07 225
 A Appendix
A.1 Appendix A - Units
Table A.1 below shows scaling factors and formulas for converting physical units to drive units. 
TABLE A.1  Drive Units and Scaling Factors
1.Multiply physical units by the scaling factor to obtain drive units. Divide drive units by the scaling factor to obtain physical units.
The drive units used for a parameter depend upon the parameter type and size. Drive units 
must be rounded to the nearest integer and then converted to a hexadecimal base of the 
appropriate data type before they are written to the drive. When converting to a signed integer 
Abbreviation Drive Unit Type Physical Units Data Type Scaling Factor
DA1 Acceleration counts/s2 Integer32/Unsigned32 234/KS
2
DA2 Acceleration counts/s2 Unsigned48 234/KIKS
2
DA3 Acceleration counts/s2 Integer32 228/KMS KS
DA4 Acceleration counts/s2 Integer32 (218)/(KS
2)
DA5 Acceleration counts/s2 Unsigned48 228/KDS KS
DC1 Current A Integer16 213/KP
DC2 Current A Integer32 215/KP
DJ1 Jerk A/s Unsigned48 232/(KP KS)
DG1 Angle degrees Integer16/Unsigned16 216/360
DS1 Speed/Velocity counts/s Integer32 217/KIKS
DS2 Speed/Velocity counts/s Unsigned48 217/KS
DS3 Speed/Velocity counts/s Integer64 233/KS
DS4 Speed/Velocity counts/s Unsigned32 217/KS
DV1 Voltage V Integer16 214/(1.05 KOV)
DPV Phase Voltage V Integer16 214/KB
DAI Analog Input Voltage V Integer16 214/20
DAO Analog Output Voltage V Integer16 214/10
DT1 Temperature °C Integer32 216
PBC Power Board Current A Unsigned16 10
PBV Power Board Voltage V Unsigned16 10
PBT Power Board Time s Unsigned16 100
PBF Power Board Frequency Hz Unsigned32 216/1000
SF1 Scale Factor 1 - - 214

---
## Page 236

MNCMECRF-07 226
 / Appendix A - Units
data type, use two’s complement for representation of negative numbers (see “Conversion 
Example 3” on page 227). Some scaling factors involve drive dependent constants. These 
constants are given in Table A.2, along with details on determining their values.
TABLE A.2  Drive dependent conversion constants
A.1.1 Conversion Example 1
• Drive: DPRAL TE-020B080
• Feedback: 1000 Line Incremental Encoder
To specify a Motor Over Speed Limit (2037.01h) of 10,000 RPM, first convert to the 
appropriate physical unit as shown below, keeping in mind that counts have a quadrature 
resolution (4X) over lines.
Motor Over Speed is of data type Integer32 and uses DS1 drive units. Taking the appropriate 
32-bit scaling factor from Table A.1 yields
where KI = 1 because we are not dealing with 1 VPP Sin/Cos feedback. Rounding this to the 
nearest integer and converting to a hexadecimal base then results in
.
Now, to apply the setting, a value of 42AAABh would be written to sub-index 2037.01h.
A.1.2 Conversion Example 2
• Drive: 1000 cycles per revolution; DPCANIA-030A400
Constant Value
KB DC Bus Voltage in volts. This value can be read from 200F.01h.
KDS Maximum dynamic index speed (in counts/s). This value can be read from 20CA.07h, 20CA.08h, 20CA.09h, and 20CA.0Ah.
KI Feedback interpolation value. Only applies to drives that support 1 Vpp Sin/Cos feedback. For all other drives, KI = 1. When applicable, this 
value can be read from 2032.08h.
KMS Maximum profiler speed (in counts/s) for an Accel/Decel command profile. This value can be read from 203C.09h for Configuration 0 and 
203C.0Ch for Configuration 1.
KOV The hardware defined, DC bus, over-voltage limit of the drive in volts. This value can be read from 20D8.09h.
KP The maximum rated peak current of the drive in amps. For example, 20 for the DPRALTE-020B080. This value can be read from 
20D8.0Ch.
KS Switching frequency of the drive in Hz. This value can be found on the drive datasheet, or can be read from 20D8.24h and divided by 
65.536.
sec
counts7 . 666 , 666sec 60
min 1
line 1
counts 4
rev 1
lines  1000
min
rev000 , 10 = × ××
9 . 4369066000 , 20 1
27 . 666 , 66627 . 666 , 666
1717
=××= ×
S IK K
1610 42AAAB4369067 =

---
## Page 237

MNCMECRF-07 227
 / Appendix A - Units
• Feedback: 1Vp-p Sine/Cosine Encoder
To specify a Motor Over Speed Limit (2037.01h) of 10,000 RPM, first convert to the 
appropriate physical unit as shown below, keeping in mind that counts have a quadrature 
resolution (4X) over each cycle.
Motor Over Speed is of data type Integer32 and uses DS1 drive units. Taking the appropriate 
32-bit scaling factor from Table A.1 yields:
where the KI term cancels out. Note that “#” in the two conversions (shown above) equal 
1000. Rounding this to the nearest integer and converting to a hexadecimal base then results 
in:
.
Now, to apply the setting, a value of 42AAABh would be written to sub-index 2037.01h. 
A.1.3 Conversion Example 3
To set a temperature parameter to 23°F first convert to the appropriate physical unit as 
shown below. 
°C.
Referring to Table A.1, the appropriate scaling factor yields:
.
Because the resulting integer value is negative, two’s complement notation will be used to 
represent its hexadecimal equivalent. To obtain the two’s complement, the positive version of 
the desired number should be subtracted from 2N, where N is the number of bits in the data 
type. Temperature parameters use the data type Integer32 so the calculation is as follows:
The final step would be to write a value of FFFB0000h to the appropriate parameter.
sec
counts# 7 . 666sec 60
min 1
cycle 1
counts 4
rev 1
cycles #  K
min
rev000 , 10 I ⋅ ⋅ = × ×⋅× IK
# 0669 . 4369000 , 20
2# 7 . 6662# 7 . 666
1717
⋅= × ⋅ = × ⋅ ⋅
S I
I
K KK
1610 42AAAB4369067 =
() 5 32 239
5 − = −
3276802 516 − = × −
1610
32
FFFB00004294639616
42946396163276802 3276802
=
= − = −N

---
## Page 238

MNCMECRF-07 228
 / Appendix B - Current Limiting Algorithm
A.2 Appendix B - Current Limiting Algorithm
In order to understand the current limiting algorithm used by ADVANCED Motion Controls DP 
Series drives, it is necessary to first understand the different current limiting regions. The 
graph in Figure A.1 breaks the available current into three different regions.
FIGURE A.1 Current Limiting Regions
• Continuous Region: The commanded current is less than or equal to the continuous 
current limit. The available current is equal to the commanded current.
• Peak Region: The commanded current is between the continuous and peak current 
limits. The available current is equal to the commanded current for a limited time (Peak 
Time).
• Foldback Region: Commanded current is between the continuous and peak current limits 
of the drive. The available current is less than the commanded current. The available 
current decreases over time until it equals the continuous current limit. The rate of this 
decrease is equal to:
Ip Peak current limit
Ic Continuous current limit
tf Foldback time
Ip
Ic
Continuous Region
Foldback Region
Peak Time Foldback Time
Time
Peak 
Region
Current
Slope Ip Ic–
tf- - - - - - - - - - - - - - - - - =

---
## Page 239

MNCMECRF-07 229
 / Appendix B - Current Limiting Algorithm
A.2.1 Time-Based Peak Current Limiting
The full peak value of current is available to begin with. When a current command is equal to 
the peak current limit, the current begins to foldback to the continuous limit after Tp, 
following the same slope as given in Figure A.1. Once the available current has reached the 
continuous current limit after tf, the available current will be limited to the continuous current 
limit until the commanded current is dropped below the continuous level.
FIGURE A.2 Time-Based Peak Current Limiting
Ip
Ic
Current-Time
Tp
Icommanded
Iavailable
tf

---
## Page 240

MNCMECRF-07 230
 / Appendix B - Current Limiting Algorithm
A.2.2 Time-Based Non-Peak Current Limiting
When the commanded current is between the peak and continuous current limits, the 
available current will begin to foldback at the intersection with the slope from “Time-Based 
Peak Current Limiting”. The larger the commanded current, the sooner the available current 
will begin to foldback.
FIGURE A.3 Time-Based Non-Peak Current Limiting
Ip
Ic
Current-Time
Icommanded
Iavailable
Tp
tf

---
## Page 241

MNCMECRF-07 231
 / Appendix B - Current Limiting Algorithm
A.2.3 Time-Based Current Recovery
Initially, the full peak value of current is available. A commanded current above the continuous 
level causes the available current to foldback to the continuous level as shown in the first graph 
of Figure A.4. When the commanded current drops below the continuous current limit value 
(A1 in the first graph), the available current will then begin to recover along the slope of the 
foldback line towards the peak current level, as shown in the second graph of Figure A.4. The 
relationship between the commanded current and the recovered current is given as: 
Using this relationship, you can calculate the amount of time recovered, t, by using the 
following equation:
FIGURE A.4 Time-Based Current Recovery - Foldback and Commanded Current
Note that current must be commanded below the specified continuous value to start 
recovering from a foldback condition.
A2
1
2- - -A1=
t A1
2 Ip Ic– - - - - - - - - - - - - - - - - - - - - - - - =
Ip
Ic
Iavailable
Zero 
Current
t
t = A1
2(Ip – Ic)
A2
Ip
Ic
Current-Time
Tp
tf
Icommanded
Iavailable
Zero 
Current
Foldback
A1

---
## Page 242

MNCMECRF-07 232
 / Appendix B - Current Limiting Algorithm
A.2.4 Charge-Based Peak Current Limiting
The charge is full to begin with. When a current greater than the continuous current limit is 
commanded, the charge begins to decay. The loss of charge is determined by the area under 
the curve as shown in Figure A.5. The larger the command, the faster the charge will decay. 
When the charge decreases to zero, the available current will be limited to the continuous 
current limit until the charge is restored.
FIGURE A.5 Charge-Based Peak Current Limiting
Ip
Ic
Full Charge
Zero Charge
Current-Time
Charge-Time

---
## Page 243

MNCMECRF-07 233
 / Appendix B - Current Limiting Algorithm
A.2.5 Charge-Based Non-Peak Current Limiting
When the commanded current is between the peak and continuous current limits, the 
commanded current will be available for a longer period when compared to limiting at peak 
command. Note that the slope of the line during foldback is the same for both cases.
FIGURE A.6 Charge-Based Non-Peak Current Limiting
Ip
Ic
Full Charge
Zero Charge
Current-Time
Charge-Time
Icommanded
Slope during foldback

---
## Page 244

MNCMECRF-07 234
 / Appendix B - Current Limiting Algorithm
A.2.6 Charge-Based Current Recovery
After losing some value of charge, the charge may be recovered when the commanded value is 
dropped less than the continuous current limit. The amount of charge recovered depends on 
the magnitude of the commanded current and the amount of time in which it is commanded. 
The amount of charge recovered can be calculated by measuring the area within the curve as 
shown during the charge recovery phase in Figure A.7.
FIGURE A.7 Charge Recovery
Ip
Ic
Full Charge
Zero 
Charge
Current-Time
Charge-Time
Commanded Current
Foldback Foldback
Charge 
Recovery
0

---
## Page 245

MNCMECRF-07 235
 / Appendix B - Current Limiting Algorithm
A.2.7 RMS Current Scaling
RMS Current Scaling uses the charge-based algorithm described above. The only difference is 
the value of the continuous current the drive is capable of outputting. The continuous RMS 
limit can be used when the motor is moving so that the electrical cycle frequency is greater 
than the upper frequency assigned to that drive. The upper frequency is typically around 5Hz 
or 150 RPM for a 4-pole motor. The continuous RMS value is the continuous DC value 
multiplied by the square root of two.
When the electrical cycle frequency drops below the upper frequency, the continuous current 
drops below the RMS value. When the motor is moving at slow speeds, the continuous current 
is equal to the DC value of the current.
FIGURE A.8 RMS Current Limiting
Icrms 2 Icdc 
Ip
Icdc
RMS Current Scaling
Icrms
Electrical cycle frequency 
Above RMS cutoff frequeny  
Electrical Cycle Frequency 
below DC cutoff frequency
Tp Time
Current

---
## Page 246

MNCMECRF-07 236
 B Appendix B
B.1 Appendix B - EtherCAT PDO Assignments
Default PDO mappings for ADVANCED Motion Controls’ EtherCAT drives are intended to meet 
the requirements for most applications. In some cases the mapped objects may need to be 
modified.
The default RPDO and TPDO mappings are listed in Table B.1 and Table B.2. There are 16 
locations for each PDO. Only 5 are used in the default configuration. Mappings can be added or 
removed to better fit the application requirements as long as the total size of the mapped 
object data does not exceed 16 words (256 bits) for the RPDO and 16 words (256) for the 
TPDO.
TABLE B.1 Default Pre-Mapped RPDOs 
Offset Name Index Sub-Index Size (Word) Type
1 Control Word 6040.00 1 UINT
2 Target Position 607A.00 2 DINT
3 Target Velocity 60FF.00 2 DINT
4 Target Current 6071.00 1 INT
5 User Bits 2001.03 1 UINT
6 - - - -
7 - - - -
8 - - - -
9 - - - -
10 - - - -
11 - - - -
12 - - - -
13 - - - -
14 - - - -
15 - - - -
16 - - - -

---
## Page 247

MNCMECRF-07 237
 / Appendix B - EtherCAT PDO Assignments
TABLE B.2 Default Pre-Mapped TPDOs 
The list of PDOs may be modified or added to. It is not recommended to remove the pre-
mapped PDOs.
B.1.1 Modifying PDO Assignments in TwinCAT
This is a three-step procedure that requires changes to the project file and XML files:
1. Modify and download the new project file settings using DriveWare.
2. Modify the EtherCAT device description files.
3. Write the device description data to the drive using the EtherCAT host.
1 - Modify and Download the New Project File Settings Using DriveWare   
From the DriveWare Setup Panel, navigate to the RPDO or TPDO window under Network.
Offset Name Index Sub-Index Size (Word) Type
1 Status Word 6041.00 1 UINT
2 Actual Position 6064.00 2 DINT
3 Actual Velocity 606C.00 2 DINT
4 Actual Current 6077.00 1 INT
5 Digital Inputs 2023.01 1 UINT
6 - - - -
7 - - - -
8 - - - -
9 - - - -
10 - - - -
11 - - - -
12 - - - -
13 - - - -
14 - - - -
15 - - - -
16 - - - -


---
## Page 248

MNCMECRF-07 238
 / Appendix B - EtherCAT PDO Assignments
Available objects will be listed for mapping assignment. Drag the desired objects from the left 
panel to the object assignments panel on the right. You can remove assigned objects by 
highlighting and clicking on the red X, or pressing the delete key on your keyboard. The order 
of the mapping assignments may be adjusted by highlighting an object and then clicking on 
the up or down arrow button. Once all changes are made and applied, store the project to the 
drive.
Alternatively, the project file mappings can be modified outside of DriveWare through an 
EtherCAT host by writing to the PDO mapping objects 1600h and 1A00h.
2 - Modify the EtherCAT Device Description File   Note: For this step, an XML file editor 
is recommened (but not required). XML Notepad is a free download from Microsoft.
 Locate the primary device description file. It should have the following format: 
" AMC_DPE_xxx_x.xml". Make a backup copy of this file before continuing.
This file contains PDO mapping information in the "Modules" section. Mapped objects can be 
removed by deleting the entry for that object. Content can be added by entering in the new 
index, sub-index, bit length in bytes, name, and data type. Use the existing mapping information 
as a guide for formatting the new data correctly. The following shows the typical 
representation in XML Notepad.


---
## Page 249

MNCMECRF-07 239
 / Appendix B - EtherCAT PDO Assignments
Below each PDO heading are individual PDO entries. To add a new entry, highlight an entry 
then right-click and select Duplicate. A new Entry folder is visible below the highlighted Entry.
This entry may now be modified with new information. Each entry contains the following:
• CANopen object index
• Sub-index
• Bitlength
• Name
• Data Type
Note: Consult the Object Dictionary in ADVANCED Motion Controls’ EtherCAT Communication 
Manual for further information on a particular object.
The secondary XML files are in the folder labeled " AMC DP_DZ". There are 4 different files to 
support a 1 to 4 axis configuration. If using a DPE drive, select the 1-axis file. Otherwise select 
the XML file associated with the number of axes used on your Node/Sub-node mounting card 
or assembly. The data type descriptions are listed near the beginning of the file. The data types 
that need to be modified are DT1600 for RPDO changes or DT1A00 for TPDO changes. Edit 
the listings to reflect the PDO mappings in the project and main XML file. The following shows 
the typical representation in XML Notepad:


---
## Page 250

MNCMECRF-07 240
 / Appendix B - EtherCAT PDO Assignments
3 - Write the Device Description Data to the Drive Using the EtherCAT Host   
Note: TwinCAT must be restarted to rebuild the device description cache after the XML file has 
been modified. Close and restart TwinCAT if necessary before proceeding.
The modified XML file will need to get written to the drive. This is accomplished using the 
EtherCAT host software. Below is an example of how to write the file to the drive using 
TwinCAT . Methods and requirements will vary depending on the host software.
1. Navigate to Drive 1 (AMC):
2. Select the EtherCAT tab on the right, and click on the Advanced Settings button:


---
## Page 251

MNCMECRF-07 241
 / Appendix B - EtherCAT PDO Assignments
3. Navigate to ESC Access -> E2PROM -> Smart View, and select the Write E2PROM button:
4. Select the file associated with the configuration you have, and press OK. This action will 
store settings to the drive.
Note: If there are any syntax errors in the XML file, the Write EEPROM window may be blank. 
Check XML syntax and restart TwinCAT in this case.
5. Power cycle the drive to activate the new settings.


---
## Page 252

MNCMECRF-07 I
Index
Numerics
1000h:
Device Type....................... 32
1018h:
Identity Object.................. 32
1C00h:
Sync Manager 
Communication Type ...... 33
2001h:
Control Parameters........ 182
2002h:
Drive Status..................... 191
2003h:
Drive Status History ...... 194
2006h:
Network Configuration.... 35
2008h:
Drive Initialization 
Parameters ........................ 71
2009h:
Load EEPROM Values..... 31
200Ah:
AMC Store Drive 
Parameters ........................ 31
200Bh:
Stored User Parameters .. 71
200Eh:
Feedback Sensor Values 197
200Fh:
Power Bridge Values...... 209
2010h:
Current Values................ 201
2011h:
Velocity Values ............... 206
2012h:
Position Values ............... 207
2014h:
Command Limiter Input208
2015h:
Deadband Input Value .. 214
2018h:
Programmable Limit Switch 
Values............................... 214
2019h:
Capture Values................ 210
201Ah:
Analog Input Values....... 212
201Bh:
PWM and Direction Input 
Values............................... 215
201Ch:
Gearing Values................ 200
201Eh:
Auxiliary Encoder Value 200
2021h:
Drive Temperature Values..
210
2022h:
Analog Input ADC Raw 
Values............................... 213
2023h:
Digital Input Values....... 211
2024h:
Digital Output Values .... 212
2025h:
Analog Output Values.... 214
2027h:
Feedback Hardware 
Diagnostics...................... 198
2028h:
Fault Log Counter .......... 215
2029h:
Motion Engine Status .... 195
2032h:
Feedback Sensor 
Parameters ........................ 42
2033h:
User Voltage Protection 
Parameters ........................ 72
2034h:
Current Loop & 
Commutation Control 
Parameters ........................ 47
2036h:
Velocity Loop Control 
Parameters ........................ 55
2037h:
Velocity Limits.................. 59
2038h:
Position Loop Control 
Parameters ........................ 60
2039h:
Position Limits..................63
203Ch:
Command Limiter 
Parameters ........................ 67
203Dh:
Deadband Parameters ... 114
203Eh:
Jog Parameters ............... 115
2040h:
Programmable Limit Switch 
Parameters ...................... 111
2043h:
Capture Configuration 
Parameters ........................ 75
2044h:
Analog Input Parameters ....
101
2045h:
Interface Inputs .............. 185
2046h:
Auxiliary Input Parameters
47
2054h:
Drive Temperature 
Parameters ........................ 74
2058h:
Digital Input Parameters. 78
205Ah:
Digital Output Parameters..
84
205Bh:
Programmable Status 
Parameters ...................... 157
205Ch:
Analog Output Parameters .
109
2062h:
Braking/Stop General 
Properties ........................ 116
2064h:
Event Response Time 
Parameters ...................... 117
2065h: 
Event Action Parameters124

---
## Page 253

 / 
II MNCMECRF-07
2066h:
Event Recovery Time 
Parameters ...................... 135
2067h:
Event Time-Out Window 
Parameters ...................... 140
2068h:
Event Maximum Recoveries 
Parameters ...................... 147
208Ch:
Product Information...... 173
208Dh:
Firmware Information... 174
20C8h:
Motion Engine 
Configuration.................... 72
20C9h:
Motion Engine Control.. 187
20CAh:
Dynamic Index Data ...... 187
20D0h:
Control Loop Configuration 
Parameters ........................ 41
20D8h:
Power Board Information...
174
20E6h:
CANopen Parameters ...... 34
6040h:
ControlWord................... 181
6041h:
StatusWord ..................... 190
6060h:
Modes Of Operation ...... 184
6061h:
Modes Of Operation Display
197
6064h:
Actual Position................ 207
6065h:
Position Following Error 
Window.............................. 65
6066h:
Position Following Error 
Time Out............................ 65
6069h:
Velocity Sensor Actual Value
205
606Bh:
Velocity Demand ............ 204
606Ch:
Actual Velocity................ 205
606Dh:
Velocity Window ............ 205
606Eh:
Velocity Window Time .. 205
6071h:
Target Current ................ 184
6077h:
Actual Current ................ 201
607Ah:
Target Position................ 185
607Ch:
Home Offset ...................... 67
6086h:
Motion Profile Type ......... 67
6088h:
Torque Profile Type ......... 67
6098h:
Homing Method ............... 66
6099h:
Homing Speeds................. 66
609Ah:
Homing Acceleration....... 66
60B1h:
Velocity Offset................. 185
60B2h:
Current Offset ................. 185
60C2h
Interpolation Time Period ......70
60F4h:
Position Following Error 
Actual Value ...................... 66
60FFh:
Target Velocity................ 184
A
Agency Compliances ...........................i
Attention Symbols..............................ii
C
Communication Hardware
CAN hardware Setup ...............29
RS-232 hardware Setup ..........29
Company Website ............................... i
Control State Machine..................... 10
ControlWord (6040h) ............... 10, 13
Current Limiting............... 54, 228–235
Charge-Based..................232–234
RMS Current Scaling .............235
Time-Based .....................229–231
D
DS301................................................... 1
DSP402................................................ 1
H
Homing ........................................ 15, 25
Method 1 ....................................17
Method 2....................................17
Method 35..................................21
Methods 17 – 30 .......................21
Methods 3 & 4...........................18
Methods 33 – 34.......................21
Methods 5 & 6...........................18
Methods 7 – 14..........................19
M
Mapping Parameter Object See 
Process Data Object
Configuration
Messages
PDO See Process Data Object
SDO See Service Data Object
Modes of Operation..........................22
Custom Defined Modes ...........28
Profile Current Mode...............25
Profile Position Mode ..............23
Profile Velocity Mode...............24
O
Objects ................................................. 2
P
Process Data Object
Configuration..............................7
Messages......................................6
Receive PDO................................6
SDO Comparison........................5
Transmit PDO.............................6
R
Revision History................................iii
RPDO See Process Data Object
S
SDO See Service Data Object
Service Data Object
Messages......................................5
PDO Comparison........................5
States
Control (Operational) ..............11
StatusWord (6041h)................... 11, 14
T
TPDO See Process Data Object
Trademarks ..........................................i
U
Units................................................. 225
V
Velocity Divider ................................ 44
W
Warning Symbols ...............................ii

---
## Page 254

ADVANCED Motion Controls® EtherCAT® Communication 
Reference Manual
MNCMECRF-07
3805 Calle Tecate  Camarillo, CA 93012-5068
Tel: (805) 389-1935      Fax: (805) 384-2315 www.a-m-c.com