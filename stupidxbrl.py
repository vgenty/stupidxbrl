import re

import pandas
import bs4

class stupidXBRL():
    def __init__(self,filename):

        assert isinstance(filename,str)
        
        self._filename = filename;

        self._idsearch       = re.compile('ID_[0-9]+')
        self._txtblocksearch = re.compile('TextBlock$')
        try: 
            self._xbrl     = bs4.BeautifulSoup(open(filename),"lxml-xml")
        except IOError:
            print '%s does not exist' % filename
            raise;


    def Build(self):
        ##########################
        #Build the xbrl "contexts" - date ranges for reported fields
        #
        self.contexts = {}

        for context in self._xbrl.findAll(lambda tag : tag.prefix == 'xbrli' and tag.name == 'context'): 
            period = context.findChildren(name='period')[0]
            
            if period.startDate is not None and period.instant is not None: 
                raise Exception("Weird context found!")

            if period.startDate is not None:
                self.contexts[context.attrs['id']] = {'period' : {'startDate' : period.startDate.contents[0], 'endDate' : period.endDate.contents[0] },
                                                 'type'   : 'range'}
            if period.instant is not None:
                self.contexts[context.attrs['id']] = {'period' : {'Date' : period.instant.contents[0] },
                                                 'type'   : 'instant'}
    
        ##########################
        #Build the xbrl "dei" - document data
        #
        self.document = {}
        for dei in self._xbrl.find_all(lambda tag : tag.prefix == 'dei' and self._idsearch.search(tag.attrs['id']) is not None):
            self.document[dei.name] = {'attrs' : dei.attrs , 'value' : dei.contents}
                
        ##########################
        #Build the xbrl "gaap" fields - anything and everything reported as GAAP field
        #
        self.gaap = {}
        for gaap in self._xbrl.find_all(lambda tag : tag.prefix == 'us-gaap' and self._idsearch.search(tag.attrs['id']) is not None):
            self.gaap[gaap.name] = {'attrs' : gaap.attrs , 'value' : gaap.contents}
                
        ##########################
        #Build the xbrl "special" fields - non standard gaap prefix (maybe stock ticker lowercase?)
        #
        extra_prefix = self._xbrl.find(lambda tag : tag.prefix != 'us-gaap' and tag.prefix != 'dei'
                                      and 'id' in tag.attrs 
                                      and self._idsearch.search(tag.attrs['id']) is not None).prefix

        self.special= {}
        for special in self._xbrl.find_all(lambda tag : tag.prefix == extra_prefix and self._idsearch.search(tag.attrs['id']) is not None):
            self.special[special.name] = {'attrs' : special.attrs , 'value' : special.contents}


        
    def ToPandas(self):
        if not hasattr(self,'contexts'):
            print "Call %s.Build() first" % self.__class__.__name__
            return

        self.contexts = pandas.DataFrame(self.contexts)
        self.document = pandas.DataFrame(self.document)        
        self.gaap     = pandas.DataFrame(self.gaap)        
        self.special  = pandas.DataFrame(self.special)

