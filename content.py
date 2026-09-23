#!/usr/bin/env python3
"""Everything a person might want to change lives in this file.

`build.py` is a generator and holds no copy of its own. If you are about to
edit a sentence, a temperature or a phone number anywhere else, that is a bug.

SOURCES FOR THIS CONTENT
  - amtheat.com (founding year, headcount, process list, gallery photographs
    and one customer testimonial)
  - "Everest Heat Treaters Profile 2025" PDF (furnace and lab equipment,
    monthly tonnage, customer list, team, ISO history, works address)

Both documents were supplied by the client as their own company data. Where
the two disagree, the figure used is noted in a comment so it can be settled
in one place.
"""

# ---------------------------------------------------------------- flags ----

# Draft builds must never be indexed. Flip to False at launch.
NOINDEX = False

# The "figures need a final check" banner. Off once the client has confirmed
# every number in this file.
SHOW_CONCEPT_NOTE = False

# ---------------------------------------------------------------- brand ----

NAME = "Everest Heat Treaters"
SHORT_NAME = "Everest Heat Treaters"
INITIALS = "EHT"
# What shows in the browser tab. "Everest" leads so the tab stays
# identifiable even where the title is truncated.
TAB_NAME = "Everest Heat Treaters"
TAGLINE = "Heat treatment for ferrous &amp; non-ferrous metals"
CERT = "An ISO 9001:2015 certified company"
DESCRIPTION = (
    "Commercial heat treatment in Chennai — hardening and tempering, "
    "case hardening, annealing, normalising, stress relieving "
    "and solution treatment for ferrous and non-ferrous components. "
    "ISO 9001:2015 certified, working to ASTM standards."
)

# Who a customer deals with, in order: the managing director first, then
# the metallurgist. Shown in the footer, on About and on Contact.
CONTACTS = [
    ("R. Sathyamoorthy", "Managing Director", ""),
    ("S. Aravindth", "Metallurgist", "B.E., M.E."),
]

PHONE = "+91 6379 547 322"
PHONE_LINK = "+916379547322"
WHATSAPP = "916379547322"
EMAIL = "everest_heattreaters@yahoo.co.in"
GSTIN = "33ANNPS4415M1ZK"

# The postal address, as it appears on the company profile and the GST
# registration. The client asked for Ambattur to be left out of it.
LOCALITY = "Nazarathpettai, Chennai"
ADDRESS_LINES = [
    "S. No. 315/1, Meppur Road",
    "Malayambakkam, Nazarathpettai",
    "Chennai &ndash; 600 123",
    "Tamil Nadu, India",
]
ADDRESS_ONE_LINE = ("S. No. 315/1, Meppur Road, Malayambakkam, "
                    "Nazarathpettai, Chennai 600123")
# Points at the works itself. The business has a Google listing, so the
# name resolves to the right pin.
MAP_QUERY = ("Everest Heat Treaters, Meppur Road, Malayambakkam, "
             "Nazarathpettai, Chennai 600123")

HOURS = [("Monday &ndash; Saturday", "9:00 AM &ndash; 7:00 PM"),
         ("Sunday", "By prior arrangement")]

# ------------------------------------------------------------------ nav ----

NAV = [
    ("index.html", "Home"),
    ("processes.html", "Processes"),
    ("materials.html", "Materials"),
    ("quality.html", "Quality"),
    ("industries.html", "Industries"),
    ("gallery.html", "Gallery"),
    ("about.html", "About"),
]
# Contact sits outside NAV: it is the button at the end of the header, so
# listing it twice would put two routes to one page side by side. Quote
# requests and general contact are the same page.
CONTACT_PAGE = ("contact.html", "Contact")

# ----------------------------------------------------------------- hero ----

HERO_EYEBROW = "Nazarathpettai, Chennai &middot; ISO 9001:2015"
# "Metal" cycles through the incandescent colours with a live temperature
# reading above it, driven from GLOW_COLOURS — the same table as the scale
# further down the page.
HERO_TITLE = ('<span class="heat" data-heat-word>'
              '<span class="heat__t" data-heat-temp aria-hidden="true"></span>'
              'Metal</span>, the way<br>you want it to be.')
# The stretch of the scale the word travels, in degrees C. The floor is set
# by legibility rather than taste: below about 715C the incandescent colours
# fall under 3:1 against the dark ground and the word starts to disappear.
# verify.py enforces this.
HERO_HEAT_RANGE = (740, 1250)
# The header brand runs half a cycle out of step, so when the hero word is at
# red the name is at orange and the two never sit on the same colour. Its
# floor is higher because the name drops to 16px on a phone, where it is no
# longer "large text" and needs 4.5:1 rather than 3:1.
BRAND_HEAT_RANGE = (840, 1250)
HERO_TEXT = (
    "ISO 9001:2015 certified for the heat treatment of ferrous and "
    "non-ferrous metals. We work to your specification and reach the "
    "hardness you ask for, and every batch leaves here with a report that "
    "says so."
)
# No photograph behind the hero. The mark is drawn as line art instead —
# see trace.py and mark_paths.py.
HERO_IMAGE = None

