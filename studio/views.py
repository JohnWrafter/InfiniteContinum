from django.contrib import messages
from django.shortcuts import redirect, render

from studio.forms import MemberInquiryForm

WORKOUTS = {
    "strength": {
        "title": "Build strength",
        "intro": "A little more capable, one good rep at a time.",
        "sessions": [
            ("01", "Full-body foundations", "Squat, push and pull", "45 min", "MON"),
            ("02", "Strong from the center", "Core and controlled lifts", "40 min", "WED"),
            ("03", "Power, at your pace", "Hinge, carry and reset", "50 min", "FRI"),
        ],
    },
    "endurance": {
        "title": "Improve endurance",
        "intro": "More energy for the long run and everything after it.",
        "sessions": [
            ("01", "Find your stride", "Easy aerobic intervals", "35 min", "MON"),
            ("02", "A little faster", "Short, steady efforts", "30 min", "WED"),
            ("03", "Go the distance", "Low-impact endurance", "45 min", "FRI"),
        ],
    },
    "mobility": {
        "title": "Move with more ease",
        "intro": "Feel at home in your body, from warm-up to wind-down.",
        "sessions": [
            ("01", "Space to move", "Hips, ankles and flow", "30 min", "MON"),
            ("02", "A stronger range", "Stability and control", "35 min", "WED"),
            ("03", "Reset and restore", "Mobility and breathwork", "30 min", "FRI"),
        ],
    },
    "consistency": {
        "title": "Find your rhythm",
        "intro": "A flexible routine that fits around your actual life.",
        "sessions": [
            ("01", "Start where you are", "A full-body reset", "30 min", "MON"),
            ("02", "Build a little momentum", "Strength and steady cardio", "35 min", "WED"),
            ("03", "Show up for yourself", "A feel-good finish", "30 min", "FRI"),
        ],
    },
}

APPAREL_CATEGORIES = (
    ("sports-bras", "Sports bras"),
    ("bodysuits", "Bodysuits"),
    ("leggings", "Leggings"),
    ("sports-tops", "Sports tops"),
    ("matching-sets", "Matching sets"),
)

