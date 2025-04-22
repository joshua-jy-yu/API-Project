*IP Address*: 34.44.44.14

*To call the api*:

Send a request to the following:
http://34.44.44.14:5000/api/secure-data?=CAPITALCITYHERE
and replace CAPITALCITYHERE with the capital city of your choosing.

However, without a token, it will be unauthorized.
So, in the header, provide the secret token "supersecrettoken123" by doing the following:
curl -H "Authorization: Bearer supersecrettoken123" http://34.44.44.14:5000/api/secure-data?=CAPITALCITYHERE

You will receive a JSON response with the capital name, local time, and the UTC offset.


