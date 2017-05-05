# -*- coding: utf-8 -*-
import os
from shutil import copyfile
import copy
import yaml
import markdown
from docdata.mmddata import get_data
import jinja2
import json
from bs4 import BeautifulSoup
from collections import OrderedDict


def check_mkdir(outpath):
    directory = os.path.dirname(outpath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def text_export(outputText, outputPath):
    check_mkdir(outputPath)
    f = open(outputPath, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()

def copy_directories(static_path_in, static_path_out):
    for dirName, subdirList, fileList in os.walk(static_path_in):
        for fname in fileList:
            inf = os.path.join(dirName,fname)
            relf = os.path.relpath(inf, static_path_in)
            outf = os.path.join(static_path_out, relf)
            check_mkdir(outf)
            copyfile(inf, outf)


class wiki():
    def __init__(self, mpath):
        #, output_dir='html', template_dir='template', static_dir='static'):
        config = self.get_config(mpath)
        self.config = config

        if not(os.path.isabs(mpath)):
            mpath = os.path.abspath(mpath)
        self.mpath = mpath

        if 'base_url' in config:
            self.base_url = config['base_url']
        else:
            self.base_url = ''
        self.pageDir = os.path.join(mpath, config['page_dir'])
        self.rootDir = os.path.join(mpath, config['wiki_dir'])
        self.export_path = os.path.join(mpath,  config['output_dir'], self.base_url)
        self.mdlist_wiki, self.exlist_wiki = self.get_docpath()
        self.mdlist_page, self.exlist_page = self.get_pagepath()

        static_path_out = os.path.join(self.export_path, 'static')
        self.static_path_out = static_path_out
        for d in config['static_dir']:
            static_path_in = os.path.join(mpath, d)
            copy_directories(static_path_in, static_path_out)

        """
        plugin_path_in = os.path.join(mpath, config['plugin_dir'])
        plugin_path_out = os.path.join(self.export_path, config['plugin_dir'])
        self.copy_statics(plugin_path_in, plugin_path_out)
        """

        self.template_dir = config['template_dir']
        self.static_dir = config['static_dir']
        self.process_docs()

        if self.config['generate_listing']:
            self.get_listing()

    def get_config(self, mpath):
        configf = os.path.join(mpath, 'config.yaml')
        default_config = dict(output_dir='html', wiki_dir='wiki', template_dir='template', static_dir='static', base_url='/', plugin_dir='plugins')
        if not(os.path.exists(configf)):
            config = default_config
        else:
            with open(configf, 'r') as f:
                cf = f.read()
            config = yaml.load(cf)
            for k,v in default_config.iteritems():
                if k not in config:
                    config[k] = v
        return config

    def get_docpath(self):
        rootDir = self.rootDir
        export_path = self.export_path

        mdlist = []
        exlist = []
        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                mdf = os.path.join(dirName,fname)
                mdlist.append(mdf)
                exloc = os.path.join(export_path, 'docs', os.path.relpath(mdf, rootDir).replace('.md', '.html'))
                exlist.append(exloc)
        return mdlist,exlist

    def get_pagepath(self):
        rootDir = self.pageDir
        export_path = self.export_path

        mdlist = []
        exlist = []
        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                mdf = os.path.join(dirName,fname)
                mdlist.append(mdf)
                exloc = os.path.join(export_path, os.path.relpath(mdf, rootDir).replace('.md', '.html'))
                exlist.append(exloc)
        return mdlist,exlist


    def process_docs(self):
        mpath = self.mpath
        template_dir = self.template_dir
        template_path = os.path.join(mpath, template_dir)
        self.templateLoader = jinja2.FileSystemLoader( searchpath=template_path )
        docs = []
        pages = []
        for m,e in zip(self.mdlist_page, self.exlist_page):
            d = doc(m,e, self)
            docs.append(d)
            pages.append(d)
        #self.pages_doc = pages

        pages_tuple = []
        ind = ()
        for p in pages:
            t = p.title
            u = p.rel
            u = '/'+u
            if not(u=='/index.html'):
                pages_tuple.append((t,u))
            else:
                ind = (t,u)
        pages_tuple = sorted(pages_tuple)
        pages_tuple.insert(0,ind)
        render_update = dict(pages=pages_tuple)

        for m,e in zip(self.mdlist_wiki, self.exlist_wiki):
            d = doc(m,e, self)
            docs.append(d)

        tipues = []
        for d in docs:
            d.render(render_update)
            tips = d.get_tip()
            tipues.append(tips)

        self.gather_tipuejs(tipues)

        tipuejs_path = 'plugins/tipuesearch'
        copy_directories(tipuejs_path, self.static_path_out)

        if 'wiki_name' in self.config:
            wn = self.config['wiki_name']
        else:
            wn = '-'
        static_dir = '../static'
        #web_relroot = '../'
        search_dic = dict(wiki_name=wn, static_dir=static_dir, title='Search result')
        templateEnv = jinja2.Environment( loader=self.templateLoader )
        TEMPLATE_FILE = "search.html"
        template = templateEnv.get_template( TEMPLATE_FILE )
        outputText = template.render( search_dic )
        searchfileloc = os.path.join(self.export_path, 'tipuesearch', 'search.html')
        text_export(outputText, searchfileloc)

    def gather_tipuejs(self, tipues):
        tipuedic = dict(pages=tipues)
        #print tipuedic
        tjson = json.dumps(tipuedic)#, indent=4, sort_keys=False)
        #print tjson
        tjs = 'var tipuesearch = '+tjson +';'

        outpath = os.path.join(self.export_path, 'tipuesearch', 'tipuesearch_content.js')
        text_export(tjs, outpath)

    def get_listing(self):
        export_path = os.path.join(self.export_path)
        exclude = set(['static', 'tipuesearch'])

        dirs = []
        for dirName, subdirList, fileList in os.walk(export_path, topdown=True):
            subdirList[:] = [d for d in subdirList if d not in exclude]
            name = os.path.relpath(dirName, export_path)
            items = (sorted(subdirList), sorted(fileList))
            dirs.append((name, items))

        for name, items in dirs:
            dirs, docs = items
            if name=='.':
                name = ''
            else:
                name = name + '/'

            liststr = ''
            lsn = self.config['listing_filename']
            if len(name)>0:
                d = '..'
                liststr = '  <li><a href="%s/%s">%s/</a></li>\n'%(d,lsn,d)

            if len(dirs)>0:
                ml = ''
                for d in dirs:
                    ml = ml + '  <li><a href="%s/%s">%s/</a></li>\n'%(d,lsn,d)
                #ml = '<ul>\n'+ml+'\n</ul>\n'
                liststr+=ml

            if lsn in docs:
                docs.remove(lsn)
            if 'index.html' in docs:
                docs.remove('index.html')
                docs.insert(0, 'index.html')
            if len(docs)>0:
                ml = ''
                for d in docs:
                    ml = ml + '  <li><a href="%s">%s</a></li>\n'%(d,d)
                #ml = '<ul>\n'+ml+'\n</ul>\n'
                liststr+=ml
            liststr = '<ul>\n'+liststr+'\n</ul>\n'
            list_loc = os.path.join(export_path, name, lsn)
            list_dic = dict( lists=liststr, title=name )
            for k,v in self.config.iteritems():
                if k not in list_dic:
                    list_dic.update({k:v})

            webrelpath = name#os.path.relpath(name, wiki.export_path)
            rel_count = webrelpath.count('/')
            if rel_count==0:
                static_rel = './'
            else:
                static_rel = ''
                for i in range(rel_count):
                    static_rel+='../'
            for i in range(rel_count):
                static_rel+='../'
            rel = webrelpath
            list_dic.update(dict(static_dir=static_rel+'static'))
            list_dic.update(dict(web_relroot=static_rel))

            templateEnv = jinja2.Environment( loader=self.templateLoader )
            TEMPLATE_FILE = "listing.html"
            template = templateEnv.get_template( TEMPLATE_FILE )
            outputText = template.render( list_dic )
            text_export(outputText, list_loc)

            if not('index.html' in docs):
                list_loc2 = list_loc = os.path.join(export_path, name, 'index.html')
                text_export(outputText, list_loc2)

        return dirs

class doc():
    def __init__(self, inpath, outpath, wiki):
        self.wiki = wiki
        self.outpath = outpath
        with open(inpath, 'r') as f:
            doc = f.read()
        doc, data = get_data(doc)
        self.doc = doc.decode('utf-8')
        self.data = data
        for k,v in self.wiki.config.iteritems():
            if k not in self.data:
                self.data.update({k:v})
        self.text = ''
        self.templateLoader = wiki.templateLoader

        webrelpath = os.path.relpath(outpath, wiki.export_path)
        rel_count = webrelpath.count('/')
        if rel_count==0:
            static_rel = './'
        else:
            static_rel = ''
            for i in range(rel_count):
                static_rel+='../'
        self.rel = webrelpath
        self.data.update(dict(static_dir=static_rel+'static'))
        self.data.update(dict(web_relroot=static_rel))

        #self.data.update(dict(wiki_name=self.wiki.config['wiki_name']))
        if not('title' in self.data):
            tt = os.path.basename(inpath).replace('.md','')
            self.data['title'] = tt
        else:
            self.data['title'] = self.data['title'][0]
        self.title = self.data['title']

    def get_tip(self):
        t = self.data['title']
        text = self.clean_text(self.text)
        tag = '-'
        url = '../'+self.rel
        td = OrderedDict([("title", t), ("text", text), ("tags", tag), ("url", url)])
        return td

    def clean_text(self, text):
        text = ''.join(BeautifulSoup(text, 'lxml').findAll(text=True))
        """
        text = text.replace('\n',' ')#.replace("/","-")#.replace('"','\'')
        text = text.replace(u"\u2019","'").replace(u"\u2018","'")
        other_chr = [':','[',']','   ','"', '/', '(',')']
        for k in other_chr:
            text = text.replace(k, '-')
        """
        return text

    def render(self, render_update=None):
        maindic = self.data
        if not(render_update is None):
            maindic.update(render_update)
        body, toc = self.tobody()
        self.text = body
        maindic.update(dict(content=body, toc=toc))

        templateEnv = jinja2.Environment( loader=self.templateLoader )
        TEMPLATE_FILE = "document.html"
        template = templateEnv.get_template( TEMPLATE_FILE )
        outputText = template.render( maindic )

        text_export(outputText, self.outpath)

    def tobody(self):
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(self.doc)
        toc = md.toc
        return (html, toc)



if __name__ == '__main__':
    mpath = '/home/benny/Workspaces/markypydia/miki2/'
    w = wiki(mpath)
