
import re
import os
import csv  # Store backlinks in a csv file.

data_directory = './data/'

class WikiBacklinks:
    def __init__(self,data_path):
        self.backlinks = dict()
        self.backlink_filename = 'backlinks.dat'
        self.data_path = data_path
        self.full_filename = '{0}{1}'.format(self.data_path,self.backlink_filename)
        self.load_backlinks()

    def load_backlinks(self):
        print "Loading Backlinks..."
        if os.path.isfile(self.full_filename):
            fh = open('{0}{1}'.format(self.data_path,self.backlink_filename),'rb')
            reader = csv.reader(fh)
            for row in reader:

                # field 0 is the page name. Successive fields are the pages which backlink to that page
                self.backlinks[row[0]] = list(row[1:])
            fh.close()

    def add_backlink(self,linkto,linkfrom):
        froms = list()

        if linkto in self.backlinks.keys():
            froms = self.backlinks[linkto]

        if linkfrom not in froms:
            froms.append(linkfrom)
            self.backlinks[linkto] = froms

    def get_backlinks(self,linkto):
        return self.backlinks[linkto]

    def save_backlinks(self):
        fh = open('{0}{1}'.format(self.data_path, self.backlink_filename), 'wb')
        print "Saving backlinks:"
        writer = csv.writer(fh)
        for key in self.backlinks.keys():
            row = list()
            row.append(key)

            for link in self.backlinks[key]:
                row.append(link)
            print row
            writer.writerow(row)
        fh.close()
        print "Saved Backlinks"

    def old_save_backlinks(self):
        fh = open('{0}{1}'.format(self.data_path, self.backlink_filename), 'wb')
        print "Saving backlinks:"
        writer = csv.writer(fh)
        for key in self.backlinks.keys():

            row = list()
            row.append(key)

            for link in self.backlinks[key]:
                row.append(link)
            print row
            writer.writerow(row)
        fh.close()
        print "Saved Backlinks"

    def process_pagelinks(self,pagename,pagelist):
        for page in pagelist:
            self.add_backlink(page,pagename)
        print self.backlinks
        self.save_backlinks()

backlinks = WikiBacklinks(data_directory)

def load_file(filename):
    fh= open(filename,'r')
    return fh.read()

def save_file(filename,content):
    fh=open(filename,'w')
    fh.write(content)
    fh.close()

def is_wikiword(candidate):
    wikiword = re.compile('^\W*([A-Z][a-z]+){2,}\W*$')
    return wikiword.match(candidate) is not None

def render_word(word):
    content = word
    if is_wikiword(word):
        if page_exists(word):
            content = '<a href="/wiki/{0}">{0}</a>'.format(word)
        else:
            content = '<a href="/wiki/edit/{0}">?</a>{0}'.format(word)
    return content

def horizontal_rule(line):
    replaced = re.sub('^(\-{4,})','<hr/>',line)
    return replaced

def render_line(line):
    # This is where this shit gets squirrelly.

    line = horizontal_rule(line)
    match = re.compile("\w+")
    items = match.findall(line)
    processed = list()
    for item in items:
        if item not in processed:
            line = line.replace(item,render_word(item))
            processed.append(item)
    return line

def html_render(body):

    content = ''
    for line in body.split('\n'):
        content += render_line(line) + "<br/>"
    return content

def get_page(pagename):
    return load_file("{0}{1}.dat".format(data_directory,pagename))

def extract_backlinks(content):
    pages = page_list()
    backlinks = list()
    for pagename in pages:
        if content.find(pagename) != -1:
            backlinks.append(pagename)
    return backlinks

def save_page(pagename,content):
    backlink_list = extract_backlinks(content)
    backlinks.process_pagelinks(pagename,backlink_list)
    return save_file("{0}{1}.dat".format(data_directory,pagename),content)

def page_exists(pagename):
    pages = page_list()
    return (pagename in pages)

def page_list():
    pages = list()
    for filename in os.listdir(data_directory):
        if '.' in filename:
            (name,ext) = filename.split('.')
            if ext == 'dat' and is_wikiword(name):
                pages.append(name)
    return pages

def get_backlinks(pagename):
    return backlinks.get_backlinks(pagename)

def get_all_backlinks():
    # This is a simple serialized version so I can produce a big ol' content body of them.
    content = ''
    for key in backlinks.backlinks:
        content = content + key + ': ' + str(backlinks.backlinks[key]) + '\n'
    return content
    #return str(backlinks.backlinks)

