from dotenv import load_dotenv
from datetime import date
from notion_client import Client
import os

# Load the .env file
load_dotenv()

# Initialize the client with your Notion API key
notion = Client(auth=os.getenv("NOTION_KEY"))
spandupPageId = os.getenv("STANDUP_PAGE_ID")
archivePageId = os.getenv("ARCHIVE_PAGE_ID")
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

    inner_block = [
        # To Do Block
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "To Do"}
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
            "type": "to_do",
            "to_do": {"rich_text": [], "checked": False}
        },
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
                        "text": {"content": "Red Alerts"}
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
                        "text": {"content": "Yellow Alerts"}
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

    notion.blocks.children.append(block_id=block_id, children=inner_block)