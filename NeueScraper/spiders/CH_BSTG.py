# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import datetime
import random
import time
import json
from NeueScraper.spiders.basis import BasisSpider
from NeueScraper.pipelines import PipelineHelper as PH

logger = logging.getLogger(__name__)

class CH_BSTG(BasisSpider):
	name = 'CH_BSTG'
	HOST='https://bstger.weblaw.ch'
	URL='/api/.netlify/functions/searchQueryService'
	
	JSON={"sortOrder":"desc","sortField":"publicationDate","size":60,"guiLanguage":"de","userID":"_9ynrsjyup","sessionDuration":1638755448,"origin":"Dashboard","aggs":{"fields":["rulingType","tipoSentenza","year","court","language","lex-ch-bund-srList","ch-jurivocList","jud-ch-bund-bgeList","jud-ch-bund-bguList","jud-ch-bund-bvgeList","jud-ch-bund-bvgerList","jud-ch-bund-tpfList","jud-ch-bund-bstgerList","lex-ch-bund-asList","lex-ch-bund-bblList","lex-ch-bund-abList","jud-ch-ag-agveList"],"size":10}}

	def get_next_request(self, fromwert=0):
		userID='_'
		random.seed()
		while len(userID)<10:
			userID+="0123456789abcdefghijklmnopqrstuvwxyz"[random.randint(0,35)]
		epoch=str(int(time.mktime(time.localtime())))
		self.JSON['userID']=userID
		self.JSON['sessionDuration']=epoch
		if fromwert>0: self.JSON['from']=fromwert
		return scrapy.http.JsonRequest(url=self.HOST+self.URL, data=self.JSON, callback=self.parse_trefferliste, errback=self.errback_httpbin, meta={'from': fromwert})
	
	def __init__(self, ab=None, neu=None):
		super().__init__()
		self.ab=ab
		if ab:
			self.JSON['metadataDateMap']={'publicationDate' : { 'from': ab+'T00:00:00.000Z', 'to': '2051-12-31T22:59:59.999Z'}}
		self.neu=neu
		self.request_gen = [self.get_next_request(0)]
		
	def parse_trefferliste(self, response):
		logger.info("parse_einzelseite response.status "+str(response.status))
		antwort=response.body_as_unicode()
		logger.info("parse_einzelseite Rohergebnis "+str(len(antwort))+" Zeichen")
		logger.info("parse_einzelseite Rohergebnis: "+antwort[0:50000])
		
		struktur=json.loads(antwort)
		treffer=struktur['totalNumberOfDocuments']
		logger.info(str(treffer)+" Entscheide insgesamt.")
		entscheide=struktur['documents']
		logger.info(str(len(entscheide))+" Entscheide in dieser Liste.")
		for entscheid in entscheide:
			item={}
			item['Leitsatz']=PH.NC(entscheid['content'], error="keine Titelzeile in "+json.dumps(entscheid))
			if 'tipoSentenza' in entscheid['metadataKeywordTextMap']:
				item['Weiterzug']=PH.NC(entscheid['metadataKeywordTextMap']['tipoSentenza'][0], warning="keine Weiterzugsinfo in "+json.dumps(entscheid))			
			item['Num']=PH.NC(entscheid['metadataKeywordTextMap']['dossiernummer'][0], error="keine Geschäftsnummer in "+json.dumps(entscheid))
			item['PDFUrls']=[PH.NC(entscheid['metadataKeywordTextMap']['originalUrl'][0], error="keine URL in "+json.dumps(entscheid))]
			if 'rulingDate' in entscheid['metadataDateMap']:
				item['EDatum']=self.norm_datum(PH.NC(entscheid['metadataDateMap']['rulingDate'], error="kein Entscheiddatum in "+json.dumps(entscheid))[:10])
			else:
				logger.warning("kein Entscheiddatum in "+item['Num'])
			if 'publicationDate' in entscheid['metadataDateMap']:
				item['PDatum']=self.norm_datum(PH.NC(entscheid['metadataDateMap']['publicationDate'], warning="kein Publikationsdatum in "+json.dumps(entscheid))[:10])
			else:
				if 'year' in entscheid['metadataKeywordTextMap']:
					item['PDatum']=self.norm_datum(PH.NC(entscheid['metadataKeywordTextMap']['year'][0], warning="kein Publikationsdatum und auch kein Jahr in "+json.dumps(entscheid))[:10])
				else:
					logger.warning("kein Entscheiddatum in "+item['Num'])
			item['VGericht']=''
			item['VKammer']=''
			item['Signatur'], item['Gericht'], item['Kammer']=self.detect(item['VGericht'], item['VKammer'], item['Num'])
			item['Kanton']=self.kanton_kurz
			if 'PDatum' in item or 'EDatum' in item:
				yield item
			else:
				logger.error('Entscheid ohne Datum (weder EDatum, PDatum noch year) '+item['Num'])
		neufrom=response.meta['from']+len(entscheide)
		if neufrom < treffer:
			request=self.get_next_request(neufrom)
			logger.info("Hole Entscheide ab: "+str(neufrom))
			yield request
		else:
			if neufrom > treffer:
				logger.error("Mehr Entscheide geladen ("+str(neufrom)+") als Treffer ("+str(treffer)+").")
