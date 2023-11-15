# CLZero
A project for fuzzing HTTP/1.1 CL.0 Attack Vectors. 

# About 
Thank you to @albinowax and @defparam, else this tool would not exist. Inspired by the tool [Smuggler](https://github.com/defparam/smuggler) all attack methods adapted from there and https://portswigger.net/research/how-to-turn-security-research-into-profit

For more info see: https://moopinger.github.io/blog/fuzzing/clzero/tools/request/smuggling/2023/11/15/Fuzzing-With-CLZero.html

# Usage

```
usage: clzero.py [-h] [-url URL] [-file FILE] [-index INDEX] [-verbose] [-no-color] [-resume] [-skipread] [-quiet] [-lb] [-config CONFIG] [-method METHOD]

CLZero by Moopinger

optional arguments:
  -h, --help      show this help message and exit
  -url URL        (-u), Single target URL.
  -file FILE      (-f), Files containing multiple targets.
  -index INDEX    (-i), Index start point when using a file list. Default is first line.
  -verbose        (-v), Enable verbose output.
  -no-color       Disable colors in HTTP Status
  -resume         Resume scan from last index place.
  -skipread       Skip the read response on smuggle requests, recommended. This will save a lot of time between requests. Ideal for targets with standard HTTP traffic.
  -quiet          (-q), Disable output. Only successful payloads will be written to ./payloads/
  -lb             Last byte sync method for least request latency. Due to the nature of the request, it cannot guarantee that the smuggle request will be processed first. Ideal for targets with a high
                  amount of traffic, and you do not mind sending multiple requests.
  -config CONFIG  (-c) Config file to load, see ./configs/ to create custom payloads
  -method METHOD  (-m) Method to use when sending the smuggle request. Default: POST
```
single target attack:

* `python3 clzero.py -u https://www.target.com/ -c configs/default.py -skipread`

* `python3 clzero.py -u https://www.target.com/ -c configs/default.py -lb`

Multi target attack:

* `python3 clzero.py -l urls.txt -c configs/default.py -skipread`

* `python3 clzero.py -l urls.txt -c configs/default.py -lb`

# Install

```
git clone https://github.com/Moopinger/CLZero.git
cd CLZero
pip3 install -r requirements.txt
```
