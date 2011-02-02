# WikiWatch

This project comprises two parts; a Chrome browser extension which reports whenever you are viewing an article on Wikipedia, and a Django site which accepts and processes the URLs passed from the Chrome extension. The aim is to keep a log of all articles visited, per user, and then to display that data in an interesting way.

### Thoughts

The following namespaces need to be handled in some way:

* Special:
* Help:
* Talk:
* Wikipedia:
* File:
* Category:

Should we strip hashes from the end of urls?