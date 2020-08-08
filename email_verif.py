import re
import smtplib
import dns.resolver
import socket
# Address used for SMTP MAIL FROM command
from_address = 'arshitjain6@gmail.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

# Email address to verify
inputAddress = input('Please enter the emailAddress to verify:')
address_To_Verify = str(inputAddress)

# Get domain for DNS lookup
split_Address = address_To_Verify.split('@')
domain = str(split_Address[1])
print('Domain:', domain)

# MX record lookup
records = dns.resolver.resolve(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

host = socket.gethostname()

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
server.mail(from_address)
code, message = server.rcpt(str(address_To_Verify))
server.quit()

print(code)
print(message)

# Assume SMTP response 250 is success
if code == 250:
	print('Success')
else:
	print('Fail')