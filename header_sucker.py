# python requests
import requests

x = requests.head('https://www.w3schools.com/python/demopage.php')

print(x.headers)

# answer is a dictionary:
# {'Content-Encoding': 'gzip', 'Cache-Control': 'public', 'Content-Type': 'text/html', 'Date': 'Thu Jul 02 2020 23:24:10 GMT-0500 (Central Daylight Time)', 'Server': 'Microsoft-IIS/7.5', 'Vary': 'Accept-Encoding', 'X-Frame-Options': 'SAMEORIGIN', 'X-Powered-By': 'PHP/5-4-2. ASP.NET', 'Content-Length': '0'}

# 
