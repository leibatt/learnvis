
class VisData():
    def __init__(self, raw_data,column_names, indexes, source, url,location,label):
        self.raw_data = raw_data
        self.features = None
        self.groupings = indexes['g']
        self.positions = indexes['p']
        self.size = indexes['s'][:1]
        self.color = indexes['c'][:1] # assume only one of each
        self.url = url
        self.source = source
        self.column_names = column_names
        self.total_columns = len(column_names)
        self.location = location
        self.label = label
        
    def update_features(features):
        self.features = features

    def __repr__(self):
        return "VisData(%r,(%r),(%r))" % (self.source,",".join(self.column_names),",".join(self.features) if self.features is not None else None)

