var tipuesearch = {"pages": [{"title": "Home", "text": "A small static wiki generator.\nI am sure there are a lot's of static site generators (and quite a lot is in python). \nAnd, this may be just \"yet another static site generator\". \nActually I am not sure whether this is the case, or not.\nI am designing this for personal learning. But, I have also tried to make something different. \nMost of the static site generator intended for making a static blog, or maybe something like the CMS. \nOthers that are designed for softwares' documentation, or something that can be use as a manual.\nBut, these are not suitable for a personal wiki.\nA personal wiki -- something that is like a personal knowledge storage for some notes about things that one learn. \nI think, a personal wiki should be something like the wikipedia, which has tons of pages, and each page has one thing to be written down. \nThese pages could be (should be) unorganized, unstructured. Because knowledge is meant to be free in terms of formation. \nAll topics, all pages should be in a same level, and maybe some lists that recorded the related topics. \nAnd a very long list, maybe sorted alphabetically, as the referencing list like the encyclopedia or dictionary, for searching topics.\nBesides, a simple search function for looking related words from the documents and pages sea should be included too. \nSo, I made this Markypydia, which is designed to be the personal wiki I have just mentioned.\nWhat is this\nMarkypydia is a static wiki generator, which takes the markdown wiki pages and convert it into html pages, and automatically generate the long lists as the reference list. \nThere are two types of pages, one is for the general purpose pages, e.g. index page, about page...\nThe other type is for the wiki documents, which is about all types of topics, which will be put inside the \"wiki\" directory. \nMarkypydia will also \"walk\" down into each of the directories inside the wiki documents, and generate the wiki webpages for each of the wiki pages in the same directory structure. (using os.walk)\nTemplates and themes\nI have designed or modified several theme for the use of the Markypydia, including one is modified from the orderedlist's minimal, one is build from the skeleton framework, and another is build from the milligram framework. \nThe theme should have three main file, document.html, list.html, and a search.html. \ndocument.html is for the wiki documents and main pages lookings; list.html is for the references list; search.html should be simple, is for the search result list. \ncondition of this project: under development\nWell, although it looks like this could work, there are a lots of things to do before it is useable. \nIt can now create the pages, but the links between pages is still needed to be \"process\". Now the links will be created automatically from the markdown. \ntodo\n\nadd the function for searching the documents for internal references links, and make sure the links will find a page.\nmaybe, try to automatically add reference links for those words that we have a matching documents in the wiki document sea.  \nadd a \"not created yet\" page for those words that cannot match but has been mentioned, like wikipedia. \nadd a shell script function, and create the install setup.py file.\nreset the default templates folders locations.\n", "tags": "-", "url": "../index.html"}, {"title": "abc_noname", "text": "this is a test file with no title\nsee what the title is. ", "tags": "-", "url": "../docs/abc_noname.html"}, {"title": "wiki", "text": "testing testing ", "tags": "-", "url": "../docs/wiki.html"}]};