# The band under the hero. Every figure here comes from the Everest Heat
# Treaters 2025 company profile — 2005, 200,000 kg a month, 100+ customers,
# 800-1000 kg charges. Do not take figures from amtheat.com: that is a
# different company with a different founding year and headcount.
STATS = [
    ("21", "years", "Treating metal in Chennai"),
    ("200", "tonnes", "Through the furnaces monthly"),
    ("100", "+", "Manufacturers served"),
    ("1,000", "kg", "Per furnace charge"),
]

# ------------------------------------------------------- temperature UI ----
# The centrepiece. Real metallurgy, not decoration.
#
# Below roughly 400 C steel does not glow; what you see is the interference
# colour of the oxide film, which is why toolmakers have judged tempering by
# eye for two centuries. Above it, the metal is incandescent and the colour
# is blackbody radiation. The scale below crosses that boundary honestly.

TEMP_MIN = 150
TEMP_MAX = 1300

# (temp C, swatch colour, name) — oxide interference colours on clean steel.
TEMPER_COLOURS = [
    (150, "#C9C6BE", "Bare steel"),
    (176, "#E4D9A8", "Pale yellow"),
    (205, "#E6C874", "Light straw"),
    (226, "#D8A94E", "Dark straw"),
    (245, "#B87A3C", "Brown"),
    (265, "#9A5740", "Purple-brown"),
    (277, "#7E4A62", "Purple"),
    (293, "#4E568F", "Blue"),
    (315, "#5E7FA8", "Light blue"),
    (337, "#7C8A93", "Grey-blue"),
    (400, "#6E6E6E", "Scaled grey"),
]

# (temp C, glow colour, name) — incandescence, the smith's colour scale.
GLOW_COLOURS = [
    (480, "#4A1206", "First visible red"),
    (580, "#7E1B05", "Blood red"),
    (700, "#A82D04", "Dark cherry"),
    (800, "#D14405", "Cherry red"),
    (870, "#E85F06", "Bright cherry"),
    (930, "#F6790A", "Orange"),
    (1000, "#FF9420", "Orange-yellow"),
    (1100, "#FFB63F", "Yellow"),
    (1200, "#FFD26B", "Light yellow"),
    (1300, "#FFE9A8", "White heat"),
]

# --------------------------------------------------------------- process ---
# The eight processes, described the way the plant actually runs them.
# Each has its own picture so the homepage tiles read apart: stills from the
# client's own videos for the furnace and quench work, and licensed
# micrographs (see CREDITS.md) for the two that happen inside the metal. The
# temperatures and times are the client's own figures (September 2026); where
# a figure depends on the grade, the text says so rather than inventing one.
# The first six also appear on the homepage, so the order is the order of
# importance.

