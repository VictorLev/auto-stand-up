from dotenv import load_dotenv
from datetime import date, timedelta
from notion_client import Client
import os
import urllib.request
import json

def get_random_quote():
    try:
        with urllib.request.urlopen("https://zenquotes.io/api/random") as response:
            data = json.loads(response.read())
            return f'"{data[0]["q"]}" — {data[0]["a"]}'
    except:
        return "Make each day your masterpiece."

# Load the .env file
load_dotenv()

# Initialize the client with your Notion API key
notion = Client(auth=os.getenv("NOTION_KEY"))
spandupPageId = os.getenv("STANDUP_PAGE_ID")
today = str(date.today() + timedelta(days=7))

Week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

# Create a page
page = notion.pages.create(
    parent={
        "page_id": spandupPageId
    },
    properties={
        "title": {
            "title": [
                {
                    "text": {
                        "content": "Semaine du ",
                    }
                },
                {
                    "mention": {
                        "type": "date",
                        "date": {
                            "start": today
                        }
                    }
                }
            ]
        }
    }
)

# Notes section at the top of the page
notion.blocks.children.append(block_id=page['id'], children=[
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "Notes de la semaine"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": []}
    }
])

for day in Week:

    # Create Day Title

    week_block = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": day
                        }
                    }
                ],
                "is_toggleable": True
            }
        }
    ]
    response = notion.blocks.children.append(block_id=page['id'], children=week_block)
    block_id = response.get("results")[0].get("id")

    quote_text = get_random_quote()
    notion.blocks.children.append(block_id=block_id, children=[
        {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": quote_text}}]
            }
        }
    ])

    daily_items = [
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "📧 Vérifier les courriels"}}], "checked": False}},
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "📅 Planifier ta journée"}}], "checked": False}},
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "🤝 Réunions"}}], "checked": False}},
    ]
    if day == "Vendredi":
        daily_items.append({"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "⏱️ Feuille de temps"}}], "checked": False}})

    def h3(text):
        return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}], "is_toggleable": True}}

    def todo():
        return {"object": "block", "type": "to_do", "to_do": {"rich_text": [], "checked": False}}

    def bullet():
        return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": []}}

    sections = [
        ("Quotidien", daily_items),
        ("AI Champion", [todo(), todo()]),
        ("Projet 1", [todo(), todo(), todo(), todo()]),
        ("Projet 2", [todo(), todo(), todo(), todo()]),
        ("Notes de réunion", [bullet()]),
        ("Plan pour demain", [bullet()]),
    ]

    for section_name, section_children in sections:
        response = notion.blocks.children.append(block_id=block_id, children=[h3(section_name)])
        section_id = response.get("results")[0].get("id")
        notion.blocks.children.append(block_id=section_id, children=section_children)
