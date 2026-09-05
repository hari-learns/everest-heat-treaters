#!/usr/bin/env python3
"""Everything a person might want to change lives in this file.

`build.py` is a generator and holds no copy of its own. If you are about to
edit a sentence, a temperature or a phone number anywhere else, that is a bug.

⚠️  CONCEPT BUILD.
    The company identity is real and taken from their own business card —
    name, person, address, phone, email, GSTIN, ISO 9001:2015 certification.
    Everything ELSE is illustrative: the capability figures, the equipment
    list, the year founded, the testimonials. Those are written to show what
    the site can hold, not to make claims on the company's behalf. They must
    be confirmed or replaced before this goes anywhere near a live domain.
"""

# ---------------------------------------------------------------- flags ----

# Concept builds must never be indexed.
NOINDEX = True

# The "figures are illustrative" banner. Off only when every number below has
# been confirmed by the company.
SHOW_CONCEPT_NOTE = True

# ---------------------------------------------------------------- brand ----
# All of this block is REAL, from the business card.

NAME = "Everest Heat Treaters"
SHORT_NAME = "Everest"
INITIALS = "EHT"
TAGLINE = "Specialists in heat treatment of ferrous &amp; non-ferrous metals"
CERT = "An ISO 9001:2015 certified company"
DESCRIPTION = (
    "Commercial heat treatment in Chennai — hardening and tempering, case "
    "carburising, induction hardening, annealing, normalising and stress "
    "relieving for ferrous and non-ferrous components. ISO 9001:2015 certified."
)

CONTACT_NAME = "S. Aravindth"
CONTACT_QUALS = "B.E., M.E."
CONTACT_ROLE = "Metallurgist"

PHONE = "+91 63795 47322"
PHONE_LINK = "+916379547322"
WHATSAPP = "916379547322"
EMAIL = "sathyaaravindth03@gmail.com"
EMAIL_ALT = "everest_heattreaters@yahoo.co.in"
GSTIN = "33ANNPS4415M1ZK"

ADDRESS_LINES = [
    "S. No. 315/1, Meppur Road",
    "Malayambakkam, Nazarathpettai",
    "Chennai &ndash; 600 123",
    "Tamil Nadu, India",
]
ADDRESS_ONE_LINE = ("S. No. 315/1, Meppur Road, Malayambakkam, "
                    "Nazarathpettai, Chennai 600123")
MAP_QUERY = "Nazarathpettai, Chennai, Tamil Nadu 600123"

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

HERO_EYEBROW = "Chennai &middot; ISO 9001:2015"
HERO_TITLE = "We change what<br>metal <em>is</em>."
HERO_TEXT = (
    "Heat treatment is not a coating. It rewrites the crystal structure of "
    "the steel itself &mdash; harder, tougher, more stable, all the way "
    "through. We do it to a specified hardness, and we document every batch."
)
HERO_IMAGE = "furnace-castings"

