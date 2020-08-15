#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:02:49 2020

@author: ichraf ben fadhel
"""

import urllib.request as url
import json
import os , sys ,argparse

class issuesFromGithub :
    def __init__(self,repo_owner,repo_name):
        self.repo_owner=repo_owner
        self.repo_name=repo_name
        
    def fetch_from_github(self):

        #specifiy features in the request  
        request="https://api.github.com/repos/"+self.repo_owner+"/"+self.repo_name+"/issues?state=closed&labels=bug&per_page=100&page="
        print(request)
        i=1 # number of page
        downloading=True 
        data=[]
        #create issues directory if it don't exist
        os.makedirs('issues', exist_ok=True)
        #continue downloading issues while there are data 
        while downloading :
       
            req = url.Request(request+str(i))
        
            with url.urlopen(req) as conn:
                issues = json.loads(conn.read().decode('utf-8'))
                # when the result is empty mean we downloaded all issues => so stop  
                if issues ==[] :
                    downloading =False
                else :
                # add  the downloaded data to issue list
                    for issue in issues :
                        data.append(issue)
        # increment the page number to get  the next page            
            i+=1
    # write the issues in json file
        file_result_path=os.path.join('issues',self.repo_name+'.json') # to make it independent of the plateform 
        with open(file_result_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(data))
   
        print("file created => "+file_result_path)    

#repo_owner= str(sys.argv[1])
#repo_name=str(sys.argv[2])

if __name__ =="__main__" :
    parser = argparse.ArgumentParser(description="""fetch issues from github api""")
    parser.add_argument('--repo_owner', type=str,
                        help='repository owner')
    parser.add_argument('--repo_name', type=str,
                        help='repository name')
    args = parser.parse_args()
    #initialise class
    issuesGithub=issuesFromGithub(args.repo_owner,args.repo_name)
    #call the method to fetch issues 
    issuesGithub.fetch_from_github()
#fetch_from_github("eclipse","openj9")
