from dotenv import load_dotenv
from datetime import date
from notion_client import Client
import os

# Load the .env file
load_dotenv()

# Initialize the client with your Notion API key
notion = Client(auth=os.getenv("NOTION_KEY"))
spandupPageId = os.getenv("STANDUP_PAGE_ID")
today  = str(date.today())

Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

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
                        "content": "Week of ",
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

for day in Week:

    # Create Day Title

    week_block = [
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": day
                        }
                    }
                ]
            }
        }
    ]
    response = notion.blocks.children.append(block_id=page['id'], children=week_block)
    block_id = response.get("results")[0].get("id")

    to_do_items = [
    "Touch typing practice",
    "Check emails",
    "Write Pending Tasks",
    ]
    if day == "Friday" : to_do_items.append("Timesheet")

    to_do_blocks = []

    for item in to_do_items:
        block = {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": item}
                }],
                "checked": False
            }
        }
        to_do_blocks.append(block)

    inner_block = [
        # Daily Checks Block
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Daily Checks"}
                }]
            }
        }
        ,
        *to_do_blocks
        ,
        # To Do Block
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Pending Tasks"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {"rich_text": [], "checked": False}
        },

        # What Happened Block
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "What Happened"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Morning"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": []}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Afternoon"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": []}
        },


    ]

    notion.blocks.children.append(block_id=block_id, children=inner_block)

notion.blocks.children.append(block_id=page['id'], children=
    [
    # Next Week Block
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Next week items"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": []}
        }
    ]
)