# The band under the hero. Framed as process capability, not company claims.
STATS = [
    ("1250", "&deg;C", "Maximum furnace temperature"),
    ("65", "HRC", "Hardness achievable"),
    ("&plusmn;5", "&deg;C", "Furnace uniformity, surveyed"),
    ("100", "%", "Batches with a hardness report"),
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
     "Stress is relieved from a freshly quenched part while almost all of its "
     "hardness is kept. Where case-hardened gears and springs are finished."),
    (200, 350, "Tempering &mdash; tool range",
     "Hardness is traded for toughness a few degrees at a time. The oxide "
     "colour on clean steel is a direct readout of the temperature reached."),
    (350, 500, "High-temperature tempering",
     "For dies and shafts that must survive shock. Toughness rises sharply; "
     "hardness settles into the 40s HRC."),
    (500, 580, "Nitriding &amp; stress relieving",
     "Nitrogen diffuses into the surface, giving extreme hardness with almost "
     "no distortion &mdash; the part never gets hot enough to transform."),
    (580, 720, "Sub-critical annealing",
     "Below the critical point. Machining stresses are erased and the "
     "structure is softened without re-hardening the part."),
    (720, 800, "Into the critical range",
     "The steel begins converting to austenite. Cross this line and the "
     "structure can be reset entirely."),
    (800, 880, "Austenitising &amp; hardening",
     "Fully austenitic. Quench from here and carbon is trapped in place as "
     "martensite &mdash; this is the moment hardness is created."),
    (880, 950, "Carburising &amp; normalising",
     "Carbon is driven into the surface of low-carbon steel to build a hard "
     "case over a tough core. Also where forged grain is refined."),
    (950, 1150, "Solution annealing",
     "Carbides and alloying elements are dissolved back into solution &mdash; "
     "stainless steels and aluminium alloys are prepared for ageing here."),
    (1150, 1301, "Forging heat",
     "Beyond treatment and into forming. Grain grows fast at these "
     "temperatures; time at heat matters as much as the heat itself."),
]