APPAREL_PRODUCTS = (
    {
        "category": "sports-bras",
        "category_label": "SPORTS BRA",
        "name": "Contrast Voltage Sports Bra",
        "color": "Hollywood Pink",
        "price": "£65",
        "description": "Contrast trim, adjustable straps and V-front detail combine a bold look with supportive hold.",
        "image": "Sports-Bras/contrast-voltage-hollywood-pink.jpg",
        "image_alt": "Bombshell Sportswear Contrast Voltage Sports Bra in Hollywood Pink",
        "url": "https://www.bombshellsportswear.com/products/contrast-voltage-sports-bra-hollywood-pink",
        "sizes": (("XS", "43609887309911"), ("S", "43609887342679"), ("M", "43609887375447"), ("L", "43609887408215"), ("XL", "43609887440983")),
    },
    {
        "category": "sports-bras",
        "category_label": "SPORTS BRA",
        "name": "Trailblaze Sports Bra",
        "color": "Hyper Violet",
        "price": "£63",
        "description": "A backless cut, adjustable halter straps and a wide underband are made for supported movement.",
        "image": "Sports-Bras/trailblaze-hyper-violet.jpg",
        "image_alt": "Bombshell Sportswear Trailblaze Sports Bra in Hyper Violet",
        "url": "https://www.bombshellsportswear.com/products/trailblaze-sports-bra-hyper-violet",
        "sizes": (("XS", "41648594649175"), ("S", "41648594681943"), ("M", "41648594714711"), ("L", "41648594747479"), ("XL", "41648594780247")),
    },
    {
        "category": "bodysuits",
        "category_label": "BODYSUIT",
        "name": "Flatter Bodysuit Shorts",
        "color": "Neon Flame",
        "price": "£120",
        "description": "An open V-back, adjustable straps and a built-in bra meet a deep scoop neckline.",
        "image": "Bodysuits/flatter-neon-flame.jpg",
        "image_alt": "Bombshell Sportswear Flatter Bodysuit Shorts in Neon Flame",
        "url": "https://www.bombshellsportswear.com/products/flatter-bodysuit-shorts-neon-flame",
        "sizes": (("XS", "43610760904791"), ("S", "43610760937559"), ("M", "43610760970327"), ("L", "43610761003095"), ("XL", "43610761035863")),
    },
    {
        "category": "bodysuits",
        "category_label": "BODYSUIT",
        "name": "Bombshell Bodysuit",
        "color": "Obsidian Black",
        "price": "£130",
        "description": "A sculpting one-piece with a built-in push-up bra, adjustable straps and an open back.",
        "image": "Bodysuits/bombshell-obsidian-black.jpg",
        "image_alt": "Bombshell Sportswear Bombshell Bodysuit in Obsidian Black",
        "url": "https://www.bombshellsportswear.com/products/bombshell-bodysuit-obsidian-black",
        "sizes": (("XXS", "42667349639255"), ("XS", "42667349672023"), ("S", "42667349704791"), ("M", "42667349737559"), ("L", "42667349770327"), ("XL", "42667349803095")),
    },
    {
        "category": "leggings",
        "category_label": "LEGGINGS",
        "name": "Inline Straight Leggings",
        "color": "Ice Queen",
        "price": "£110",
        "description": "A straight-leg silhouette, curved waistband and contour seams create a streamlined fit.",
        "image": "Leggings/inline-straight-ice-queen.jpg",
        "image_alt": "Bombshell Sportswear Inline Straight Leggings in Ice Queen",
        "url": "https://www.bombshellsportswear.com/products/inline-straight-leggings-ice-queen",
        "sizes": (("XXS", "43983769075799"), ("XS", "43983769108567"), ("S", "43983769141335"), ("M", "43983769174103"), ("L", "43983769206871"), ("XL", "43983769239639")),
    },
    {
        "category": "leggings",
        "category_label": "LEGGINGS",
        "name": "Curvepro Leggings",
        "color": "Coral Peach",
        "price": "£93",
        "description": "A convertible waistband lets you wear a deep V or fold it up for a high-rise fit.",
        "image": "Leggings/curvepro-coral-peach.jpg",
        "image_alt": "Bombshell Sportswear Curvepro Leggings in Coral Peach",
        "url": "https://www.bombshellsportswear.com/products/curvepro-leggings-coral-peach",
        "sizes": (("XXS", "43613466787927"), ("XS", "43613466820695"), ("S", "43613466853463"), ("M", "43613466886231"), ("L", "43613466918999"), ("XL", "43613466951767")),
    },
    {
        "category": "sports-tops",
        "category_label": "SPORTS TOP",
        "name": "Cinch Cami Tank",
        "color": "White",
        "price": "£59",
        "description": "A clean cami silhouette in soft, supportive performance fabric for training or everyday wear.",
        "image": "Sports-Tops/cinch-cami-white.jpg",
        "image_alt": "Bombshell Sportswear Cinch Cami Tank in White",
        "url": "https://www.bombshellsportswear.com/products/cinch-cami-tank-white",
        "sizes": (("XS", "44088105402455"), ("S", "44088105435223"), ("M", "44088105467991"), ("L", "44088105500759"), ("XL", "44088105533527")),
    },
    {
        "category": "sports-tops",
        "category_label": "SPORTS TOP",
        "name": "Muscle Muse Tee",
        "color": "White",
        "price": "£49",
        "description": "A lightweight cropped tee with a relaxed fit for warm-ups, training and easy layering.",
        "image": "Sports-Tops/muscle-muse-white.jpg",
        "image_alt": "Bombshell Sportswear Muscle Muse Tee in White",
        "url": "https://www.bombshellsportswear.com/products/muscle-muse-tee-white",
        "sizes": (("XS", "43899720335447"), ("S", "43899720368215"), ("M", "43899720400983"), ("L", "43899720433751"), ("XL", "43899720466519")),
    },
    {
        "category": "matching-sets",
        "category_label": "MATCHING SET",
        "name": "Movement Set",
        "color": "Bubblegum",
        "detail": "Seamless leggings and a coordinating Resilient sports bra.",
        "price": "£162",
        "image": "Matching-Sets/movement-bubblegum.jpg",
        "image_alt": "Bombshell Sportswear Bubblegum Movement Leggings and matching sports bra",
        "components": (
            ("Leggings", "https://www.bombshellsportswear.com/products/movement-leggings-bubblegum", (("XXS", "44105869623383"), ("XS", "44105869656151"), ("S", "44105869688919"), ("M", "44105869721687"), ("L", "44105869754455"), ("XL", "44105869787223"))),
            ("Sports bra", "https://www.bombshellsportswear.com/products/resilient-sports-bra-bubblegum", (("XS", "44105874243671"), ("S", "44105874276439"), ("M", "44105874309207"), ("L", "44105874341975"), ("XL", "44105874374743"))),
        ),
    },
    {
        "category": "matching-sets",
        "category_label": "MATCHING SET",
        "name": "Movement Set",
        "color": "Watermelon Punch",
        "detail": "Seamless leggings and a coordinating Resilient sports bra.",
        "price": "£162",
        "image": "Matching-Sets/movement-watermelon-punch.jpg",
        "image_alt": "Bombshell Sportswear Watermelon Punch Movement Leggings and matching sports bra",
        "components": (
            ("Leggings", "https://www.bombshellsportswear.com/products/movement-leggings-watermelon-punch", (("XXS", "44105872572503"), ("XS", "44105872605271"), ("S", "44105872638039"), ("M", "44105872670807"), ("L", "44105872703575"), ("XL", "44105872736343"))),
            ("Sports bra", "https://www.bombshellsportswear.com/products/resilient-sports-bra-watermelon-punch", (("XS", "44105878437975"), ("S", "44105878470743"), ("M", "44105878503511"), ("L", "44105878536279"), ("XL", "44105878569047"))),
        ),
    },
)

