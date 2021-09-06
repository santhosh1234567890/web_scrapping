import requests
import re
import urllib.request
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import urllib3
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datatagging import DataTag 
import os.path
from bs4 import BeautifulSoup
import config as cfg
from datetime import timezone
import datetime
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

working_directory = cfg.url["working_directory"]

class Extraction:
    def __init__(self,content_type,query):
        self.content_type = content_type
        self.query = query

    def pdf_content(self,url):
    # In pdf_content function extract content from url and save it as .pdf 
    # if url ends with .pdf extract the whole content and write itt as .pdf or else it will look for .pdf files in hyperlink and write it as .pdf.
    # 1.url = url to download the pdf files.  
    # 2.query: keyword to download the documents using search result
    # 3.content_type:pdf and multi type.
        #folder location to save pdf files

        directory =self.query.replace (" ", "_")
        folder_location=working_directory+directory+'/'
        dir_path = folder_location+'pdf/'
        pdf_content_type  = "pdf"
        desc = "one"
        if os.path.exists(folder_location) == False:
            os.mkdir(folder_location)
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
        if(url.endswith('pdf')):
            try:
                req = requests.get(url,verify=False,allow_redirects=True,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'})
                filename = url.split('/')[-1] # this will take only -1 splitted part of the url
                file_name= dir_path+filename
                # print(file_name)
                with open(file_name,'wb') as output_file:
                    output_file.write(req.content)
                output = DataTag(file_name,url,pdf_content_type,self.query,desc)
                output = output.tagging_documents()
                print('Download Completed!!!')
                return output
            except Exception as e:
                print("\nNo pdf found on the page ")
        else:
            try:
                #search for pdf in url and save it
                response = requests.get(url,verify=False,allow_redirects=True)
                soup= BeautifulSoup(response.text, "html.parser")
                n_pdfs = 0
                if(soup.select("a[href$='.pdf']")):
                    for link in soup.select("a[href$='.pdf']"):
                        n_pdfs+= 1
                        filename = os.path.join(dir_path,link['href'].split('/')[-1])
    #                     print(filename)
                #save pdf file
                        with open(filename, 'wb') as f:
                            f.write(requests.get(urljoin(str(url),link['href'])).content)
                        #tag the saved pdf file
                        output=DataTag(filename,url,pdf_content_type,self.query,self.desc)
                        output = output.tagging_documents() 
                        return output
                else:
                    print('\nNo pdfs found on the page')
            except Exception as e:
                print("NO") 

                
    def text_content(self,url,count):
    # In text_content function extract content from url and save it as .txt 
    # 1.url = url to download the text or html files.  
    # 2.query: keyword to download the documents using search result
    # 3.content_type:text or multi
        count = count 
        directory =self.query.replace (" ", "_")
        folder_location = working_directory+directory+'/'
        text_content_type  = "text"
        desc = "one"
        dir_path = folder_location+'text/'
        if os.path.exists(folder_location) == False:
            os.mkdir(folder_location)
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
        try:
            # req = urllib.request.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }) 
            # page = urllib.request.urlopen(req)
            # soup = BeautifulSoup(page,"html.parser")
            req = url
            headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
    # page = urllib.request.urlopen(req)
            source = requests.get(req,data=None, headers=headers).text
            soup = BeautifulSoup(source,'html.parser')
            #preprocess the text 
            txt = '\n'.join([x.text for x in soup.find_all('p')])
            txt = txt.replace('  ', ' ')
            txt = re.sub('\[\d+\]', '', txt)
            txt = re.sub('\d+. ', '', txt)
            txt = txt.replace("\n\n", "\n")
            #filename to save text files
            filename_text = dir_path+directory +'-%d.txt'%count
            print(filename_text)
            #save text file
            with open(filename_text,'w')as f:
                f.write(txt)
            str_directory = dir_path
            # get list of all files in the directory and remove possible hidden files
            list_files = [files for files in os.listdir(str_directory) if files[0]!='.']
            # now loop through the files and remove empty ones
            for each_file in list_files:
                file_path = '%s/%s' % (str_directory, each_file)
                # check size and delete if 0
                if os.path.getsize(file_path)==0:
                    os.remove(file_path)
                else:
                    pass
        #tag the saved text file
            output = DataTag(filename_text,url,text_content_type,self.query,desc)
            output = output.tagging_documents()
            return output

        except Exception as e:
            print('\nNo text has been found')
                  
    def video_content(self,url):
    # In video_content function,  extract youtube videos from url and save it as .mp4 file.
    # if videos has transcript files then save it as .txt files. 
    # 1.url = url to download the videos files.  
    # 2.query: keyword to download the documents using search result
    # 3.content_type:videos or multi
        #folder location for videos and transcript files
        directory =self.query.replace (" ", "_")
        folder_location_video = working_directory+directory+'/'
        dir_path = folder_location_video+'videos/'
        video_content_type  = "videos"
        desc = "one"
        # transcript = folder_location_video+'Videos/'
        if os.path.exists(folder_location_video) == False:
            os.mkdir(folder_location_video)
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
        file_name_start_pos = url.rfind("=") + 1
        file_name = url[file_name_start_pos:]
        try:
            #if the url have transcript download the video and extract transcript from it or print no video found
            if(YouTubeTranscriptApi.get_transcript(file_name)):
                srt= YouTubeTranscriptApi.get_transcript(file_name)
                try:
                    yt_obj = YouTube(url)
                    yt_obj_download = yt_obj.streams.get_highest_resolution()                
                    #download video with transcript
                    video = yt_obj_download.download(dir_path)
                except Exception as e:
                    print("No videos found on the page")
                #print('All YouTube videos downloaded successfully.')
                name = video.split('/')[-1]
                video_name = os.path.splitext(name)[0]
                print(video_name)
                filename_youtube_text = dir_path+video_name+'.txt'
                print(filename_youtube_text)
                #save transcript
                with open(filename_youtube_text,'w')as f:
                    for i in srt:
                        f.write('%s\n' %i['text'])
                #tag the saved transcipt
                output = DataTag(filename_youtube_text,url,video_content_type,self.query,desc)
                output = output.tagging_documents()
                # print(output)
                return output
        except Exception as e:
            print("\nNo YouTube videos found on the page")


    def code_snippet(self,url,title,content_type,desc):
    # In code_snippet function, search for specifc html elements to extract code from url and save it as .txt 
    # 1.url = url to download the program files.  
    # 2.query: keyword to download the documents using search result
    # 3.content_type:program or multi 
        directory =self.query.replace (" ", "_")
        folder_location = working_directory+directory+'/'
        dir_path = folder_location+'codes/'
        if os.path.exists(folder_location) == False:
            os.mkdir(folder_location)
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
        try:
            req = url
            headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
    # page = urllib.request.urlopen(req)
            source = requests.get(req,data=None, headers=headers).text
            soup = BeautifulSoup(source,"html.parser")
            # req = urllib.request.Request(url,data=None,headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15' }) 
            # page = urllib.request.urlopen(req)
            # soup = BeautifulSoup(source,"html.parser")
            if(soup.find_all('code')):
                txt = '\n'.join([content.text for content in soup.find_all('code')])
            elif(soup.find_all('div',class_='codeblock')):
                txt= '\n'.join([content.text for content in soup.find_all('div',class_='codeblock')])
            elif(soup.find_all('pre')):
                txt = '\n'.join([content.text for content in soup.find_all('pre')])
            else:
                txt = '\n'.join([content.text for content in soup.find_all('div',class_='geshifilter')])
                txt = txt.rstrip()
            file = dir_path+title+'.bw_txt'
            with open(file,'w')as f:
                f.write(txt)
                f.close()
            str_directory = dir_path
            # get list of all files in the directory and remove possible hidden files
            list_files = [files for files in os.listdir(str_directory) if files[0]!='.']

            # now loop through the files and remove empty ones
            for each_file in list_files:
                file_path = '%s/%s' % (str_directory, each_file)
                # check size and delete if 0
                if os.path.getsize(file_path)==0:
                    os.remove(file_path)
                else:
                    pass
            output = DataTag(file,url,content_type,self.query,desc)
            output = output.tagging_documents()
            return output
        except Exception as e:
            print("No code")
                
