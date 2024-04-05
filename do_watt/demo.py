from collections.abc import Sequence
import random
from typing import Any, Type, TypeVar

from textual.app import App, CSSPathType, ComposeResult
from textual.driver import Driver
from textual.widgets import Header, Footer
from textual import containers
from textual import widgets

import data as dummy_data
import clickup


_T = TypeVar('_T')


def pick_random(seq: Sequence[_T]) -> _T:
  """Picks a random item."""
  return seq[random.randint(0, len(seq)-1)]


def seq_dict_to_data_table(data: Sequence[dict[str, Any]]): # -> tuple[tuple[str], tuple[Any]]:
  """Converts a sequence of dicts to header and rows."""
  example = data[0]
  headers = tuple(example.keys())
  rows = (tuple(d[k] for k in example.keys()) for d in data)
  print(rows)
  return headers, rows


class DoWattApp(App):
  """A Textual app to automatically decide watt to do for maximum power."""

  BINDINGS = [
      ("d", "toggle_dark", "Toggle dark mode"),
      ("p", "pick_random", "Pick a random activity."),
      ("enter", "select", "Select!"),
      ("q", "exit", "Exit"),
      #("k", "page_up", "PageUp"),
      #("j", "page_down", "PageDown"),
  ]

  def __init__(
      self,
      driver_class: Type[Driver] | None = None,
      css_path: CSSPathType | None = None,
      watch_css: bool = False,
  ):
     super().__init__(driver_class, css_path, watch_css)
     self._data = None
     self._mode = clickup.Entities.SPACE
     self.load_data()


  def load_data(self):
    spaces = clickup.get_spaces()
    # TODO(elpiloto): Hide id column
    self._data = dummy_data.add_id_inplace(
        [dict(name=s.name, id=s.id) for s in spaces]
    )
    self._headers, self._rows = seq_dict_to_data_table(self._data)

  def reload_data(self, new_data):
    # TODO(elpiloto): Hide id column
    self._data = dummy_data.add_id_inplace(
        [dict(name=x.name, id=x.id) for x in new_data]
    )
    self._headers, self._rows = seq_dict_to_data_table(self._data)
    self._populate_table()

  def compose(self) -> ComposeResult:
      """Create child widgets for the app."""
      yield widgets.Header()
      table = widgets.DataTable()
      table.focus()  # this enable pageup/pagedown to work
      yield containers.HorizontalScroll(
          table,
          # widgets.Button('Pick', id='pick',),
          # widgets.Label(''),
      )
      yield widgets.Footer()

  def on_mount(self) -> None:
    self._populate_table()

  def _populate_table(self) -> None:
    table = self.query_one(widgets.DataTable)
    for header in self._headers:
      table.add_column(header, key=header)
    table.add_rows(self._rows)
    table.cursor_type = 'row'

  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.dark = not self.dark

  def action_pick_random(self) -> None:
    picked_item = pick_random(self._data)
    picked_name = picked_item['name']
    picked_index = picked_item[dummy_data.ID_KEY]
    
    table = self.query_one(widgets.DataTable)
    table.move_cursor(row=picked_index)
    table.cursor_type = 'row'

  def action_exit(self) -> None:
    exit(0)

  def on_data_table_row_selected(self, event: widgets.DataTable.RowSelected) -> None:
    table = self.query_one(widgets.DataTable)
    id = table.get_cell(event.row_key, 'id')
    self._mode, output = clickup.get_subentity(self._mode, id)
    table.clear(columns=True)
    self.reload_data(output)
    

  def on_button_pressed(self, event: widgets.Button.Pressed) -> None:
    """Event handler called when a button is pressed."""
    # button_id = event.button.id
    self.action_pick_random()

    # label = self.query_one(widgets.Label)
    # label.update(picked_name)

if __name__ == "__main__":
    app = DoWattApp()
    app.run()