PROCESSES = [
    dict(
        slug="hardening-tempering",
        name="Hardening &amp; Tempering",
        short="Heat, quench in oil, then temper back to the hardness the part "
              "needs. The temperature is set by the material.",
        temp="Set by grade. EN24 hardens at 840&ndash;860&deg;C",
        result="The hardness your drawing specifies",
        image="g-oil-quench",
        body=[
            "Every material has its own hardening temperature, so the cycle "
            "starts from the grade. Take EN24: it goes up to 840&ndash;860&deg;C, "
            "holds until the whole section has reached temperature, and is "
            "then quenched in oil. The quench locks the steel into its "
            "hardest structure.",
            "Straight out of the quench the part is too brittle to use. "
            "Tempering at a lower temperature brings it back to the hardness "
            "you asked for, and that number is what the tempering cycle is "
            "set to.",
        ],
        points=["Hardening temperature set by grade",
                "Oil quenching",
                "Tempered to the hardness you ask for",
                "Hardness checked before dispatch"],
        suits=["EN24", "EN19", "EN8", "EN9", "EN31", "C45", "410"],
    ),
    dict(
        slug="case-hardening",
        name="Case Hardening &amp; Tempering",
        short="A hard, wear-resistant case over a tough core. Carburised at "
              "940&deg;C, then hardened from 840&deg;C.",
        temp="Carburise at 940&deg;C, harden from 840&deg;C",
        result="1.5&ndash;2 mm case from a six-hour soak",
        image="p-case-lift",
        body=[
            "Low-carbon steel like EN1A can&rsquo;t take much hardness on its "
            "own, so carbon is added to the surface first. The parts are "
            "carburised at 940&deg;C, and a six-hour soak builds a case "
            "about 1.5 to 2 mm deep.",
            "For case hardening and tempering, the charge then comes down to "
            "840&deg;C, soaks for an hour and is quenched in oil or water, "
            "depending on the grade. When only the case is wanted, the parts "
            "cool inside the furnace and come out cold, ready for machining.",
        ],
        points=["Carburised at 940&deg;C",
                "Six-hour soak for a 1.5&ndash;2 mm case",
                "Hardened from 840&deg;C, one-hour soak",
                "Oil or water quench, or furnace cooled for case only"],
        suits=["EN1A", "EN36", "EN353", "SAE 8620", "16MnCr5", "20MnCr5"],
    ),
    dict(
        slug="annealing",
        name="Annealing",
        short="Making a material softer so it machines and forms easily. "
              "Heated for its grade, then cooled in the furnace.",
        temp="Set by grade. 410 anneals at 880&ndash;900&deg;C",
        result="Softened and ready to machine",
        image="p-furnace-glow",
        body=[
            "Annealing makes a material softer. Each grade has its own "
            "annealing temperature; 410 stainless, for example, goes to "
            "880&ndash;900&deg;C.",
            "The part holds there until it is even all the way through, then "
            "cools slowly inside the furnace and only comes out once it has "
            "cooled. That slow cool is what leaves it soft.",
        ],
        points=["Temperature set by grade",
                "Soaked through the full section",
                "Cooled inside the furnace",
                "Taken out after cooling"],
        suits=["410", "EN31", "EN8", "C45", "Castings", "Forgings"],
    ),
    dict(
        slug="normalising",
        name="Normalising &amp; Tempering",
        short="The step after forging. Heated to 900&ndash;940&deg;C, held for "
              "the section thickness, cooled in air.",
        temp="900&ndash;940&deg;C, as the standard sets",
        result="A refined, even grain after forging",
        image="g-normalising",
        body=[
            "Most of our normalising work arrives as forgings. The temperature "
            "depends on the material, and the standard puts most grades at "
            "900&ndash;940&deg;C.",
            "Holding time comes from the thickness of the part. A 50 mm "
            "section holds for about two hours. After the soak the charge "
            "comes out and cools in air, and is tempered afterwards where the "
            "specification calls for it.",
        ],
        points=["900&ndash;940&deg;C as per standard",
                "Holding time set by section thickness",
                "About two hours for a 50 mm section",
                "Air cooled, then tempered"],
        suits=["Forgings", "EN8", "EN19", "C45", "Carbon steels"],
    ),
    dict(
        slug="stress-relieving",
        name="Stress Relieving",
        short="Mostly for welded components. Taking out the stress welding "
              "leaves behind, without changing the hardness.",
        temp="Set by the base material and the weld",
        result="Stress relieved, hardness unchanged",
        image="p-bogie",
        body=[
            "Most of the stress relieving we do is on welded components. The "
            "base metal and the weld carry different stresses, and a part "
            "left that way can crack or move once it is machined or put into "
            "service.",
            "A typical job is a cast valve body with weld deposited on top. "
            "The whole part is held at the temperature its base grade and "
            "welding procedure call for, then cooled slowly so the stress "
            "comes out evenly.",
        ],
        points=["Welded components and fabrications",
                "Base metal and weld relieved together",
                "Temperature set by grade and welding procedure",
                "Slow, even cooling"],
        suits=["Weldments", "Valve bodies", "Castings", "Fabrications"],
    ),
    dict(
        slug="solution-annealing",
        name="Solution Annealing",
        short="For non-magnetic stainless steels. Heated to "
              "1040&ndash;1080&deg;C, then quenched within 20 seconds.",
        temp="1040&ndash;1080&deg;C, time by thickness",
        result="Corrosion resistance restored, magnetism relieved",
        image="p-water-quench",
        body=[
            "Solution annealing is for the non-magnetic stainless steels. The "
            "charge goes to 1040&ndash;1080&deg;C and holds for a time set "
            "by the thickness, often around two hours.",
            "Then speed matters. The parts go from the furnace into the "
            "liquid quench within 20 seconds. That fixes the structure, "
            "restores corrosion resistance and relieves the magnetism that "
            "welding or cold work can bring in.",
        ],
        points=["1040&ndash;1080&deg;C",
                "Soak time by thickness, around two hours",
                "Into the quench within 20 seconds",
                "Relieves induced magnetism"],
        suits=["304", "316", "321", "347", "Duplex"],
    ),
    dict(
        slug="age-hardening",
        name="Age Hardening &amp; Precipitation Hardening",
        short="For special grades like 718. After solution treatment, two "
              "long ageing holds bring out the strength.",
        temp="Two-step ageing, the second at 620&deg;C",
        result="Precipitation hardened to specification",
        image="p-precipitates",
        body=[
            "Special grades such as 718 get their strength from "
            "precipitation, not from a quench. The material is solution "
            "treated first and aged afterwards.",
            "Ageing is two long holds. The charge soaks for ten hours at the "
            "first ageing temperature, is furnace cooled to 620&deg;C, holds "
            "there for eight hours and is then air cooled. Fine particles "
            "form inside the metal during those holds, and they are what "
            "bring the hardness up.",
        ],
        points=["Solution treated first",
                "Ten-hour soak at the first ageing step",
                "Furnace cooled to 620&deg;C, eight-hour hold",
                "Air cooled"],
        suits=["718", "17-4 PH", "PH stainless"],
    ),
    dict(
        slug="stabilising",
        name="Stabilising",
        short="For the stabilised stainless grades F321 and F347, run to the "
              "cycle their specification sets.",
        temp="As the grade&rsquo;s specification sets",
        result="Protected against grain-boundary corrosion",
        image="micro-stainless",
        body=[
            "F321 and F347 are stainless steels with titanium or niobium "
            "added to protect them from corrosion at the grain boundaries. "
            "A stabilising treatment is what puts that protection to work.",
            "The parts are held to the cycle their specification calls for, "
            "so the titanium or niobium ties up the carbon before chromium "
            "can. The grain boundaries stay corrosion resistant, even in "
            "high-temperature service.",
        ],
        points=["F321 and F347",
                "Held to the specified cycle",
                "Protects against grain-boundary corrosion",
                "For high-temperature service"],
        suits=["F321", "F347"],
    ),
]

