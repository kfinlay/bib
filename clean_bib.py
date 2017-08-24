# from https://github.com/scotartt/clean_bib
# customized by KF

import datetime
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import *

input_b = "keithfinlay.bib"
output_b = "keithfinlay_clean.bib"

now = datetime.datetime.now()
print("{0} Cleaning duff bib records from {1} into {2}".format(now, input_b, output_b))


# Let's define a function to customize our entries.
# It takes a record and return this record.
def customizations(record):
    """Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    # print(dir(record))
    record = type(record)
    # print(record)
    # record = page_double_hyphen(record)
    # record = doi(record)
    # record = keyword(record)
    # record = link(record)
    record = convert_to_unicode(record)
    # delete keys for all entry types
    unwanted = ['bdsk-url-1', 'Bdsk-Url-1', 'bdsk-url-2', 'Bdsk-Url-2', 'journal1', 'title1', 'annote1', 'ty', 'n2', 'm3', 'numpages', 'acmid', 'copyright', 'year1', 'bepress_citation_abstract_html_,url''bepress_citation_author', 'bepress_citation_date', 'bepress_citation_firstpage', 'bepress_citation_issue', 'bepress_citation_journal_title', 'bepress_citation_online_date', 'bepress_citation_pdf_url', 'bepress_citation_title', 'bepress_citation_volume', 'documenttype', 'generator', 'publicationdate', 'topic', 'da', 'issn', 'xaddress', 'xpublisher', 'id', 'description', 'format-detection', 'news_keywords', 'revisit-after', 'robots', 'twitter:card', 'twitter:image', 'twitter:site', 'viewport', 'journal-full', 'mesh', 'pmid', 'pst', 'affiliation', 'referrer', 'referrer', 'google-site-verification', 'article_template_version', 'articleid', 'byl', 'cre', 'dat', 'des', 'hdl', 'pg', 'sec', 'thumbnail_width', 'tom', 'xlarge', 'xlarge_height', 'xlarge_width', 'address', 'ajournal', 'lastchecked', 'page', 'application-name', 'msapplication-task', 'msapplication-tooltip', 'msapplication-window', 'mssmarttagspreventparsing', 'originator', 'progid', 'bepress_is_article_cover_page', 'inpages', 'db', 'dp', 'ifp-current-doc-uri', 'ifpdoctype', 'pageclass', 'last-modified', 'pubnote', 'l3', 'group', 'issue_date', 'issue_num', 'mmwr_type', 'accessdate', 'keywordsold', 'adsnote', 'adsurl', 'language']
    for val in unwanted:
        record.pop(val, None)
    # delete keys only if entry is an article
    if record['ENTRYTYPE'] == "article":
        unwanted = ['publisher', 'isbn', 'booktitle']
        for val in unwanted:
            record.pop(val, None)
    # link field to url is url is missing
    if 'link' in record and 'url' not in record:
        record['url'] = record['link']
    record.pop('link', None)
    # useless summary field (should be annotation field actually)
    if 'summary' in record and record['summary'] == 'No annotations':
        record.pop('summary', None)
    if 'summary' in record and 'annote' not in record:
        record['annote'] = record['summary']
        record.pop('summary', None)
    # make months numerical
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monabbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for monlist in [months, monabbr]:
        for monnum, monname in enumerate(monlist, 1):
            if 'month' in record:
                if record['month'].lower() == monname.lower():
                    record['month'] = str(monnum)
    # make doi the url
    if 'doi' in record:
        # if '{' in record['doi']:
        #     print(record['doi'])
        for prefix in ['http://dx.doi.org/', 'https://dx.doi.org/', 'doi:', '{', '}']:
            record['doi'] = record['doi'].replace(prefix, '')
        if record['doi'].startswith('10'):
            link = record['doi']
            link = 'http://dx.doi.org/' + link
            record['url'] = link
        else:
            print('bad doi deleted: ', record['doi'])
            record.pop('doi', None)
    return record


bib_database = None
with open(input_b, encoding='utf-8') as bibtex_file:
    parser = BibTexParser()
    parser.customization = customizations
    # parser.customization = homogeneize_latex_encoding
    # print(parser.customization)
    parser.ignore_nonstandard_types = False
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

if bib_database:
    now = datetime.datetime.now()
    success = "{0} Loaded {1} found {2} entries".format(now, input_b, len(bib_database.entries))
    print(success)
else:
    now = datetime.datetime.now()
    errs = "{0} Failed to read {1}".format(now, input_b)
    print(errs)
    sys.exit(errs)

bibtex_str = None
if bib_database:
    writer = BibTexWriter()
    writer.order_entries_by = ('author', 'year', 'type')
    bibtex_str = bibtexparser.dumps(bib_database, writer)
    # print(str(bibtex_str))
    with open(output_b, "w", encoding='utf-8') as text_file:
        print(bibtex_str, file=text_file)

if bibtex_str:
    now = datetime.datetime.now()
    success = "{0} Wrote to {1} with len {2}".format(now, output_b, len(bibtex_str))
    print(success)
else:
    now = datetime.datetime.now()
    errs = "{0} Failed to write {1}".format(now, output_b)
    print(errs)
    sys.exit(errs)
