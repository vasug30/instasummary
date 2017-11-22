from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Summarize
from .serializers import summarizeSerializer

from isummary.Parser.html import HtmlParser
from isummary.Tokenizer.tokenizer import Tokenizer
from isummary.Summary.textrank import LsaSummarizer as Summarizer
from isummary.Tokenizer.stem import Stemmer
from isummary.Tokenizer.getstopwords import get_stop_words


LANGUAGE = "czech"
SENTENCES_COUNT = 10


class urlList(APIView):

    def get(self, request):
        urls = Summarize.objects.all()
        serializer = summarizeSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        posturl = request.data['url']  # url to be summarized
        sites = ['youtube', 'angel', 'twitter', 'hackerearth', 'salesforce', 'linkedin', 'facebook', 'instagram',
                 'stackoverflow', 'hackerrank', 'google', 'geeksfogeeks']
        for s in sites:
            if posturl.__contains__(s):
                siteerror = "This site cannot be summarized"
                return Response(siteerror)

        if posturl.endswith("pdf") or posturl.endswith("img") or posturl.endswith("jpeg") or posturl.endswith(
                "jpg") or posturl.endswith("gif") or posturl.endswith("png") or posturl.endswith(
                "ico") or posturl.endswith("svg") or posturl.endswith("xml") or posturl.endswith(
                "mkv") or posturl.endswith("flv") or posturl.endswith("gif") or posturl.endswith(
                "avi") or posturl.endswith("mp4") or posturl.endswith("mpv") or posturl.endswith(
                "m4p") or posturl.endswith("svi") or posturl.endswith("dll") or posturl.endswith("exe"):
            formaterror = "This is a file. If it is pdf,doc or a text file, please upload it in our site and get a summary"
            return Response(formaterror)
        s1 = 'chrome://newtab/'

        if posturl.__contains__(s1):
            emptytaberror = "This is an empty tab. Open a website to get a summary"
            return Response(emptytaberror)
        parser = HtmlParser.from_url(posturl, Tokenizer(LANGUAGE))
        # or for plain text files
        # parser = Plaintext1Parser.from_file("document.txt", Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        summary = ''
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary += str(sentence)
            foo_instance = Summarize.objects.create(url=posturl, summarized=summary)
            html = "%s" % summary

        output = {'resp': html}

        return Response(output)




