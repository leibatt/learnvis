class Fscore:
  def __init__(self):
    self.tp = 0;
    self.fp = 0
    self.tn = 0
    self.fn = 0

  def precision(self):
    denom = self.tp + self.fp
    if denom == 0:
      return 0.0
    else:
      return self.tp / denom

  def recall(self):
    denom = self.tp + self.fn
    if denom == 0:
      return 0.0
    else:
      return self.tp / denom

  def f1(self):
    denom = self.precision() + self.recall()
    if denom == 0:
      return 0.0
    else:
      return ((2 * self.precision() * self.recall()) / denom)

  def ingest(self, fscore):
    self.tp += fscore.tp
    self.tn += fscore.tn
    self.fp += fscore.fp
    self.fn += fscore.fn

  def toString(self):
    return "<FScore {tp: %d, fp: %d, tn: %d, fn: %d, p: %f, r: %f, f1: %r" % (
        self.tp, self.fp, self.tn, self.fn, self.precision(), self.recall(), self.f1());
