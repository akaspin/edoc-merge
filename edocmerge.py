'''
EDOC postprocessor
'''

import os
import sys
import optparse
import shutil
import pystache
import re
import markdown
import codecs

class Processor:
    def __init__(self, apps, dest, pivot):
        self.apps = apps
        self.app_list = sorted(os.listdir(apps))
        self.dest = dest
        
        s_path = os.path.dirname(os.path.realpath(__file__))
        self.pivot = os.path.join(s_path, pivot)
        
    def go(self):
        self.pull()
        self.make_readme()
        self.make_mods()
        
        
    def pull(self):
        '''Pull all data'''
        # pull pivot
        if os.path.exists(self.dest) == False:
            os.makedirs(self.dest)
        
        for stat in os.listdir(os.path.join(self.pivot, "static")):
            shutil.copy(os.path.join(self.pivot, "static", stat), 
                        os.path.join(self.dest, stat))
#        shutil.copytree(os.path.join(self.pivot, "static"), self.dest)
        
    def make_readme(self):
        '''process readme.md'''
        f = codecs.open("overview.md", mode="r", encoding="utf8")
        text = f.read()
        out = markdown.markdown(text)
        
        tpl = self.load_file("overview-summary.mustache")
        out = pystache.render(tpl, {'content':out})
        
        output_file = codecs.open(os.path.join(self.dest, 
                                               "overview-summary.html"), 
                                  "w", encoding="utf8")
        output_file.write(out)
            
    def make_mods(self):
        '''make modules frame'''
        
        apps = []
        for app in self.app_list:
            spec = self.prepare_app(app)
            apps.append(spec)
        
        mod_tpl = self.load_file("modules-frame.mustache")
        out = pystache.render(mod_tpl, {'apps':apps})
        
        f = open(os.path.join(self.dest, "modules-frame.html"), 'w')
        f.write(out)
        f.close()
        
    def prepare_app(self, app):
        out = {'name': app,
               'mods': []}
        
        app_path = os.path.join(self.apps, app, "doc")
        
        for f in sorted(os.listdir(app_path)):
            basename, extension = os.path.splitext(f)
            if extension == '.html':
                if not basename in ['index', 'modules-frame', 
                                    'packages-frame', 'overview-summary']:
                    out['mods'].append({'name': basename})
                    self.process_file(os.path.join(app_path, f), 
                                      os.path.join(self.dest, f))
        
        self.process_file(os.path.join(app_path, 'overview-summary.html'), 
                          os.path.join(self.dest, 
                                       app+'-app.html'))
        return out
        
    def load_file(self, name):
        ''' load file '''
        path = os.path.join(self.pivot, name)
        f = open(path, 'r')
        
        try:
            out = f.read()
        finally:
            f.close
        
        return out
    
    def process_file(self, src, dest):
        '''process source'''
        src_f = open(src, 'r')
        out = src_f.read()
        src_f.close()
        
        #cwd cleanup
        cwd_re = re.compile(os.getcwd() + '/apps/')
        out = re.sub(cwd_re, '', out)
         
        # index cleanup
        index_re = re.compile('"(.*)/doc/index\.html" target="_top"')
        out = index_re.sub(r'"\1-app.html"', out)
        
        # final cleanup
        fin_re = re.compile('href="[a-zA-Z_0-9]+/doc/')
        out = fin_re.sub(r'href="', out)

        # UTF fix
        fin_re = re.compile('</title>')
        out = fin_re.sub(r'</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />', out)
        
        dest_f = open(dest, 'w')
        dest_f.write(out)
        dest_f.close()

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog base')
    parser.add_option('-a', '--apps', action='store', dest='apps',
                      type='string', default='apps', help='Apps dir')
    parser.add_option('-d', '--dest', action='store', dest='dest',
                      type='string', default='doc', help='Dest dir')
    parser.add_option('-f', '--pivot', action='store', dest='pivot',
                      type='string', default='pivot', help='pivot dir')
    
    (options, args) = parser.parse_args()
    
    proc = Processor(options.apps, options.dest, options.pivot)
    proc.go()