# The homepage line under "The process of transformation." The processes
# page carries the longer PROCESSES_INTRO, so the two never repeat.
PROCESSES_HOME_INTRO = (
    "Eight processes for ferrous and non-ferrous metals. Pick one to see how "
    "we run it."
)
H_PROCESSES_PAGE = "How we run each process"
# The order of the tiles on the homepage only. Four pictures glow and four
# are cool (the bogie, the water quench and two micrographs), so they are
# laid out as a checkerboard rather than all the hot ones in the top row.
# Everywhere else keeps the order of PROCESSES.
PROCESSES_HOME_ORDER = [
    "hardening-tempering", "stress-relieving", "case-hardening",
    "solution-annealing",
    "age-hardening", "annealing", "stabilising", "normalising",
]

PROCESSES_INTRO = (
    "Eight processes, for ferrous and non-ferrous metals. We work to your "
    "specification, and where there isn&rsquo;t one, to ASTM and other "
    "general standards. Whatever hardness you need, we have the experience "
    "to reach it."
)

# ------------------------------------------------------------- materials ---
# (grade, family, typical process, typical result, note)
MATERIALS = [
    ("EN8 / 080M40", "Medium carbon", "Harden &amp; temper", "25&ndash;35 HRC",
     "General shafts, studs, keys"),
    ("EN9 / 070M55", "Medium carbon", "Harden &amp; temper", "30&ndash;40 HRC",
     "Higher strength than EN8"),
    ("C45", "Medium carbon", "Harden &amp; temper", "45&ndash;55 HRC",
     "Very common general engineering grade"),
    ("EN19 / 709M40", "Cr-Mo alloy", "Harden &amp; temper", "28&ndash;40 HRC",
     "Good through-hardening in section"),
    ("EN24 / 817M40", "Ni-Cr-Mo alloy", "Harden &amp; temper", "32&ndash;45 HRC",
     "Hardened at 840&ndash;860&deg;C, oil quenched"),
    ("EN31 / 534A99", "Bearing steel", "Harden, temper &amp; stabilise",
     "58&ndash;63 HRC", "Spheroidise anneal before machining"),
    ("EN1A", "Free-cutting low carbon", "Case harden &amp; temper",
     "1.5&ndash;2 mm case", "Carburised at 940&deg;C for six hours"),
    ("EN36 / 655M13", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Tough core, hard case"),
    ("SAE 8620", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "The default gear steel"),
    ("16MnCr5", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Automotive transmission"),
    ("20MnCr5", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Deeper case than 16MnCr5"),
    ("D2 / X153CrMoV12", "Cold work tool", "Harden &amp; temper",
     "58&ndash;62 HRC", "Blanking and forming dies"),
    ("D3", "Cold work tool", "Harden &amp; temper", "58&ndash;62 HRC",
     "High wear, lower toughness"),
    ("O1", "Oil hardening tool", "Harden, temper &amp; stabilise",
     "58&ndash;62 HRC", "Low distortion, gauges and cutters"),
    ("H13 / X40CrMoV5-1", "Hot work tool", "Harden &amp; temper",
     "44&ndash;52 HRC", "Die casting and extrusion dies"),
    ("M2 HSS", "High speed steel", "Harden &amp; triple temper",
     "62&ndash;65 HRC", "Tight control through the cycle"),
    ("S7", "Shock resisting", "Harden &amp; temper", "54&ndash;58 HRC",
     "Punches and chisels"),
    ("SG Iron / Ductile", "Cast iron", "Normalise &amp; temper", "Varies",
     "Austemper available on enquiry"),
    ("Grey cast iron", "Cast iron", "Stress relieve", "Hardness unchanged",
     "Machine bed and housing stability"),
    ("304 / 316", "Austenitic stainless", "Solution anneal", "Soft, ~80 HRB",
     "Restores corrosion resistance after welding"),
    ("F321 / F347", "Stabilised stainless", "Solution anneal / stabilise",
     "Soft, ~80 HRB", "For high-temperature service"),
    ("410 / 420", "Martensitic stainless", "Harden &amp; temper / anneal",
     "40&ndash;50 HRC", "410 anneals at 880&ndash;900&deg;C"),
    ("718", "Nickel alloy", "Solution + age", "To specification",
     "Two-step ageing, second hold at 620&deg;C"),
    ("17-4 PH", "PH stainless", "Solution + age", "40&ndash;44 HRC",
     "Condition H900 to H1150"),
    ("Al 6061 / 6082", "Aluminium", "Solution + age (T6)", "~95 HB",
     "Most common structural temper"),
    ("Al 7075", "Aluminium", "Solution + age (T6)", "~150 HB",
     "High strength, quench sensitive"),
    ("Al 2014", "Aluminium", "Solution + age (T6)", "~135 HB",
     "Aerospace and tooling plate"),
    ("Brass &amp; bronze", "Copper alloy", "Anneal / stress relieve", "Softened",
     "Prevents season cracking"),
]

MATERIALS_INTRO = (
    "The grades we treat most, and what they usually land at. "
    "Tap any grade to enquire about it."
)

# --------------------------------------------------------------- quality ---

QUALITY_INTRO = (
    "How we show you which one you are getting, on every batch."
)

QUALITY = [
    dict(name="Rockwell, Brinell &amp; optical Brinell", image="g-rockwell-floor",
         text="Rockwell, Brinell and optical Brinell-cum-Rockwell testers in "
              "house, reading at the points your drawing specifies. The "
              "number goes on the report that travels with the parts."),
    dict(name="Portable hardness testing", image="g-inspection-area",
         text="A portable tester reaches long shafts, bogie-load work and "
              "finished assemblies that will never fit under a bench "
              "machine, so big parts get the same proof as small ones."),
    dict(name="Microstructure at 500&times;", image="g-lab-2",
         text="Cut on the abrasive saw, mounted, polished on the twin-disc "
              "grinder, etched and examined at up to 500&times;. It confirms "
              "the structure the process was meant to produce."),
    dict(name="Calibration &amp; power backup", image="g-shop-floor",
         text="Every furnace is calibrated as per standard by an "
              "NABL-accredited lab, across 100&ndash;1050&deg;C. Two gensets "
              "back up the power, a 125&nbsp;kVA Kirloskar GenLight and a "
              "45&nbsp;kVA Powerica, so a long cycle finishes the way it "
              "started."),
]

QUALITY_POINTS = [
    ("ISO 9001:2015", "Certified since 2006 for the heat treatment of "
                      "ferrous and non-ferrous metals, and audited every "
                      "year."),
    ("Your specification first", "We work to the customer&rsquo;s "
                                 "specification, whatever it asks for. "
                                 "Where there isn&rsquo;t one, we follow "
                                 "ASTM and other general standards."),
    ("Calibrated furnaces", "Every furnace is calibrated as per standard by "
                            "an NABL-accredited lab, across its working "
                            "range of 100&ndash;1050&deg;C."),
    ("The hardness you need", "Years on the floor mean we reach the hardness "
                              "you ask for, and a report travels with every "
                              "batch to show it."),
]

# ------------------------------------------------------------- headings ---
# Section headlines. They live here so build.py stays a pure generator.

H_PROCESSES = "The process of transformation."
H_PROOF = "We measure the treatment"
H_QUALITY = "Every batch is tested before it leaves."
H_QUALITY_SYSTEM = "How it is controlled"
H_MICRO = "The evidence is in the grain."
H_MICRO_TEXT = ("Etched cross-sections under the microscope at up to "
                "500&times; &mdash; a direct look at what the process did to "
                "the metal.")
H_INDUSTRIES = "We treat for many industries. These three lead."
H_CUSTOMERS = "Who our parts go back to"
H_ABOUT_PILLARS = "Three things we hold to"
H_VISION = "What we are aiming at"

# ------------------------------------------------------------- customers ---
# (name, logo file in assets/logos/). The logos are the companies' own marks,
# shown white on the dark ground: Wikimedia Commons for five of them, Wheels
# India's own site for the sixth.
CUSTOMERS = [
    ("L&amp;T Valves", "lt.svg"),
    ("Flowserve", "flowserve.svg"),
    ("Schwing Stetter", "schwing.png"),
    ("Caterpillar", "caterpillar.svg"),
    ("Wheels India", "wheelsindia.png"),
    ("BHEL", "bhel.svg"),
]

CUSTOMERS_INTRO = (
    "Over a hundred manufacturers send us work, from single prototypes to "
    "steady production. A few of the names our parts go back to:"
)

# ------------------------------------------------------------ industries ---
# The three fields the client named. Each gets an image from the gallery.

INDUSTRIES = [
    dict(
        name="Valves, oil &amp; gas",
        image="g-dispatch-2",
        alt="Treated valve components racked for dispatch",
        body=[
            "Valve bodies, bonnets, stems, discs and seats, much of it in "
            "stainless and alloy steel for oil, gas and process plant. These "
            "parts have to hold pressure and resist corrosion for years, and "
            "valve makers check the paperwork as closely as the parts.",
            "Cast bodies are normalised, or stress relieved after weld "
            "build-up. Stainless trim is solution annealed and quenched "
            "within 20 seconds, stabilised grades like F321 and F347 get "
            "their own cycle, and special alloys such as 718 are aged to "
            "specification. Every batch goes back with its hardness report.",
        ],
        points=["Solution annealing", "Stress relieving", "Stabilising",
                "Age hardening"],
    ),
    dict(
        name="Cement mixer trucks",
        image="g-receiving-3",
        alt="Components arriving at the receiving area",
        body=[
            "A transit mixer turns a loaded drum all day on rough site roads. "
            "The shafts, pins, bushes, gears and wear parts behind it take "
            "abrasion, shock and constant vibration, and a soft part shows up "
            "quickly.",
            "These parts are hardened and tempered for strength, or case "
            "hardened so the surface resists wear while the core takes the "
            "shock. Welded brackets and frames are stress relieved so they "
            "hold their shape.",
        ],
        points=["Hardening &amp; tempering", "Case hardening",
                "Stress relieving"],
    ),
    dict(
        name="Railways",
        image="g-receiving-area",
        alt="Shafts and bar stock laid out on the shop floor",
        body=[
            "Railway parts are expected to run for years with little "
            "maintenance and no surprises, often under heavy, repeated load.",
            "We treat forged and machined parts for rail use: forgings are "
            "normalised and tempered to refine the grain, shafts and pins are "
            "hardened and tempered to the specified hardness, and welded "
            "assemblies are stress relieved. All of it is done to the "
            "customer&rsquo;s specification.",
        ],
        points=["Normalising &amp; tempering", "Hardening &amp; tempering",
                "Stress relieving"],
    ),
]

INDUSTRIES_INTRO = (
    "Three kinds of work fill most of our furnaces: valves for oil and gas, "
    "the cement mixer trucks that serve every building site, and parts for "
    "the railways. Batch sizes run from a single prototype to steady "
    "production."
)

# ---------------------------------------------------------------- about ----

ABOUT_TITLE = "Twenty-one years of getting metal to behave"
# No photograph behind the About heading: the team shot is shown whole in the
# team section instead, where no one gets cropped.
ABOUT_IMAGE = None
ABOUT_BODY = [
    "Everest Heat Treaters is a commercial heat treatment works in "
    "Nazarathpettai, on the western edge of Chennai. Manufacturers across the "
    "country send us components and we return them harder, tougher or softer "
    "&mdash; whatever the specification asks for &mdash; with the "
    "documentation to prove it. We have been doing this since 2005, for "
    "ferrous and non-ferrous metals alike.",
    "The plant runs a bogie hearth furnace for long and heavy work, gas "
    "carburising and tempering pit furnaces, and a deep pit furnace for parts "
    "up to two metres long, with charges of 800 to 1,000 kg. Quenching is "
    "done in an oil tank and a water tank, each stirred by an impeller so the "
    "whole charge cools evenly. Two-tonne cranes move the work, and two "
    "gensets, a 125&nbsp;kVA Kirloskar GenLight and a 45&nbsp;kVA Powerica, "
    "back up the power. Around 200 tonnes a month goes through.",
    "Most heat treatment problems arrive as a part that cracked, distorted or "
    "came out soft, and the answer usually sits in the steel grade, a section "
    "change, a sharp corner or a specification that was never right for the "
    "application. We would much rather have that conversation before the "
    "batch runs. If your drawing specifies a treatment that will struggle to "
    "do what you need, you will hear it from us early.",
]

ABOUT_PILLARS = [
    ("Advice before the batch runs", "If the spec looks wrong for the "
     "application, we say so while it is still cheap to change."),
    ("Every batch documented", "ISO 9001:2015 since 2006, with a hardness "
     "report on every delivery."),
    ("Built for job work", "One prototype or a thousand pieces, treated on "
     "the same recorded cycle."),
]

# --------------------------------------------------------------- the team --

TEAM_TITLE = "The people who run the works"
TEAM_INTRO = ("The same team has run the floor for years, and you will deal "
              "with them directly.")
TEAM_IMAGE = ("g-team-2", "The Everest Heat Treaters team outside the works")
TEAM = [
    ("R. Sathyamoorthy", "Proprietor &amp; Managing Director"),
    ("S. Aravindth", "Metallurgist"),
    ("A. Selvam", "Quality In-charge"),
    ("Saravana Pandian", "Production In-charge"),
    ("T. R. Thiyagarajan", "Maintenance"),
]

# ------------------------------------------------------------------ plant --
# From the list of machineries in the 2025 company profile.
PLANT_TITLE = "Furnaces and sizes"
PLANT_INTRO = ("What each furnace takes. Charges run from 800 to 1,000 kg, "
               "and every furnace is calibrated by an NABL-accredited lab.")
PLANT = [
    ("Bogie hearth furnace", "3000 L &times; 900 W &times; 450 H mm",
     "Long, heavy and welded work"),
    ("Pit furnace, gas carburising", "800 dia &times; 1200 mm",
     "Case hardening"),
    ("Pit furnace, gas carburising", "700 dia &times; 1200 mm",
     "Case hardening"),
    ("Pit furnace, tempering", "800 dia &times; 1200 mm", "Tempering"),
    ("Pit furnace, tempering", "700 dia &times; 1200 mm", "Tempering"),
    ("Deep pit furnace", "700 dia &times; 2000 mm", "Long shafts and bars"),
    ("Quench tanks", "Oil and water", "Impeller agitated"),
    ("Power backup", "125 kVA + 45 kVA",
     "Kirloskar GenLight and Powerica gensets"),
]

# ----------------------------------------------------------------- safety --
SAFETY_TITLE = "Safety on the floor"
# Supplied by the client (September 2026): an illustration of the practices
# below, from face shield and gloves to the chained quench tank.
SAFETY_IMAGE = ("safety", "Illustration of safe practice in a heat "
                "treatment shop: a worker in helmet, face shield and gloves "
                "clear of the furnace, a charge moved by overhead crane, a "
                "quench tank fenced with posts and chain, yellow walkway "
                "markings and a fire extinguisher")
SAFETY_INTRO = (
    "A heat treatment shop works with furnaces near 1,000&deg;C, tanks of "
    "quench oil and loads lifted by crane. Our aim is on the board at the "
    "factory entrance, and zero accidents is the first line on it."
)
SAFETY_POINTS = [
    ("Protective gear", "Heat-resistant gloves, safety shoes and face "
     "protection for anyone loading a furnace or working at the quench."),
    ("Guarded pits and tanks", "Furnace pits and quench tanks are fenced "
     "with posts and chains, and walkways are marked in yellow."),
    ("Lifting by crane", "Hot and heavy charges move only on the two-tonne "
     "cranes, on rated hooks and fixtures, never by hand."),
    ("Fire readiness", "Extinguishers are kept at the furnaces and the "
     "quench tanks, and the team knows where each one is."),
    ("Maintained equipment", "Furnaces, cranes and electrical panels are "
     "checked on schedule by our maintenance team."),
    ("Clear housekeeping", "Receiving, process, inspection and dispatch each "
     "have their own marked area, so work never piles up in a walkway."),
]

# ------------------------------------------------------- industrial visits --
VISITS_TITLE = "Industrial visits, every year"
VISITS_BODY = (
    "Every year engineering students visit the works to see heat treatment "
    "happen for real: a charge lifted out glowing, the quench, and the "
    "hardness test that proves it. Our metallurgist walks them through each "
    "step on the floor."
)
VISITS = [
    ("g-iv-explaining", "Our metallurgist explaining the process to visiting "
     "students"),
    ("g-iv-furnace", "Students watching a pit furnace charge"),
    ("g-iv-group", "A visiting batch of engineering students outside the "
     "works"),
]
VISITS_VIDEO = "v-industrial-visit"

# ------------------------------------------------- vision, mission, policy --
# From page 5 of the 2025 company profile, rewritten in the site's voice.
# The substance is theirs; only the wording is new.

VISION_TITLE = "Vision"
VISION_BODY = [
    "To be the heat treatment business this industry measures itself against, "
    "through better technology, better process control and a standard of work "
    "that holds across every function.",
    "And to build partnerships with our customers and our suppliers that are "
    "worth keeping for decades.",
]

MISSION_TITLE = "Mission"
MISSION_BODY = [
    "Complete customer satisfaction, earned the only way it can be: by "
    "delivering the highest quality in every component we treat and every "
    "service we put our name to.",
    "We get there by holding to the three principles the company was founded "
    "on &mdash; integrity, quality and innovation.",
]

POLICY_TITLE = "Our quality policy"
POLICY_INTRO = (
    "We commit to heat treatment that meets or exceeds what our customers "
    "expect, through standard practice and a process we keep improving."
)
POLICY_POINTS = [
    "Deliver precisely what the customer needs.",
    "Provide heat treatment services of consistently high quality.",
    "Determine, understand and consistently meet every statutory and "
    "regulatory requirement that applies to the customer's work.",
    "Identify and address the risks and opportunities that affect conformity "
    "of materials and products.",
    "Keep the focus on satisfying our customers and everyone else with a "
    "stake in the work.",
]

# --------------------------------------------------------------- reviews ---
# Real customer words, as published on amtheat.com, quoted as written.
#
# Two of them name "Ambattur Metal Treat" inside the quote. That is left
# exactly as the customer wrote it rather than edited to read "Everest" —
# changing someone's words is not ours to do. If the client wants the name to
# match, ask them for a reworded version rather than editing it here.
# The client asked for reviews to come off the site (September 2026). The
# quotes stay here so they can go back with one flag.
SHOW_TESTIMONIALS = False
TESTIMONIALS = [
    dict(text="Excellent workmanship and timely delivery. Their heat treatment "
              "quality has consistently exceeded our expectations.",
         name="Adhithi Meenakshi", meta="Customer"),
    dict(text="Reliable service, skilled team, and outstanding results. We "
              "trust Ambattur Metal Treat for all our heat treatment "
              "requirements.",
         name="HariHaran Rathinakumar", meta="Customer"),
    dict(text="Ambattur Metal Treat is the best heat treatment company in "
              "Chennai. Excellent quality and on-time delivery.",
         name="G. Mathi", meta="Customer"),
]

# --------------------------------------------------------------- gallery ---
# The client's own photographs and videos of the works, September 2026.
# media.py converts them; the file names they were supplied under became
# these captions. The first entry leads the gallery page at full width.
#   (slug, caption)            a photograph in assets/img/
#   (slug, caption, "video")   a video in assets/video/, poster alongside

GALLERY_TITLE = "Inside the works"
GALLERY_INTRO = (
    "The furnaces, the quench, the laboratory and the people, photographed "
    "on the floor at Nazarathpettai."
)
GALLERY = [
    ("g-normalising", "Normalising: a charge glowing on the way out of the "
     "furnace"),
    ("v-oil-quench", "Hardening: a charge lifted from the furnace into the "
     "oil quench", "video"),
    ("g-oil-quench", "Hardening: the charge going into oil tank 1, 7,500 "
     "litres"),
    ("g-charge-lift", "A charge at temperature, lifted from a pit furnace"),
    ("g-bogie-furnace", "Bogie hearth furnace F3"),
    ("g-pit-furnaces", "Pit type furnaces"),
    ("g-pit-furnace-f5", "Pit type furnace F5"),
    ("g-tempering-furnace", "Tempering furnace F2"),
    ("g-quench-tanks", "Oil and water quench tanks beside the pit furnaces"),
    ("v-oil-agitation", "Oil quench tank, agitated by its impeller", "video"),
    ("v-quench-tanks", "The oil and water quench tanks", "video"),
    ("g-rockwell-floor", "Rockwell hardness tester and furnace control "
     "panels"),
    ("g-lab", "Metallurgical laboratory"),
    ("g-lab-2", "Laboratory: hardness testers and specimen preparation"),
    ("g-inspection-area", "Inspection area"),
    ("g-inspection", "Inspection on the shop floor"),
    ("g-process-area", "Process area"),
    ("g-shop-floor", "The shop floor and office"),
    ("g-receiving-area", "Receiving area"),
    ("g-receiving-2", "Incoming components at receiving"),
    ("g-receiving-3", "Receiving area, loaded for the day"),
    ("g-bolts", "Fasteners fixtured for treatment"),
    ("g-dispatch", "Dispatch area"),
    ("g-dispatch-2", "Treated components ready for dispatch"),
    ("g-prod-plan", "Daily production plan"),
    ("g-board", "Job status board"),
    ("g-safety", "Safety board at the factory entrance"),
    ("g-office", "Office"),
    ("g-meeting", "A customer meeting"),
    ("g-team", "The Everest Heat Treaters team"),
    ("g-team-2", "The team outside the works"),
    ("g-iv-explaining", "Industrial visit: explaining the process"),
    ("v-industrial-visit", "Industrial visit", "video"),
    ("g-iv-furnace", "Industrial visit: at the pit furnace"),
    ("g-iv-pit", "Industrial visit: a charge in the furnace"),
    ("g-iv-group", "Industrial visit: students outside the works"),
    ("g-iv-group-2", "Industrial visit: a visiting batch"),
]
# The strip on the homepage: the most telling eight, linking to the rest.
GALLERY_HOME = ["g-normalising", "g-charge-lift", "g-bogie-furnace",
                "g-quench-tanks", "g-pit-furnaces", "g-lab-2",
                "g-dispatch-2", "g-team"]

# ---------------------------------------------------------- certificates ---
# Cropped from page 11 of the company profile by plant.py.
CERTS_TITLE = "On the record"
CERTS_INTRO = (
    "The registration and the certificate, as issued. ISO 9001:2015 through "
    "BSI, held since 2006 and audited every year since."
)
CERTIFICATES = [
    ("cert-iso", "ISO 9001:2015",
     "BSI certificate FS 617633, for heat treatment of ferrous and "
     "non-ferrous metals. Valid to 18 July 2026.",
     "Certificate of Registration, ISO 9001:2015, issued by BSI to "
     "Everest Heat Treaters"),
    ("cert-gst", "GST registration",
     "Form GST REG-25, trade name Everest Heat Treaters, "
     "GSTIN 33ANNPS4415M1ZK.",
     "Government of India GST certificate of provisional registration for "
     "Everest Heat Treaters"),
]

# --------------------------------------------------------------- contact ---

CONTACT_INTRO = (
    "Send the grade, the drawing and the hardness you need. "
    "We will reach out to you soon."
)

# ----------------------------------------------------------- form wiring ---
# Where enquiries go. Leave empty and everything falls back to WhatsApp, which
# is what ships today. Set this to an endpoint (Formspree, a Worker, your own
# mailer) and both the quote form and the one-tap grade enquiry POST JSON to
# it as well, so nothing has to be rewired later.
#
# The POST body is flat JSON: source, grade, phone, name, email, company,
# process, weight, size, hardness, message, page. When a drawing is attached
# it goes as multipart form data instead, with the file under "drawing".
FORM_ENDPOINT = ""
FORM_EMAIL = "everest_heattreaters@yahoo.co.in"

RFQ_FIELDS_NOTE = "We will reach out to you soon."

FAQ = [
    ("What information do you need to quote?",
     "Material grade, weight, size, and the hardness or case depth "
     "required. A drawing is ideal."),
    ("What is the usual turnaround?",
     "Most conventional work runs two to three days. Long-cycle processes "
     "like deep case hardening take longer, and we will "
     "give you a realistic date when we quote."),
    ("Do you handle small quantities?",
     "Yes. Single pieces, prototypes and trial batches are all normal work "
     "here. Small lots get batched with compatible cycles."),
    ("How big a part can you take?",
     "The bogie hearth handles work up to three metres long, 900 mm wide and "
     "450 mm tall, and the deep pit furnace takes parts up to two metres "
     "long. Charges run from 800 to 1,000 kg, and two-tonne cranes cover "
     "the handling."),
    ("My parts came out distorted somewhere else. Can you help?",
     "Usually. Distortion tends to be a design, grade or fixturing question "
     "rather than a furnace one. Send the part and the drawing and we will "
     "tell you what is causing it."),
    ("Can you tell me what treatment I need?",
     "That is a large part of the job. Tell us what the part does, what it "
     "runs against and how it is failing, and we will specify the treatment."),
    ("Do you provide test certificates?",
     "A hardness report goes out with every batch. Microhardness traverses, "
     "case depth measurement and microstructure reports are available on "
     "request."),
]

# ---------------------------------------------------------------- footer ---

FOOTER_NOTE = ""

CTA_TITLE = "Send us the grade and the hardness."
CTA_TEXT = "We will get back to you soon."
