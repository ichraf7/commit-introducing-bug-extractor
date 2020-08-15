# commit-introducing-bug-extractor


## ABOUT SZZ

SZZ is an algorithm that able to extract commits that introduced bugs based on commits that fix bugs and git history and this task is done throw two phases . 
the first phase consist of fetching and selecting bugs reports ,extract the commits that fixed bugs based on git history , and the second phase consist of extracting the commits that introduced the bugs . 
The  implementation of the SZZ algorithm provided in this repo https://github.com/wogscpar/SZZUnleashed , fetch and process only bug reports in jira but the features in bug reports in jira differ from bug reports in bugzilla and github issues , so this implementation provides the process of szz phase one.

## Steps & Scripts :

### 1. Fetching Data 
**fetch_version_github.py :** script for fetching issues from github issues it select issues that are close and labeled as bug , this will create folder called "issues" in which it contain the resulted file <project_name>.json

To run the script all you have to do is to provide the repository owner and repository name 
**python3 fetch_version_github.py --repo_owner "REPOSITORY OWNER" --repo_name "PROJECT NAME"**

_*eg :*_ to fetch deeplearning4j issues , it repo owner is **'eclipse'** and the repository name is ***deeplearning4j***
**python3 fetch_version_github.py --repo_owner eclipse --repo_name deeplearning4j** 

To fetch data from jira or bugzilla , just download the issues in csv format , we developed a script to clean the issues . Please make sure that you select the feature "opened" when downloading issues from bugzilla .

### 2. Filtering issue  :
The filtering phase is useful to select only specific 
This script **filter_issue_bugzilla.py** filter the bugs reports fetched from bugzilla , in this script we choose to filter :
	***Component="Core" , Resolution="FIXED | RESOLVED" , Status="CLOSED|FIXED"*** 
	some parameters depend on the project so it may that are named differently so feel free to adapted to your project 
	the issues are ordered ,as described in szz algo paper, in reverse chronological order
To run the script :
**python3 filter_issue_bugzilla.py <issues_file_path> <output_file_name>**
eg:
  **python3 filter_issue_bugzilla.py bugs.csv output.csv**

### 3. Finding fix commits :
In this part we introduce the scripts used for searching for commits that fixed bug . The three scripts mentioned above are : to search for fix commit from github issue (issues are in json form) , bugzilla and jira (issuses in csv file) .The idea behind this script is first it start by selecting commits candidate (to limit the search space ), then based on "issue pattern" of the project and the issue id it select the commit that fixed issue ( note : generally dev team use specific pattern when fixing issue for example "FIX : issue ID or BUG ID ..." , this pattern is given by the user ) .

**find_fix_commit_vbugzilla.py :** this script is used to search for fix commit of issues host in bugzilla

**find_fix_commit_vgithub.py :** this script is used to search for fix commit of issues host in github
Note : These scripts will be used from another scripts (internal call from extract_commit_intro_bug.py )
 
### 4. Extracting tag names :
Extract releases names of the project , this will be used to be able extract the fix commits in each release . 
To run the script , go to the project folder (make sure that you cloned the project not downloaded and extracted , so that the project have .git folder ) and then just run in cmd :

**python tags.py :** it will generate file called **tags_commits.csv**
in the same directory . which will contain the tag name ,it first commit , and the creation date .

### 5. Extracting commits introducing bug : 
Finally after extracting the commits that fixed the bug it's time to extract the commits that introduced bugs . Run this script : 

***extract_commit_intro_bug.py "tags_commits_path" "pattern" "git_repo_url" "issue_path" "project_local"***

**tags_commits_path :** the path to tags_commits.csv
**pattern :** the pattern used of fix commits eg: FIX:ID , ISSUE:ID ...
**git_repo_url :** the project github url 
**issue_path :** the path to file of issue list 
**project local :** the path to the project locally .

Please ensure these things :
First make sure that **find_bug_fix_vbugzilla**, **find_bug_fixes_vgithub**,**gitlog _to_array.py** are in the same repo as the script **extract_commit_intro_bug.py** 
Second generate the jar file check this [Link](https://github.com/wogscpar/SZZUnleashed) you will find everything you need it to create it . 

The final result will output 