# --------------------------------------------------------------- process ---

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
            "The part is taken above its critical temperature until the "
            "structure is fully austenitic, held long enough to be uniform "
            "through section, then quenched fast enough to trap the carbon in "
            "place. What comes out is martensite &mdash; extremely hard, and "
            "far too brittle to use.",
            "Tempering is what makes it useful. A second, lower heat lets some "
            "of that trapped carbon precipitate out, trading a little hardness "
            "for a great deal of toughness. The tempering temperature is "
            "chosen from the hardness the drawing calls for, and it is the "
            "single most important number on the job card.",
        ],
        points=["Oil, polymer and air quench", "Section-appropriate soak times",
                "Tempered to a specified HRC band, not a guess",
                "Double tempering on tool steels"],
        suits=["EN8", "EN9", "EN19", "EN24", "EN31", "C45", "D2", "H13", "O1"],
    ),
    dict(
        slug="case-carburising",
        name="Case Carburising",
        short="A hard, wear-resistant skin over a core that stays tough. The "
              "standard treatment for gears and transmission parts.",
        temp="900&ndash;930&deg;C",
        result="58&ndash;62 HRC case, 0.2&ndash;1.5 mm effective depth",
        image="crankshaft",
        body=[
            "Low-carbon steel will not harden &mdash; there is not enough "
            "carbon in it to form martensite. Carburising fixes that from the "
            "outside in: the part is held in a carbon-rich atmosphere at "
            "around 920&deg;C, and carbon diffuses into the surface layer.",
            "Quench it and you get a component with two personalities. The "
            "case is glass-hard and resists wear and pitting; the core stays "
            "at its original low carbon and absorbs shock without cracking. A "
            "gear tooth needs to be both, which is why almost every gear in "
            "every gearbox has been through this.",
        ],
        points=["Case depth to drawing, verified by microhardness traverse",
                "Selective carburising with stop-off paint",
                "Core hardness reported alongside case",
                "Tempered after quench to stabilise"],
        suits=["SAE 8620", "16MnCr5", "20MnCr5", "EN36", "EN353", "EN354"],
    ),
    dict(
        slug="induction-hardening",
        name="Induction Hardening",
        short="Hardness exactly where it is needed and nowhere else. Seconds, "
              "not hours, and the rest of the part never gets hot.",
        temp="850&ndash;950&deg;C at the surface only",
        result="50&ndash;60 HRC, 1&ndash;5 mm depth",
        image="furnace-computer",
        body=[
            "An alternating field in a shaped copper coil induces current in "
            "the surface of the part, which heats in seconds while the core "
            "stays cold. A quench follows immediately, usually from the same "
            "fixture.",
            "Because only the surface is transformed, distortion is very low "
            "and the untreated regions stay machinable. It suits journals, "
            "cam lobes, spline ends and shaft bearing surfaces &mdash; "
            "anywhere one feature wears and the rest of the part must not "
            "move.",
        ],
        points=["Profiled coils for shafts, pins and cam surfaces",
                "Very low distortion", "Selective &mdash; mask nothing, heat nothing",
                "Repeatable cycle, recorded per part"],
        suits=["C45", "EN8", "EN9", "EN19", "SG iron"],
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
            "&mdash; usually in the furnace itself, over many hours. That "
            "cooling rate is the whole process; rush it and you have simply "
            "hardened the part again.",
            "Full annealing resets a structure above the critical point. "
            "Process annealing works below it, to relieve the work hardening "
            "that builds up during drawing and forming. Spheroidise annealing "
            "rounds the carbides in high-carbon steel into globules, which is "
            "what makes bearing steel machinable at all.",
        ],
        points=["Full, process and spheroidise cycles",
                "Controlled furnace cooling", "Bright annealing for finished surfaces",
                "Non-ferrous annealing for copper alloys and aluminium"],
        suits=["EN31", "C45", "Tool steels", "Copper alloys", "Brass"],
    ),
    dict(
        slug="normalising",
        name="Normalising",
        short="Grain refinement after forging or casting. The step that makes "
              "everything downstream predictable.",
        temp="870&ndash;950&deg;C, air cooled",
        result="Uniform fine grain, improved machinability",
        image="forged-part",
        body=[
            "Forging and casting leave a coarse, uneven grain structure and "
            "wildly variable properties through the part. Normalising heats "
            "above the critical range and cools in still air &mdash; faster "
            "than annealing, slower than a quench.",
            "The result is a fine, even grain throughout. It is rarely the "
            "final treatment; it is the one that makes the final treatment "
            "behave the same way every time.",
        ],
        points=["Post-forging and post-casting grain refinement",
                "Improves response to later hardening",
                "Air cool on open racks", "Relieves casting segregation"],
        suits=["Forgings", "Castings", "EN8", "EN19", "Weldments"],
    ),
    dict(
        slug="stress-relieving",
        name="Stress Relieving",
        short="Removing the locked-in stress from welding and machining, "
              "before it removes your tolerances.",
        temp="550&ndash;650&deg;C",
        result="Dimensional stability, no change to hardness",
        image="furnace-metal",
        body=[
            "Welding, heavy machining and cold forming all leave residual "
            "stress locked into a part. It sits there quietly until the part "
            "is finish-machined or put into service, and then it releases and "
            "the geometry moves.",
            "A stress relieve is a soak below the critical point and a slow "
            "cool. Hardness and structure are untouched &mdash; only the "
            "internal stress is let go. On any long, thin or precision-ground "
            "component it is the difference between holding a tolerance and "
            "scrapping the batch.",
        ],
        points=["Post-weld and post-machining", "Below critical &mdash; hardness unaffected",
                "Slow controlled cool", "Critical before finish grinding"],
        suits=["Weldments", "Fabrications", "Machined blanks", "Castings"],
    ),
    dict(
        slug="nitriding",
        name="Nitriding &amp; Carbonitriding",
        short="Extreme surface hardness with almost no distortion, because "
              "the part never gets hot enough to transform.",
        temp="500&ndash;580&deg;C",
        result="Up to 1100 HV surface, 0.1&ndash;0.6 mm case",
        image="micro-duplex",
        body=[
            "Nitrogen diffuses into the surface at around 520&deg;C and forms "
            "hard nitrides with the chromium, aluminium and molybdenum already "
            "in the steel. No quench is involved and the part never crosses "
            "its critical temperature.",
            "That is the whole point. Distortion is negligible, so finished "
            "and even ground components can be treated. The surface that "
            "results is harder than anything achievable by through-hardening, "
            "and it holds that hardness at temperatures that would temper a "
            "conventionally hardened part straight back down.",
        ],
        points=["Treat finished and ground components",
                "Negligible distortion &mdash; no quench",
                "Excellent wear and galling resistance",
                "Retains hardness at elevated service temperature"],
        suits=["EN41B", "H13", "EN19", "EN24", "Nitralloy", "Die steels"],
    ),
    dict(
        slug="solution-ageing",
        name="Solution Annealing &amp; Age Hardening",
        short="The non-ferrous side. Aluminium and stainless are strengthened "
              "by dissolving, then precipitating.",
        temp="Solution 480&ndash;1100&deg;C, age 120&ndash;600&deg;C",
        result="T4 / T6 tempers, PH stainless conditions",
        image="micro-stainless",
        body=[
            "Aluminium alloys and precipitation-hardening stainless do not "
            "harden by quenching to martensite. They are strengthened by "
            "putting the alloying elements into solid solution at high "
            "temperature, quenching to hold them there, and then ageing at a "
            "low temperature so they precipitate out as fine particles that "
            "obstruct movement through the crystal.",
            "The ageing step is where the strength appears, and it is entirely "
            "a function of time and temperature &mdash; which is why a T6 "
            "temper is a recipe, not a setting.",
        ],
        points=["Aluminium T4 and T6 tempers",
                "Solution annealing of austenitic stainless",
                "17-4 PH condition H900 and up",
                "Close control of ageing time and temperature"],
        suits=["Al 6061", "Al 6082", "Al 7075", "Al 2014", "17-4 PH", "304", "316"],
    ),
]

