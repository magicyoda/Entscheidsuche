# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from NeueScraper.spiders.tribuna import TribunaSpider

logger = logging.getLogger(__name__)

class ZG_Verwaltungsgericht(TribunaSpider):
	name = 'ZG_Verwaltungsgericht'
	
	RESULT_PAGE_URL = 'https://verwaltungsgericht.zg.ch/tribunavtplus/loadTable'
	# Hole immer nur ein Dokument um Probleme mit Deduplizierung und unterschiedlichen Reihenfolgen zu verringern
	# RESULT_QUERY_TPL = r'''7|0|62|https://verwaltungsgericht.zg.ch/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|TRI|0;false|5;true|C:\\DeltaLogic\\Pub\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|C:\\DeltaLogic\\Pub\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|C:\\DeltaLogic\\Pub\\Reports\\Export_1609522279554|reportname|Export_1609522279554|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|41|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|5|10|11|6|0|0|6|1|5|12|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|1|{page_nr}|13|14|15|16|0|17|5|5|18|5|19|5|20|5|21|5|22|5|10|5|23|5|24|5|25|5|26|17|18|5|27|5|28|5|29|5|30|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|-10|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|10|62|10|10|11|11|0|'''
	RESULT_QUERY_TPL = r'''7|0|59|https://verwaltungsgericht.zg.ch/tribunavtplus/|650CC7EFF80D4E2F1340EDCB95B99785|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.lang.Integer/3438268394|[B/3308590456|java.util.Map||0|TRI|0;false|5;true|1|java.util.HashMap/1797211028|reportpath|viewtype|reporttitle|reportexportpath|reportname|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|47|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|8|5|5|9|9|9|5|5|10|5|7|11|11|5|5|5|5|5|5|5|12|13|6|0|0|6|1|5|14|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|1|{page_nr}|-1|12|12|9|673|9|0|9|-1|15|16|10|42|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|84|104|101|115|97|117|114|117|115|92|92|115|117|105|115|115|101|46|102|116|115|17|0|18|5|5|19|10|49|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|82|101|112|111|114|116|115|92|69|120|112|111|114|116|82|101|115|117|108|116|115|46|106|97|115|112|101|114|5|20|10|1|50|5|21|10|0|5|22|10|49|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|82|101|112|111|114|116|115|92|69|120|112|111|114|116|95|49|54|56|52|52|51|51|52|55|48|55|56|52|5|23|10|22|34|69|120|112|111|114|116|95|34|49|54|56|52|52|51|51|52|55|48|55|56|52|18|18|5|24|5|25|5|26|5|27|5|28|5|29|5|30|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|12|5|39|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|12|59|12|12|13|13|0|'''

	# RESULT_QUERY_TPL_AB = r'''7|0|63|https://verwaltungsgericht.zg.ch/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|TRI|{datum}|0;false|5;true|C:\\DeltaLogic\\Pub\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|C:\\DeltaLogic\\Pub\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|C:\\DeltaLogic\\Pub\\Reports\\Export_1609522400769|reportname|Export_1609522400769|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|41|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|5|10|11|6|0|0|6|1|5|12|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|13|1|{page_nr}|14|15|16|17|0|18|5|5|19|5|20|5|21|5|22|5|23|5|10|5|24|5|25|5|26|5|27|18|18|5|28|5|29|5|30|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|5|42|-10|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|5|62|10|63|10|10|11|11|0|'''
	RESULT_QUERY_TPL_AB = r'''7|0|60|https://verwaltungsgericht.zg.ch/tribunavtplus/|650CC7EFF80D4E2F1340EDCB95B99785|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.lang.Integer/3438268394|[B/3308590456|java.util.Map||0|TRI|{datum}|0;false|5;true|1|java.util.HashMap/1797211028|reportpath|viewtype|reporttitle|reportexportpath|reportname|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|47|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|8|5|5|9|9|9|5|5|10|5|7|11|11|5|5|5|5|5|5|5|12|13|6|0|0|6|1|5|14|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|12|15|1|{page_nr}|-1|12|12|9|673|9|0|9|-1|16|17|10|42|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|84|104|101|115|97|117|114|117|115|92|92|115|117|105|115|115|101|46|102|116|115|18|0|19|5|5|20|10|49|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|82|101|112|111|114|116|115|92|69|120|112|111|114|116|82|101|115|117|108|116|115|46|106|97|115|112|101|114|5|21|10|1|50|5|22|10|0|5|23|10|49|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|82|101|112|111|114|116|115|92|69|120|112|111|114|116|95|49|54|56|52|52|51|51|56|50|54|52|54|48|5|24|10|22|34|69|120|112|111|114|116|95|34|49|54|56|52|52|51|51|56|50|54|52|54|48|19|18|5|25|5|26|5|27|5|28|5|29|5|30|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|12|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|12|60|12|12|13|13|0|'''

	HEADERS = { 'Content-type': 'text/x-gwt-rpc; charset=utf-8'
			  , 'X-GWT-Permutation': '1ABD52BDF54ACEC06A4E0EEDA12D4178'
			  , 'X-GWT-Module-Base': 'https://verwaltungsgericht.zg.ch/tribunavtplus/'
			  , 'Host': 'verwaltungsgericht.zg.ch'
			  , 'Origin': 'https://verwaltungsgericht.zg.ch'
			  , 'Referer': 'https://verwaltungsgericht.zg.ch/'
			  , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0'
			  }
	MINIMUM_PAGE_LEN = 100
	DOWNLOAD_URL = 'https://verwaltungsgericht.zg.ch/tribunavtplus/ServletDownload/'
					
	# PDF_PATH = 'C%3A%5CDeltaLogic%5CPub%5CDocs_VG%5C'
	PDF_PATH = ''

	PDF_PATTERN = "{}{}_{}.pdf?path={}&pathIsEncrypted=1&dossiernummer={}"


	reNum=re.compile('[A-Z0-9]{1,3}\s(19|20)\d\d\s\d+')
	
	ENCRYPTED = True
	ASCII_ENCRYPTED = True
	# Versehentlich die Entschlüsselung bei Schwyz gemacht, funktioniert aber
	DECRYPT_PAGE_URL = "https://gerichte.sz.ch/tribunavtplus/decrypt"
	DECRYPT_START ='7|0|5|https://verwaltungsgericht.zg.ch/tribunavtplus/|27D15B82643FBEE798506E3AEC7D40C0|tribunavtplus.client.zugriff.DecryptService|encrypt|[B/3308590456|1|2|3|4|2|5|5|5|62'
	DECRYPT_END = "|5|16|118|36|104|80|89|76|77|72|76|103|50|84|84|65|68|69|"

