import sys
import requests
from datetime import *
import twilio.rest
import smtplib
from email.mime.text import MIMEText
import logging
import json

GOES_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={0}&minimum=1"


def get_loc_date(in_loc_id, in_loc_url, in_curr_appt):
    logging.info("Looking up available appointments")
    logging.debug("Input arguments for get_loc_date %s %s %s" % (in_loc_id, in_loc_url, in_curr_appt))

    try:
        data = requests.get(in_loc_url.format(in_loc_id)).json()
        if not data:
            logging.info("No Appointment available at this location")

        for o in data:
            if o['active']:
                dt = o['startTimestamp']
                dtp = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
                if in_curr_appt > dtp:
                    logging.info("APPOINTMENTS AVAILABLE!!!")
                    logging.debug("Current Available Appointment: %s" % dtp)
                    return str(dtp)
                else:
                    logging.debug("Current Available Appointment: %s" % dtp)
                    logging.info("Appointment after your date :(")

    except OSError:
        logging.critical("Unable to query the API")


def notify_sms(in_dates):
    if smsFlag:
        logging.info("config flag set to true, trying to send SMS")
        try:
            client = twilio.rest.Client(twilioAccountSID, twilioAuthToken)
            message_body = "Appointments available for: " + str(in_dates)
            message = client.messages.create(
                body=message_body,
                to=toPhone,
                from_=fromPhone
            )
        except twilio.rest.TwilioException as ex:
            logging.critical("Unable to send SMS")
            logging.critical(ex)
    else:
        logging.info("Not sending SMS as config flag set to false")


def send_email(in_dates):
    if emailFlag:
        logging.info("config flag set to true, trying to send email")
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromEmail, emailAppPassword)
            msg = MIMEText('Appointment Available, from cron!!')
            msg['Subject'] = "APPOINTMENT AVAILABLE For: " + str(in_dates)
            msg['From'] = fromEmail
            msg['To'] = toEmail
            s.sendmail(fromEmail, toEmail, msg.as_string())
            s.quit()
        except Exception as ex:
            logging.critical("Unable to send email")
            logging.critical(ex)
    else:
        logging.info("Not sending email as config flag set to false")


if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H:%M")
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        stream=sys.stdout
    )
    logging.info("Starting Application")
    try:
        with open("config.json", "r") as myConfig:
            data = myConfig.read()
        jsonObj = json.loads(data)
        currentAppointmentDate = str(jsonObj["current_apt_date"])
        locationId = str(jsonObj["location_id"])
        smsFlag = jsonObj["sms_flag"]
        twilioAccountSID = str(jsonObj["twilio_account_sid"])
        twilioAuthToken = str(jsonObj["twilio_auth_token"])
        fromPhone = str(jsonObj["twilio_from_number"])
        toPhone = str(jsonObj["twilio_to_number"])
        emailFlag = jsonObj["email_flag"]
        fromEmail = str(jsonObj["from_email"])
        toEmail = str(jsonObj["to_email"])
        emailAppPassword = str(jsonObj["from_email_password"])

        currentappt = datetime.strptime(currentAppointmentDate, '%B %d, %Y')
        locationDateAvail = get_loc_date(locationId, GOES_URL, currentappt)

        if locationDateAvail is not None:
            send_email(locationDateAvail)
            notify_sms(locationDateAvail)

    except Exception as e:
        logging.critical("Unable to locate config.json")
        logging.critical(e)



