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
        "price": "$64",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/ContrastVoltageSportsBra_HollywoodPink_02.jpg?v=1784049960&width=720",
        "image_alt": "Bombshell Sportswear Contrast Voltage Sports Bra in Hollywood Pink",
        "url": "https://www.bombshellsportswear.com/products/contrast-voltage-sports-bra-hollywood-pink",
    },
    {
        "category": "sports-bras",
        "category_label": "SPORTS BRA",
        "name": "Trailblaze Sports Bra",
        "color": "Hyper Violet",
        "price": "$62",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/TrailblazeSportsBra_HyperViolet_03.jpg?v=1758917482&width=720",
        "image_alt": "Bombshell Sportswear Trailblaze Sports Bra in Hyper Violet",
        "url": "https://www.bombshellsportswear.com/products/trailblaze-sports-bra-hyper-violet",
    },
    {
        "category": "bodysuits",
        "category_label": "BODYSUIT",
        "name": "Flatter Bodysuit Shorts",
        "color": "Neon Flame",
        "price": "$115",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/FlatterBodsyuitShorts_NeonFlame_01.jpg?v=1784902173&width=720",
        "image_alt": "Bombshell Sportswear Flatter Bodysuit Shorts in Neon Flame",
        "url": "https://www.bombshellsportswear.com/products/flatter-bodysuit-shorts-neon-flame",
    },
    {
        "category": "bodysuits",
        "category_label": "BODYSUIT",
        "name": "Bombshell Bodysuit",
        "color": "Obsidian Black",
        "price": "$125",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/BombshellBodysuit_HeatheredBlack_02_01c3cf60-c6d0-4940-9474-df05c2d1a26c.jpg?v=1779889894&width=720",
        "image_alt": "Bombshell Sportswear Bombshell Bodysuit in Obsidian Black",
        "url": "https://www.bombshellsportswear.com/products/bombshell-bodysuit-obsidian-black",
    },
    {
        "category": "leggings",
        "category_label": "LEGGINGS",
        "name": "Inline Straight Leggings",
        "color": "Ice Queen",
        "price": "$105",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/InlineStraightLeggings_IceQueen_04.jpg?v=1785682941&width=720",
        "image_alt": "Bombshell Sportswear Inline Straight Leggings in Ice Queen",
        "url": "https://www.bombshellsportswear.com/products/inline-straight-leggings-ice-queen",
    },
    {
        "category": "leggings",
        "category_label": "LEGGINGS",
        "name": "Curvepro Leggings",
        "color": "Coral Peach",
        "price": "$92",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/CurveProLeggings_CoralPeach_02.jpg?v=1786026527&width=720",
        "image_alt": "Bombshell Sportswear Curvepro Leggings in Coral Peach",
        "url": "https://www.bombshellsportswear.com/products/curvepro-leggings-coral-peach",
    },
    {
        "category": "sports-tops",
        "category_label": "SPORTS TOP",
        "name": "Cinch Cami Tank",
        "color": "White",
        "price": "$58",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/CinchCamiTank_White_06.jpg?v=1789760046&width=720",
        "image_alt": "Bombshell Sportswear Cinch Cami Tank in White",
        "url": "https://www.bombshellsportswear.com/products/cinch-cami-tank-white",
    },
    {
        "category": "sports-tops",
        "category_label": "SPORTS TOP",
        "name": "Muscle Muse Tee",
        "color": "White",
        "price": "$48",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/MuscleMuseTee_White_09.jpg?v=1786027431&width=720",
        "image_alt": "Bombshell Sportswear Muscle Muse Tee in White",
        "url": "https://www.bombshellsportswear.com/products/muscle-muse-tee-white",
    },
    {
        "category": "matching-sets",
        "category_label": "MATCHING SET",
        "name": "Movement Set",
        "color": "Bubblegum",
        "detail": "Leggings + Resilient Sports Bra",
        "price": "$160 together",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/MovementLeggings_Bubblegum_01.jpg?v=1790273377&width=720",
        "image_alt": "Bombshell Sportswear Bubblegum Movement Leggings and matching sports bra",
        "url": "https://www.bombshellsportswear.com/collections/matching-sets",
    },
    {
        "category": "matching-sets",
        "category_label": "MATCHING SET",
        "name": "Movement Set",
        "color": "Watermelon Punch",
        "detail": "Leggings + Resilient Sports Bra",
        "price": "$160 together",
        "image": "https://cdn.shopify.com/s/files/1/0580/1077/files/MovementLeggings_WatermelonPunch_03.jpg?v=1790273275&width=720",
        "image_alt": "Bombshell Sportswear Watermelon Punch Movement Leggings and matching sports bra",
        "url": "https://www.bombshellsportswear.com/collections/matching-sets",
    },
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
        },
    )