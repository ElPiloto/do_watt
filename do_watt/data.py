"""This is a placeholder for when we get real data."""
ID_KEY = '__ID__'


def add_id_inplace(x: list[dict]) -> list[dict]:
  """Adds integer id key."""
  for i, d in enumerate(x):
    d[ID_KEY] = i
  return x


activities = add_id_inplace([
    dict(name='Veg out', type='', tags=[], minimum_duration_mins=100),
    dict(name='Movie Night', type='', tags=[], minimum_duration_mins=150),
    dict(name='Family Meeting', type='', tags=[], minimum_duration_mins=60),
    dict(name='Video Games', type='', tags=[], minimum_duration_mins=30),
    dict(name='Tech Hobby', type='', tags=[], minimum_duration_mins=120),
])