PROCESSES_INTRO = (
    "Eight processes cover almost everything that comes through the door. If "
    "your drawing calls for something else, or does not specify at all, send "
    "it over &mdash; specifying the treatment is part of the job."
)

# ------------------------------------------------------------- materials ---
# (grade, family, typical process, typical result, note)
MATERIALS = [
    ("EN8 / 080M40", "Medium carbon", "Harden &amp; temper", "25&ndash;35 HRC",
     "General shafts, studs, keys"),
    ("EN9 / 070M55", "Medium carbon", "Harden &amp; temper", "30&ndash;40 HRC",
     "Higher strength than EN8"),
    ("C45", "Medium carbon", "Induction / harden &amp; temper", "45&ndash;55 HRC",
     "Very common for induction work"),
    ("EN19 / 709M40", "Cr-Mo alloy", "Harden &amp; temper", "28&ndash;40 HRC",
     "Good through-hardening in section"),
    ("EN24 / 817M40", "Ni-Cr-Mo alloy", "Harden &amp; temper", "32&ndash;45 HRC",
     "High strength shafts and gears"),
    ("EN31 / 534A99", "Bearing steel", "Harden &amp; temper", "58&ndash;63 HRC",
     "Spheroidise anneal before machining"),
    ("EN36 / 655M13", "Case hardening", "Carburise &amp; temper",
     "58&ndash;62 HRC case", "Tough core, hard case"),
    ("SAE 8620", "Case hardening", "Carburise &amp; temper",
     "58&ndash;62 HRC case", "The default gear steel"),
    ("16MnCr5", "Case hardening", "Carburise &amp; temper",
     "58&ndash;62 HRC case", "Automotive transmission"),
    ("20MnCr5", "Case hardening", "Carburise &amp; temper",
     "58&ndash;62 HRC case", "Deeper case than 16MnCr5"),
    ("EN41B", "Nitriding steel", "Nitride", "up to 1100 HV",
     "Aluminium-bearing, made for nitriding"),
    ("D2 / X153CrMoV12", "Cold work tool", "Harden &amp; temper",
     "58&ndash;62 HRC", "Blanking and forming dies"),
    ("D3", "Cold work tool", "Harden &amp; temper", "58&ndash;62 HRC",
     "High wear, lower toughness"),
    ("O1", "Oil hardening tool", "Harden &amp; temper", "58&ndash;62 HRC",
     "Low distortion, gauges and cutters"),
    ("H13 / X40CrMoV5-1", "Hot work tool", "Harden &amp; temper / nitride",
     "44&ndash;52 HRC", "Die casting and extrusion dies"),
    ("M2 HSS", "High speed steel", "Harden &amp; triple temper",
     "62&ndash;65 HRC", "Salt or vacuum, tight control"),
    ("S7", "Shock resisting", "Harden &amp; temper", "54&ndash;58 HRC",
     "Punches and chisels"),
    ("SG Iron / Ductile", "Cast iron", "Normalise / austemper", "Varies",
     "ADI available on enquiry"),
    ("Grey cast iron", "Cast iron", "Stress relieve", "No change",
     "Machine bed and housing stability"),
    ("304 / 316", "Austenitic stainless", "Solution anneal", "Soft, ~80 HRB",
     "Restores corrosion resistance after welding"),
    ("410 / 420", "Martensitic stainless", "Harden &amp; temper",
     "40&ndash;50 HRC", "Cutlery, valve trim"),
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
    "always takes precedence &mdash; this is a starting point for a "
    "conversation, not a substitute for a spec."
)

