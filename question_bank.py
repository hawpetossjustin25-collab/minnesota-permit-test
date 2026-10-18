#!/usr/bin/env python3
"""
Minnesota permit test question bank.

build_bank() returns 1000+ unique questions:
  - ~70 hand-written questions covering the MN Driver's Manual
  - generated variants from ~220 manual facts (rephrased stems and
    different answer arrangements so no two entries are identical)

Content is based on the official Minnesota Driver's Manual.
This is a PRACTICE bank - not the protected AutoTest database.
"""

import hashlib


def _q(question, options, correct, explanation, chapter):
    return {
        "question": question,
        "options": options,
        "correct": correct,
        "explanation": explanation,
        "chapter": chapter,
    }


# ============================================================
# PART 1 - HAND-WRITTEN CORE QUESTIONS
# ============================================================
CORE = [
    _q("What is the minimum age to get a Minnesota instruction permit?",
       ["14 years old", "15 years old", "15 and a half years old", "16 years old"], 1,
       "You can get an instruction permit at 15. Under 18 you also need classroom driver education first.",
       "Permits & Licensing"),
    _q("How many questions are on the Minnesota Class D knowledge test and what score do you need to pass?",
       ["20 questions, 70% to pass", "30 questions, 75% to pass", "40 questions, 80% to pass", "50 questions, 85% to pass"], 2,
       "The real test has 40 questions and you need at least 80% (32 correct) to pass.",
       "Permits & Licensing"),
    _q("How long is a Minnesota instruction permit valid?",
       ["6 months", "1 year", "2 years", "It never expires"], 2,
       "An instruction permit is valid for 2 years.",
       "Permits & Licensing"),
    _q("How long must a driver under 18 hold an instruction permit before taking the road test?",
       ["3 months", "6 months", "9 months", "12 months"], 1,
       "Under 18 you must hold the permit at least 6 months before the road test.",
       "Permits & Licensing"),
    _q("Who must ride with you when you drive on an instruction permit?",
       ["Any licensed driver", "A licensed driver age 21 or older", "A parent only", "A licensed driver 18 or older"], 1,
       "Permit holders must be supervised by a licensed driver age 21 or older sitting beside them.",
       "Permits & Licensing"),
    _q("In Minnesota, at what alcohol concentration can a driver 21 or older be arrested for DWI?",
       ["0.02 percent or higher", "0.04 percent or higher", "0.08 percent or higher", "0.16 percent or higher"], 2,
       "0.08 is the DWI limit for drivers 21+. Enhanced penalties apply at 0.16.",
       "DWI Laws"),
    _q("What is the alcohol concentration limit for commercial drivers (CDL)?",
       ["0.08%", "0.02%", "0.04%", "0.10%"], 2,
       "Commercial drivers face a stricter 0.04 limit.",
       "DWI Laws"),
    _q("What is Minnesota's 'Not a Drop' law?",
       ["Bars cannot serve minors", "Drivers under 21 cannot drive with ANY detectable alcohol", "No open containers in bars", "No alcohol sales on Sundays"], 1,
       "Under-21 drivers may not operate a vehicle with any detectable amount of alcohol at all.",
       "DWI Laws"),
    _q("Under Minnesota's implied consent law, refusing the alcohol test when arrested for DWI means:",
       ["Nothing happens", "Your license can be revoked and refusal is a crime", "Only a warning", "Only a small fine"], 1,
       "By driving you consent to testing. Refusing is a crime and brings license revocation.",
       "DWI Laws"),
    _q("Minnesota's hands-free law makes it illegal to:",
       ["Talk on any phone while driving", "Hold a phone in your hand while driving", "Use Bluetooth headsets", "Have a phone in the car"], 1,
       "You cannot hold a phone while driving. Hands-free use is allowed for drivers 18+.",
       "Traffic Laws"),
    _q("Texting or reading email while driving in Minnesota is:",
       ["Legal at red lights", "Illegal for all drivers", "Legal for drivers over 21", "Only illegal for teens"], 1,
       "Texting, emailing, or web browsing while driving is illegal for everyone.",
       "Traffic Laws"),
    _q("It is illegal to have an open container of alcohol:",
       ["Only if the driver is drinking", "Anywhere in the passenger area of the vehicle", "Only in the front seat", "Only on highways"], 1,
       "Open bottles or cans cannot be anywhere in the passenger compartment.",
       "DWI Laws"),
    _q("What kind of insurance must Minnesota vehicle owners carry?",
       ["Collision only", "No-fault and liability insurance", "Comprehensive only", "None if you drive carefully"], 1,
       "Minnesota is a no-fault state. You must carry no-fault and liability coverage and keep proof in the vehicle.",
       "Insurance"),
    _q("Can a Minnesota officer stop you just for not wearing a seat belt?",
       ["Yes, it is a primary offense", "No, another violation is needed", "Only for drivers under 18", "Only on freeways"], 0,
       "Seat belt violations alone justify a stop. Everyone in the vehicle must be belted.",
       "Traffic Laws"),
    _q("Children must ride in a car seat or booster seat in Minnesota until they are:",
       ["Age 4", "Age 8 or 4 feet 9 inches tall", "Age 6", "Age 10"], 1,
       "Minnesota requires child restraints until age 8 or 4'9\" tall, whichever comes first.",
       "Traffic Laws"),
    _q("You may pass another vehicle if the line dividing your lane is a ____ line.",
       ["Solid white", "Double solid yellow", "Solid yellow", "Broken white"], 3,
       "Broken white lines separate same-direction lanes and may be crossed.",
       "Pavement Markings"),
    _q("A solid yellow line on your side of the center line means:",
       ["Passing is permitted", "No passing allowed", "Speed limit reduced", "Road closed ahead"], 1,
       "A solid yellow line on your side means no passing.",
       "Pavement Markings"),
    _q("Yellow pavement lines separate traffic moving in:",
       ["The same direction", "Opposite directions", "Parking lanes", "Bike lanes"], 1,
       "Yellow lines separate opposing traffic. White lines separate same-direction traffic.",
       "Pavement Markings"),
    _q("A center lane marked with yellow lines on both sides is used for:",
       ["Passing", "Left turns only", "Parking", "Emergency stopping"], 1,
       "Two-way left turn lanes are for turning left only - never for passing or travel.",
       "Pavement Markings"),
    _q("What does a flashing yellow traffic light mean?",
       ["Stop", "Proceed with caution", "Prepare to stop", "Speed up"], 1,
       "Flashing yellow means slow down and proceed with caution.",
       "Traffic Signals"),
    _q("What does a flashing red traffic light mean?",
       ["Proceed with caution", "Stop completely, then go when safe", "Speed up", "Ignore it"], 1,
       "Flashing red means the same as a stop sign.",
       "Traffic Signals"),
    _q("When a traffic signal is completely dark (power outage), treat it as:",
       ["A yield sign", "A four-way stop", "An open intersection", "A green light"], 1,
       "A dark or malfunctioning signal is treated as a four-way stop.",
       "Traffic Signals"),
    _q("A flashing yellow arrow at a left turn means:",
       ["Turn immediately - you have the right of way", "Yield to oncoming traffic, then turn when clear", "No left turns", "Stop and wait for green"], 1,
       "A flashing yellow arrow means yield to oncoming traffic and pedestrians, then turn when safe.",
       "Traffic Signals"),
    _q("You may turn right on a red light:",
       ["Never", "After stopping, unless a sign prohibits it", "Only at night", "Only with a green arrow"], 1,
       "Right on red is legal after a complete stop unless a sign prohibits it.",
       "Traffic Signals"),
    _q("In Minnesota you may turn left on red only:",
       ["Never", "From a one-way street onto another one-way street, after stopping", "Whenever traffic is clear", "Only with a green arrow"], 1,
       "Left on red is allowed one-way to one-way after stopping.",
       "Traffic Signals"),
    _q("How far before a turn must you signal in Minnesota?",
       ["At least 50 feet", "At least 100 feet", "At least 150 feet", "At least 25 feet"], 1,
       "Signal at least 100 feet before turning.",
       "Turning"),
    _q("When making a turn, you should ____ your speed before entering the turn.",
       ["Increase", "Maintain", "Reduce", "Vary"], 2,
       "Slow before the turn, then accelerate gently through it.",
       "Turning"),
    _q("It is illegal to make a U-turn:",
       ["Only at night", "On a curve or near the top of a hill where you cannot be seen", "In residential areas", "On any two-lane road"], 1,
       "Never U-turn where approaching drivers cannot see you - curves, hill crests, or less than 1,000 feet of visibility.",
       "Turning"),
    _q("At a four-way stop where two vehicles arrive at the same time, who goes first?",
       ["The vehicle on the left", "The vehicle on the right", "The larger vehicle", "The faster vehicle"], 1,
       "Simultaneous arrival - the vehicle on the right has the right of way.",
       "Right of Way"),
    _q("When turning left on a green light without an arrow, you must:",
       ["Turn immediately", "Yield to oncoming traffic going straight or turning right", "Honk first", "Wait for a green arrow only"], 1,
       "Left-turning traffic yields to oncoming through traffic.",
       "Right of Way"),
    _q("When entering a road from a driveway or alley, you must:",
       ["Enter quickly", "Yield to all traffic and pedestrians", "Honk and proceed", "Stop only if cars are coming"], 1,
       "Traffic entering the roadway always yields to traffic already on it and to pedestrians.",
       "Right of Way"),
    _q("When approaching a roundabout, you must:",
       ["Stop every time before entering", "Yield to traffic already circulating", "Enter before other traffic", "Always turn left to enter"], 1,
       "Yield to traffic already in the roundabout (from your left), then enter a safe gap.",
       "Right of Way"),
    _q("When an emergency vehicle approaches with lights and siren, you must:",
       ["Speed up to clear the way", "Pull to the right edge and stop", "Stop in your lane", "Keep driving normally"], 1,
       "Pull right and stop until the emergency vehicle passes.",
       "Emergency Vehicles"),
    _q("Minnesota's Move Over law requires you, when passing a stopped emergency vehicle with flashing lights, to:",
       ["Honk and pass slowly", "Move over a lane, or slow down if you cannot", "Stop completely", "Flash your headlights"], 1,
       "Move to a lane away from the stopped vehicle, or slow down if changing lanes is unsafe.",
       "Emergency Vehicles"),
    _q("You must stop for a school bus with flashing red lights and an extended stop arm at least:",
       ["10 feet away", "20 feet away", "30 feet away", "50 feet away"], 1,
       "Stop at least 20 feet from the bus, front or rear, on undivided roads.",
       "School Buses"),
    _q("On a divided highway with a median, you must stop for a school bus with red lights:",
       ["From both directions", "Only when traveling the same direction as the bus", "Never", "Only if children are crossing"], 1,
       "On a separated/divided roadway only same-direction traffic must stop.",
       "School Buses"),
    _q("A school bus flashing yellow (amber) lights means:",
       ["Stop immediately", "The bus is preparing to stop - slow down and prepare to stop", "Pass quickly", "The bus is empty"], 1,
       "Amber lights warn the bus is about to stop. Red lights and the stop arm come next.",
       "School Buses"),
    _q("When may you proceed after stopping for a school bus?",
       ["After 10 seconds", "When the red lights stop flashing and the stop arm is withdrawn", "When children are seated", "After honking"], 1,
       "Wait until red lights are off and the arm is retracted, or the driver signals you on.",
       "School Buses"),
    _q("When approaching a railroad crossing with flashing lights, you must stop:",
       ["Within 5 feet of the tracks", "At least 15 feet from the nearest rail", "Only if a train is visible", "Only if gates are down"], 1,
       "Stop at least 15 feet (and no more than 50) from the nearest rail. Never go around gates.",
       "Railroad Crossings"),
    _q("If your vehicle stalls on railroad tracks and a train is coming, you should:",
       ["Keep trying to start it", "Get out immediately and run toward the train at an angle away from the tracks", "Hide behind the vehicle", "Honk the horn"], 1,
       "Get everyone out and run toward the train at a 45-degree angle away from the tracks - debris flies forward.",
       "Emergencies"),
    _q("What should you do if your vehicle starts to hydroplane?",
       ["Brake hard", "Ease off the gas and keep steering straight", "Accelerate", "Turn sharply"], 1,
       "Ease off the gas, hold the wheel straight, and let the tires regain grip. No sudden moves.",
       "Driving Conditions"),
    _q("Hydroplaning can begin at speeds as low as:",
       ["15 mph", "35 mph", "55 mph", "70 mph"], 1,
       "Tires can start riding on water at about 35 mph, sooner with worn tires.",
       "Driving Conditions"),
    _q("The minimum safe following distance in good conditions is:",
       ["1 second", "2 seconds", "3 seconds", "5 seconds"], 2,
       "Keep at least 3 seconds in good conditions - more in rain, snow, traffic, or behind big vehicles.",
       "Following Distance"),
    _q("Roads are most slippery when:",
       ["Rain has fallen for hours", "Rain first begins and lifts oil to the surface", "The road is dry", "At night only"], 1,
       "The first rain mixes with oil and grease, making roads slickest right at the start.",
       "Driving Conditions"),
    _q("In winter, which surfaces freeze first?",
       ["Main highways", "Bridges and overpasses", "City streets", "Parking lots"], 1,
       "Bridges and overpasses have cold air above and below - they ice before other pavement.",
       "Driving Conditions"),
    _q("If your tire blows out while driving, you should:",
       ["Brake hard immediately", "Grip the wheel firmly, ease off the gas, steer straight", "Turn sharply off the road", "Shift to neutral instantly"], 1,
       "Hold the wheel, ease off gas, steer straight, slow gradually, then pull off. No hard braking.",
       "Emergencies"),
    _q("If your brakes fail, you should FIRST:",
       ["Turn off the engine", "Pump the brake pedal rapidly, then downshift", "Pull the parking brake fully", "Open your door"], 1,
       "Pump brakes to build pressure, downshift to a lower gear, and use the parking brake gradually.",
       "Emergencies"),
    _q("If your accelerator sticks, you should:",
       ["Turn the key fully off immediately", "Shift to neutral, brake, and pull off the road", "Brake hard while still in gear", "Reach down and pull it up"], 1,
       "Shift to neutral and brake to a stop off the road. Do not turn the key to lock while moving.",
       "Emergencies"),
    _q("If your vehicle starts to skid, you should:",
       ["Brake hard", "Ease off the gas and steer in the direction you want the front to go", "Accelerate", "Turn the wheel opposite the skid"], 1,
       "Ease off gas/brakes and steer where you want to go. Look where you want to go.",
       "Emergencies"),
    _q("The best way to check your blind spot before changing lanes is to:",
       ["Use only your mirrors", "Look over your shoulder", "Honk first", "Signal and move quickly"], 1,
       "Mirrors leave blind spots. Always glance over your shoulder before moving over.",
       "Lane Changes"),
    _q("When parking uphill WITH a curb, turn your wheels:",
       ["Toward the curb", "Away from the curb", "Straight ahead", "Either way"], 1,
       "Uphill with a curb: wheels away from the curb so the car rolls back into it.",
       "Parking"),
    _q("When parking downhill, turn your wheels:",
       ["Toward the curb or road edge", "Away from the curb", "Straight ahead", "It does not matter"], 0,
       "Downhill: wheels toward the curb so the car rolls into it, not into traffic.",
       "Parking"),
    _q("When parallel parking, your vehicle must be within how many inches of the curb?",
       ["6 inches", "12 inches", "18 inches", "24 inches"], 1,
       "You must finish within 12 inches of the curb.",
       "Parking"),
    _q("In Minnesota it is illegal to park within how many feet of a fire hydrant?",
       ["5 feet", "10 feet", "15 feet", "20 feet"], 1,
       "No parking within 10 feet of a fire hydrant.",
       "Parking"),
    _q("When driving in fog, you should use:",
       ["High beam headlights", "Low beam headlights", "Parking lights only", "No lights"], 1,
       "Use low beams - high beams reflect off fog and reduce visibility.",
       "Driving Conditions"),
    _q("Minnesota law requires headlights to be on:",
       ["Only after dark", "From sunset to sunrise AND whenever visibility is reduced", "Only in rain", "Only on highways"], 1,
       "Headlights must be on from sunset to sunrise and whenever weather reduces visibility.",
       "Vehicle Equipment"),
    _q("If you miss your exit on a freeway, you should:",
       ["Back up on the shoulder", "Make a U-turn", "Continue to the next exit", "Stop and wait"], 2,
       "Never back up on a freeway. Continue to the next exit.",
       "Highway Driving"),
    _q("When merging onto a freeway, you should:",
       ["Stop at the end of the ramp", "Match freeway speed and merge into a safe gap", "Merge at 20 mph", "Force your way in"], 1,
       "Use the ramp to match traffic speed, signal, and merge into a gap.",
       "Highway Driving"),
    _q("A diamond-shaped sign is a:",
       ["Regulatory sign", "Warning sign", "Guide sign", "Stop sign"], 1,
       "Diamond signs warn of hazards or special conditions ahead.",
       "Traffic Signs"),
    _q("A circular yellow sign with a black X and two Rs warns of:",
       ["A hospital zone", "A railroad crossing ahead", "A rest area", "A roundabout"], 1,
       "The circular advance sign warns that a railroad crossing is ahead.",
       "Traffic Signs"),
    _q("A pennant-shaped yellow sign on the left side of the road marks:",
       ["A school zone", "The start of a no-passing zone", "A railroad crossing", "A yield point"], 1,
       "The pennant marks the beginning of a no-passing zone.",
       "Traffic Signs"),
    _q("A five-sided (pentagon) sign warns of:",
       ["A no-passing zone", "A school zone or school crossing", "A railroad crossing", "Road construction"], 1,
       "Pentagon signs mark school zones and crossings. Watch for children.",
       "Traffic Signs"),
    _q("Orange signs with black lettering warn of:",
       ["School zones", "Construction and maintenance work zones", "Hospitals", "Recreation areas"], 1,
       "Orange signs mark work zones. Fines are higher for violations there.",
       "Traffic Signs"),
    _q("Blue signs with white lettering tell you about:",
       ["Parks and recreation", "Motorist services like gas, food, and lodging", "Directions and distances", "Construction zones"], 1,
       "Blue signs point to services: gas, food, lodging, hospitals, rest areas.",
       "Traffic Signs"),
    _q("Green signs with white lettering provide:",
       ["Warnings", "Directions, distances, and exit numbers", "Prohibitions", "School info"], 1,
       "Green signs are guide signs for directions, distances, and exits.",
       "Traffic Signs"),
    _q("An octagon-shaped sign always means:",
       ["Yield", "Stop", "Warning", "No passing"], 1,
       "Only stop signs are eight-sided.",
       "Traffic Signs"),
    _q("A pedestrian carrying a white cane or using a guide dog is:",
       ["Blind or visually impaired", "Deaf", "Physically disabled", "Training a dog"], 0,
       "A white cane or guide dog means the pedestrian is blind - you must stop and yield.",
       "Pedestrians"),
    _q("A yield sign means you must:",
       ["Always come to a complete stop", "Slow down and give right of way, stopping if needed", "Speed up to merge", "Ignore it if the road looks clear"], 1,
       "Yield means slow down, give right of way, and stop if necessary.",
       "Traffic Signs"),
    _q("If your vehicle's wheels drop off the pavement edge, you should:",
       ["Steer sharply back onto the road", "Slow down, then ease back onto the pavement", "Accelerate back on", "Brake hard"], 1,
       "Don't jerk the wheel back. Slow down and steer gently back onto the road.",
       "Emergencies"),
    _q("When following a large truck, remember:",
       ["They can stop quickly", "If you can't see the driver's mirrors, the driver can't see you", "They have no blind spots", "Passing them is always safe"], 1,
       "Trucks have huge blind spots. If you can't see their mirrors, you're invisible to them.",
       "Sharing the Road"),
    _q("When passing a bicyclist, Minnesota law requires at least how much space?",
       ["1 foot", "3 feet", "5 feet", "6 inches"], 1,
       "Give bicyclists at least 3 feet when passing.",
       "Sharing the Road"),
]


