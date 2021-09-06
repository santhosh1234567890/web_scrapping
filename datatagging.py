from tika import parser
import os.path
import json
import requests
from datetime import timezone
import datetime
import os.path
from os import path
import config as cfg

working_directory = cfg.url["working_directory"]

class DataTag:

    def __init__(self, file_name, link, content_type, query,desc):
        self.file_name = file_name
        self.link = link
        self.content_type = content_type
        self.query = query
        self.desc = desc
        self.tag_post = []
        self.new_list = [] 
        self.solr_tag_post = []

        
    def store_documents_json(self):
        folder_location = working_directory +'Tags/tag_details.json'
        # save the response into Json file
        # if file already exist save it or create a file then save it
        tag_details_list = self.new_list
        length_tag_details_list = len(tag_details_list)
        # print(length_tag_details_list)
        if path.exists(folder_location) == True:
            with open(folder_location) as outfile:
                data = json.loads(outfile.read())
                temp = data['content_tagging']
                for length in range(length_tag_details_list):
                    y = {
                        'url': self.link,
                        'query': self.query,
                        'content_type': self.content_type,
                        'title': tag_details_list[length]['title'],
                        'tag_details': {
                            'no_of_tags': tag_details_list[length]['tag_details']['no_of_tags'],
                            'tags': tag_details_list[length]['tag_details']['tags'],
                            'individual_tags': tag_details_list[length]['tag_details']['individual_tags'],
                            }
                        }
                    temp.append(y)
            with open(folder_location, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        else:
            data = {}
            for length in range(length_tag_details_list) :
              data['content_tagging'] = [
                  {
                      'url': self.link,
                      'query': self.query,
                      'content_type': self.content_type,
                      'title': tag_details_list[length]['title'],
                      'tag_details': {
                          'no_of_tags': tag_details_list[length]['tag_details']['no_of_tags'],
                          'tags': tag_details_list[length]['tag_details']['tags'],
                          'individual_tags': tag_details_list[length]['tag_details']['individual_tags'],
                      }
                  }
              ]
              with open(folder_location, 'w') as outfile:
                  json.dump(data, outfile)

    def tagging_documents(self):
        # In tagging function, tag downloaded files using curl command in solr.
        # 1.file = name of the downloaded files
        # 2.query: keyword to download the documents using search result
        # 3.content_type:pdf,text,videos or multi
        # 4.link= keyword to download the documents using search result
       
        # Solr query for tagging
        
        # content type must be text
        
        # parse content from file using Tika
        if self.content_type == 'program':
            text = self.tagging_code_snippet()
        else:
            text = self.tagging()
        url = cfg.solr["url"]+'/btags/tag?fl=id,primary.tag,primary.secondary.tag,primary.secondary.tertiary.tag&wt=json&indent=true'
        headers = {"Content_type": "text/plain"}
        # post the parsed content into Solr for tagging
        posting = requests.post(url, data=text.encode('utf-8'), headers=headers)
        response_json = posting.json()
        # print(response_json)
        # response we got from solr
        total_tag_count = response_json['tagsCount']
        individual_tag = response_json['response']['numFound']
        tags = response_json['response']['docs'][0:individual_tag]
        tags_individual = response_json['response']['docs']
        #     print(response_json)
        if total_tag_count == 0:
            os.remove(self.file_name)
        else:
            print("\nTotal Number of Tags: ", total_tag_count)
            print("\nIndividual Tag Count: ", individual_tag)
            for i in range(individual_tag):
                main_tag = tags_individual[i]['primary.tag']
                print("\nMain Tag :", main_tag)
                sub_tag_main = tags_individual[i]['primary.secondary.tag']
                print("Sub Tag Main :", sub_tag_main)
                sub_tags = tags_individual[i]['primary.secondary.tertiary.tag']
                print("Sub Tags :",sub_tags)
                solr_tag_details = main_tag + sub_tag_main + sub_tags
                print(solr_tag_details)
                if solr_tag_details not in self.tag_post:
                    self.tag_post.append(solr_tag_details)
                tag_id = tags_individual[i]['id']
                print("Tag ID :", tag_id)
            file_name = self.file_name.split('/')[-1]
            title_name = os.path.splitext(file_name)[0]
            # self.posting_documents(text)
            y = {
                'url': self.link,
                'query': self.query,
                'content_type': self.content_type,
                'title': title_name,
                'tag_details': {
                    'no_of_tags': total_tag_count,
                    'tags': tags,
                    'individual_tags': individual_tag,
                }
            }
            self.new_list.append(y)
            self.store_documents_json()
        return self.new_list

    def tagging(self):
        file_data = parser.from_file(self.file_name)
        text = file_data['content']
        return text

    def tagging_code_snippet(self):
        tagging_filename = self.desc
        # print(tagging_filename)
        return tagging_filename

    def posting_documents(self,text):
        filename = self.file_name.split('/')[-1]
        title_name = filename.split('.')[0]
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        utc_final = int(utc_timestamp)
        # if self.content_type == 'program':
        #     solr_tag_string = self.tag_post[0][0]['tagname']
        #     self.solr_tag_post.append(solr_tag_string)
        # else:
        for assest in range(len(self.tag_post)):
            solr_tag_string = str(self.tag_post[assest][0]) + ' ' + str(self.tag_post[assest][1] + ' ' + str(self.tag_post[assest][2]))
            solr_tag_string = solr_tag_string.lower()
            solr_tag_string = solr_tag_string.replace(" ","_")
            self.solr_tag_post.append(solr_tag_string)
        data = [
            {
                'path' : self.file_name,
                'title' : title_name,
                'doc_name' : filename,
                'content_type' : self.content_type,
                'doc_content' : text,
                'tag_details' : self.solr_tag_post,
                'date' : utc_final
            }
            ]    
        dataset = json.dumps(data)
        url = cfg.solr["url"]+'/documents/update?commit=true'
        headers={'Content-Type': 'text/json'}
        response = requests.post(url,data=dataset.encode('utf-8'),headers=headers) 