# --------------------------------------------------------------- quality ---

QUALITY_INTRO = (
    "Heat treatment is invisible from the outside. A part that was never "
    "properly hardened looks exactly like one that was, right up until it "
    "fails in service. Everything below exists so you do not have to take our "
    "word for it."
)

QUALITY = [
    dict(name="Rockwell hardness", image="hardness-tester",
         text="HRC and HRB on every batch, at the points the drawing "
              "specifies. The number goes on the report that travels with "
              "the parts."),
    dict(name="Microhardness &amp; case depth", image="hardness-close",
         text="Vickers traverse on a mounted, polished cross-section to "
              "measure effective and total case depth &mdash; the only "
              "honest way to verify a carburised or nitrided case."),
    dict(name="Microstructure", image="micro-ferrite",
         text="Mounted, polished, etched and examined. Confirms the "
              "structure is what the process was supposed to produce, and "
              "catches retained austenite, decarburisation and grain growth."),
    dict(name="Furnace survey &amp; pyrometry", image="furnace-computer",
         text="Temperature uniformity surveys and instrument calibration on "
              "schedule. A furnace that reads 30&deg;C low will pass every "
              "visual check and fail every part."),
]

QUALITY_POINTS = [
    ("ISO 9001:2015", "Certified by BSI. The quality system is audited, not "
                      "self-declared."),
    ("Batch traceability", "Every batch carries an identity from goods-in to "
                           "dispatch, with the cycle recorded against it."),
    ("Reports with the parts", "A hardness report travels with every "
                               "delivery. No chasing paperwork afterwards."),
    ("Written cycles", "Each grade and part number has a recorded cycle, so "
                       "the tenth order runs exactly like the first."),
]

# ------------------------------------------------------------ industries ---

INDUSTRIES = [
    ("Automotive components", "Gears, shafts, pins, levers and linkages for "
     "the tier-one and tier-two supply base around Chennai."),
    ("Transmission &amp; gearing", "Carburised gear sets, splines and "
     "sprockets, with case depth verified per drawing."),
    ("Fasteners", "High-tensile bolts, studs and specials, hardened and "
     "tempered to property class."),
    ("Dies, moulds &amp; tooling", "Cold and hot work tool steels, press "
     "tools, and nitrided die surfaces."),
    ("Pumps &amp; valves", "Shafts, stems and wear parts, including "
     "martensitic and PH stainless."),
    ("Hand &amp; machine tools", "Cutting edges, punches and chisels where "
     "hardness and toughness both matter."),
    ("Agricultural equipment", "Tines, blades and ground-engaging parts built "
     "for abrasion."),
    ("General engineering", "Job work, one-offs, prototypes and the awkward "
     "parts nobody else wants to quote."),
]

