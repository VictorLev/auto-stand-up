from dotenv import load_dotenv
from datetime import date
from notion_client import Client
import os

# Load the .env file
load_dotenv()

# Initialize the client with your Notion API key
notion = Client(auth=os.getenv("NOTION_KEY"))
today  = str(date.today())

Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Create a page
page = notion.pages.create(
    parent={
        "page_id": os.getenv("STANDUP_PAGE_ID")
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
        {
            "object": "block",
            "type": "to_do",
            "to_do": {"rich_text": [], "checked": False}
        }
    ]

    notion.blocks.children.append(block_id=block_id, children=inner_block)

# Create 2 Blocks

# Append 2 Blcoks to the Day Title 


# Adding headings and to-do tasks
# Monday_block = [
#     {
#         "object": "block",

#     },
#     {
#         "object": "block",
#         "type": "heading_3",
#         "heading_3": {
#             "rich_text": [
#                 {
#                     "type": "text",
#                     "text": {"content": "To Do"}
#                 }
#             ]
#         }
#     }
# ]

# USE append() FUNCTION TO CREATE EVERY WEEKBLOCK AND ADD THE CHILDREN BLOCKS
# THEN ADD THE WEEKBLOCK TO THE PARENT PAGE
# notion.blocks.children.append(block_id=page_id, children=Monday_block)



