import numpy as np
import datetime as dt #datetime.strptime(date_string, format)

date_range_min = 5

def get_features_new(visdataobj,include=['a','g','p','s','c']):
    raw_data = visdataobj.raw_data
    features = []

    a = range(visdataobj.total_columns)
    g = visdataobj.groupings
    p = visdataobj.positions
    s = visdataobj.size
    c = visdataobj.color

    #print "**********c:",c
    mvs = get_mean_skew_and_std
    #    'mean':[max_mean,min_mean,1.0*avg_mean/l],
    #    'std':[max_std,min_std,1.0*avg_std/l],
    #    'skew':[max_skew,min_skew,1.0*avg_skew/l]}
    cov_corr = get_covariance_and_correlation_features
    #return {'covariance':[np.sum(covariance) * .5 / n,np.sum(np.absolute(covariance))*.5/n,np.max(np.absolute(covariance)),np.min(np.absolute(covariance))],
    fnumcols = get_fraction_num_cols
    #return fraction / len(index_list)
    unique_vals = get_unique_values
    #return {'all_counts':un,'max_count':max(un),'min_count':min(un),'avg_count':np.mean(un)}
    has_date = get_has_date
    #return 1.0

    prevcount = 0
    currcount = 0
    #all columns: skew, correlation, fraction numeric cols, fraction unique vals
    if 'a' in include:
        features.append(has_date(raw_data,index_list=a)) # 1
        features.extend(mvs(raw_data,index_list=a)['skew']) # 2 - 4
        features.extend(cov_corr(raw_data,index_list=a)['covariance']) # 5 - 8
        features.extend(cov_corr(raw_data,index_list=a)['correlation']) # 9 - 12
        features.append(fnumcols(raw_data,index_list=a)) # 13
        for k,v in unique_vals(raw_data,index_list=a).items(): # 14 - 16
            if k in ['max_count','min_count','avg_count']:
                features.append(v)
    currcount = len(features)
    print "total a features:",currcount
    print "current count of features:",currcount
    # g: skew, variance, mean, correlation, has time column, fraction numeric cols, fraction unique vals
    if 'g' in include:
        features.append(has_date(raw_data,index_list=g)) # 1
        for k,v in mvs(raw_data,index_list=g).items(): # 2-4, 5-7, 8-10
            features.extend(v)
        features.extend(cov_corr(raw_data,index_list=g)['covariance']) # 11 - 14
        features.extend(cov_corr(raw_data,index_list=g)['correlation']) # 15 - 18
        features.append(fnumcols(raw_data,index_list=g)) # 19
        for k,v in unique_vals(raw_data,index_list=g).items(): # 20 - 22
            if k in ['max_count','min_count','avg_count']:
                features.append(v)

    prevcount = currcount
    currcount = len(features)
    print "total g features:",currcount-prevcount
    print "current count of features:",currcount

    # p: skew, variance, mean, correlation, has time column, fraction numeric cols, fraction unique vals
    if 'p' in include:
        features.append(has_date(raw_data,index_list=p)) # 1
        for k,v in mvs(raw_data,index_list=p).items(): # 2-4,5-7,8-10
            features.extend(v)
        features.extend(cov_corr(raw_data,index_list=p)['covariance']) # 11-14
        features.extend(cov_corr(raw_data,index_list=p)['correlation']) # 15 - 18
        features.append(fnumcols(raw_data,index_list=p)) # 19
        for k,v in unique_vals(raw_data,index_list=p).items(): # 20 - 22
            if k in ['max_count','min_count','avg_count']:
                features.append(v)

    prevcount = currcount
    currcount = len(features)
    print "total p features:",currcount-prevcount
    print "current count of features:",currcount

    # s: skew, variance, mean 
    if 's' in include:
        for k,v in mvs(raw_data,index_list=s).items():
            features.append(v[0])

    prevcount = currcount
    currcount = len(features)
    print "total s features:",currcount-prevcount
    print "current count of features:",currcount

    # c: skew, variance, mean 
    if 'c' in include:
        for k,v in mvs(raw_data,index_list=c).items():
            features.append(v[0])

    prevcount = currcount
    currcount = len(features)
    print "total c features:",currcount-prevcount
    print "current count of features:",currcount

    ### get density (all cols, ints only, all nums+dates)
    # skew (all,'g','p') * (max,min,avg)
    # skew ('s','c')
    # variance ('g','p') * (max,min,avg)
    # variance ('s','c')
    # mean ('g','p') * (max,min,avg)
    # mean ('s','c')
    ### covariance (all,'p') * (avg, avg magnitude, max magnitude)
    # correlation (all,'p') * (avg, avg magnitude, max magnitude)
    # has time column (all,'g','p')
    # % num cols (all, 'g', 'p')
    ### overlapping points (all,'g','p') * (max, min, avg)
    # unique values/row length (all,'g','p') * (max, min, avg)
    print "total features recorded:",len(features)
    return features