SPORTS_BRA_IMAGE_EDITS = (
    ("sportsbra_1.webp", "Twist-front keyhole bra", "Warm taupe", "A gathered front and small keyhole detail, styled with coordinating leggings."),
    ("sportsbra_2.webp", "Twist-front keyhole bra", "Black", "A black twist-front silhouette with narrow shoulder straps and a clean finish."),
    ("sportsbra_3.webp", "Cross-strap longline bra", "Heather blue", "A heather-blue crop with crossed neckline straps and a wide underband."),
    ("sportsbra_4.webp", "Contrast cutout bra", "Volt green", "A bright cutout crop styled with black leggings and vivid contrast bands."),
    ("sportsbra_5.webp", "Zip-detail crop bra", "Electric blue", "A smooth blue crop with a scoop neckline and subtle side hardware."),
    ("sportsbra_6.webp", "Cross-back crop bra", "Coral", "A coral crop with crossed back straps and a coordinating set look."),
    ("sportsbra_7.webp", "Ruched-side crop bra", "Black", "A black crop with gathered side details and a simple scoop neckline."),
    ("sportsbra_8.webp", "Multi-strap back bra", "Berry pink", "A pink crop with a multi-strap open back and matching leggings."),
    ("sportsbra_9.webp", "Ruched halter crop bra", "Pink marble", "A marbled pink halter crop with an adjustable-looking centre detail."),
    ("sportsbra_10.webp", "Classic racerback crop bra", "Lilac", "A soft lilac crop with a clean scoop front and broad racerback straps."),
    ("sportsbra_11.webp", "Textured racerback crop bra", "Black", "A black textured crop photographed from the back to show its racerback shape."),
    ("sportsbra_12.webp", "Gloss-finish crop bra", "Navy", "A deep navy crop with a smooth, light-catching finish and wide straps."),
    ("sportsbra_13.webp", "Zebra-print crop bra", "Rose", "A rose-pink crop with a tonal zebra print and coordinating leggings."),
    ("sportsbra_14.webp", "Zebra-print crop bra", "Violet", "A violet crop with a tonal zebra print and matching set styling."),
    ("sportsbra_15.webp", "Cross-front keyhole bra", "Slate", "A slate-grey crop with crossed front straps and a gathered keyhole detail."),
    ("sportsbra_16.webp", "Contrast halter crop bra", "Neon pink", "A bright pink halter-style crop with black contrast straps and cutouts."),
)