# ============================================================
# PART 2 - FACT TABLE (stem, correct, distractors, explanation, chapter)
# The builder rephrases stems and rearranges options to make variants.
# ============================================================
FACTS = [
    # ---------- Distances & Legal Numbers ----------
    ("You must signal at least how many feet before a turn", "100 feet", ["50 feet", "25 feet", "200 feet"], "Signal at least 100 feet before turning.", "Turning"),
    ("You must stop at least how many feet from a school bus with red lights", "20 feet", ["10 feet", "15 feet", "30 feet"], "Stop at least 20 feet from the bus.", "School Buses"),
    ("At a railroad crossing with flashing lights, stop at least how many feet from the nearest rail", "15 feet", ["10 feet", "5 feet", "25 feet"], "Stop 15 to 50 feet from the nearest rail.", "Railroad Crossings"),
    ("You may not park closer than how many feet to a fire hydrant", "10 feet", ["5 feet", "15 feet", "20 feet"], "Parking within 10 feet of a hydrant is illegal.", "Parking"),
    ("You may not park within how many feet of a crosswalk at an intersection", "20 feet", ["10 feet", "15 feet", "30 feet"], "No parking within 20 feet of a marked or unmarked crosswalk.", "Parking"),
    ("You may not park within how many feet of a stop sign or traffic signal", "30 feet", ["20 feet", "40 feet", "50 feet"], "No parking within 30 feet of a stop sign or signal.", "Parking"),
    ("You may not park within how many feet of a fire station driveway on the same side", "20 feet", ["10 feet", "15 feet", "30 feet"], "Stay 20 feet from a fire station driveway on the same side.", "Parking"),
    ("You may not park within how many feet of a fire station on the opposite side", "75 feet", ["50 feet", "60 feet", "100 feet"], "Stay 75 feet from a fire station on the opposite side.", "Parking"),
    ("You must dim high beams when an oncoming vehicle is within how many feet", "1,000 feet", ["500 feet", "300 feet", "200 feet"], "Dim high beams at least 1,000 feet before meeting an oncoming vehicle.", "Vehicle Equipment"),
    ("You must dim high beams when following within how many feet of another vehicle", "200 feet", ["100 feet", "300 feet", "500 feet"], "Dim to low beams within 200 feet behind another vehicle.", "Vehicle Equipment"),
    ("You may not follow a fire truck answering an alarm closer than how many feet", "500 feet", ["300 feet", "200 feet", "1,000 feet"], "Stay at least 500 feet behind an emergency vehicle responding to a call.", "Emergency Vehicles"),
    ("When parallel parking you must be within how many inches of the curb", "12 inches", ["6 inches", "18 inches", "24 inches"], "Finish within 12 inches of the curb.", "Parking"),
    ("When passing a bicyclist you must leave at least how much space", "3 feet", ["1 foot", "2 feet", "5 feet"], "Give bicycles at least 3 feet when passing.", "Sharing the Road"),
    ("The minimum safe following distance in good conditions is how many seconds", "3 seconds", ["2 seconds", "1 second", "5 seconds"], "Keep at least 3 seconds; add more in bad conditions.", "Following Distance"),
    ("You must file a crash report if damage or injury totals at least how much", "$1,000", ["$500", "$750", "$1,500"], "Crashes involving $1,000+ damage or any injury must be reported.", "Crashes"),
    ("Your horn must be loud enough to be heard from how many feet away", "200 feet", ["100 feet", "300 feet", "500 feet"], "Horns must be audible at 200 feet.", "Vehicle Equipment"),
    ("You may not make a U-turn unless visible to approaching drivers for how many feet", "1,000 feet", ["500 feet", "300 feet", "200 feet"], "U-turns require 1,000 feet of visibility in both directions.", "Turning"),
    ("You may not pass within how many feet of an intersection, railroad crossing, bridge, or tunnel", "100 feet", ["50 feet", "75 feet", "150 feet"], "No passing within 100 feet of intersections, crossings, bridges, or tunnels.", "Passing"),

    # ---------- Speed Limits ----------
    ("The speed limit on urban interstate highways in Minnesota is", "55 mph", ["60 mph", "65 mph", "70 mph"], "Urban interstates: 55 mph unless otherwise posted.", "Speed Limits"),
    ("The speed limit on rural interstate highways in Minnesota is", "70 mph", ["55 mph", "60 mph", "65 mph"], "Rural interstates: 70 mph unless otherwise posted.", "Speed Limits"),
    ("The speed limit in alleys in Minnesota is", "10 mph", ["15 mph", "20 mph", "25 mph"], "Alley speed limit is 10 mph.", "Speed Limits"),
    ("The default speed limit on urban or residential streets in Minnesota is", "30 mph", ["25 mph", "35 mph", "20 mph"], "Urban/residential streets: 30 mph unless otherwise posted.", "Speed Limits"),
    ("The default speed limit on other Minnesota roads and highways is", "55 mph", ["45 mph", "50 mph", "60 mph"], "Non-posted rural roads: 55 mph unless otherwise posted.", "Speed Limits"),
    ("Driving slower than the flow of traffic when it is not necessary is", "Illegal - it can impede traffic", ["Always safer", "Required in the right lane", "Fine on highways"], "Unreasonably slow driving that blocks traffic is illegal.", "Speed Limits"),
    ("Speeding fines in Minnesota work zones are", "Higher than normal", ["Lower", "The same", "Waived"], "Work zone violations carry increased fines.", "Speed Limits"),
    ("The correct speed in a Minnesota school zone is", "The posted school zone limit", ["Always 20 mph", "Always 15 mph", "The normal limit"], "Obey the posted school zone speed limit when it applies.", "Speed Limits"),

    # ---------- Traffic Signs ----------
    ("An octagon-shaped sign means", "Stop", ["Yield", "Warning", "No passing"], "Eight sides always means stop.", "Traffic Signs"),
    ("An upside-down triangle sign means", "Yield", ["Stop", "Warning", "No passing"], "The triangular sign means yield right of way.", "Traffic Signs"),
    ("A pennant-shaped sign on the left side of the road means", "No passing zone ahead", ["School zone", "Railroad crossing", "Yield ahead"], "Pennants mark the start of no-passing zones.", "Traffic Signs"),
    ("A diamond-shaped sign means", "Warning of a hazard ahead", ["Stop", "Guide information", "Prohibition"], "Diamond signs warn of hazards.", "Traffic Signs"),
    ("A pentagon-shaped (five-sided) sign means", "School zone or crossing", ["No passing", "Railroad", "Hospital"], "Five-sided signs mark school areas.", "Traffic Signs"),
    ("A round (circular) yellow sign means", "Railroad crossing ahead", ["Stop", "Yield", "Hospital"], "Round yellow signs warn of railroad crossings.", "Traffic Signs"),
    ("A white X-shaped crossbuck sign means", "Railroad crossing - yield to trains", ["Stop sign", "Crosswalk", "Intersection"], "The crossbuck marks the crossing; yield to trains.", "Railroad Crossings"),
    ("A tall vertical rectangular sign is usually", "A regulatory sign", ["A warning", "A guide sign", "A school sign"], "Vertical rectangles state laws you must follow.", "Traffic Signs"),
    ("A wide horizontal rectangular sign is usually", "A guide sign", ["A warning", "A prohibition", "A school sign"], "Horizontal rectangles give directions and guidance.", "Traffic Signs"),
    ("Orange-colored signs warn of", "Construction or maintenance work zones", ["School zones", "Hospitals", "Recreation"], "Orange = work zones.", "Traffic Signs"),
    ("Yellow-colored signs generally mean", "Warning", ["Stop", "Services", "Directions"], "Yellow signs are warnings.", "Traffic Signs"),
    ("Blue signs provide information about", "Motorist services", ["Warnings", "Directions", "Work zones"], "Blue = services like gas, food, lodging.", "Traffic Signs"),
    ("Brown signs point out", "Parks, recreation, and historic sites", ["Hospitals", "Work zones", "Speed limits"], "Brown = recreation and cultural sites.", "Traffic Signs"),
    ("Green signs provide", "Directions, distances, and exits", ["Warnings", "Prohibitions", "Work zone info"], "Green = guide information.", "Traffic Signs"),
    ("Red on a sign means", "Stop, yield, or a prohibition", ["Warning", "Services", "Directions"], "Red is used for stops, yields, and things you may not do.", "Traffic Signs"),
    ("A DO NOT ENTER sign means", "You are facing wrong-way traffic - do not enter", ["Proceed slowly", "Construction ahead", "Yield"], "Do Not Enter warns of wrong-way travel, often at ramps.", "Traffic Signs"),
    ("A WRONG WAY sign means", "You are driving against traffic - turn around safely", ["Proceed", "Slow down", "Merge left"], "Wrong Way means you are traveling against traffic.", "Traffic Signs"),
    ("A sign showing a person in a wheelchair means", "Handicap-accessible parking - permit required", ["Hospital zone", "Rest area", "Bus stop"], "Only vehicles with disability permits may park there.", "Traffic Signs"),
    ("A sign showing a U-turn arrow crossed out in red means", "No U-turn allowed", ["U-turn required", "Turn lane", "Roundabout"], "A red slash through a symbol prohibits the action.", "Traffic Signs"),
    ("A sign showing a deer warns of", "An area where deer commonly cross", ["Hunting zone", "Zoo nearby", "Animal hospital"], "Deer signs mark areas with high animal-crossing risk.", "Traffic Signs"),
    ("A sign reading SLIPPERY WHEN WET warns that", "The road becomes slick when wet - reduce speed", ["The road floods", "Ice ahead only", "Fog zone"], "Slow down and avoid sudden moves on that stretch when wet.", "Traffic Signs"),
    ("A merge sign warns that", "Another lane of traffic will merge with yours", ["Your lane ends", "Passing zone", "Divided highway"], "A merge sign means traffic joins your lane ahead.", "Traffic Signs"),
    ("A LANE ENDS or lane-reduction sign means", "Your lane will end - merge left or right safely", ["Merge traffic joins you", "New lane begins", "Passing allowed"], "Lane ends signs tell you to merge before your lane disappears.", "Traffic Signs"),
    ("A DIVIDED HIGHWAY BEGINS sign means", "A median or barrier will separate opposing traffic ahead", ["The highway ends", "Two-way traffic begins", "Passing zone"], "Opposing traffic will soon be separated by a median.", "Traffic Signs"),
    ("A TWO-WAY TRAFFIC sign warns that", "You are entering a road with opposing traffic in the adjacent lane", ["One-way street", "Passing zone", "Divided road"], "Two-way traffic signs appear where traffic flows in both directions.", "Traffic Signs"),
    ("A hill/downgrade warning sign means", "A steep slope ahead - you may need a lower gear", ["Bumpy road", "Falling rocks", "Truck stop"], "Downhill signs warn of steep grades; larger vehicles may need lower gears.", "Traffic Signs"),
    ("A low clearance sign warns that", "A bridge or overpass has limited height", ["Low speed zone", "Dip in road", "Weight limit"], "Low clearance signs give the maximum vehicle height for the structure ahead.", "Traffic Signs"),
    ("A speed number posted under a yellow warning sign is", "An advisory speed for the hazard", ["The legal limit", "A minimum speed", "A school limit"], "Advisory speeds are recommended safe speeds for curves or hazards.", "Traffic Signs"),
    ("A SIGNAL AHEAD sign warns that", "A traffic light is ahead - be ready to stop", ["A stop sign is ahead", "A school is ahead", "A railroad is ahead"], "Signal ahead signs warn of traffic lights you may not see yet.", "Traffic Signs"),
    ("A sign showing a bicycle warns of", "An area where bicycles commonly travel or cross", ["A bike shop", "A no-bike zone", "A park"], "Bicycle warning signs mark areas to watch for cyclists.", "Traffic Signs"),
    ("A pedestrian-crossing sign (person walking) warns of", "An area where pedestrians cross", ["A school only", "A mall", "A bus stop"], "Pedestrian signs mark crossings - watch for people on foot.", "Traffic Signs"),
    ("A YIELD AHEAD sign warns that", "A yield sign is coming - prepare to give right of way", ["Stop ahead", "Merge", "School zone"], "Yield ahead signs give advance notice of a yield point.", "Traffic Signs"),
    ("A roundabout warning sign (circular arrows) means", "A roundabout intersection is ahead", ["A U-turn zone", "A rest area", "A detour"], "Circular arrow signs warn of roundabouts ahead.", "Traffic Signs"),
    ("A REDUCED SPEED AHEAD sign means", "The speed limit drops ahead - slow down gradually", ["Speed up", "Stop ahead", "Passing ends"], "Prepare to comply with a lower posted limit ahead.", "Traffic Signs"),
    ("A KEEP RIGHT sign means", "Pass on the right side of an obstruction or island", ["Turn right only", "Right lane ends", "Stay right of yellow line"], "Keep Right signs mark obstructions you must pass on the right.", "Traffic Signs"),
    ("A ONE WAY sign means", "Traffic on that street moves in one direction only", ["One lane", "No passing", "Single file"], "One Way signs mark streets where all traffic flows one direction.", "Traffic Signs"),
    ("An orange triangular emblem on the back of a vehicle means", "It is a slow-moving vehicle (25 mph or less)", ["Farm auction", "Oversized load", "Handicap vehicle"], "Slow-moving vehicle emblems mark farm equipment and similar vehicles.", "Sharing the Road"),

    # ---------- Traffic Signals ----------
    ("A steady red light means", "Stop completely", ["Slow down", "Proceed", "Yield"], "Red means stop before the line or crosswalk.", "Traffic Signals"),
    ("A steady yellow light means", "The light is about to turn red - stop if you safely can", ["Speed up", "Go quickly", "Yield only"], "Yellow warns the signal is turning red; clear the intersection.", "Traffic Signals"),
    ("A steady green light means", "Go if the intersection is clear", ["Stop", "You always have right of way", "Speed up"], "Green means proceed when clear - yield to anyone still in the intersection.", "Traffic Signals"),
    ("A flashing red light means", "Treat it like a stop sign", ["Proceed", "Caution only", "Yield"], "Flashing red = complete stop, then proceed when safe.", "Traffic Signals"),
    ("A flashing yellow light means", "Slow down and proceed with caution", ["Stop", "Yield to all traffic", "Turn only"], "Flashing yellow = caution.", "Traffic Signals"),
    ("A flashing yellow arrow means", "Yield to oncoming traffic, then turn when safe", ["Protected turn", "No turns", "Turn immediately"], "Flashing yellow arrow = unprotected turn after yielding.", "Traffic Signals"),
    ("A green arrow means", "A protected turn - go in the arrow's direction when clear", ["Yield first", "Stop", "Oncoming traffic also goes"], "A green arrow protects your turn, but check the intersection is clear.", "Traffic Signals"),
    ("A red X over a lane means", "Do not drive in that lane", ["Lane for trucks", "Express lane", "HOV lane"], "Red X lane signals close that lane to your direction.", "Traffic Signals"),
    ("A green arrow pointing down over a lane means", "You may use that lane", ["Lane closed", "Trucks only", "Toll lane"], "Downward green arrows mark lanes open to traffic.", "Traffic Signals"),
    ("A steady yellow X over a lane means", "Move out of that lane - it will soon close to your direction", ["Lane open", "Speed up", "HOV only"], "Yellow X means vacate the lane safely.", "Traffic Signals"),
    ("A WALK pedestrian signal means", "Pedestrians may begin crossing", ["Don't cross", "Finish crossing only", "Drivers stop always"], "WALK allows pedestrians to start crossing.", "Traffic Signals"),
    ("A flashing DON'T WALK signal means", "Finish crossing if started, but don't begin", ["Run across", "Stop in street", "Drivers may go"], "Flashing Don't Walk = clear the street, don't start.", "Traffic Signals"),
    ("A steady DON'T WALK signal means", "Do not enter the roadway", ["Cross quickly", "Yield to cars in crosswalk", "Walk anytime"], "Steady Don't Walk = stay on the curb.", "Traffic Signals"),
    ("When a traffic signal is dark or malfunctioning you must", "Treat it as a four-way stop", ["Drive through", "Yield only", "Turn around"], "A dead signal is handled like an all-way stop.", "Traffic Signals"),

    # ---------- Right of Way ----------
    ("At a four-way stop, the first vehicle to arrive", "Goes first", ["Waits for others", "Yields to the left", "Must honk"], "First to arrive goes first at all-way stops.", "Right of Way"),
    ("When two vehicles reach a four-way stop simultaneously, who proceeds", "The vehicle on the right", ["The vehicle on the left", "The bigger vehicle", "Whoever honks first"], "Simultaneous arrivals - the driver on the right goes first.", "Right of Way"),
    ("When turning left at an intersection you must yield to", "Oncoming traffic going straight or turning right", ["No one", "Only pedestrians", "Traffic behind you"], "Left turns yield to oncoming through traffic.", "Right of Way"),
    ("At an intersection with no signs or signals you should yield to", "The vehicle on your right", ["The vehicle on your left", "Faster traffic", "Larger vehicles"], "Uncontrolled intersections: yield to traffic from the right.", "Right of Way"),
    ("At a T-intersection, traffic on the road that ends must yield to", "Traffic on the through road", ["No one", "Pedestrians only", "Bicycles only"], "The terminating road yields to the through road.", "Right of Way"),
    ("Entering a road from a driveway or alley, you must yield to", "All vehicles and pedestrians on the road", ["Only cars", "No one - you have right of way", "Only trucks"], "Entering traffic always yields to road traffic and pedestrians.", "Right of Way"),
    ("When an emergency vehicle approaches with lights and siren you must", "Pull to the right edge and stop", ["Speed up", "Stop in place", "Continue normally"], "Always yield to emergency vehicles by pulling right and stopping.", "Emergency Vehicles"),
    ("You must yield to pedestrians", "In marked and unmarked crosswalks at intersections", ["Only in marked crosswalks", "Only at signals", "Never"], "Every intersection is legally a crosswalk - yield to pedestrians.", "Pedestrians"),
    ("When you see a blind pedestrian with a white cane or guide dog you must", "Stop and yield the right of way", ["Honk to warn them", "Pass carefully", "Flash lights"], "Always stop for visually impaired pedestrians.", "Pedestrians"),
    ("At a school crossing with a crossing guard you must", "Obey the crossing guard", ["Obey only the signals", "Proceed carefully", "Yield to students only"], "Crossing guards have authority - follow their directions.", "School Zones"),
    ("You should never", "Drive between the vehicles of a funeral procession", ["Follow a procession", "Yield to a procession", "Stop for a procession"], "Do not cut into or through a funeral procession.", "Right of Way"),
    ("In a roundabout you must yield to", "Traffic already circulating (approaching from your left)", ["Traffic on your right", "Traffic behind you", "No one"], "Roundabouts flow counterclockwise - yield to traffic inside.", "Right of Way"),
    ("Merging onto a freeway, you must yield to", "Traffic already on the freeway", ["No one - they must let you in", "Only trucks", "Only the right lane"], "Freeway traffic has the right of way over merging traffic.", "Highway Driving"),
    ("If traffic is backed up at a green light and you cannot clear the intersection, you should", "Wait before the intersection - never block it", ["Enter and stop", "Honk to clear traffic", "Go around on the shoulder"], "Blocking an intersection (gridlocking) is illegal even on green.", "Right of Way"),
    ("A green light gives you the right to go", "Only when the intersection is clear", ["Always", "If you honk first", "Only at night"], "Green means go when safe - never enter a blocked intersection.", "Right of Way"),
    ("Vehicles backing up must yield to", "All other traffic and pedestrians", ["No one", "Only larger vehicles", "Only bicycles"], "Backing vehicles never have right of way.", "Right of Way"),
    ("Re-entering traffic from a parked position, you must", "Signal and yield to all traffic", ["Pull out quickly", "Wait for a wave", "Honk first"], "Parked vehicles re-entering must yield to moving traffic.", "Right of Way"),
    ("A yield sign tells you to", "Slow down, give right of way, and stop if needed", ["Always stop", "Speed up", "Ignore cross traffic"], "Yield = let others go first, stopping when required.", "Traffic Signs"),
    ("On a narrow mountain road, the vehicle going downhill should", "Back up or yield to the uphill vehicle", ["Force the uphill vehicle back", "Stop and wait", "Honk"], "Uphill vehicles may be unable to reverse safely - downhill drivers yield.", "Right of Way"),
    ("Bicycles on the road must follow", "The same traffic laws as motor vehicles", ["No laws", "Pedestrian laws", "Different signals"], "Bicyclists have the same rights and duties as drivers.", "Sharing the Road"),

    # ---------- Pavement Markings ----------
    ("Broken white lines separate", "Lanes of traffic going the same direction", ["Opposite directions", "Parking lanes", "Shoulders"], "Broken white = same-direction lanes you may cross.", "Pavement Markings"),
    ("A solid white line between same-direction lanes means", "Lane changes are discouraged", ["Passing encouraged", "Lane closed", "Truck lane"], "Solid white marks lane boundaries you should not cross unless necessary.", "Pavement Markings"),
    ("A solid yellow line on your side means", "No passing", ["Passing allowed", "Passing encouraged", "Truck only"], "Solid yellow on your side = no passing.", "Pavement Markings"),
    ("A broken yellow center line means", "Passing is allowed in either direction when safe", ["No passing", "Passing only for you", "One-way road"], "Broken yellow = passing permitted when safe.", "Pavement Markings"),
    ("Two solid yellow lines together mean", "No passing in either direction", ["Passing both ways", "Passing one way", "HOV lane"], "Double solid yellow = no passing either direction.", "Pavement Markings"),
    ("Yellow lines separate traffic moving in", "Opposite directions", ["Same direction", "Parking zones", "Bike lanes"], "Yellow divides opposing flows.", "Pavement Markings"),
    ("White lines separate traffic moving in", "The same direction", ["Opposite directions", "Bikes from cars", "Parking lanes"], "White divides same-direction lanes.", "Pavement Markings"),
    ("A two-way left turn lane in the center is for", "Left turns only - never passing or travel", ["Passing", "Parking", "U-turns only"], "Center turn lanes exist only for left turns.", "Pavement Markings"),
    ("A painted median (diagonal yellow stripes) means", "Do not drive on it", ["Parking allowed", "Passing lane", "Stopping zone"], "Painted medians are not travel lanes.", "Pavement Markings"),
    ("Red pavement reflectors or markers mean", "You are going the wrong way", ["Rough road", "Toll lane", "Emergency lane"], "Red markers warn you are traveling against traffic.", "Pavement Markings"),
    ("The left edge line of a roadway is", "Yellow", ["White", "Red", "Blue"], "Yellow edge lines mark the left side of the road.", "Pavement Markings"),
    ("The right edge line of a roadway is", "White", ["Yellow", "Red", "Green"], "White edge lines mark the right side of the road.", "Pavement Markings"),

    # ---------- School Buses ----------
    ("When a school bus flashes red lights with its stop arm out, traffic must stop within how many feet", "20 feet", ["10 feet", "30 feet", "50 feet"], "Stop at least 20 feet away in both directions on undivided roads.", "School Buses"),
    ("On an undivided road, school bus stop rules apply to", "Traffic in BOTH directions", ["Only traffic behind the bus", "Only oncoming traffic", "No one"], "Undivided roads: everyone stops, both directions.", "School Buses"),
    ("On a divided highway with a median, who must stop for a school bus", "Only traffic traveling the same direction as the bus", ["Both directions", "No one", "Only the car behind"], "Separated roadways exempt opposing traffic.", "School Buses"),
    ("Amber (yellow) flashing lights on a school bus mean", "The bus is preparing to stop - slow and prepare", ["Stop now", "Bus is empty", "Pass freely"], "Amber warns red lights and the stop arm are coming.", "School Buses"),
    ("You may pass a stopped school bus when", "The red lights stop flashing and the arm retracts, or the driver signals", ["After 5 seconds", "When children sit down", "Never"], "Wait until signals end or the driver waves you through.", "School Buses"),

    # ---------- Emergency Vehicles / Move Over ----------
    ("When an emergency vehicle approaches with lights and siren, pull", "To the right edge of the road and stop", ["Left", "Into the middle", "Nowhere - keep driving"], "Always pull right and stop for emergency vehicles.", "Emergency Vehicles"),
    ("The Move Over law applies to stopped vehicles with flashing lights including", "Emergency, tow, and road maintenance vehicles", ["Only police", "Only ambulances", "Only fire trucks"], "Move over or slow for ANY stopped vehicle with flashing lights.", "Emergency Vehicles"),
    ("Never follow an emergency vehicle responding to a call closer than", "500 feet", ["200 feet", "300 feet", "1,000 feet"], "Stay 500 feet behind responding emergency vehicles.", "Emergency Vehicles"),

    # ---------- Weather & Visibility ----------
    ("In fog you should use", "Low beam headlights", ["High beams", "Parking lights", "No lights"], "High beams reflect off fog - low beams work better.", "Driving Conditions"),
    ("High beam headlights in fog will", "Reflect back and reduce your visibility", ["Improve vision", "Warm the fog away", "Alert others better"], "High beams bounce off moisture and blind the driver.", "Driving Conditions"),
    ("When you must use your windshield wipers, Minnesota law requires", "Headlights on", ["Hazards on", "High beams", "Parking lights"], "Wipers on = headlights on.", "Vehicle Equipment"),
    ("If your car begins to hydroplane you should", "Ease off the gas and steer straight", ["Brake hard", "Speed up", "Turn sharply"], "No sudden moves - ease off gas, hold the wheel straight.", "Driving Conditions"),
    ("Hydroplaning can start at about", "35 mph", ["15 mph", "55 mph", "75 mph"], "Tires ride on water starting around 35 mph.", "Driving Conditions"),
    ("In snow or ice you should increase your following distance to", "Much more than 3 seconds", ["2 seconds", "Stay the same", "1 second"], "Winter traction demands far greater following distance.", "Following Distance"),
    ("Roads are most slippery", "When rain first begins", ["After hours of rain", "When dry", "Only in winter"], "First rain lifts oil and makes pavement slickest.", "Driving Conditions"),
    ("In cold weather, ice forms first on", "Bridges and overpasses", ["Main roads", "Parking lots", "City streets"], "Cold air above and below freezes bridges first.", "Driving Conditions"),
    ("Black ice is most likely on", "Shaded areas, bridges, and underpasses", ["Sunny roads", "Gravel roads", "Wide highways"], "Hidden thin ice lurks on shaded and elevated surfaces.", "Driving Conditions"),
    ("With ABS brakes during a hard stop you should", "Press firmly and hold", ["Pump rapidly", "Tap lightly", "Avoid using them"], "ABS does the pumping - press and hold steady.", "Emergencies"),
    ("If your vehicle starts to skid, steer", "In the direction you want the front to go", ["Opposite the skid", "Hard right", "Into the shoulder"], "Steer toward your intended path and ease off the pedals.", "Emergencies"),
    ("You should avoid using cruise control when", "Roads are wet, icy, or slippery", ["At night", "On highways", "In the city"], "Cruise control on slick roads can cause loss of control.", "Driving Conditions"),
    ("In a blizzard or whiteout, if you cannot see at all you should", "Pull completely off the road and stop with hazards on", ["Keep driving slowly", "Speed up", "Stop in your lane"], "Never stop in the travel lane - pull fully off the road.", "Driving Conditions"),
    ("After driving through deep water you should", "Test your brakes gently", ["Speed up", "Turn off the car", "Add washer fluid"], "Water can reduce braking - dry them with gentle use.", "Driving Conditions"),
    ("At night you should reduce speed enough that", "You can stop within the distance your headlights illuminate", ["You match other traffic", "You use cruise control", "You stay at the limit"], "Never outdrive your headlights.", "Driving Conditions"),
    ("In bright sun glare you should", "Use the sun visor, slow down, and increase distance", ["Drive faster", "Close your eyes briefly", "Use high beams"], "Glare reduces visibility - slow and shield your eyes.", "Driving Conditions"),
    ("Approaching a curve you should reduce speed", "Before entering the curve", ["In the middle", "After exiting", "Never"], "Brake before the curve, not during it.", "Driving Conditions"),

    # ---------- Emergencies ----------
    ("If a tire blows out you should", "Grip the wheel, ease off gas, steer straight", ["Brake hard", "Turn quickly", "Shift to park"], "Hold steady, ease off the gas, slow gradually, pull off.", "Emergencies"),
    ("If your brakes completely fail you should", "Pump the pedal, downshift, and use the parking brake gradually", ["Turn off the ignition", "Open the door", "Accelerate"], "Rebuild pressure by pumping, then use gears and the parking brake.", "Emergencies"),
    ("If the gas pedal sticks you should", "Shift to neutral and brake off the road", ["Turn the key to lock", "Keep driving", "Pull the pedal up while driving"], "Neutral disconnects engine power - then brake safely off the road.", "Emergencies"),
    ("If your hood suddenly flies up while driving you should", "Look through the gap under the hood, slow down, and pull off", ["Brake hard in place", "Open your door", "Speed up"], "Slow safely using the gap below the hood and exit the roadway.", "Emergencies"),
    ("If your headlights fail at night you should", "Try other lights/flashers and pull off the road", ["Keep driving in darkness", "Speed up home", "Follow another car closely"], "Get off the road using parking lights or hazards.", "Emergencies"),
    ("If your power steering fails you should", "Steer harder manually and pull over", ["Stop in the lane", "Turn off the car in traffic", "Pump the wheel"], "The car still steers - it just takes more effort. Pull over.", "Emergencies"),
    ("If your vehicle catches fire you should", "Pull off the road, get everyone out, and move away", ["Open the hood wide", "Pour water on the engine", "Drive to a shop"], "Get off the road and get clear - never open a burning hood.", "Emergencies"),
    ("If your engine overheats you should", "Pull over and let it cool - never open a hot radiator", ["Open the radiator cap", "Keep driving faster", "Add cold water immediately"], "Hot coolant can scald - wait for the engine to cool.", "Emergencies"),
    ("If your wheels drop off the pavement edge you should", "Slow down, then steer gently back onto the road", ["Jerk the wheel back", "Brake hard", "Accelerate onto the shoulder"], "Never yank the wheel - slow first, ease back on.", "Emergencies"),
    ("If your car stalls on railroad tracks with a train coming", "Get out and run toward the train at an angle away from tracks", ["Stay in the car", "Push the car", "Hide nearby"], "Debris blows forward - run toward the train at 45 degrees.", "Emergencies"),
    ("If your vehicle goes into deep water you should", "Unbuckle and exit through a window quickly", ["Wait for rescue inside", "Open the door against water", "Turn on lights"], "Escape through windows fast - doors won't open against water pressure.", "Emergencies"),
    ("If another driver is tailgating you, the safest response is", "Change lanes or slow down to encourage passing", ["Brake-check them", "Speed up hard", "Honk repeatedly"], "Increase space in front and let them pass - never brake-check.", "Driving Safety"),

    # ---------- Parking ----------
    ("When parking downhill with a curb, turn wheels", "Toward the curb", ["Away from the curb", "Straight", "Either way"], "Downhill: wheels toward the curb.", "Parking"),
    ("When parking uphill WITH a curb, turn wheels", "Away from the curb", ["Toward the curb", "Straight", "Either way"], "Uphill with curb: wheels away - the car rolls into the curb.", "Parking"),
    ("When parking uphill with NO curb, turn wheels", "Toward the road edge", ["Away from the road edge", "Straight", "Either way"], "No curb: wheels right so the car rolls off the road, not into traffic.", "Parking"),
    ("When parking on any hill you should always", "Set the parking brake", ["Leave it in neutral", "Turn off headlights", "Open windows"], "Always use the parking brake on hills.", "Parking"),
    ("It is illegal to park", "On a sidewalk, crosswalk, bridge, tunnel, or in an intersection", ["In your driveway", "On gravel shoulders only", "Near mailboxes"], "Never park where you block walkways, bridges, tunnels, or intersections.", "Parking"),
    ("It is illegal to park", "Blocking a public or private driveway", ["Next to a curb", "In marked spaces", "On your own street"], "Never block driveways.", "Parking"),
    ("Double parking (stopping beside a vehicle already at the curb) is", "Illegal - even for a moment", ["Legal for quick stops", "Legal downtown", "Allowed with hazards on"], "Double parking is illegal even briefly.", "Parking"),
    ("Parking in a handicap zone without a permit is", "Illegal and carries a fine", ["Allowed briefly", "Fine at night", "OK if spots are open"], "Disability spaces require proper permits.", "Parking"),

    # ---------- DWI / Legal ----------
    ("The DWI alcohol concentration limit for drivers 21 and over is", "0.08", ["0.04", "0.02", "0.16"], "0.08 is the adult limit; 0.16 brings enhanced penalties.", "DWI Laws"),
    ("The alcohol limit for commercial drivers is", "0.04", ["0.08", "0.02", "0.10"], "CDL holders face a 0.04 limit.", "DWI Laws"),
    ("Drivers under 21 may drive with an alcohol concentration of", "Zero - any amount violates Not a Drop", ["0.02", "0.04", "0.08"], "Not a Drop: no detectable alcohol for under-21 drivers.", "DWI Laws"),
    ("Refusing a DWI test under implied consent is", "A crime that revokes your license", ["Legal", "Just a fine", "A warning"], "Refusal itself is a crime in Minnesota.", "DWI Laws"),
    ("Driving can be impaired by", "Alcohol, illegal drugs, AND prescription medications", ["Alcohol only", "Drugs only", "Nothing legal"], "Any impairing substance - including legal prescriptions - can cause DWI.", "DWI Laws"),
    ("An alcohol concentration of 0.16 or higher brings", "Enhanced/aggravated DWI penalties", ["No extra penalty", "A warning", "Lower fines"], "Twice the limit means harsher consequences.", "DWI Laws"),
    ("Open alcoholic beverage containers in a vehicle", "Cannot be anywhere in the passenger area", ["Are fine if sealed", "Allowed in back seat", "OK if driver is sober"], "Open bottles belong in the trunk or not at all.", "DWI Laws"),
    ("Minnesota drivers must carry proof of insurance", "In the vehicle at all times", ["Only at renewal", "Only on highways", "At home"], "Proof of insurance must be available when you drive.", "Insurance"),
    ("Leaving the scene of a crash you are involved in is", "Illegal - a hit and run", ["Legal if damage is minor", "OK if no one is hurt", "Fine on private property"], "You must stop, help, and exchange information at any crash.", "Crashes"),
    ("At a crash scene you are required to", "Stop, render aid, exchange information, and report it", ["Just exchange info", "Only stop if injured", "Drive away slowly"], "Stop, help the injured, exchange info, and report crashes.", "Crashes"),
    ("Minnesota's hands-free law prohibits", "Holding a phone while driving", ["All phone use", "Bluetooth", "Passenger phone use"], "No holding phones - hands-free only for adults.", "Traffic Laws"),
    ("Drivers under 18 with a permit or provisional license", "May not use a phone at all while driving", ["May text only", "May call only", "Have no phone rules"], "Under-18 drivers: no phone use of any kind behind the wheel.", "Permits & Licensing"),
    ("Everyone in a moving vehicle must", "Wear a seat belt, front and back seats", ["Only front seat belts", "Only driver belts", "Only kids belted"], "Minnesota requires all occupants belted.", "Traffic Laws"),
    ("Child passengers must use a car seat or booster until", "Age 8 or 4 feet 9 inches tall", ["Age 4", "Age 6", "Age 10"], "Restraints required until 8 years old or 4'9\".", "Traffic Laws"),

    # ---------- Permits / GDL ----------
    ("You can apply for an instruction permit in Minnesota at age", "15", ["14", "16", "18"], "Permit age is 15.", "Permits & Licensing"),
    ("An instruction permit is valid for", "2 years", ["6 months", "1 year", "5 years"], "Permits last 2 years.", "Permits & Licensing"),
    ("Under-18 drivers must hold a permit at least ___ before the road test", "6 months", ["3 months", "1 month", "12 months"], "Six months minimum permit holding period.", "Permits & Licensing"),
    ("Permit holders under 18 must log supervised driving hours including", "50 total hours, 15 at night (40/15 if a parent takes the course)", ["20 hours", "10 hours", "No hours"], "MN requires 50 supervised hours with 15 at night; reduced to 40/15 with the parent course.", "Permits & Licensing"),
    ("The supervising driver for a permit holder must be", "A licensed driver 21 or older", ["Any licensed driver", "18 or older", "A parent only"], "Supervisors must be licensed and at least 21.", "Permits & Licensing"),
    ("While driving on a permit, you must", "Carry the permit and have every occupant belted", ["Only drive daytime", "Stay under 30 mph", "Drive only local streets"], "Carry your permit; everyone belts; no phone use.", "Permits & Licensing"),
    ("During the first 6 months of a provisional license, passengers under 20 are limited to", "One (unless accompanied by a parent/guardian)", ["Two", "Three", "None"], "First 6 months: only one non-family passenger under 20.", "Permits & Licensing"),
    ("During the first 6 months of a provisional license, night driving is restricted between", "Midnight and 5 a.m.", ["10 p.m. and 6 a.m.", "11 p.m. and 4 a.m.", "1 a.m. and 6 a.m."], "No driving midnight-5 a.m. in the first 6 months except with a 25+ licensed adult or for work/school.", "Permits & Licensing"),
    ("A driver with a provisional license becomes eligible for a full license at", "18 after meeting requirements", ["16 immediately", "21", "17"], "Full license at 18 after holding the provisional and staying violation-free.", "Permits & Licensing"),
    ("The Minnesota Class D knowledge test contains ___ questions and requires ___ to pass", "40 questions and 80% (32 correct)", ["20 and 70%", "30 and 75%", "50 and 90%"], "40 questions, 80% required.", "Permits & Licensing"),
    ("For the road test you must bring", "Your permit, insurance proof, and a safe registered vehicle", ["Only your permit", "Nothing", "A parent only"], "Bring permit, proof of insurance, registration, and a legal vehicle.", "Permits & Licensing"),

    # ---------- Sharing the Road ----------
    ("Motorcycles are legally entitled to", "A full lane", ["Half a lane", "The shoulder", "No lane rights"], "Never share a lane with a motorcycle - they get the full lane.", "Sharing the Road"),
    ("Before turning right, check carefully for", "Bicyclists approaching on your right", ["Nothing", "Only cars", "Only pedestrians behind"], "Bikes can be beside you - look before turning right.", "Sharing the Road"),
    ("Large trucks need", "More room to stop and wider turns", ["Less room", "The same as cars", "Only more speed"], "Trucks stop slower and swing wide - give them space.", "Sharing the Road"),
    ("Never cut in directly in front of a truck because", "They cannot stop as quickly as you", ["They will honk", "It is only rude, not dangerous", "Trucks stop faster"], "Trucks need much more stopping distance.", "Sharing the Road"),
    ("When a truck makes a wide right turn, you should", "Never squeeze into the space on the right", ["Fill the gap quickly", "Honk them forward", "Pass on the right"], "Trucks swing wide - the right side gap is deadly.", "Sharing the Road"),
    ("When following a motorcycle you should", "Increase your following distance", ["Follow closer", "Share their lane", "Use high beams"], "Motorcycles can stop faster - give extra space.", "Sharing the Road"),
    ("When passing slow farm equipment you should", "Pass carefully with plenty of clearance", ["Honk continuously", "Follow within 5 feet", "Pass on the shoulder"], "Slow-moving vehicles need wide, careful passing.", "Sharing the Road"),
    ("Approaching horses or horse-drawn vehicles you should", "Slow down and never honk", ["Honk to move them", "Speed past", "Flash high beams"], "Loud noises spook horses - slow and quiet is safest.", "Sharing the Road"),

    # ---------- Freeway / Highway ----------
    ("When merging onto a freeway you should", "Match freeway speed and merge into a gap", ["Stop at ramp end", "Merge at 25 mph", "Force in quickly"], "Use the acceleration lane to match speed and merge.", "Highway Driving"),
    ("If you miss your freeway exit you should", "Continue to the next exit", ["Back up", "Stop on the shoulder", "U-turn across the median"], "Never reverse on a freeway - take the next exit.", "Highway Driving"),
    ("The left lane of a multi-lane highway is for", "Passing and faster traffic", ["Cruising slowly", "Trucks only", "Parking"], "Slower traffic keeps right; left is for passing.", "Highway Driving"),
    ("A ramp meter signal means", "One vehicle proceeds per green light", ["Everyone goes on green", "Stop permanently", "Carpool lane only"], "Ramp meters space out merging traffic one at a time.", "Highway Driving"),
    ("On a freeway you may stop", "Only on the shoulder in an emergency", ["In any lane", "In the median", "On the ramp"], "Never stop in freeway lanes except emergencies on the shoulder.", "Highway Driving"),
    ("When exiting a freeway you should", "Move to the deceleration lane, then slow down", ["Brake hard in the travel lane", "Cut across lanes", "Stop before exiting"], "Exit lanes are where you decelerate - not the travel lanes.", "Highway Driving"),
    ("Slower vehicles on a multi-lane highway should", "Keep right", ["Keep left", "Use the center", "Stop"], "Slower traffic stays right.", "Highway Driving"),

    # ---------- Safe Habits ----------
    ("You should check your mirrors", "Regularly - every several seconds", ["Once per trip", "Only when changing lanes", "Never"], "Scan mirrors constantly to know what is around you.", "Driving Safety"),
    ("Defensive driving means", "Anticipating other drivers' mistakes", ["Driving fast", "Always yielding", "Driving only daytime"], "Expect errors from others and plan escape paths.", "Driving Safety"),
    ("If you are too tired to drive you should", "Pull over somewhere safe and rest", ["Open a window and continue", "Drink coffee and speed up", "Turn up the radio"], "Drowsy driving is like impaired driving - rest first.", "Driving Safety"),
    ("Drowsy driving affects you", "Similar to driving under the influence", ["Not at all", "Only at night", "Only on highways"], "Fatigue slows reactions like alcohol does.", "Driving Safety"),
    ("If an aggressive driver confronts you you should", "Create distance and avoid engagement", ["Confront them", "Race them", "Block their lane"], "Never engage with aggressive drivers - distance wins.", "Driving Safety"),
    ("You should look ahead while driving", "Well down the road - about a city block or more", ["Just at your bumper", "Only at mirrors", "Behind you"], "Scan far ahead to spot hazards early.", "Driving Safety"),
    ("Keeping a space cushion around your vehicle means", "Leaving room on all sides for escape", ["Parking far away", "Driving slow", "Tailgating less"], "Space on every side gives you room to react.", "Driving Safety"),
    ("Before driving in winter you should", "Clear all windows, lights, and the roof of snow and ice", ["Only the windshield", "Nothing", "Only mirrors"], "Flying snow/ice blinds you and others - clear the whole vehicle.", "Driving Conditions"),
    ("You should never leave a vehicle idling in a closed garage because of", "Carbon monoxide poisoning", ["Fuel waste", "Noise", "Battery drain"], "CO is odorless and deadly in enclosed spaces.", "Driving Safety"),
    ("Before changing lanes you should", "Signal, check mirrors, and look over your shoulder", ["Just signal", "Honk and go", "Brake first"], "Signal + mirrors + blind-spot check every time.", "Lane Changes"),

    # ---------- Vehicle Equipment ----------
    ("Minnesota requires tire tread depth of at least", "2/32 of an inch", ["1/32", "3/32", "4/32"], "Tires worn to 2/32 inch are legally bald.", "Vehicle Equipment"),
    ("Minnesota law requires your vehicle to have", "Working brakes, horn, mirrors, wipers, lights, and muffler", ["Only brakes", "Only lights", "Nothing if new"], "All required equipment must work.", "Vehicle Equipment"),
    ("Your horn must be audible from", "200 feet", ["100 feet", "500 feet", "50 feet"], "Horns must be heard at 200 feet.", "Vehicle Equipment"),
    ("Brakes on your vehicle must include", "Two separate braking systems", ["One system", "Three systems", "Only hand brake"], "Two independent systems are required in case one fails.", "Vehicle Equipment"),
    ("Front headlights must shine", "White or amber", ["Red", "Blue", "Green"], "White or amber forward lights; red is reserved for the rear.", "Vehicle Equipment"),
    ("Rear license plates at night must be lit with", "A white light", ["A red light", "No light", "A green light"], "Plates must be illuminated white so they can be read.", "Vehicle Equipment"),
    ("Tail lights must be", "Red and visible from 500 feet", ["White", "Blue", "Yellow"], "Red tail lights visible from 500 feet.", "Vehicle Equipment"),
    ("Windshield wipers must", "Be in working condition", ["Be optional", "Only work on driver side", "Be removed"], "Working wipers are required equipment.", "Vehicle Equipment"),
    ("Your muffler must", "Prevent loud or excessive noise", ["Be removed", "Be extra loud", "Be optional"], "Mufflers are required and must limit exhaust noise.", "Vehicle Equipment"),
    ("Seat belts in your vehicle must", "Work in every seating position", ["Only in front", "Be optional for adults", "Only for children"], "Every seat needs a working belt.", "Vehicle Equipment"),
]


