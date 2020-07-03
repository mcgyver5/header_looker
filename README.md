# header_looker

need to scan a network full of web applications and collect statistics on usage of security headers / all headers, especially those relating to caching
Accepts a list of urls looks at each one and saves the header names and values to a database.

creates reports for security header statistics:
* CSP
* HSTS preload
* http_only
* x-frame-options
* cross domain policies
* referrer-policy
* xss-protection

Uses Google searches to find other urls in the same domains