INDUSTRIES_INTRO = (
    "Chennai is an engineering city, and most of what we treat ends up inside "
    "something that moves. Batch sizes run from a single prototype to "
    "production quantities."
)

# ---------------------------------------------------------------- about ----

ABOUT_TITLE = "A metallurgist on the shop floor, not just on the letterhead"
ABOUT_IMAGE = "forge"
ABOUT_BODY = [
    "Everest Heat Treaters is a commercial heat treatment shop in "
    "Nazarathpettai, on the western edge of Chennai. We take in components "
    "from manufacturers across the city and return them harder, tougher or "
    "softer &mdash; whatever the drawing asks for &mdash; with the "
    "documentation to prove it.",
    "The business is run by S. Aravindth, a metallurgist by training rather "
    "than a plant operator who learned the trade by repetition. That "
    "distinction matters more than it sounds. Most heat treatment problems "
    "arrive as a part that cracked, distorted or came out soft, and the "
    "answer is almost never in the furnace settings &mdash; it is in the "
    "steel grade, the section change, the sharp corner, or a specification "
    "that was never right for the application.",
    "We would rather have that conversation before the batch runs than after "
    "it fails. If your drawing specifies a treatment that will not do what "
    "you need, we will tell you.",
]

ABOUT_PILLARS = [
    ("Advice before the batch", "If the spec is wrong for the application, "
     "you hear it from us first, not from a failed part."),
    ("Documented, not asserted", "ISO 9001:2015 certified, with a hardness "
     "report on every delivery."),
    ("Built for job work", "One prototype or a thousand pieces, treated with "
     "the same recorded cycle."),
]

# --------------------------------------------------------------- reviews ---
# Illustrative. Written to show the layout; replace with real customer words.
TESTIMONIALS = [
    dict(text="We had a recurring distortion problem on long slender shafts. "
              "Aravindth changed the fixturing and the quench, and the scrap "
              "rate went to almost nothing.",
         name="Sample testimonial", meta="Placeholder &middot; auto components"),
    dict(text="They spotted that our drawing called for a case depth the "
              "grade could not support, and told us before running the "
              "batch. That is not typical.",
         name="Sample testimonial", meta="Placeholder &middot; gear manufacturer"),
]

# --------------------------------------------------------------- contact ---

CONTACT_INTRO = (
    "Send the grade, the drawing and the hardness you need &mdash; or just "
    "describe the problem and we will work out the treatment."
)

RFQ_FIELDS_NOTE = ("Goes straight to WhatsApp with your details filled in. "
                   "No account, no form to chase.")

FAQ = [
    ("What information do you need to quote?",
     "Material grade, quantity, rough size and weight, and the hardness or "
     "case depth required. A drawing is ideal. If you do not know the grade, "
     "say so &mdash; that is a solvable problem."),
    ("What is the usual turnaround?",
     "Most conventional work is a two to three day turnaround. Long-cycle "
     "processes like deep carburising and nitriding take longer, and we will "
     "tell you the realistic date when we quote, not an optimistic one."),
    ("Do you handle small quantities?",
     "Yes. Single pieces, prototypes and trial batches are all normal work "
     "here. Small lots are batched with compatible cycles."),
    ("My parts came out distorted somewhere else. Can you help?",
     "Usually. Distortion is generally a design, grade or fixturing problem "
     "rather than a furnace problem. Send the part and the drawing and we "
     "will tell you what is causing it."),
    ("Can you tell me what treatment I need?",
     "That is a large part of the job. Tell us what the part does, what it "
     "runs against and how it is failing, and we will specify the treatment."),
    ("Do you provide test certificates?",
     "A hardness report goes out with every batch. Microhardness traverses, "
     "case depth measurement and microstructure reports are available on "
     "request."),
]

# ---------------------------------------------------------------- footer ---

FOOTER_NOTE = (
    "Concept design. The company details are genuine; the capability figures, "
    "equipment list and testimonials are illustrative and need confirming."
)