def get_features(raw_data,indexes=[1,3,4]):
    features ={}
    densities = get_density(raw_data,index_list=indexes)
    cov_corr = get_covariance_and_correlation_features(raw_data,index_list=indexes)
    label_counts = get_unique_labels(raw_data,index_list=indexes)
    mvs = get_mean_skew_and_std(raw_data,index_list=indexes)
    features['unique_values'] = get_unique_values(raw_data,index_list=indexes)
    features['mean/std/skew'] = mvs
    features['overlap'] = overlapping_points(raw_data,index_list=indexes)#[2,3,4])
    features['density'] = densities[0]
    features['density_minus_one'] = densities[1]
    features['density_all_nums'] = densities[2]
    features['density_strict'] = densities[3]
    features['fnumcols'] = get_fraction_num_cols(raw_data,index_list=indexes)
    features['hasdate'] = get_has_date(raw_data,index_list=indexes)
    features['avg_covariance'] = cov_corr['covariance'][0]
    features['avg_abs_covariance'] = cov_corr['covariance'][1]
    features['max_abs_covariance'] = cov_corr['covariance'][2]
    features['avg_correlation'] = cov_corr['correlation'][0]
    features['avg_abs_correlation'] = cov_corr['correlation'][1]
    features['max_abs_correlation'] = cov_corr['correlation'][2]
    features['total_unique_labels'] = label_counts['unique_labels'][0]
    features['first_unique_labels'] = label_counts['unique_labels'][1]
    return features

'''
finds count of unique values
'''
def get_unique_values(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)
    un = []
    for i,col in enumerate(raw_data):
        if i in index_list:
             un.append(np.unique(col).size * 1.0 / col.size)
        else:
            un.append(0)
    return {'all_counts':un,'max_count':max(un),'min_count':min(un),'avg_count':np.mean(un)}
 
'''
finds overlapping points, includes duplicates
'''
def overlapping_points(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)
    overlap = []
    for i,col in enumerate(raw_data):
        if i in index_list:
             nu = np.unique(col).size
             overlap.append((col.size - nu) * 1.0 / col.size)
        else:
            overlap.append(0)
    return {'all_overlaps':overlap,'max_overlap':max(overlap),'min_overlap':min(overlap),'avg_overlap':np.mean(overlap)}
    

