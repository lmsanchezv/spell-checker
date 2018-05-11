#!/usr/bin/python
import sys,string,re,os
import multiprocessing as mp


url_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
INPUT_FILE = "datos_original_mitad.txt"
OUTPUT_FILE = "output5.txt"
matches = []
counter = 0
modifiedWords = []

def process_match(m):
    matches.append(m.group(0))
    return '{{URL}}'

def process(line):
    global counter,modifiedWords
    #print ' '.join([str(x) for x in modifiedWords])
    print counter
    try:
        counter += 1
        if counter % 500 == 0:
            print str(counter)
        cleanedLine = line.strip()   
        cleanedLine = url_regex.sub(process_match, cleanedLine)

        words = cleanedLine.split()
        for r, word in enumerate(words):
            if r == 0:
                modifiedWords = (modifiedWords + ['<s> '])
            word = word.translate(string.maketrans("",""), string.punctuation).lower()
            modifiedWords = modifiedWords + [word + ' ']
        modifiedWords = (modifiedWords + ['</s>'] + ['\n'])
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to be printed directly

def process_wrapper(chunkStart, chunkSize):
    with open(INPUT_FILE) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            print "Processing %s" % (line)
            process(line)
        with open(OUTPUT_FILE, 'a') as f:
            for line in modifiedWords:
                f.write(line)

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

def stringManipulation(file):
    file = open(file)
    counter = 0
    modifiedWords = []
    for line in file.readlines():
        try:
            counter += 1
            if counter % 500 == 0:
                print str(counter)

            cleanedLine = line.strip()
            
            cleanedLine = url_regex.sub(process_match, cleanedLine)

            words = cleanedLine.split()
            for r, word in enumerate(words):
                if r == 0:
                    modifiedWords = (modifiedWords + ['<s> '])
                word = word.translate(string.maketrans("",""), string.punctuation).lower()
                modifiedWords = modifiedWords + [word + ' ']
            modifiedWords = (modifiedWords + ['</s>'] + ['\n'])
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
    with open(OUTPUT_FILE, 'w') as f:
        for line in modifiedWords:
            f.write(line)
    return OUTPUT_FILE

def readFile(file):
    file = open(file)
    for line in file.readlines():
        line = line.strip()
        print line

def processFileMultipleJobs():
    print "================="
    print "Process Started"
    #init objects
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    jobs = []
    #create jobs
    for chunkStart,chunkSize in chunkify(INPUT_FILE):
        jobs.append(pool.apply_async(process_wrapper,(chunkStart,chunkSize)))

    #wait for all jobs to finish
    for job in jobs:
        job.get()
    print "================="
    print "Process Completed"
    pool.close()

if __name__ == '__main__':
    processFileMultipleJobs()
    #readFile(stringManipulation(INPUT_FILE))