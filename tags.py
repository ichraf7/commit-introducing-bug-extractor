#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:35:38 2020

@author: ichraf
"""

import subprocess
import numpy as np 
import pandas as pd 
from dateutil.parser import parse


def get_tags():
    # get all the tags of the project 
    process = subprocess.Popen("git for-each-ref --sort=creatordate --format '%(refname) , %(creatordate)' refs/tags", 
                           stdout=subprocess.PIPE,shell=True)
    
    #get all the tags found 
    tags_dates=process.communicate()[0].decode('utf-8').split("\n")
    
    return tags_dates[:-1]

# for every release get it initial commit
def get_commits(tags):
    commits=[]
    # for every tag get the corespondant commit
    for tag in tags :
        proc = subprocess.Popen("git rev-list -n 1 "+tag , stdout=subprocess.PIPE,shell=True)
        # get all commits and tags
        commits.append(proc.communicate()[0].decode('utf-8')) 
    return commits

def getLastCommitPerTag():
    
    tags_dates=get_tags()
    dates=[]
    tags=[]    
    
    for tag_date in tags_dates :        
        # split tags and dates   
        tags.append(tag_date.split(",")[0])
        dates.append(parse(tag_date.split(",")[1].replace('\n','')).strftime('%Y-%m-%d %H:%M:%S %z'))
        	
    all_commits=get_commits(tags)
    
    all_tags=np.array(tags)
    all_dates=np.array(dates)

    #combine tag to it commit and then write in csv
    df = pd.DataFrame({"tag" : all_tags, "commit" : all_commits , "creationdate":all_dates})    
    df.to_csv("tags_commits.csv",index=False)        
    
getLastCommitPerTag()    