'''
find overlap, ignoring duplicates
'''
def overlapping_points_no_duplicates(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    overlap = []
    for i in range(numcols):
        overlap.append(0)

    for i in range(numcols):
        if i in index_list:
            to_sort = []
            # last sorted first
            for ts in reversed(range(numcols)):
                if not ts == i and ts in index_list:
                    if raw_data[i].dtype == np.datetime64:
                        to_sort.append(raw_data[ts].astype(np.int64))
                    else:
                        to_sort.append(raw_data[ts])
            to_sort.append(raw_data[i]) # primary sort key
            ind = np.lexsort(tuple(to_sort))
            #print ind
            o = 0
            for j in range(1,len(ind)):
                #print "i:",i,",j:",j
                if raw_data[i][ind[j]] == raw_data[i][ind[j-1]]: # overlap in dimension i between
                    for k in range(numcols):
                        if k in index_list and not i == k:
                            if not raw_data[k][ind[j]] == raw_data[k][ind[j-1]]:
                                o =o + 1 # found overlap
                                break
            overlap[i] = o * 1.0 / len(ind) # scale according to length of column
    return {'all_overlaps':overlap,'max_overlap':max(overlap),'min_overlap':min(overlap)}

def is_dtype_string(col):
    returnval = str(col.dtype)[:2] == '|S'
    if not returnval:
        try:
            len(col[0])
            return True
        except:
            return False
    return True

def get_unique_labels(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    first = True
    first_range = 0
    total_range = 0
    avg_range = 0
    num_str_cols = 0
    for i,col in enumerate(raw_data):
        if i in index_list and is_dtype_string(col):
            r = get_range(col)
            if total_range == 0:
                total_range = r
                avg_range = r
            else:
                total_range = total_range * r
                avg_range = avg_range + r
            if first:
                first_range = r
                first = False
    if num_str_cols > 0:
        avg_range = avg_range * 1.0 / num_str_cols
    return {'unique_labels':[total_range,first_range,avg_range], 'num_str_cols':num_str_cols}

def get_covariance_and_correlation_features(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    samples = None
    nsamples = 0
    for i,col in enumerate(raw_data):
        if i in index_list and col.dtype in [np.int64,np.float64,np.datetime64]:
            old_shape = col.shape
            col.shape = (1,col.size)
            if samples is None:
                samples = col.astype(np.float64)
            else:
                samples = np.concatenate((samples,col.astype(np.float64)),axis=0)
            nsamples = nsamples + 1
            col.shape = old_shape
    #print "samples:",samples,",shape:",samples.shape
    if samples is not None and samples.shape[0] > 1:
        covariance = np.cov(samples)
        correlation = np.corrcoef(samples)
        np.fill_diagonal(covariance,0)
        np.fill_diagonal(correlation,0)
        #print "covariance:",covariance
        #print "correlation:",correlation
        n = (1.0 * nsamples * nsamples - nsamples) / 2
        return {'covariance':[np.sum(covariance) * .5 / n,np.sum(np.absolute(covariance))*.5/n,np.max(np.absolute(covariance)),np.min(np.absolute(covariance))],
            'correlation':[np.sum(correlation)*.5/n,np.sum(np.absolute(correlation))*.5/n,np.max(np.absolute(correlation)),np.min(np.absolute(correlation))]}
    else:
        return {'covariance':[0,0,0,0],'correlation':[0,0,0,0]}

def get_has_date(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)
    for i,col in enumerate(raw_data):
        if i in index_list and col.dtype == np.datetime64:
            return 1.0
    else:
        return 0.0

def get_total_cols(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    return len(index_list)

def get_mean_skew_and_std(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    max_mean = 0
    min_mean = 0
    avg_mean = 0

    max_std= 0
    min_std = 0
    avg_std = 0

    max_skew = 0
    min_skew = 0
    avg_skew = 0
    l = len(raw_data[0])
    for i,col in enumerate(raw_data):
        if i in index_list and col.dtype in [np.float64,np.int64,np.datetime64]:
            c = col.astype(np.float64) 
            #print "orig c:",c
            cmax = np.max(c)
            cmin = np.min(c)
            cdiff = cmax - cmin
            s = 0
            m = 0
            skew = 0
            if not cdiff == 0:
                c = (c - cmin) / cdiff # map to 0 - 1 range
                #print "c:",c,",cdiff:",cdiff
                m = np.mean(c) # between 0 and 1
                s = np.std(c) # between 0 and 1?
                skew = 2 * np.absolute(.5 - m) # definitely between 0 and 1
            max_mean = max(max_mean,m)
            min_mean = min(min_mean,m)
            avg_mean = avg_mean + m

            max_std = max(max_std,s)
            min_std = min(min_std,s)
            avg_std = avg_std + s

            max_skew = max(max_skew,skew)
            min_skew = max(min_skew,skew)
            avg_skew = avg_skew + skew

    return {'mean':[max_mean,min_mean,1.0*avg_mean/l],
        'std':[max_std,min_std,1.0*avg_std/l],
        'skew':[max_skew,min_skew,1.0*avg_skew/l]}

def get_fraction_num_cols(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    fraction = 0.0
    for i,col in enumerate(raw_data):
        if i in index_list and col.dtype in [np.int64,np.float64]:
            fraction = fraction + 1
    if len(index_list) > 0:
       fraction = fraction / len(index_list)
    return fraction

'''
return total data points/array size
'''
def get_density(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    # divide length of column 0 by array size
    sizes = get_array_size(raw_data,index_list)
    count = raw_data[0].size
    #print "size:",sizes[0],",",sizes[1]
    return [count/ sizes[0],count/sizes[1],count/sizes[2],count/sizes[3]]
    
def get_array_size(raw_data,index_list=None):
    numcols = len(raw_data)
    if index_list is None:
        index_list = range(numcols)

    size_all = 1.0 # all columns are dims
    size_all_1 = 1.0 # all but last column are dims
    size_strict = 1.0 # only int columns are dims
    size_all_nums = 1.0 # only number cols are dims

    last = None
    for i,col in enumerate(raw_data):
        if i in index_list:
            r = get_range(col)
            size_all = size_all * r
            if col.dtype == np.int64:
                size_strict = size_strict * r
                size_all_nums = size_all_nums * r
            elif col.dtype == np.float64:
                size_all_nums = size_all_nums * r
            last = r
    size_strict = max(size_strict,raw_data[0].size)
    size_all_1 = size_all / last
    return [size_all,size_all_1,size_all_nums,size_strict]

def get_range(col):
    if col.dtype == np.int64: # ints
        returnval = np.max(col) - np.min(col)
    elif col.dtype == np.float64: # floats
        returnval = np.unique(col).size # each float maps to it's own dimension index
    elif col.dtype == np.datetime64: # checks for granularity (years,months,days,etc.)
        returnval = get_date_range(col)
    else: # assume string, look for all unique strings
        returnval = np.unique(col).size
    return max(returnval,1)

def get_date_range(col):
    r = 1
    diff = np.max(col) - np.min(col)
    days = diff.item().days
    seconds = diff.item().seconds
    daychecks = [365,30,1]
    secondchecks = [3600,60,1]
    for check in daychecks:
        r = days / check
        if r >= date_range_min:
            break
    else:
        for check in secondchecks:
            r = days * 24 + seconds / check
            if r >= date_range_min:
                break
        else:
            r = 1
    # check for days
    # check for hours
    # check for seconds
    return r

