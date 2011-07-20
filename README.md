# EDoc-Merge

Fast and dirty EDoc merger.

## Considerations

By Erlang/OTP design principles, large projects are consists of applications 
and has following structure:

    /apps
        first_app
            src
        second_app
            src
            
It's good. But after `rebar doc`, we obtain `doc` in each app directory. And 
cross-app links will point just not where we would like. `EDoc-Merge` solves 
this problem:

* Pull all docs in target directory.
* Correct links.
* Fix UTF-8.
* Make index file from `overview.md` markdown file.

## Usage

`EDoc-Merge` written in python. It uses following dependencies:

* [pystache](https://github.com/defunkt/pystache.git)
* [python-markdown](http://www.freewisdom.org/projects/python-markdown)

You can merge generated docs by

    python path/to/edoc-merge.py

## Options

`EDoc-Merge` supports three options.

### Apps source

    python path/to/edocmerge.py --apps=another
    
This option tells `EDoc-Merge` to search for docs in another directory.

### Doc destination

    python path/to/edocmerge.py --dest=MySuperDocs

`dest` just changes destination directory.

### Change design

    python path/to/edocmerge.py --pivot=MyTemplates

`EDoc-Merge` uses some files to generate docs. They are in the directory 
`pivot`. It's two templates for `pystache` and some static files in 
(surprise!) `static` directory.
