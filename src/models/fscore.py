class Fscore:
  def __init__(self):
    self.tp = 0
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

  def __repr__(self):
    return "<FScore {tp: %d, fp: %d, tn: %d, fn: %d, p: %f, r: %f, f1: %r" % (
        self.tp, self.fp, self.tn, self.fn, self.precision(), self.recall(), self.f1());

class MulticlassFscore:
  def __init__(self):
    self.labels = {}
    self.finalized = False

  def ensureLabel(self, label):
    if label not in self.labels:
      self.labels[label] = Fscore()

  def registerResult(self, gold, predicted):
    if self.finalized:
      print "Can't register result, already finalized!"
    else:
      self.ensureLabel(gold)
      self.ensureLabel(predicted)
      if gold == predicted:
        self.labels[gold].tp = self.labels[gold].tp + 1
      else:
        self.labels[gold].fn = self.labels[gold].fn + 1
        self.labels[predicted].fp = self.labels[predicted].fp + 1

  # Calculate the true negatives. We can only do this once all true positives
  # are accounted for because we're building up the dataset incrementally.
  def finalize(self):
    if not self.finalized:
      self.finalized = True
      # For each tp in each label, give all other labels a tn
      for label1 in self.labels:
        for label2 in self.labels:
          if label1 != label2:
            self.labels[label2].tn += self.labels[label1].tp

  def ingest(self, other):
    if not self.finalized:
      print "Ingest called, finalizing self"
      self.finalize()
    if not other.finalized:
      print "Ingest called, finalizing other"
      other.finalize()

    for label in other.labels:
      otherFscore = other.labels[label]
      if label in self.labels:
        self.labels[label].ingest(otherFscore)
      else:
        self.labels[label] = otherFscore

  def __repr__(self):
    ret = [] 
    for label in self.labels:
      ret.append("%s:%s" % (label, repr(self.labels[label])))
    return "\n".join(ret)


