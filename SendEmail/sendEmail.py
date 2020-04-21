import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from config_reader import ConfigReader
from email.mime.image import MIMEImage

from Visualization.visualization import GenerateGraph


class EmailSender:

    def send_email_to_user(self, recepient_email, message):
        try:

            generate = GenerateGraph()
            generate.india_or_worldwide(message)

            self.config_reader = ConfigReader()
            self.configuration = self.config_reader.read_config()

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            self.msg['From'] = self.configuration['SENDER_EMAIL']

            # storing the receivers email address
            self.msg['To'] = recepient_email

            # storing the subject
            self.msg['Subject'] = self.configuration['EMAIL_SUBJECT']

            # converting DataFrame to HTML in body
            # body = "This will contain attachment"
            body = message.to_html()
            body1 = "Source for World data : https://www.worldometers.info/coronavirus/ " \
                    "Source for India data : https://api.covid19india.org/data.json"

            # attach the body with the msg instance
            self.msg.attach(MIMEText(body, 'html'))
            self.msg.attach(MIMEText(body1, 'plain'))
            self.msg.attach(MIMEImage(open('../Visualization/Active.png', 'rb').read()))
            self.msg.attach(MIMEImage(open('../Visualization/Confirmed.png', 'rb').read()))
            self.msg.attach(MIMEImage(open('../Visualization/Deceased.png', 'rb').read()))
            self.msg.attach(MIMEImage(open('../Visualization/Recovered.png', 'rb').read()))
            self.msg.attach(MIMEImage(open('../Visualization/Pie_chart.png', 'rb').read()))

            # instance of MIMEBase and named as p
            self.p = MIMEBase('application', 'octet-stream')

            # creates SMTP session
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            self.smtp.starttls()

            # Authentication
            self.smtp.login(self.msg['From'], self.configuration['PASSWORD'])

            # Converts the Multipart msg into a string
            # No need to do this
            # self.text = self.msg.as_string()

            # sending the mail
            self.smtp.send_message(self.msg)

            # terminating the session
            self.smtp.quit()
        except Exception as e:
            print('the exception is '+str(e))

    def send_email_to_support(self, cust_name, cust_email, cust_pincode, cust_contact, topic_selected, message):
        try:
            self.config_reader = ConfigReader()
            self.configuration = self.config_reader.read_config()

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            self.msg['From'] = self.configuration['SENDER_EMAIL']

            self.msg['To'] = self.configuration['SALES_TEAM_EMAIL']

            # storing the subject
            self.msg['Subject'] = self.configuration['SALES_TEAM_EMAIL_SUBJECT']

            # string to store the body of the mail
            # body = "This will contain attachment"

            body = message

            body = body.replace('cust_name', cust_name)
            body = body.replace('cust_contact', str(cust_contact))
            body = body.replace('cust_email', cust_email)
            body = body.replace('topic_selected', topic_selected)
            body = body.replace('cust_pincode', str(cust_pincode))

            # attach the body with the msg instance
            self.msg.attach(MIMEText(body, 'html'))

            # instance of MIMEBase and named as p
            self.p = MIMEBase('application', 'octet-stream')

            # creates SMTP session
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            self.smtp.starttls()

            # Authentication
            self.smtp.login(self.msg['From'], self.configuration['PASSWORD'])

            # Converts the Multipart msg into a string
            self.text = self.msg.as_string()

            # sending the mail
            self.support_team_email = self.configuration['SALES_TEAM_EMAIL']

            self.smtp.sendmail(self.msg['From'], self.support_team_email, self.text)

            # terminating the session
            self.smtp.quit()
        except Exception as e:
            print('the exception is ' + str(e))