# ============================================================
# BUILDER - generate phrasing/arrangement variants of each fact
# ============================================================
def _variants(stem, correct, wrongs, exp, ch):
    out = []
    stems = [stem if stem.endswith("?") else stem + "?"]
    # Rephrasing prefixes for statement-style stems -> more unique texts
    if not stem.startswith(("What", "Which", "How", "When", "Who", "At what", "A ", "An ",
                            "Minnesota", "True", "If ", "In ", "On ", "The ")):
        low = stem[0].lower() + stem[1:]
        stems.append("In Minnesota, " + low + "?")
        stems.append("Under Minnesota driving rules, " + low + "?")
        stems.append("According to the Minnesota Driver's Manual, " + low + "?")
        stems.append("For a Minnesota Class D driver, " + low + "?")
    for pos in range(4):
        for s in stems:
            rotated = wrongs[pos:] + wrongs[:pos]
            it = iter(rotated)
            opts = [correct if i == pos else next(it) for i in range(4)]
            out.append(_q(s, opts, pos, exp, ch))
    return out


def build_bank(target=1000):
    bank = []
    seen = set()

    def add(v):
        key = (v["question"], tuple(v["options"]))
        if key in seen:
            return
        seen.add(key)
        v["id"] = hashlib.md5(
            (v["question"] + "|" + "|".join(v["options"])).encode()
        ).hexdigest()[:12]
        bank.append(v)

    for q in CORE:
        add(dict(q))

    per_fact = [_variants(*f) for f in FACTS]
    depth = 0
    while len(bank) < target:
        added = 0
        for vs in per_fact:
            if depth < len(vs):
                add(vs[depth])
                added += 1
            if len(bank) >= target:
                break
        if added == 0:
            break
        depth += 1
    return bank


if __name__ == "__main__":
    b = build_bank()
    print(f"Bank size: {len(b)}")
    texts = {q["question"] for q in b}
    print(f"Unique question texts: {len(texts)}")
