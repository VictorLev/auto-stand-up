from dotenv import load_dotenv
from datetime import date, timedelta
from notion_client import Client
import os

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

# Set page to full width
notion.pages.update(page_id=page['id'], **{"full_width": True})

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

    daily_items = [
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "📧 Vérifier les courriels"}}], "checked": False}},
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "📅 Planifier ta journée"}}], "checked": False}},
        {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "🤝 Réunions"}}], "checked": False}},
    ]
    if day == "Vendredi":
        daily_items.append({"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": "⏱️ Feuille de temps"}}], "checked": False}})

    def h3(text, children):
        return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}], "is_toggleable": True}, "children": children}

    def todo():
        return {"object": "block", "type": "to_do", "to_do": {"rich_text": [], "checked": False}}

    def bullet():
        return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": []}}

    inner_block = [
        h3("Quotidien", daily_items),
        h3("AI Champion", [todo(), todo()]),
        h3("Projet 1", [todo(), todo(), todo(), todo()]),
        h3("Projet 2", [todo(), todo(), todo(), todo()]),
        h3("Notes de réunion", [bullet()]),
        h3("Plan pour demain", [bullet()]),
    ]

    notion.blocks.children.append(block_id=block_id, children=inner_block)
