import urllib2
import re
import string
import time

# jared chandler
# chandler@eecs.tufts.edu
# march 22, 2013


thumbnailpath = 'thumbnails/'  #The dir we store the thumbnail in
imagepagepath = 'imagepages/'  #The dir we store the HTML page we get when requesting the large image of the vis
imagepath = 'images/'          #The dir we store the image in 
rawpagepath = 'rawpages/'      #The dir we store the raw HTML page for the vis
rawdatapath = 'rawdatapages/'  #The dir we store the intermediate page to the raw data
rawfinalpath = 'rawfinaldatapages/' #The actual raw data
metapath = 'metadata/'  #Where we write our visualization metadata
indexpath = 'indexpages/'   #Where we store the intermediate html pages from the crawl 

baseurl = 'http://www-958.ibm.com'


f=open('log.txt','a')
f.write('\t'.join([string.strip(field) for field in ["uid","vistype","title","up","down","tags","url","dataseturl","datasettitle","rawdataurl","time"]])+'\n')
f.close()

#get the little image
def fetchThumbnail(url,uid):
    req = urllib2.Request(baseurl+url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    f = open(thumbnailpath+uid+'.png','wb')
    f.write(the_page)
    f.close()

#get the big image (if it has one)
def fetchImage(url,uid):
    req = urllib2.Request(baseurl+url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    f = open(imagepath+uid+'.png','wb')
    f.write(the_page)
    f.close()

#get an html page
def fetchPage(path,url,uid):    
    req = urllib2.Request(baseurl+url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    f = open(path+uid+'.txt','w')
    f.write(the_page)
    f.close()
    return the_page

#only do the first 5 pages of many-eyes
for pnum in range(1,5):

    #get the page
    data = fetchPage(indexpath,"/software/data/cognos/manyeyes/visualizations?page="+str(pnum)+"&sort=rating",'index'+str(pnum))

    #find all the visualizations on the page
    res = re.findall("<td class='thumbnailCell'>(.*?)</td>",data,flags=re.DOTALL|re.MULTILINE)
    for r in res:

        #get each vis
        try:
         
            print r
            thumbnail_url = re.findall("src='(.*?)'",r,flags=re.DOTALL|re.MULTILINE)[0]
            print "thumbnail_url\t",thumbnail_url
            filename = thumbnail_url.split('/')[-1].split('?')[0]
            uid = filename.split('.')[0]
            print "uid\t",uid
            print "filename\t",filename
            url = re.findall("href='(.*?)'",r,flags=re.DOTALL|re.MULTILINE)[0]
            print "url\t",url
            tags = re.findall('alt="(.*?)"',r,flags=re.DOTALL|re.MULTILINE)[0]
            title = string.strip(re.findall("<div class='footerline'>.*?</div>(.*?)</a>",r,flags=re.DOTALL|re.MULTILINE)[0])
            print "tags\t",tags
            print "title\t",string.strip(title)

         

            
            fetchThumbnail(thumbnail_url,uid)

            page = fetchPage(rawpagepath,url,uid)
            
            img = re.findall('"/software/data/cognos/manyeyes/vis/FullScreen/fullscreenvisualization.html(.*?)" class="clickable"',page,flags=re.DOTALL|re.MULTILINE)[0]
            print img
            img = "/software/data/cognos/manyeyes/vis/FullScreen/fullscreenvisualization.html" + img
            print img

            
            imgpage = fetchPage(imagepagepath,img,uid)
            img_url = re.findall("src='(.*?)'",imgpage,flags=re.DOTALL|re.MULTILINE)[0]

            fetchImage(img_url,uid)
            
            vistype= re.findall("<a href='/software/data/cognos/manyeyes/page/(.*?)'>.*?<img alt='Thumbnail",page,flags=re.DOTALL|re.MULTILINE)[0]
            vistype = vistype.split('.')[0]
            print "vistype\t",vistype

            up = string.strip(re.findall("<span class='ratedUp'>(.*?)positive",page,flags=re.DOTALL|re.MULTILINE)[0])
            down = string.strip(re.findall("<span class='ratedDown'>(.*?)negative",page,flags=re.DOTALL|re.MULTILINE)[0])

            dataset = re.findall('<img alt="Dataset".*?<a href="/software/data/cognos/manyeyes/datasets/(.*?)">(.*?)</a>',page,flags=re.DOTALL|re.MULTILINE)[0]
            dataset_url = "/software/data/cognos/manyeyes/datasets/"+dataset[0]
            dataset_title = dataset[1]
            print dataset_url,dataset_title
            #<a href="/software/data/cognos/manyeyes/datasets/89ade5ae104fee3a011052036ae202fe/versions/1" tabindex="0">Disney Princess vs. Mueslix</a>


            datasetpage = fetchPage(rawdatapath,dataset_url,uid)

            #<button class="mainBtn" onclick="location.href='/software/data/cognos/manyeyes/datasets/disney-princess-vs-mueslix/versions/1.txt'" value="submit">
            rawdata_url =re.findall("location.href='(.*?)'",datasetpage,flags=re.DOTALL|re.MULTILINE)[0]
            print rawdata_url

            rawdatapage = fetchPage(rawfinalpath,rawdata_url,uid)

            f=open(metapath+uid+'.txt','w')
            f.write('\n'.join([string.strip(field) for field in ["uid\t"+uid,"vistype\t"+vistype,"title\t"+title,"up\t"+up,"down\t"+down,"tags\t"+tags,"url\t"+baseurl+url,"dataseturl\t"+baseurl+dataset_url,"datasettitle\t"+dataset_title,
                                                                 "rawdataurl\t"+baseurl+rawdata_url,"time\t"+str(time.time())]]))
            f.close()

            f=open('log.txt','a')
            f.write('\t'.join([string.strip(field) for field in [uid,vistype,title,up,down,tags,baseurl+url,baseurl+dataset_url,dataset_title,baseurl+rawdata_url,str(time.time())]])+'\n')
            f.close()
        except:
            print('error')
        time.sleep(2)


