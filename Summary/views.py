from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import json
from io import StringIO
import docx
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from urllib.request import urlopen
from django.core.files.storage import FileSystemStorage


def home(request):
    try:
        if request.method == "POST":
            singleurl = request.POST['url']
            if singleurl.startswith("www"):
                singleurl="https://"+singleurl

            if invalid_url(singleurl) is False:

                    context = {
                                    "error": "error"
                              }
                    return render(request, "home.html", context)

            sites = ['youtube', 'angel', 'twitter','hackerearth','salesforce', 'linkedin', 'facebook', 'instagram', 'stackoverflow', 'hackerrank']
            for s in sites:
                if singleurl.__contains__(s):
                    context = {
                                    "error1": "error1"
                              }
                    return render(request, "home.html", context)

            if singleurl.endswith("pdf")or singleurl.endswith("img") or singleurl.endswith("jpeg") or singleurl.endswith("jpg") or singleurl.endswith("gif") or singleurl.endswith("png") or singleurl.endswith("ico") or singleurl.endswith("svg") or singleurl.endswith("xml") or singleurl.endswith("mkv") or singleurl.endswith("flv") or singleurl.endswith("gif") or singleurl.endswith("avi") or singleurl.endswith("mp4") or singleurl.endswith("mpv") or singleurl.endswith("m4p") or singleurl.endswith("svi") or singleurl.endswith("dll") or singleurl.endswith("exe"):
                    context = {
                                    "error2": "error2"
                              }
                    return render(request, "home.html", context)

            def get_output(singleurl):
                url = 'http://127.0.0.1:8000/summarizer/'
                # params = {'url': singleurl}
                r = requests.post(url, data={'url' : singleurl})
                out = r.json()
                for key, value in out.items():
                    print(value)
                    output1 = value
                return output1

            output = get_output(singleurl)

            print(output)
            context = {
                "summ": output
            }

            return render(request, "finalsummary.html", context)
        else:
            return render(request, "home.html", {})
    except Exception:
        output = " Enter something in textbox"
        context = {
            "exception": output
        }

        return render(request, "errorRedirect.html", context)


def keyword(request):
    if request.method == "POST":
        word = request.POST['keyword']
        if find_length(word)>10:
            context = {
                                "error": "error"
                          }
            return render(request, "keyword.html", context)
        max_url = request.POST['max_url']
        max_url = int(max_url)

        queue = []
        summ = []
        LANGUAGE = "english"
        SENTENCES_COUNT = 20
        output = ""
        page = 0
        out = 0
        count = 0
        limit_reached = False

        while True:
            url = "https://www.google.com/search?q=" + word + "&start=" + str(page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'lxml')
            sites = ['youtube', 'twitter', 'linkedin', 'facebook', 'instagram', 'stackoverflow', 'hackerrank',
                     '/download', 'geeksforgeeks', 'hackerearth', 'salesforce', 'angel']
            for link in soup.select('h3.r a'):
                count += 1
                flag = 0
                href = link.get('href')
                title = link.text
                for s in sites:
                    if href.find(s) != -1:
                        flag = 1

                if title.find('Download') != -1 or title.find('download') != -1:
                    flag = 1

                if flag == 0:
                    if '/search' not in href:
                        hyref = parse.parse_qs(href)
                        ref = hyref['/url?q'][0]
                        queue.append(ref)
                        out = out + 1

                if out >= max_url:
                    break
            if out < max_url:
                page = page + 10
            if out < max_url and page == 10:
                limit_reached = True
                break

            if out > max_url:
                break

            if len(queue) == 0:
                context = {
                        "error1": "error1"
                          }
                return render(request, "keyword.html", context)
        length = len(queue)-1
        for i in range(length):
            def get_output(singleurl):
                url = 'http://127.0.0.1:8000/summarizer/'
                # params = {'url': singleurl}
                r = requests.post(url, data={'url' : singleurl})
                out = r.json()
                for key, value in out.items():
                    print(value)
                    output1 = value
                return output1

            output = get_output(queue[i])
            summ.append(queue[i])
            summ.append(output)

        if limit_reached:
            output = "Reference limit reached. Sorry."
            summ.append(output)

        context = {
           "keyword": summ
        }
        return render(request, "finalsummary.html", context)
    else:
        return render(request, "keyword.html", {})


def fileupload(request):
    if request.method == "POST" and request.FILES['file']:
        filepath = request.FILES['file']
        filepath.name = filepath.name.replace(" ", "")
        fs = FileSystemStorage()
        filename = fs.save(filepath.name, filepath)

        uploaded_file_url = fs.url(filename)
        LANGUAGE = "czech"
        SENTENCES_COUNT = 20
        text = ""
        output = ""

        if uploaded_file_url.endswith('.pdf'):
            rsr_mgr = PDFResourceManager()
            sio = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsr_mgr, sio, codec=codec, laparams=laparams)
            interpreter = PDFPageInterpreter(rsr_mgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set()
            fp = open(uploaded_file_url, 'rb')
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                          check_extractable=True):
                interpreter.process_page(page)
            fp.close()
            device.close()
            text = sio.getvalue()
            sio.close()

        elif uploaded_file_url.endswith('.txt'):
            file_access = open(uploaded_file_url, 'r', encoding="ISO-8859-1")
            text = file_access.read()

        elif uploaded_file_url.endswith('.docx'):
            doc = docx.Document(uploaded_file_url)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)

            text = '\n'.join(fullText)

        def get_output(text):
            url = 'http://127.0.0.1:8000/pdfsummary/'
            r = requests.post(url, data={'text': text})
            out = r.json()
            for key, value in out.items():
                print(value)
                outprint = value
            return outprint

        output = get_output(text)

        context = {
            "summ_text": output
        }

        return render(request, "fileupload.html", context)

    else:
        return render(request, "fileupload.html", {"summ_text": "ERROR"})


def invalid_url(url):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()

        except HttpResponse:
            return False
        except URLError:
            return False


def find_length(str):
    str=str.strip()
    count=str.split(' ')
    return len(count)
























