# header_looker

## Scanner: to scan a network full of web applications and collect statistics on usage of security headers / all headers, especially those relating to caching
Accepts a list of urls looks at each one and saves the header names and values to a database.
needs to follow redirects.
Needs ability to crawl a page of links and visit those.
## Reporter: creates reports for security header statistics:
* CSP
* HSTS preload
* http_only
* x-frame-options
* cross domain policies
* referrer-policy
* xss-protection

Later Feature:  Uses Google searches to find other urls in the same domains
What if it tracked all states, counties, cities, k12, community colleges, = all state and local governments?
What if I published the data
What is an application?  Scanner will follow links and spider entire .gov domains.  an application is not a subdomain.

## Storage:
* phase one:  A really simple SQL-Lite DB
** Application
** Header:
*** Record_ID
*** Scan ID
*** 
** Scan - Scan has scan date, 
* phase two: a beefier one of the above
