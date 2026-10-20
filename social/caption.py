import os
import random
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

THEMES = [
    "sunset views over Galveston Bay from the deck",
    "a luxurious bayfront escape for the whole family",
    "the hot tub at golden hour with bay views",
    "waking up to sweeping water views in Galveston",
    "the private boardwalk and dock on Galveston Bay",
    "a long weekend getaway for a large group",
    "the chef's kitchen and open living space",
    "exploring Galveston Island from a bayfront home",
    "the master suite with panoramic bay views",
    "gathering the whole family under one roof in Galveston",
    "watching the sunset turn the bay gold from your deck",
    "a home that sleeps 16 — because the more the merrier",
]

HASHTAGS = [
    "#GalvestonVacation #BayfrontRental #RoadLessTraveled",
    "#GalvestonBay #VacationRental #TexasGetaway",
    "#GalvestonTexas #LuxuryRental #FamilyVacation",
    "#VisitGalveston #BeachHouse #GulfCoast",
    "#GalvestonBayClub #VacationHome #TexasTravel",
    "#SunsetViews #BayLife #GalvestonIsland",
]


def generate_caption(theme: str = None, content_type: str = "property") -> str:
    if theme is None:
        theme = random.choice(THEMES)

    if content_type == "galveston":
        prompt = f"""Write an engaging Instagram caption about {theme}.
The caption is for a luxury bayfront vacation rental called Road Less Traveled
in Galveston Bay Club, Galveston, TX. It sleeps up to 16 guests.
Keep it warm, evocative, and aspirational — like you're inviting someone to escape.
2-4 sentences. End with a subtle call to action to book the link in bio.
Do not use quotation marks. Do not use emojis."""
    else:
        prompt = f"""Write an engaging Instagram caption about {theme}.
The caption is for a luxury bayfront vacation rental called Road Less Traveled
in Galveston Bay Club, Galveston, TX. Features include: 4BR/4BA, sleeps 16,
private hot tub, private boardwalk and dock, chef's kitchen, sweeping bay views.
Keep it warm, evocative, and aspirational — like you're inviting someone to escape.
2-4 sentences. End with a subtle call to action to book the link in bio.
Do not use quotation marks. Do not use emojis."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    caption = message.content[0].text.strip()
    hashtags = random.choice(HASHTAGS)
    return f"{caption}\n\n{hashtags}"


if __name__ == "__main__":
    print(generate_caption())