APPAREL_PRODUCTS += tuple(
    {
        "category": "sports-bras",
        "category_label": "SPORTS BRA EDIT",
        "name": name,
        "color": color,
        "price": "From £59",
        "description": description,
        "image": f"Sports-Bras/{image}",
        "image_alt": f"Women's {name.lower()} in {color}, styled by Bombshell Sportswear",
        "url": "https://www.bombshellsportswear.com/collections/sports-bras",
        "collection_only": True,
        "size_options": ("XS", "S", "M", "L", "XL"),
    }
    for image, name, color, description in SPORTS_BRA_IMAGE_EDITS
)

LEGGINGS_IMAGE_EDITS = (
    ("leggings_1.webp", "Contour Leggings", "Soft grey", "A clean, high-rise silhouette styled with a matching cutout sports bra."),
    ("leggings_2.webp", "Drawcord-cuff Leggings", "Coral pink", "Bright cropped leggings with gathered drawcord cuffs for an adjustable finish."),
    ("leggings_3.webp", "Gloss Leggings", "Midnight blue", "A light-catching finish gives this deep-blue legging set a sleek studio look."),
    ("leggings_4.webp", "Marble-print Leggings", "Pink marble", "Soft pink marbling and a high-rise waistband add pattern to a classic legging shape."),
    ("leggings_5.webp", "Lace-up Waist Leggings", "Violet zebra", "A tonal zebra print meets a lace-up waist detail in this matching set."),
    ("leggings_6.webp", "Gathered-cuff Leggings", "Coral", "A soft coral pair with gathered cuffs for a cropped, adjustable silhouette."),
    ("leggings_7.webp", "Animal-print Leggings", "Charcoal leopard", "A subtle animal print adds texture to a neutral matching workout set."),
    ("leggings_8.webp", "Graphic Leggings", "Violet", "Bold violet leggings with graphic side detailing and a cross-strap set styling."),
    ("leggings_9.webp", "Sculpt Leggings", "White", "A bright white legging with a smooth finish and shaped seam detailing."),
    ("leggings_10.jpg", "Tie-cuff Leggings", "Rose red", "A vivid rose-red pair with adjustable ankle ties and a gathered finish."),
    ("leggings_11.webp", "Textured Leggings", "Teal", "A deep teal set with a subtle ribbed texture and high-rise waistband."),
    ("leggings_12.webp", "Studio Leggings", "Hot pink", "An all-over hot-pink look with a coordinating top and practical side pocket."),
    ("leggings_13.webp", "Gloss Leggings", "Ruby red", "A reflective ruby-red finish brings a statement look to a streamlined fit."),
    ("leggings_14.webp", "Hook-waist Leggings", "Navy", "A high-rise navy silhouette finished with a distinctive hook-detail waistband."),
    ("leggings_15.webp", "Studio Leggings", "Golden yellow", "A warm golden-yellow set with a simple high-rise legging silhouette."),
    ("leggings_16.webp", "Chevron-texture Leggings", "Deep charcoal", "A dark textured fabric and tonal chevron pattern create a subtle statement."),
)

APPAREL_PRODUCTS += tuple(
    {
        "category": "leggings",
        "category_label": "LEGGINGS EDIT",
        "name": name,
        "color": color,
        "price": "From £93",
        "description": description,
        "image": f"Leggings/{image}",
        "image_alt": f"Women's {name.lower()} in {color}, styled by Bombshell Sportswear",
        "url": "https://www.bombshellsportswear.com/collections/leggings",
        "collection_only": True,
        "size_options": ("XXS", "XS", "S", "M", "L", "XL"),
    }
    for image, name, color, description in LEGGINGS_IMAGE_EDITS
)

