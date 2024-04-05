import json
import enum
import functools
from typing import Any
from types import SimpleNamespace
from absl import app
import requests
from pprint import pprint

@functools.cache
def api_key():
  try:
    with open('.secrets.json') as secrets_file:
      secrets = json.load(secrets_file)

    return secrets["CLICKUP_API_KEY"]
  except:
    raise RuntimeError("Unable to load api key from .secrets.json")


class Entities(enum.Enum):
  SPACE = 0
  FOLDER = 1
  LIST = 2
  TASK = 3


def get_tasks(list_id: str):
  url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"
  query = {
    "archived": "false",
    "include_markdown_description": "true",
    "page": "0",
    "order_by": "string",
    "reverse": "true",
    "subtasks": "true",
    "statuses": "string",
    "include_closed": "true",
    "assignees": "string",
    "tags": "string",
    "due_date_gt": "0",
    "due_date_lt": "0",
    "date_created_gt": "0",
    "date_created_lt": "0",
    "date_updated_gt": "0",
    "date_updated_lt": "0",
    "date_done_gt": "0",
    "date_done_lt": "0",
    "custom_fields": "string",
    "custom_items": "0"
  }
  return _make_simple_request(url).tasks



def get_lists(folder_id: str):
  url = "https://api.clickup.com/api/v2/folder/" + folder_id + "/list"
  return _make_simple_request(url).lists


def get_folders(space_id: str):
  url = "https://api.clickup.com/api/v2/space/" + space_id + "/folder"
  return _make_simple_request(url).folders


def get_teams():

  url = "https://api.clickup.com/api/v2/group"

  query = {
    "team_id": "123",
    "group_ids": "C9C58BE9-7C73-4002-A6A9-310014852858"
  }

  headers = {"Authorization": api_key()}

  response = requests.get(url, headers=headers, params=query)

  data = response.json()


def _get_spaces(team_id: str):
  url = "https://api.clickup.com/api/v2/team/" + team_id + "/space"
  return _make_simple_request(url)



def get_authorized_teams():
  url = "https://api.clickup.com/api/v2/team"
  return _make_simple_request(url)


def get_spaces():
  authorized_teams = get_authorized_teams()
  team_id = authorized_teams.teams[0].id
  spaces = _get_spaces(team_id)
  return spaces.spaces


def get_subentity(mode: Entities, entity_id: Any | None = None):
  """Will select an entity and return the contents of that entity."""
  if mode == Entities.SPACE:
    return Entities.FOLDER, get_folders(entity_id)

  if mode == Entities.FOLDER:
    return Entities.LIST, get_lists(entity_id)

  if mode == Entities.LIST:
    return Entities.TASK, get_tasks(entity_id)

  raise NotImplemented('Try again!')


def _make_simple_request(url: str, query: dict | None = None):
  if query is None:
    query = {
      "archived": "false"
    }

  headers = {"Authorization": api_key()}

  response = requests.get(url, headers=headers, params=query)

  data = response.json()
  return json.loads(response.text, object_hook=lambda x: SimpleNamespace(**x))


def main(argv):
  spaces = get_spaces()
  space_ids = {s.name: s.id for s in spaces}
  pprint(space_ids)
  space_id = spaces[0].id
  folders = get_folders(space_id)
  pprint(folders)
  breakpoint()


if __name__ == "__main__":
  app.run(main)

