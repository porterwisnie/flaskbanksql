
def html_table(lol):
  yield '<table cellspacing="10">'
  for sublist in lol:
    yield '  <tr><td>'
    yield '    </td><td>'.join(sublist)
    yield '  </td></tr>'
  yield '</table>'

def convert(x):

    return '\n'.join(list(html_table(x)))