BODYSUITS_IMAGE_EDITS = (
    ("bodysuit_1.webp", "Contour Bodysuit", "Warm taupe", "A sleek one-piece with sculpting seams, a softly open back and a supportive studio-ready fit."),
    ("bodysuit_2.webp", "Co-ord Bodysuit", "Soft black", "A smooth black bodysuit with wide straps, a deep V-neckline and a tailored finish."),
    ("bodysuit_3.webp", "Sculpt Bodysuit", "Ivory", "An elevated ivory bodysuit with contour shaping, adjustable straps and a polished silhouette."),
    ("bodysuit_4.webp", "Lift Bodysuit", "Cherry red", "A bright red bodysuit shaped for a confident fit with easy movement and strong support."),
    ("bodysuit_5.webp", "Open-back Bodysuit", "Electric blue", "A vivid electric blue bodysuit with clean lines and an open-back feel for dynamic training."),
    ("bodysuit_6.webp", "Studio Bodysuit", "Midnight blue", "A deep blue bodysuit with a seamless finish that suits both strength work and recovery days."),
    ("bodysuit_7.webp", "Contour Bodysuit", "Black", "A classic black bodysuit with a sculpting cut, smooth finish and supportive structure."),
    ("bodysuit_8.webp", "Motion Bodysuit", "Coral", "Warm coral tones bring a relaxed confidence to this striking, flexible bodysuit."),
    ("bodysuit_9.webp", "Halo Bodysuit", "Pink marble", "A marbled pink bodysuit with a softly structured front and a flattering, body-skimming fit."),
    ("bodysuit_10.webp", "Form Bodysuit", "Lilac", "A lilac bodysuit with a gentle contour and a confident, easy silhouette for everyday wear."),
    ("bodysuit_11.webp", "Shape Bodysuit", "Charcoal", "A charcoal bodysuit with a sleek finish and a clean line that pairs beautifully with layered styling."),
    ("bodysuit_12.webp", "Gloss Bodysuit", "Navy", "A polished navy bodysuit with a sleek shine and a supportive, easy-to-move-in fit."),
    ("bodysuit_13.webp", "Curve Bodysuit", "Rose pink", "A rose-pink bodysuit with a subtle contour and a smooth shape for confident movement."),
    ("bodysuit_14.webp", "Studio Bodysuit", "Pale gold", "A warm gold-toned bodysuit with a modern finish and flattering strength-focused fit."),
    ("bodysuit_15.webp", "Metro Bodysuit", "Deep charcoal", "A clean charcoal bodysuit with sculpted lines and a refined fit for everyday training."),
    ("bodysuit_16.webp", "Suit Bodysuit", "Black", "A sharp black bodysuit that keeps the focus on movement, support and an easy premium feel."),
)

APPAREL_PRODUCTS += tuple(
    {
        "category": "bodysuits",
        "category_label": "BODYSUIT EDIT",
        "name": name,
        "color": color,
        "price": "From £120",
        "description": description,
        "image": f"Bodysuits/{image}",
        "image_alt": f"Women's {name.lower()} in {color}, styled by Bombshell Sportswear",
        "url": "https://www.bombshellsportswear.com/collections/bodysuits",
        "collection_only": True,
        "size_options": ("XXS", "XS", "S", "M", "L", "XL"),
    }
    for image, name, color, description in BODYSUITS_IMAGE_EDITS
)


def home(request):
    if request.method == "POST":
        form = MemberInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You're on the list. We'll be in touch soon.")
            return redirect("home")
    else:
        form = MemberInquiryForm()

    focus = request.GET.get("focus", "strength")
    if focus not in WORKOUTS:
        focus = "strength"
    try:
        session_count = int(request.GET.get("sessions", "3"))
    except ValueError:
        session_count = 3
    if session_count not in (2, 3):
        session_count = 3

    selected_workout = WORKOUTS[focus]
    return render(
        request,
        "studio/home.html",
        {
            "form": form,
            "workouts": WORKOUTS,
            "selected_focus": focus,
            "selected_workout": selected_workout,
            "sessions_per_week": session_count,
            "planned_sessions": selected_workout["sessions"][:session_count],
            "apparel_categories": APPAREL_CATEGORIES,
            "apparel_products": APPAREL_PRODUCTS,
            "apparel_currency": "GBP",
        },
    )