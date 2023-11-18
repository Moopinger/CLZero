import socket
import ssl
from urllib.parse import urlparse
import argparse
from colorama import Fore, Back, Style
import random, string
import os

#These are later defined by the user config file. no touchy
smuggle_request = ""
smuggle_request_body = ""
regular_request = ""
clzero_headers = {}

def color_code(code):

    global NOCOLOR
    if NOCOLOR:
        return code

    if code == "200":
        msg = Fore.BLACK + Back.GREEN + code + Style.RESET_ALL
    elif code == "301" or code == "302":
        msg = Fore.BLACK + Back.YELLOW + code + Style.RESET_ALL
    elif code == "404":
        msg = Fore.WHITE + Back.BLUE + code + Style.RESET_ALL
    else:
        msg = Fore.WHITE + Back.RED + code + Style.RESET_ALL
    return msg

#cache buster
def randomword(length):
   letters = string.ascii_lowercase 
   return ''.join(random.choice(letters) for i in range(length))

def send_request(url, request_type = "regular", modified_cl = "none"):

    # Parse the URL
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
    path = parsed_url.path if parsed_url.path else '/'

    #Parse the config file values for the regular request
    regular_request_temp = regular_request.replace("__PATH__", path).replace("__HOST__", host).replace("__CACHE_BUSTER__", cache_buster)

    #Parse the config file values for the smuggle request
    smuggle_content_len = str(len(smuggle_request_body))
    smuggle_request_temp = smuggle_request.replace("__HOST__", host).replace("__PATH__", path).replace("__CACHE_BUSTER__", path).replace("__METHOD__", request_method).replace("__MOD_CL__", modified_cl)
    smuggle_request_temp = smuggle_request_temp.replace("__CL__", smuggle_content_len) + smuggle_request_body

    
    if request_type == "regular":
        http_request = regular_request_temp

    elif request_type == "smuggle":
        http_request = smuggle_request_temp

    elif request_type == "generate":
        http_request = smuggle_request_temp
        return http_request

    else:
        http_request = regular_request

    if DEBUG:
        print("\r\n========================================")
        print(http_request)
        print("========================================\r\n")
    
    if LAST_BYTE_SYNC and request_type == "smuggle":
        #We will withold the last byte of the probe request and send the smuggle. Once the last byte of the smuggle is sent, the last byte for the probe is immediately sent.
        last_byte = regular_request_temp[-1]
        regular_request_missing_byte = regular_request_temp[:-1]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.settimeout(5)
                if parsed_url.scheme == 'https':
                    context = ssl._create_unverified_context()

                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        ssock.connect((host, port))
                        ssock.send(regular_request_missing_byte.encode())

                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock2:
                            try:
                                with context.wrap_socket(sock2, server_hostname=host) as ssock2:
                                    ssock2.connect((host, port))
                                    ssock2.send(http_request.encode())
                                    #Bounce without reading response for maximum speeed

                            except:
                                return "LASTBYTE_FAIL", "0"
                                            
                        #complete the probe (regular_request) request
                        ssock.send(last_byte.encode())
                        response = ssock.recv(4096)

                        try:
                            response = response.decode()
                        except:
                            return "DECODE_ERROR", "0"
                        
                else:
                    sock.connect((host, port))
                    sock.send(regular_request_missing_byte.encode())

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock2:

                        sock2.settimeout(5)
                        sock2.connect((host, port))
                        sock2.send(http_request.encode())

                    sock.send(last_byte.encode())    
                    response = sock.recv(4096).decode()

            except socket.timeout:
                return "TIMEOUT", "0"
            
            except socket.error as e:
                string_error = str(e)
                if "Connection reset by peer" in string_error:
                    return "PEER_RESET", "0"
                else:
                    return None, None

    # Standard request method begins
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            try:
                sock.settimeout(5) 
                if parsed_url.scheme == 'https':
                    context = ssl._create_unverified_context()
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        ssock.connect((host, port))
                        ssock.send(http_request.encode())

                        if request_type == "smuggle" and SKIP_R:
                            return "Skip", "0"
                        
                        response = ssock.recv(4096)
                        try:
                            response = response.decode()
                        except:
                            return "DECODE_ERROR", "0"
                        
                else:
                    sock.connect((host, port))
                    sock.send(http_request.encode())
                    if request_type == "smuggle" and SKIP_R:
                        return "Skip", "0"
                        
                    response = sock.recv(4096).decode()

            except socket.timeout:
                return "TIMEOUT", "0"
            
            except socket.error as e:
                string_error = str(e)
                if "Connection reset by peer" in string_error:
                    return "PEER_RESET", "0"
                else:
                    return None, None

    #basic error checks below
    if response == "":
        return "EMPTY", "0"
    
    response_lines = response.split('\r\n')
    status_line = response_lines[0]
    content_length = next((line for line in response_lines if line.lower().startswith('content-length:')), None)
    
    #likely chunked if status is 200 and CL headers is 0, will just return 0 for now, has no affect
    if not content_length:
        content_length = "0"
    else:
        content_length = content_length.split(" ")[1]

    if len(status_line.split(" ")) > 1:
        status_code = status_line.split(" ")[1]
        return status_code, content_length
    
    else:
        return "NO_STATUS", "0"
    
def overwrite_file(value, filename):
    with open(filename, 'w') as file:
        file.write(value)

