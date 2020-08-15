#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:21:59 2020
@author: ichraf ben fadhel
"""
import json
import re 

import pandas as pd 
from dateutil.parser import parse

""" this script is used to search for fix commit of issues host in bugzilla (because the format of csv file differt)"""



def find_commit_candidats(gitlog_path) :
    """ to reduce the commits in which we search we run this
        function to just select commits with that have mention that it is fix commit or issue
        so as example commits that include "issue" ,"fix" , "pull request", "bz" """
    commits_candidate=[]
    pattern="[Bb][Zz]-\d+|[Bb][Zz] -\d+|[Ii]ssue #\d+|[Ff]ixe[sd]|[Ff]ixe|BZ \d+|bz \d+|[Pp][Rr]\s\d+|[Bb]ug\s\d+|#\d+|[Bb]ugzilla"
   
    # load git commits from the json 
    with open(gitlog_path) as f:
        gitlog = json.loads(f.read())
    
    # we select the commits that matchs the pattern
    for commit in gitlog :
        
        if re.search(pattern,commit) is not None :
            commits_candidate.append(commit)
    
    return commits_candidate  

            
def commit_selector_heuristic(commits):
    """ Helper method for find_bug_fixes.
    Commits are assumed to be ordered in reverse chronological order.
    Given said order, pick first commit that does not match the pattern.
    If all commits match, return newest one. """
    for commit in commits:
        if not re.search('[Mm]erge|[Cc]herry|[Nn]oting', commit):
            return commit
    return commits[0]
        
    
    
    

def find_bug_fixes(issue_path, gitlog_path,original_pattern):
    """ Identify fixed issue in repository given a list of issue gitlog and issue pattern"""
   
    matches_per_issue={}
    no_matches=[]
    issue_list={}
    total_matches=0
    # read all issues 
    data =pd.read_csv(issue_path)
    # select the commits candidates to reduce search space
    commits_candidate=find_commit_candidats(gitlog_path)
    i=0
    #some bug from bugzilla follow this pattern bz-Number or Number 
    for bug_id in data['Bug ID']: 
        # if the format is BZ-Number 
        if "-" in bug_id :
            nb=bug_id.split("-")[1]
            # extract the number and replace \d+ by the number
            pattern=original_pattern.replace("\d+",str(nb))
        # else if the Id is just number we simply replace \d+ in the pattern by the Id            
        else :
            pattern=original_pattern.replace("\d+",str(bug_id))
                
        matches=[]        
        
        # for each commit candidat , search for the commits that match the pattern  
        for commit in commits_candidate :
            if re.search(pattern,commit) :
                matches.append(commit)
        
        total_matches += len(matches)
        matches_per_issue[bug_id] = len(matches) 
        
        # if their are commits selected that matches the bug 
        if matches :
            #we select the commit that actualy fix the bug
            selected_commit = commit_selector_heuristic(matches)
            
            # after selecting the commit we added to list with
            #commit sha , commit date , resolution date , creating date and commit date
            if selected_commit :
                # get commit and issue detail
                issue_list[bug_id]={}
                issue_list[bug_id]['hash'] =  re.search('(?<=^commit )[a-z0-9]+(?=\n)', \
                              selected_commit).group(0)     
                issue_list[bug_id]['commitdate'] =  re.search('(?<=\nDate:   )[0-9 -:+]+(?=\n)',\
                                  selected_commit).group(0)    
                issue_list[bug_id]['resolutiondate'] = re.search('(?<=\nDate:   )[0-9 -:+]+(?=\n)',\
                                  selected_commit).group(0)    
                issue_list[bug_id]['creationdate'] =str( parse( data[data['Bug ID']==bug_id]['Opened'].tolist()[0]+" +0000" ).strftime('%Y-%m-%d %H:%M:%S %z'))
           
            # else the bug don't have fix commit    
            else :
                no_matches.append(bug_id)
        # else the bug don't have fix commit    
        else :
            no_matches.append(bug_id)
        i+=1     
    print("total issues"+str(data['Bug ID'].count()))
    print('Issues matched to a bugfix: ' + str(data['Bug ID'].count() - len(no_matches)))
    print('Percent of issues matched to a bugfix: ' + \
          str((data['Bug ID'].count() - len(no_matches)) / data['Bug ID'].count()))

    return issue_list 