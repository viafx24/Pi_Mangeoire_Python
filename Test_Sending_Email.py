
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['From'] = 'guillaume.baptist@free.fr'
msg['To'] = 'guillaume.baptist@gmail.com'
msg['Subject'] = 'simple email in python'
message = 'here is the email, Guillaume'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('guillaume.baptist@gmail.com', 'cqfklmiaknthsvbk')

mailserver.sendmail('guillaume.baptist@gmail.com','guillaume.baptist@free.fr',msg.as_string())

mailserver.quit()

# 
# import smtplib
# 
# sender = 'guillaume.baptist@free.fr'
# receivers = 'guillaume.baptist@gmail.com'
# 
# message = """From: From Person <guillaume.baptist@free.fr>
# To: To Person <guillaume.baptist@gmail.com>
# Subject: SMTP e-mail test
# 
# This is a test e-mail message.
# """
# 
# try:
#    smtpObj = smtplib.SMTP('smtp.sfr.fr')
#    smtpObj.sendmail(sender, receivers, message)         
#    print "Successfully sent email"
# except SMTPException:
#    print "Error: unable to send email"