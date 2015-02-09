This is a version of Beautiful Soup based on taking version 4.3.2 (the
most recent production version) and editing it so that the html.parser
back-end has a gevent-aware mode.

It's very simple. What we do is call gevent.sleep(0) to voluntarily
switch context multiple times while parsing a file. Parsing no longer
ends up being done in a single time slice, which should prove to be a
big win. First, overly long parse jobs will cease to hold all other
crawling progress hostage. Second, it will be possible to use
gevent.Timeout to interrupt and abort such long parse jobs. Third, we
won't be using LXML to parse HTML anymore; while LXML in the typical
case performs very well, it has a propensity to act pathologically for
certain cases of malformed input.

This repository is here as a short-to-medium-term arrangement. If the
effort to make Beautiful Soup gevent-aware turns out, contrary to
expectations, to not be fruitful, it will be deleted. If it turns out to
be fruitful, I will submit my changes to the Beautiful Soup development
team and this repository will be used to base crawler deployments on
until such a time as they incorporate the new gevent-aware code into
their trunk and it becomes possible to install the resulting software
via pip.

Note that Beautiful Soup itself is not hosted on Github; it is hosted on
Launchpad, which uses bzr.

= Introduction =

  >>> from bs4 import BeautifulSoup
  >>> soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
  >>> print soup.prettify()
  <html>
   <body>
    <p>
     Some
     <b>
      bad
      <i>
       HTML
      </i>
     </b>
    </p>
   </body>
  </html>
  >>> soup.find(text="bad")
  u'bad'

  >>> soup.i
  <i>HTML</i>

  >>> soup = BeautifulSoup("<tag1>Some<tag2/>bad<tag3>XML", "xml")
  >>> print soup.prettify()
  <?xml version="1.0" encoding="utf-8">
  <tag1>
   Some
   <tag2 />
   bad
   <tag3>
    XML
   </tag3>
  </tag1>

= Full documentation =

The bs4/doc/ directory contains full documentation in Sphinx
format. Run "make html" in that directory to create HTML
documentation.

= Running the unit tests =

Beautiful Soup supports unit test discovery from the project root directory:

 $ nosetests

 $ python -m unittest discover -s bs4 # Python 2.7 and up

If you checked out the source tree, you should see a script in the
home directory called test-all-versions. This script will run the unit
tests under Python 2.7, then create a temporary Python 3 conversion of
the source and run the unit tests again under Python 3.

= Links =

Homepage: http://www.crummy.com/software/BeautifulSoup/bs4/
Documentation: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
               http://readthedocs.org/docs/beautiful-soup-4/
Discussion group: http://groups.google.com/group/beautifulsoup/
Development: https://code.launchpad.net/beautifulsoup/
Bug tracker: https://bugs.launchpad.net/beautifulsoup/
