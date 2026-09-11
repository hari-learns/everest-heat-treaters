#!/usr/bin/env python3
"""Everything a person might want to change lives in this file.

`build.py` is a generator and holds no copy of its own. If you are about to
edit a sentence, a temperature or a phone number anywhere else, that is a bug.

SOURCES FOR THIS CONTENT
  - Ambattur Metal Treaters, amtheat.com (name, founding year, headcount,
    process list, contact details)
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

NAME = "Ambattur Metal Treaters"
SHORT_NAME = "Ambattur Metal Treaters"
INITIALS = "AMT"
# What shows in the browser tab. Kept short so it survives truncation —
# a tab reading "About — Ambattur Metal Trea…" identifies nothing.
TAB_NAME = "Metal Treaters"
TAGLINE = "Heat treatment for ferrous &amp; non-ferrous metals"
CERT = "An ISO 9001:2015 certified company"
DESCRIPTION = (
    "Commercial heat treatment in Ambattur, Chennai — hardening and tempering, "
    "case hardening, carbonitriding, annealing, normalising, stress relieving "
    "and solution treatment for ferrous and non-ferrous components. "
    "ISO 9001:2015 certified, working to ASTM standards."
)

CONTACT_NAME = "S. Aravindth"
CONTACT_QUALS = "B.E., M.E."
CONTACT_ROLE = "Metallurgist"

# From amtheat.com. The 2025 profile PDF lists 8056158579 / 9444412784 for the
# Nazarathpettai works — confirm which number should be the one on the site.
PHONE = "+91 98410 35501"
PHONE_LINK = "+919841035501"
WHATSAPP = "919841035501"
EMAIL = "amtheat@hotmail.com"
EMAIL_ALT = "everest_heattreaters@yahoo.co.in"
GSTIN = "33ANNPS4415M1ZK"

ADDRESS_LINES = [
    "S. No. 315/1, Meppur Road",
    "Malayambakkam, Nazarathpettai",
    "Ambattur, Chennai &ndash; 600 123",
    "Tamil Nadu, India",
]
ADDRESS_ONE_LINE = ("S. No. 315/1, Meppur Road, Malayambakkam, "
                    "Nazarathpettai, Ambattur, Chennai 600123")
MAP_QUERY = "Ambattur, Chennai, Tamil Nadu"

HOURS = [("Monday &ndash; Saturday", "9:00 AM &ndash; 7:00 PM"),
         ("Sunday", "By prior arrangement")]

# ------------------------------------------------------------------ nav ----

NAV = [
    ("index.html", "Home"),
    ("processes.html", "Processes"),
    ("materials.html", "Materials"),
    ("quality.html", "Quality"),
    ("industries.html", "Industries"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

# ----------------------------------------------------------------- hero ----

HERO_EYEBROW = "Ambattur, Chennai &middot; ISO 9001:2015"
# "Metal" cycles through the incandescent colours with a live temperature
# reading above it, driven from GLOW_COLOURS — the same table as the scale
# further down the page.
HERO_TITLE = ('<span class="heat" data-heat-word>'
              '<span class="heat__t" data-heat-temp aria-hidden="true"></span>'
              'Metal</span>, the way<br>you want it to be.')
# the stretch of the scale the word travels, in degrees C
HERO_HEAT_RANGE = (560, 1180)
HERO_TEXT = (
    "Heat treatment rewrites the crystal structure of the steel itself, so a "
    "component comes back harder, tougher or softer all the way through. We "
    "treat to the hardness your drawing asks for, and every batch leaves here "
    "with a report that says so."
)
# Rendered, not photographed — see hero.py. Same colour scale as the
# temperature control further down the page.
HERO_IMAGE = "billet-heat"

# The band under the hero. Figures from the company profile.
STATS = [
    ("22", "years", "Treating metal in Chennai"),
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

# (from C, to C, label, what is happening) — read out as the slider moves.
TEMP_BANDS = [
    (150, 200, "Low-temperature tempering",
     "Stress comes out of a freshly quenched part while almost all of its "
     "hardness stays in. This is where case-hardened gears and springs are "
     "finished."),
    (200, 350, "Tempering &mdash; tool range",
     "Hardness is traded for toughness a few degrees at a time. On clean "
     "steel the oxide colour is a direct readout of the temperature reached."),
    (350, 500, "High-temperature tempering",
     "For dies and shafts that have to survive shock. Toughness climbs "
     "sharply and hardness settles into the 40s HRC."),
    (500, 580, "Carbonitriding &amp; stress relieving",
     "Nitrogen and carbon diffuse into the surface together, giving a hard "
     "skin with very little movement, because the part stays below the "
     "temperature at which it would transform."),
    (580, 720, "Sub-critical annealing",
     "Below the critical point. Machining stresses are erased and the "
     "structure softens while the part keeps its existing hardness state."),
    (720, 800, "Into the critical range",
     "The steel begins converting to austenite. Cross this line and the "
     "structure can be reset entirely."),
    (800, 880, "Austenitising &amp; hardening",
     "Fully austenitic. Quench from here and carbon is trapped in place as "
     "martensite &mdash; this is the moment hardness is created."),
    (880, 950, "Case hardening &amp; normalising",
     "Carbon is driven into the surface of low-carbon steel to build a hard "
     "case over a tough core. This is also where forged grain is refined."),
    (950, 1150, "Solution annealing",
     "Carbides and alloying elements dissolve back into solution &mdash; "
     "stainless steels and aluminium alloys are prepared for ageing here."),
    (1150, 1301, "Forging heat",
     "Beyond treatment and into forming. Grain grows fast at these "
     "temperatures; time at heat matters as much as the heat itself."),
]

# --------------------------------------------------------------- process ---
# The nine processes named in the company profile. The first six also appear
# on the homepage, so the order here is the order of importance.

PROCESSES = [
    dict(
        slug="hardening-tempering",
        name="Hardening &amp; Tempering",
        short="The core process. Heat into the austenitic range, quench, then "
              "temper back to the hardness the part actually needs.",
        temp="820&ndash;870&deg;C, tempered 150&ndash;600&deg;C",
        result="25&ndash;62 HRC depending on grade and temper",
        image="furnace-castings",
        body=[
            "The part goes above its critical temperature until the structure "
            "is fully austenitic, holds there long enough to be uniform "
            "through section, then quenches fast enough to trap the carbon in "
            "place. What comes out is martensite &mdash; extremely hard, and "
            "far too brittle to put into service.",
            "Tempering is what makes it usable. A second, lower heat lets some "
            "of that trapped carbon precipitate out, trading a little hardness "
            "for a great deal of toughness. We pick the tempering temperature "
            "from the hardness your drawing calls for, and it is the single "
            "most important number on the job card.",
        ],
        points=["Oil, polymer and air quench",
                "Section-appropriate soak times",
                "Tempered to a specified HRC band",
                "Double tempering on tool steels"],
        suits=["EN8", "EN9", "EN19", "EN24", "EN31", "C45", "D2", "H13", "O1"],
    ),
    dict(
        slug="case-hardening",
        name="Case Hardening &amp; Tempering",
        short="A hard, wear-resistant skin over a core that stays tough. The "
              "standard treatment for gears and transmission parts.",
        temp="900&ndash;930&deg;C",
        result="58&ndash;62 HRC case, 0.2&ndash;1.5 mm effective depth",
        image="crankshaft",
        body=[
            "Low-carbon steel holds too little carbon to form martensite on "
            "its own, so we add it from the outside in. The part sits in a "
            "carbon-rich atmosphere at around 920&deg;C in one of our gas "
            "carburising furnaces, and carbon diffuses into the surface layer.",
            "Quench it and you get a component with two personalities. The "
            "case is glass-hard and shrugs off wear and pitting; the core "
            "stays at its original low carbon and absorbs shock without "
            "cracking. A gear tooth has to be both, which is why almost every "
            "gear in every gearbox has been through this.",
        ],
        points=["Case depth to drawing, verified by microhardness traverse",
                "Selective case hardening with stop-off paint",
                "Core hardness reported alongside case",
                "Tempered after quench to stabilise"],
        suits=["SAE 8620", "16MnCr5", "20MnCr5", "EN36", "EN353", "EN354"],
    ),
    dict(
        slug="carbonitriding",
        name="Carbonitriding",
        short="Carbon and nitrogen together, for a hard surface with very "
              "little movement on the part.",
        temp="500&ndash;580&deg;C",
        result="Up to 1100 HV surface, 0.1&ndash;0.6 mm case",
        image="micro-duplex",
        body=[
            "Nitrogen and carbon diffuse into the surface at around 520&deg;C "
            "and form hard nitrides with the chromium, aluminium and "
            "molybdenum already present in the steel. The cycle runs well "
            "below the critical temperature and needs no quench.",
            "That is the whole advantage. Movement is negligible, so finished "
            "and even ground components can be treated and go straight back "
            "into assembly. The surface that results is harder than anything "
            "through-hardening can reach, and it holds that hardness at "
            "service temperatures that would temper a conventionally hardened "
            "part straight back down.",
        ],
        points=["Treat finished and ground components",
                "Negligible distortion &mdash; no quench",
                "Strong wear and galling resistance",
                "Holds hardness at elevated service temperature"],
        suits=["EN41B", "H13", "EN19", "EN24", "Nitralloy", "Die steels"],
    ),
    dict(
        slug="annealing",
        name="Annealing",
        short="Softening. Taking work-hardened or previously treated material "
              "back to a machinable, stress-free state.",
        temp="650&ndash;900&deg;C, slow cooled",
        result="Softened, uniform, ready to machine or form",
        image="furnace-anneal",
        body=[
            "Annealing is a slow heat, a soak, and above all a slow cool "
            "&mdash; usually inside the furnace itself, over many hours. That "
            "cooling rate is the entire process; rush it and you have simply "
            "hardened the part again.",
            "Full annealing resets a structure above the critical point. "
            "Process annealing works below it, to relieve the work hardening "
            "that builds up during drawing and forming. Spheroidise annealing "
            "rounds the carbides in high-carbon steel into globules, which is "
            "what makes bearing steel machinable at all.",
        ],
        points=["Full, process and spheroidise cycles",
                "Controlled furnace cooling",
                "Bright annealing for finished surfaces",
                "Non-ferrous annealing for copper alloys and aluminium"],
        suits=["EN31", "C45", "Tool steels", "Copper alloys", "Brass"],
    ),
    dict(
        slug="normalising",
        name="Normalising &amp; Tempering",
        short="Grain refinement after forging or casting. The step that makes "
              "everything downstream predictable.",
        temp="870&ndash;950&deg;C, air cooled",
        result="Uniform fine grain, improved machinability",
        image="forged-part",
        body=[
            "Forging and casting leave a coarse, uneven grain structure and "
            "properties that vary wildly through the part. Normalising heats "
            "above the critical range and cools in still air &mdash; faster "
            "than annealing, slower than a quench.",
            "The result is a fine, even grain throughout. Think of it as the "
            "step that makes the final treatment behave the same way every "
            "single time, which is why so much forged and cast work starts "
            "here.",
        ],
        points=["Post-forging and post-casting grain refinement",
                "Improves response to later hardening",
                "Air cool on open racks",
                "Relieves casting segregation"],
        suits=["Forgings", "Castings", "EN8", "EN19", "Weldments"],
    ),
    dict(
        slug="stress-relieving",
        name="Stress Relieving",
        short="Taking the locked-in stress out of welded and machined parts, "
              "before it takes your tolerances out.",
        temp="550&ndash;650&deg;C",
        result="Dimensional stability, hardness unchanged",
        image="furnace-metal",
        body=[
            "Welding, heavy machining and cold forming all leave residual "
            "stress locked into a part. It sits there quietly until the part "
            "is finish-machined or put into service, and then it releases and "
            "the geometry moves.",
            "A stress relieve is a soak below the critical point and a slow "
            "cool. Hardness and structure stay exactly as they were and only "
            "the internal stress lets go. On any long, thin or "
            "precision-ground component, this is the difference between "
            "holding a tolerance and scrapping the batch.",
        ],
        points=["Post-weld and post-machining",
                "Below critical &mdash; hardness stays put",
                "Slow controlled cool",
                "Critical before finish grinding"],
        suits=["Weldments", "Fabrications", "Machined blanks", "Castings"],
    ),
    dict(
        slug="solution-annealing",
        name="Solution Annealing",
        short="Dissolving carbides back into solution, so stainless comes "
              "back to full corrosion resistance.",
        temp="950&ndash;1150&deg;C, rapid cooled",
        result="Soft, homogeneous, corrosion resistance restored",
        image="micro-stainless",
        body=[
            "Welding and hot forming let chromium carbides form at the grain "
            "boundaries of austenitic stainless, and the steel loses "
            "corrosion resistance exactly where those carbides sit. Solution "
            "annealing takes the part up high enough to dissolve them back "
            "into solution, then cools it fast enough that they stay there.",
            "The part comes out soft, chemically uniform and ready for "
            "service in the environment it was specified for. This is also "
            "the first half of age hardening, where the cooling step sets up "
            "everything that follows.",
        ],
        points=["Austenitic and duplex stainless grades",
                "Rapid cool through the sensitisation range",
                "Restores corrosion resistance after welding",
                "Also the solution step for PH grades and aluminium"],
        suits=["304", "316", "321", "Duplex 2205", "17-4 PH", "Al alloys"],
    ),
    dict(
        slug="age-hardening",
        name="Age Hardening &amp; Precipitation Hardening",
        short="The non-ferrous route to strength. Dissolve, quench, then let "
              "fine particles precipitate back out.",
        temp="Age 120&ndash;600&deg;C after solution treatment",
        result="T4 / T6 tempers, PH stainless conditions H900 upward",
        image="furnace-vacuum",
        body=[
            "Aluminium alloys and precipitation-hardening stainless gain their "
            "strength a different way from carbon steel. The alloying elements "
            "go into solid solution at high temperature, a quench holds them "
            "there, and then a long soak at a low temperature lets them "
            "precipitate out as fine particles that obstruct movement through "
            "the crystal.",
            "The ageing step is where the strength actually appears, and it is "
            "purely a function of time and temperature. A T6 temper is a "
            "recipe rather than a setting, and we run it to the clock.",
        ],
        points=["Aluminium T4 and T6 tempers",
                "17-4 PH conditions H900 to H1150",
                "Close control of ageing time and temperature",
                "Hardness verified after ageing"],
        suits=["Al 6061", "Al 6082", "Al 7075", "Al 2014", "17-4 PH", "15-5 PH"],
    ),
    dict(
        slug="stabilising",
        name="Stabilising",
        short="A long, low soak that settles a part for good, so it holds its "
              "dimensions years into service.",
        temp="150&ndash;300&deg;C, extended soak",
        result="Long-term dimensional stability",
        image="micro-duplex4",
        body=[
            "Precision components carry small amounts of retained austenite "
            "and residual stress even after a correct harden and temper. Over "
            "months in service that austenite slowly transforms, and the part "
            "grows by a few microns &mdash; enough to take a gauge, a spindle "
            "or a measuring instrument out of tolerance.",
            "Stabilising runs a long, low-temperature soak that brings those "
            "changes forward and lets them happen here instead of in the "
            "field. Gauge blocks, bearing races, machine tool spindles and "
            "instrument parts all benefit, and it is usually specified "
            "between rough and finish grinding.",
        ],
        points=["Extended low-temperature cycles",
                "Sub-zero treatment available on request",
                "Specified between rough and finish grinding",
                "For gauges, spindles and instrument components"],
        suits=["EN31", "Gauge steels", "O1", "D2", "Bearing races"],
    ),
]

PROCESSES_INTRO = (
    "Nine processes cover almost everything that comes through the door, for "
    "ferrous and non-ferrous metals alike, all of it to ASTM standards. If "
    "your drawing calls for something else, or does not specify at all, send "
    "it over &mdash; working out the right treatment is part of the job."
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
     "High strength shafts and gears"),
    ("EN31 / 534A99", "Bearing steel", "Harden, temper &amp; stabilise",
     "58&ndash;63 HRC", "Spheroidise anneal before machining"),
    ("EN36 / 655M13", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Tough core, hard case"),
    ("SAE 8620", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "The default gear steel"),
    ("16MnCr5", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Automotive transmission"),
    ("20MnCr5", "Case hardening", "Case harden &amp; temper",
     "58&ndash;62 HRC case", "Deeper case than 16MnCr5"),
    ("EN41B", "Nitriding steel", "Carbonitride", "up to 1100 HV",
     "Aluminium-bearing, made for nitriding"),
    ("D2 / X153CrMoV12", "Cold work tool", "Harden &amp; temper",
     "58&ndash;62 HRC", "Blanking and forming dies"),
    ("D3", "Cold work tool", "Harden &amp; temper", "58&ndash;62 HRC",
     "High wear, lower toughness"),
    ("O1", "Oil hardening tool", "Harden, temper &amp; stabilise",
     "58&ndash;62 HRC", "Low distortion, gauges and cutters"),
    ("H13 / X40CrMoV5-1", "Hot work tool", "Harden &amp; temper / carbonitride",
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
    ("321 / 347", "Stabilised stainless", "Solution anneal", "Soft, ~80 HRB",
     "For elevated service temperature"),
    ("410 / 420", "Martensitic stainless", "Harden &amp; temper",
     "40&ndash;50 HRC", "Valve trim, cutlery, pump parts"),
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
    "A working reference for the grades we see most often, with the treatment "
    "usually specified and the hardness it typically lands at. Your drawing "
    "always takes precedence &mdash; treat this as a good place to start the "
    "conversation."
)

# --------------------------------------------------------------- quality ---

QUALITY_INTRO = (
    "Heat treatment is invisible from the outside. A correctly hardened part "
    "and a badly hardened one look identical right up until one of them fails "
    "in service. Everything below is how we show you which one you are "
    "getting, on every batch."
)

QUALITY = [
    dict(name="Rockwell &amp; Brinell hardness", image="hardness-tester",
         text="Rockwell, optical Brinell-cum-Rockwell and Brinell testers in "
              "house, reading at the points your drawing specifies. The "
              "number goes on the report that travels with the parts."),
    dict(name="Portable hardness testing", image="hardness-close",
         text="A portable tester reaches large fabrications, bogie-load work "
              "and finished assemblies that will never fit under a bench "
              "machine, so big parts get the same proof as small ones."),
    dict(name="Microstructure at 500&times;", image="micro-ferrite",
         text="Cut on the abrasive saw, mounted, polished on the twin-disc "
              "grinder, etched and examined at up to 500&times;. Confirms the "
              "structure the process was meant to produce, and catches "
              "retained austenite, decarburisation and grain growth."),
    dict(name="Furnace control &amp; power backup", image="furnace-computer",
         text="Automated furnace control with temperature uniformity surveys "
              "and instrument calibration on schedule, backed by 24&times;7 "
              "diesel generators so a long carburising cycle finishes exactly "
              "as it started."),
]

QUALITY_POINTS = [
    ("ISO 9001:2015", "Certified by BSI and held continuously since 2006. The "
                      "quality system is externally audited every year."),
    ("ASTM standards", "Cycles and acceptance criteria follow ASTM practice, "
                       "with customer specifications layered on top."),
    ("Batch traceability", "Every batch carries an identity from goods-in to "
                           "dispatch, with the cycle recorded against it."),
    ("Reports with the parts", "A hardness report travels with every "
                               "delivery, so the paperwork arrives when the "
                               "parts do."),
]

# ------------------------------------------------------------- headings ---
# Section headlines. They live here so build.py stays a pure generator.

H_PROCESSES = "The process of transformation."
H_PROOF = "Heat treatment is invisible. So we measure it."
H_QUALITY = "How we prove the treatment landed."
H_QUALITY_SYSTEM = "How it is controlled"
H_MICRO = "The evidence is in the grain."
H_MICRO_TEXT = ("Etched cross-sections under the microscope at up to "
                "500&times; &mdash; a direct look at what the process did to "
                "the metal.")
H_INDUSTRIES = "Most of what we treat ends up inside something that moves."
H_CUSTOMERS = "Who our parts go back to"
H_ABOUT_PILLARS = "Three things we hold to"
H_VISION = "What we are aiming at"

# ------------------------------------------------------------- customers ---
# Named in the 2025 company profile.
CUSTOMERS = [
    "L&amp;T Valves Limited",
    "Flowserve India Control Pvt Ltd",
    "Schwing Stetter Pvt Ltd",
    "Severn Glocon India Pvt Ltd",
    "Bharat Heavy Electricals Ltd",
]

CUSTOMERS_INTRO = (
    "Over a hundred manufacturers send us work, from single prototypes to "
    "steady production. A few of the names our parts go back to:"
)

# ------------------------------------------------------------ industries ---

INDUSTRIES = [
    ("Valves &amp; flow control", "Stems, discs, seats and trim for valve "
     "makers, including martensitic and PH stainless grades."),
    ("Power &amp; heavy engineering", "Large fabrications and forged "
     "components, stress relieved and normalised on the bogie hearth."),
    ("Construction equipment", "Pins, bushes, levers and linkages built to "
     "take shock and abrasion on site."),
    ("Automotive components", "Gears, shafts, pins and linkages for the "
     "tier-one and tier-two supply base around Chennai."),
    ("Transmission &amp; gearing", "Case hardened gear sets, splines and "
     "sprockets, with case depth verified per drawing."),
    ("Pumps &amp; fluid handling", "Shafts, impellers and wear parts in both "
     "carbon steel and stainless."),
    ("Dies, moulds &amp; tooling", "Cold and hot work tool steels, press "
     "tools, and carbonitrided die surfaces."),
    ("General engineering", "Job work, one-offs, prototypes and the awkward "
     "parts nobody else wants to quote."),
]

INDUSTRIES_INTRO = (
    "Chennai is an engineering city, and most of what we treat ends up inside "
    "something that moves, holds pressure or carries load. Batch sizes run "
    "from a single prototype to steady production quantities."
)

# ---------------------------------------------------------------- about ----

ABOUT_TITLE = "Twenty-two years of getting metal to behave"
ABOUT_IMAGE = "forge"
ABOUT_BODY = [
    "Ambattur Metal Treaters is a commercial heat treatment works on the "
    "western edge of Chennai. Manufacturers across the city send us "
    "components and we return them harder, tougher or softer &mdash; whatever "
    "the drawing asks for &mdash; with the documentation to prove it. We have "
    "been doing this since 2004, for ferrous and non-ferrous metals alike.",
    "The plant runs automated sealed-quench and pit furnaces taking charges "
    "of 800 to 1,000 kg, a bogie hearth three metres long for the big "
    "fabrications, and dedicated tempering furnaces alongside them. Two-tonne "
    "cranes move the work and 24&times;7 diesel generators sit behind "
    "everything, which is what lets a twelve-hour carburising cycle finish "
    "exactly as it started. Around 200 tonnes a month goes through.",
    "Fifty people work here, led by a management team that has been together "
    "since the beginning: R. Sathyamoorthy as managing director, T. R. "
    "Thiyagarajan running production, A. Selvam on quality and S. Aravindth "
    "as our metallurgist. That last role is the one customers notice most.",
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
    "Deliver exactly what the customer specifies, and stay competitive doing it.",
    "Provide heat treatment services of consistently high quality.",
    "Determine, understand and consistently meet every statutory and "
    "regulatory requirement that applies to the customer's work.",
    "Identify and address the risks and opportunities that affect conformity "
    "of materials and products.",
    "Keep the focus on satisfying our customers and everyone else with a "
    "stake in the work.",
]

# --------------------------------------------------------------- reviews ---
# Real customer words, as published on amtheat.com.
TESTIMONIALS = [
    dict(text="Ambattur Metal Treaters is the best heat treatment company in "
              "Chennai. Excellent quality and on-time delivery.",
         name="G. Mathi", meta="Customer"),
    dict(text="Excellent workmanship and timely delivery. Their heat treatment "
              "quality has consistently exceeded our expectations.",
         name="Adhithi Meenakshi", meta="Customer"),
    dict(text="Reliable service, skilled team, and outstanding results. We "
              "trust Ambattur Metal Treaters for all our heat treatment "
              "requirements.",
         name="Hariharan Rathinakumar", meta="Customer"),
]

# --------------------------------------------------------------- gallery ---
# The company's own photographs of the plant and of treated work, from
# amtheat.com. See fetch_gallery.py — the originals are small, so these are
# used at tile size only.

GALLERY_TITLE = "Inside the works"
GALLERY_INTRO = (
    "The plant, the laboratory and a few of the components that have been "
    "through it."
)
GALLERY = [
    ("amt-draw-hot", "Work drawn from the furnace at temperature"),
    ("amt-loading", "Loading a gear ring into a pit furnace"),
    ("amt-furnace-line", "The continuous mesh belt furnace line"),
    ("amt-pit-bays", "Pit furnace bays on the shop floor"),
    ("amt-optical", "Optical hardness testers in the laboratory"),
    ("amt-lab-press", "Mounting press and sample preparation"),
    ("amt-part-1", "Treated fasteners"),
    ("amt-part-2", "Hardened hex keys"),
    ("amt-part-3", "Bar stock ready for treatment"),
    ("amt-part-4", "Stainless lifting eyes"),
    ("amt-part-5", "Pressed steel clips"),
    ("amt-part-6", "Bolt and nut assembly, hardened and tempered"),
]

# --------------------------------------------------------------- contact ---

CONTACT_INTRO = (
    "Send the grade, the drawing and the hardness you need &mdash; or just "
    "describe the problem and we will work out the treatment with you."
)

RFQ_FIELDS_NOTE = ("Goes straight to WhatsApp with your details filled in. "
                   "No account, no form to chase.")

FAQ = [
    ("What information do you need to quote?",
     "Material grade, quantity, rough size and weight, and the hardness or "
     "case depth required. A drawing is ideal. If the grade is a mystery, say "
     "so &mdash; that is a solvable problem and we deal with it often."),
    ("What is the usual turnaround?",
     "Most conventional work runs two to three days. Long-cycle processes "
     "like deep case hardening and carbonitriding take longer, and we will "
     "give you a realistic date when we quote."),
    ("Do you handle small quantities?",
     "Yes. Single pieces, prototypes and trial batches are all normal work "
     "here. Small lots get batched with compatible cycles."),
    ("How big a part can you take?",
     "The bogie hearth handles work up to three metres long, 900 mm wide and "
     "450 mm tall, and the pit furnaces take components up to two metres "
     "deep. Two-tonne cranes cover the handling."),
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