#7|0|5|https://verwaltungsgericht.zg.ch/tribunavtplus/|27D15B82643FBEE798506E3AEC7D40C0|tribunavtplus.client.zugriff.DecryptService|encrypt|[B/3308590456|1|2|3|4|2|5|5|5|62|67|58|92|68|101|108|116|97|76|111|103|105|99|92|80|117|98|92|68|111|99|115|95|86|71|92|67|58|92|68|101|108|116|97|76|111|103|105|99|92|80|117|98|92|68|111|99|115|95|86|71|92|54|51|55|101|57|54|55|49|52|98|48|102|52|51|54|56|98|48|49|57|101|52|101|50|57|97|53|48|98|56|100|52|46|112|100|102|5|16|118|36|104|80|89|76|77|72|76|103|50|84|84|65|68|69|
#7|0|5|https://verwaltungsgericht.zg.ch/tribunavtplus/|27D15B82643FBEE798506E3AEC7D40C0|tribunavtplus.client.zugriff.DecryptService|encrypt|[B/3308590456|1|2|3|4|2|5|5|5|62|67|58|92|68|101|108|116|97|76|111|103|105|99|92|80|117|98|92|68|111|99|115|95|86|71|92|67|58|92|92|68|101|108|116|97|76|111|103|105|99|92|92|80|117|98|92|92|68|111|99|115|95|86|71|92|92|54|57|54|55|52|52|53|48|100|97|52|51|52|51|56|102|97|98|56|101|48|100|50|54|55|57|56|57|98|101|51|54|46|112|100|102|5|16|118|36|104|80|89|76|77|72|76|103|50|84|84|65|68|69|
#7|0|5|https://verwaltungsgericht.zg.ch/tribunavtplus/|27D15B82643FBEE798506E3AEC7D40C0|tribunavtplus.client.zugriff.DecryptService|encrypt|[B/3308590456|1|2|3|4|2|5|5|5|62|67|58|92|68|101|108|116|97|76|111|103|105|99|92|80|117|98|92|68|111|99|115|95|86|71|92|51|52|102|99|52|56|57|55|99|98|57|57|52|54|98|57|97|101|100|51|48|54|51|100|54|52|50|102|99|97|102|51|46|112|100|102|5|16|118|36|104|80|89|76|77|72|76|103|50|84|84|65|68|69|
#                                                                                                                                                                                                                                                                    C:\\Del



	#Zug benötigt Cookies
	custom_settings = {
        'COOKIES_ENABLED': True
    }
