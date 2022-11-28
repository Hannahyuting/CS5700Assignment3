from base64 import *
from socket import *
import ssl
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailServer)

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# TLS connection
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recv2 = clientSocket.recv(1024).decode()

sslClientSocket = ssl.wrap_socket(clientSocket)

email = "hannahyuting717@gmail.com"
password = "testpassword"
encodedEmail = b64encode(email.encode())
encodedPassword = b64encode(password.encode())

authorization = "AUTH LOGIN\r\n"

sslClientSocket.send(authorization.encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)

sslClientSocket.send(encodedEmail + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)

sslClientSocket.send(encodedPassword + "\r\n".encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)

# Send MAIL FROM command and print server response.
mailFromCommand = "MAIL FROM: <hannahyuting717@gmail.com>\r\n"
sslClientSocket.send(mailFromCommand.encode())
recv6 = sslClientSocket.recv(1024)
print(recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = "RCPT TO: <zhang.yuti@northeastern.edu>\r\n"
sslClientSocket.send(rcptToCommand.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
sslClientSocket.send(dataCommand.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)
if recv8[:3] != '250':
    print('250 reply not received from server.')

# Send message data.
sslClientSocket.send(msg.encode())

# Message ends with a single period.
sslClientSocket.send(endmsg.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)
if recv9[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
sslClientSocket.send(quitCommand.encode())
recv10 = sslClientSocket.recv(1024)
print(recv10)
if recv10[:3] != '250':
    print('250 reply not received from server.')

sslClientSocket.close()
