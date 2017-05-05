title: Home

# A small static wiki generator. 

I am sure there are a lot's of static site generators (and quite a lot is in python). 
And, this may be just "yet another static site generator". 

Actually I am not sure whether this is the case, or not.

I am designing this for personal learning. But, I have also tried to make something different. 

Most of the static site generator intended for making a static blog, or maybe something like the CMS. 
Others that are designed for softwares' documentation, or something that can be use as a manual.

But, these are not suitable for a personal wiki.

A personal wiki -- something that is like a personal knowledge storage for some notes about things that one learn. 
I think, a personal wiki should be something like the wikipedia, which has tons of pages, and each page has one thing to be written down. 
These pages could be (should be) unorganized, unstructured. Because knowledge is meant to be free in terms of formation. 
All topics, all pages should be in a same level, and maybe some lists that recorded the related topics. 
And a very long list, maybe sorted alphabetically, as the referencing list like the encyclopedia or dictionary, for searching topics.
Besides, a simple search function for looking related words from the documents and pages sea should be included too. 

So, I made this Markypydia, which is designed to be the personal wiki I have just mentioned.

# What is this
Markypydia is a static wiki generator, which takes the markdown wiki pages and convert it into html pages, and automatically generate the long lists as the reference list. 
There are two types of pages, one is for the general purpose pages, e.g. index page, about page...
The other type is for the wiki documents, which is about all types of topics, which will be put inside the "wiki" directory. 
Markypydia will also "walk" down into each of the directories inside the wiki documents, and generate the wiki webpages for each of the wiki pages in the same directory structure. (using os.walk)

# Templates and themes
I have designed or modified several theme for the use of the Markypydia, including one is modified from the orderedlist's minimal, one is build from the skeleton framework, and another is build from the milligram framework. 

The theme should have three main file, document.html, list.html, and a search.html. 
document.html is for the wiki documents and main pages lookings; list.html is for the references list; search.html should be simple, is for the search result list. 

# condition of this project: under development
Well, although it looks like this could work, there are a lots of things to do before it is useable. 
It can now create the pages, but the links between pages is still needed to be "process". Now the links will be created automatically from the markdown. 


## todo
1. add the function for searching the documents for internal references links, and make sure the links will find a page.
2. maybe, try to automatically add reference links for those words that we have a matching documents in the wiki document sea.  
3. add a "not created yet" page for those words that cannot match but has been mentioned, like wikipedia. 
4. add a shell script function, and create the install setup.py file.
5. reset the default templates folders locations.
