from flask import Flask, request, make_response, render_template
import pandas as pd
import json
import os
from flask_cors import cross_origin
from SendEmail.sendEmail import EmailSender
from logger import logger
from email_templates import template_reader

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return 'Welcome, why are you here'

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID = req.get('responseId')

    result = req.get("queryResult")

    user_says = result.get("queryText")                       # User says
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    cust_name = parameters.get("cust_name")                   # Customer name
    #print(cust_name)
    cust_contact = parameters.get("cust_mob")                 # Customer Contact
    cust_email = parameters.get("cust_email")                 # Customer Email
    cust_email = cust_email.lower()                           # Just in case people accessing from phone mistype
    cust_pincode = parameters.get("cust_pincode")             # Customer Pincode
    topic_selected = parameters.get("topic_selected")         # Topic Selected

    intent = result.get("intent").get('displayName')
    if intent == 'topic_selected':

        email_sender = EmailSender()
        template = template_reader.TemplateReader()

        email_message = template.read_course_template(topic_selected)
        email_sender.send_email_to_user(cust_email, email_message[0])
        email_file_support = open("email_templates/send_to_mom_template.html", "r")
        email_message_support = email_file_support.read()
        email_sender.send_email_to_support(cust_name=cust_name, cust_contact=cust_contact, cust_pincode=cust_pincode,
                                           cust_email=cust_email, topic_selected=topic_selected,
                                           message=email_message_support)
        fulfillmentText = "Thank you for your interest " \
                          "-------------------" \
                          f"{email_message[1]}" \
                          "-------------------" \
                          "You will shortly receive a mail with the details " \
                          "Do you have any queries regarding coronavirus or COVID-19 ?"
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }

    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(debug=False, port=port, host='0.0.0.0')