def write_value_to_file(value, filename):
    with open(filename, 'a') as f:
        f.write(str(value) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLZero by Moopinger - Thanks: Smuggler - @Defparam. @Albinowax. D3d - @deadvolvo')
    parser.add_argument('-url', type=str, help='(-u), Single target URL.')
    parser.add_argument('-file', type=str, help='(-f), Files containing multiple targets.')
    parser.add_argument('-index', type=int, default=0, help="(-i), Index start point when using a file list.")
    parser.add_argument('-verbose', action='store_true', help="(-v), Enable verbose output.")
    parser.add_argument('-no-color', action='store_true', help="Disable colors in HTTP Status")
    parser.add_argument('-resume', action='store_true', help="Resume scan from last index place.")
    parser.add_argument('-skipread', action='store_true', help="Skip the read response on smuggle requests, recommended. This will save a lot of time between requests. Ideal for targets with standard HTTP traffic.")
    parser.add_argument('-quiet', action='store_true', help="(-q), Disable output. Only successful payloads will be written to ./payloads/ ")
    parser.add_argument('-lb', action='store_true', help="Last byte sync method for least request latency. Due to the nature of the request, it cannot guarantee that the smuggle request will be processed first. Ideal for targets with a high amount of traffic, and you do not mind sending multiple requests.")
    parser.add_argument('-config', type=str, default="./configs/default.py", help="(-c) Config file to load, see ./configs/ to create custom payloads")
    parser.add_argument('-method', type=str, default="POST", help="(-m) Method to use when sending the smuggle request. Default: POST")
    args = parser.parse_args()

    
    LAST_BYTE_SYNC = args.lb 
    DEBUG = args.verbose
    NOCOLOR = args.no_color
    QUIET = args.quiet
    SKIP_R = args.skipread
    config_file = args.config
    request_method = args.method
    slice = args.index
    targets = []
    
    if args.url:
        targets.append(args.url)
        
    elif args.file:
        my_file = open(args.file, "r")
        data = my_file.read()
        hosts = data.split("\n")
        targets = targets + hosts

    if args.url or args.file:
        if not QUIET:
            print("CLZero.py - CL.0 Finder and Fuzzer -=Moopinger=-")
    else:
        exit(parser.print_help())

    if args.resume and args.file:
        try:
            session_file = open('./resume.config', "r")
            data = session_file.read().lower().split(":::")
            data[1] = data[1].strip()
            #data[0] = string: index position
            #data[1] = string: targetname

            target_at_index = targets[int(data[0])]

            if data[1] == target_at_index:
                slice = int(data[0])
            else:
                print(f"[-] Could not resume. list is different")

        except Exception as e:
            print(f"[-] Could not read resume.config {e}")
            pass


    #load our config file
    if (config_file[1] != '/'):
        config_file = os.path.dirname(os.path.realpath(__file__)) + "/" + config_file

    try:
        f = open(config_file)
    except Exception as e:
        exit(f"[-] Could not open config file: {e}")
		
    script = f.read()
    f.close()	
    exec(script)

    total_urls = len(targets)
    count = 0
    cache_buster = randomword(10)

    if slice > 0:
        targets = targets[slice:]
        count = slice

    for target in targets:
        #dont want to overwrite valid resume.config with 0 when running single url scan
        if args.file:

            try:
                overwrite_file(str(count) + ":::" + target, "./resume.config")

            except:
                print("Cannot write session info")
                pass

        count = count + 1
        if target.lower().strip()[0:4] != "http":
            target = "https://" + target

        target = target.rstrip()
        #base request
        first_status, first_length = send_request(target, "regular")

        if first_status and first_status != "TIMEOUT":
            
            if not QUIET:
                print("[+] Target URL: " + target + " [" + str(count) + "/" + str(total_urls) + "]")
                print("[+] Base Response: "+ color_code(first_status) + " [" + first_length + "]" )

            for smuggle_name, modified_header in clzero_headers.items():

                if LAST_BYTE_SYNC:
                    reg_status, reg_length = send_request(target, "smuggle", modified_header)

                    if not QUIET:
                        print("--> [" + smuggle_name + "] [LastByte-Sync] : \t" + color_code(reg_status) + " [" + reg_length + "] ")

                #Slower way below
                else:
                    smuggle_status, smuggle_length = send_request(target, "smuggle", modified_header)

                    if not QUIET:
                        print("\r--> [" + smuggle_name + "] : \t" + color_code(smuggle_status) + " [" + smuggle_length + "] ", end="")

    
                    reg_status, reg_length = send_request(target, "regular")

                    if not QUIET:
                        print("\t[Probe]: "+ color_code(reg_status) + " [" + reg_length + "]")

                # 429 - "HTTP code: Too many requests", this will only cause FPs and heartbreak, so we ignore here
                if reg_status != first_status and reg_status != "429" and reg_status != "LASTBYTE_FAIL":

                    request_payload = send_request(target, "generate", modified_header)
                    payload_filename = target.replace("http://", "").replace("https://", "").replace("/", "")
                    payload_filename = payload_filename.replace(".", "_") + smuggle_name.replace("-","_") + ".txt"

                    try:
                        overwrite_file(request_payload , "./payloads/" + payload_filename)

                    except Exception as e:
                        print(f"[-]Could not save payload: {e}")

                    if not QUIET:
                        print(f"[+] {target} may be vulnerable. \r\n[+] Smuggle type: {smuggle_name} \r\n[+]Payload saved to ./payloads/{payload_filename}" )

        else:
            if not QUIET:
                print(f"[-] Something went wrong at: {target} - moving to next host" )
