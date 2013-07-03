# eob note: Sorry for my verbose python. I'm rusty after not using it for a while...

# ==================================
# 1. Individual predicate functions
#
#  Each takes a data point as input and returns a list of strings (or empty list)
#  as output
# ==================================

def alwaysPotato(x):
  return ["potato"]

# ==================================
# 2. Inst of predicate functions application
# ==================================

FEATURE_FUNCS = [
    alwaysPotato
]

# ==================================
# 3. Feature generation loop for a single data point
# ==================================

def featuresFor(x):
  all_features = []
  for f in FEATURE_FUNCS:
    these_features = f(x)
    for feature in these_features:
      all_features.append(feature)
  return all_features

# ==================================
# 4. EXAMPLE USAGE
# ==================================

if __name__ == "__main__":
  x = {
      "name": "Pretend datapoint"
  }

  features = featuresFor(x)
  print features
