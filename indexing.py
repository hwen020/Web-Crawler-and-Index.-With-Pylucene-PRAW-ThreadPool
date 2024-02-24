import logging, sys
import json
logging.disable(sys.maxsize)
import time

import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    start = time.perf_counter_ns()
    timelist = []
    count = 0
    for post in postlist:
        
        #title = post['title']
        url = post['url']
        context = post['title'] +"\n"+ post['selftext']

        doc = Document()
        #doc.add(Field('Title', str(title), metaType))
        doc.add(Field('Context', str(context), contextType))
        doc.add(Field('Url',str(url), metaType))
        writer.addDocument(doc)
        count += 1
        timenow = time.perf_counter_ns() - start
        timelist.append(timenow)
    writer.close()
    return timelist


def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Context', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        docdict = {}
        for field in doc.getFields():
            docdict[field.name()] = doc.get(field.name())
        topkdocs.append({
            "score": hit.score,
            "text": docdict
        })
    
    print(topkdocs)

# read every json file in target dir
# return the list of all json data in the dir
def readdir(storedir):
    datalist = []
    namelist = os.listdir(storedir)
    for jsonname in namelist:
        if os.path.splitext(jsonname)[1] == ".json":
            with open(storedir+"/"+jsonname, "r", encoding="utf-8") as fr:
                try:
                    jsondata = json.load(fr)
                except:
                    jsondata = []
                datalist.extend(jsondata)
    return datalist

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
postlist = readdir("RedditData")
timecount = create_index('IndexFolder/')
with open("timecount.txt", 'w', encoding='utf-8',newline='\n') as fw:
    for times in timecount:
        fw.write(str(times)+"\n")
    fw.close()
#retrieve('IndexFolder/', 'school')



