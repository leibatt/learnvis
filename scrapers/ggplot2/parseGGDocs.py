# This file iterates through the ggplot2 R source files and extracts the example code from the comments
# ggplot2's code is what generates the docs.ggplot2.org page so there should be lots of examples
import os


def parse(fname):
  '''
  ggplot2's source file comments are of the form

  #' @examples
  #' \noTest{
  #' <example code>
  #' }
  '''
  is_comment = lambda l: l.startswith('#\'')
  skip = lambda l: l.startswith('\\') or l == '}'
  is_example = False
  example_lines = []

  with file(fname, 'r') as f:
    for l in f:
      l = l.strip()
      if not is_comment(l): 
        is_example = False
        continue

      l = l[2:].strip()
      if l == "@examples":
        is_example = True
      elif is_example:
        if l.startswith('@'):
          is_example = False
          continue
        if skip(l): continue
        example_lines.append(l)
  return example_lines




if __name__ == "__file__":
  if len(sys.argv) <= 1:
    print "python parseGGDocs.py <ggplot R files directory>"
    exit(0)

  directory = sys.argv[1]#"/Users/sirrice/code/R/ggplot2/R"

  codes = {}
  for fname in os.listdir(directory):
    if fname.lower().endswith('r'):
      lines = parse('%s/%s' % (directory,fname))
      code = "\n".join(lines)
      if 'ggplot' in code or 'qplot' in code:
        codes[fname] = code

  print json.dumps(codes)
