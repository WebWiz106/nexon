import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import base64
import ast
from email.message import EmailMessage
from email.mime.text import MIMEText
from datetime import datetime

# Initialize SES client
ses_client = boto3.client("ses", region_name="us-east-1")
# Sending Mail using AWS SES


def convert_to_12_hour_format(time_str):
    # Convert time string to datetime object
    time_obj = datetime.strptime(time_str, "%H:%M")

    # Format the datetime object in 12-hour format with AM/PM
    formatted_time = time_obj.strftime("%I:%M %p")

    return formatted_time


def send_email(subject, body, sender, password, recipients):
    try:
        # Create a MIME message
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        # Attach the HTML body
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# Registration Mail [#1]


def Send_Booking_email(logo, name, hotelName, bookingId, email_to, email_from):
    try:
        Subject = "Booking Initiated with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p><strong>Dear {} [{}], </strong></p><p> We're excited to have you over at {} real soon now. But when you have just arrived, we hate to start bothering you with the formalities that come with travel. </p><p> We have hence moved the check-in process online, and you can complete it with just a few clicks here -&nbsp;Continue with web check-in. </p><p> We recommend you complete the web check-in before your arrival, so you can get to the good part right when you step in. If arriving with a group, we recommend all the group members complete the web check-in. </p><p> <strong><em>PS: Subject to local laws, additional verification steps might be required during check-in. </em></strong></p><p> If you have any questions, feel free to&nbsp;reach out on WhatsApp. </p><p> Wishing you a memorable holiday</p>
                    </div>
                </body>
            </html>
        """.format(
            logo, name, bookingId, hotelName
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Booking_emailToClient(
    logo, hotelName, bookingId, email_to, email_from, booking_details
):
    try:
        Subject = "Booking Initiated with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p><strong>Dear {},</strong></p><p>We're thrilled to inform you that {} has made a booking with us! They will be arriving real soon now. We understand that travel formalities can be a hassle upon arrival, so we've streamlined our check-in process for their convenience.</p><strong>GUEST INFORMATION</strong><br>Guest name:{}<br>checkin-date :{} <br>checkout-date :{} <br>Guest Phone Number:{}<br>Guest Email:{}<br>Guest Address:{}<br>Price:{}<br></p>
                    </div>
                </body>
            </html>
        """.format(
            logo,
            hotelName,
            booking_details.get("guestInfo").get("guestName"),
            booking_details.get("guestInfo").get("guestName"),
            booking_details.get("checkIn"),
            booking_details.get("checkOut"),
            booking_details.get("guestInfo").get("Phone"),
            booking_details.get("guestInfo").get("EmailId"),
            booking_details.get("guestInfo").get("address"),
            booking_details.get("price").get("Total"),
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Booking_confirmation_to_client(
    bookingId,
    email_to,
    customeremail,
    email_from,
    logo,
    name,
    hotelName,
    checkin,
    checkout,
    total,
    phone,
    hotelnumber,
):
    try:
        Subject = "Booking Recieved with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p>Subject: Booking Recieved - {} </p><p> Dear {}, </p><p> We are excited to confirm your booking with us at {}! Here are the details of your reservation: </p><p> Booking ID: {} </p><p>Check-in Date: {}</p><p>Check-out Date:{} </p><p>Total Amount: {} </p><p> Guest Information:</p><p> Name: {} </p><p>Email: {} </p><p>Phone: {} </p><p>We look forward to welcoming you on {}. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at {}. </p><p> Thank you for choosing {}. </p><p>We hope you have a pleasant stay with us! Best regards, </p><p>{}</p><p>{}</p>
                    </div>
                </body>
            </html>
        """.format(
            logo,
            bookingId,
            name,
            hotelName,
            bookingId,
            checkin,
            checkout,
            total,
            name,
            customeremail,
            phone,
            checkin,
            hotelnumber,
            hotelName,
            hotelName,
            hotelnumber,
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Booking_confirmation(
    bookingId,
    email_to,
    email_from,
    logo,
    name,
    hotelName,
    checkin,
    checkout,
    total,
    phone,
    hotelnumber,
):
    try:
        Subject = "Booking Confirmations with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p>Subject: Booking Confirmation - {} </p><p> Dear {}, </p><p> We are excited to confirm your booking with us at {}! Here are the details of your reservation: </p><p> Booking ID: {} </p><p>Check-in Date: {}</p><p>Check-out Date:{} </p><p>Total Amount: {} </p><p> Guest Information:</p><p> Name: {} </p><p>Email: {} </p><p>Phone: {} </p><p>We look forward to welcoming you on {}. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at {}. </p><p> Thank you for choosing {}. </p><p>We hope you have a pleasant stay with us! Best regards, </p><p>{}</p><p>{}</p>
                    </div>
                </body>
            </html>
        """.format(
            logo,
            bookingId,
            name,
            hotelName,
            bookingId,
            checkin,
            checkout,
            total,
            name,
            email_to,
            phone,
            checkin,
            hotelnumber,
            hotelName,
            hotelName,
            hotelnumber,
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Query_recieved(logo, name, hotelName, hotelnumber, email_to, email_from):
    try:
        Subject = "Query Received Successfully"
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p> Dear {}, </p>
                        <p> We have received your query. We appreciate your patience.</p>
                        <p>We will get back to you as soon as possible with a resolution. If you have any further questions or concerns, feel free to reach out to us.</p>
                        <p>Thank you for choosing our service!</p>
                        <p>Best Regards,</p>
                        <p>{}</p>
                        <p>{}</p>
                    </div>
                </body>
            </html>
        """.format(
            logo, name, hotelName, hotelnumber
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Query_recieved_to_client(
    logo,
    hotelName,
    cname,
    cemail,
    cnumber,
    cadult,
    ckid,
    croom,
    checkin,
    checkout,
    city,
    cmessage,
    email_to,
    email_from,
):
    try:
        Subject = "Query Received from " + cname
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p> Dear {}, </p>
                        <p> We have received a query from Booking engine.</p>
                        <p>Please reply to the user for thier query</p>
                        <p>Customer Name - {}</p>
                        <p>Customer EmailId - {}</p>
                        <p>Customer Number - {}</p>
                        <p>Adults - {}</p>
                        <p>Kids - {}</p>
                        <p>Rooms - {}</p>
                        <p>Checkin - {}</p>
                        <p>Checkout - {}</p>
                        <p>Customer City - {}</p>
                        <p>Customer Message - {}</p>
                        
                    </div>
                </body>
            </html>
        """.format(
            logo,
            hotelName,
            cname,
            cemail,
            cnumber,
            cadult,
            ckid,
            croom,
            checkin,
            checkout,
            city,
            cmessage,
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# Lone star mails system


def Send_Booking_confirmation_to_loneadmin(
    bookingId,
    email_to,
    customeremail,
    email_from,
    logo,
    name,
    hotelName,
    checkin,
    checkout,
    total,
    paid,
    phone,
    hotelnumber,
    data,
):
    try:
        starttime = convert_to_12_hour_format(
            data.get("bookedSlots")[0].get("slotstart")
        )
        endtime = convert_to_12_hour_format(data.get("bookedSlots")[-1].get("slotEnd"))
        Subject = "Booking Recieved with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p>Subject: Booking Recieved - {} - {} </p>
                        <p> Dear {}, </p><p> We are excited to confirm  booking with us at {}! Here are the details of reservation: </p>
                        <p> Booking ID: {} </p>
                        <p>Check-in Date: {}</p>
                        <p>Check-out Date:{} </p>
                        <p>Turf Booked: {}</p>
                        <p>Timing Slot: {}-{}</p>
                        <p>Total Amount: {} </p>
                        <p>Amount Paid: {} </p>
                        <p> Guest Information:</p>
                        <p> Name: {} </p>
                        <p>Email: {} </p>
                        <p>Phone: {} </p>
                        <p>We look forward to welcoming you on {}. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at {}. </p>
                        <p> Thank you for choosing {}. </p><p>We hope you have a pleasant stay with us! Best regards, </p><p>{}</p><p>{}</p>
                    </div>
                </body>
            </html>
        """.format(
            logo,
            bookingId,
            name,
            hotelName,
            hotelName,
            bookingId,
            checkin,
            checkout,
            data.get("bookedSlots")[0].get("turfName"),
            starttime,
            endtime,
            total,
            paid,
            name,
            customeremail,
            phone,
            checkin,
            hotelnumber,
            hotelName,
            hotelName,
            hotelnumber,
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Booking_confirmation_to_loneuser(
    bookingId,
    email_to,
    email_from,
    logo,
    name,
    hotelName,
    checkin,
    checkout,
    total,
    paid,
    phone,
    hotelnumber,
    data,
):
    try:
        starttime = convert_to_12_hour_format(
            data.get("bookedSlots")[0].get("slotstart")
        )
        endtime = convert_to_12_hour_format(data.get("bookedSlots")[-1].get("slotEnd"))
        Subject = "Booking Confirmations with " + bookingId
        To = [email_to]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="background-color:#e3e8d8;padding:10px 20px;">
                        <img src={} style="height: 100px;">
                    </div>
                    <div style="padding:20px 0px">
                        <p>Subject: Booking Confirmation - {} </p>
                        <p> Dear {}, </p>
                        <p> We are excited to confirm your booking with us at {}! Here are the details of your reservation: </p>
                        <p> Booking ID: {} </p>
                        <p>Check-in Date: {}</p>
                        <p>Check-out Date:{} </p>
                        <p>Turf Booked: {}</p>
                        <p>Timing Slot: {}-{}</p>
                        <p>Total Amount: {} </p>
                        <p>Paid Amount: {} </p>
                        <p> Guest Information:</p>
                        <p> Name: {} </p>
                        <p>Email: {} </p>
                        <p>Phone: {} </p>
                        <p>We look forward to welcoming you on {}. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at {}. </p>
                        <p>Please Reach 20 minutes before time.</p>
                        <p> Thank you for choosing {}. </p>
                        <p>We hope you have a pleasant stay with us! Best regards, </p>
                        <p>{}</p>
                        <p>{}</p>
                    </div>
                </body>
            </html>
        """.format(
            logo,
            bookingId,
            name,
            hotelName,
            bookingId,
            checkin,
            checkout,
            data.get("bookedSlots")[0].get("turfName"),
            starttime,
            endtime,
            total,
            paid,
            name,
            email_to,
            phone,
            checkin,
            hotelnumber,
            hotelName,
            hotelName,
            hotelnumber,
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def sendContactUsQueryMail(
    hotelName, hotelEmail, Name, Contact, email, Subject, Description, created_from
):
    try:
        Subject = "Query Recieved from {}".format(created_from)
        To = [hotelEmail]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="padding:20px 0px">
                        <p> Dear {}, </p>
                        <p> We have recieved the query from your {}. Here are the details for the query </p>
                        <p>Name: {} </p>
                        <p>Contact: {}</p>
                        <p>Email-Id: {} </p>
                        <p>Message: {}</p>
                        
                        <p>We hope you find the details well.</p>
                        
                    </div>
                </body>
            </html>
        """.format(
            hotelName, created_from, Name, Contact, email, Description
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def sendContactUsQueryReplyMail(
    hotelName, hotelEmail, Name, Contact, email, Subject, Description, reply
):
    try:
        Subject = "Reply to Query Raised on " + hotelName
        To = [email]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="padding:20px 0px">
                        <p> Dear {}, </p>
                        <p> We have recieved the query from you on website of {}. Here are the details for the query </p>
                        <p>Name: {} </p>
                        <p>Contact: {}</p>
                        <p>Email-Id: {} </p>
                        <p>Message: {}</p>
                        
                        <p>{} says:</p>
                        <p>{}</p>
                        
                    </div>
                </body>
            </html>
        """.format(
            Name, hotelName, Name, Contact, email, Description, hotelName, reply
        )
        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def send_job_application_mail(
    hotelName,
    hotelEmail,
    domain,
    contact,
    name,
    email,
    jobTitle,
    cover_letter,
    resume_url,
):
    try:
        Subject = "Query Recieved from Website"
        To = [hotelEmail]
        From = "eazotelservice@gmail.com"
        password = "xshqkvxwkdjumehh"
        body = """
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                        .email-container {{
                            font-family: Arial, sans-serif;
                            padding: 20px;
                            line-height: 1.6;
                        }}
                        .header {{
                            font-size: 20px;
                            font-weight: bold;
                            color: #333;
                        }}
                        .details {{
                            margin-top: 15px;
                            padding: 10px;
                            border: 1px solid #ddd;
                            background-color: #f9f9f9;
                            border-radius: 5px;
                        }}
                        .footer {{
                            margin-top: 20px;
                            font-size: 14px;
                            color: #555;
                        }}
                        .button {{
                            display: inline-block;
                            padding: 10px 15px;
                            margin-top: 10px;
                            font-size: 16px;
                            color: #fff;
                            background-color: #007bff;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <p class="header">New Job Application Received for {}</p>
                        <p>Dear Hiring Manager,</p>
                        <p>A new job application has been submitted for the position of <b>{}</b> at <b>{}</b>. Below are the applicant's details:</p>
                        
                        <div class="details">
                            <p><b>Name:</b> {}</p>
                            <p><b>Contact:</b> {}</p>
                            <p><b>Email:</b> {}</p>
                            <p><b>Cover Letter:</b> {}</p>
                        </div>

                        <p>You can review the applicant's resume by clicking the button below:</p>
                        <a class="button" href="{}" target="_blank">View Resume</a>

                        <p class="footer">Please respond to the candidate at your earliest convenience.</p>

                        <p>Best Regards,</p>
                        <p>Recruitment Team</p>
                    </div>
                </body>
            </html>
        """.format(
            jobTitle,
            jobTitle,
            hotelName,
            name,
            contact,
            email,
            cover_letter,
            resume_url,
        )

        send_email(
            subject=Subject, body=body, sender=From, recipients=To, password=password
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# def send_job_application_mail_reply(
#     hotelName, hotelEmail, domain, name, email, jobTitle
# ):
#     try:
#         subject = "Job Application Received - {}".format(jobTitle)
#         to = [email]
#         from_email = "career@" + domain + ".com"
#         password = "xshqkvxwkdjumehh"

#         body = """
#             <!DOCTYPE html>
#             <html>
#                 <body>
#                     <div style="padding:20px 0px">
#                         <p> Dear {}, </p>
#                         <p>Thank you for applying for the position of <b>{}</b> at our company.</p>
#                         <p>We have received your application and our team is reviewing it. We will get back to you soon.</p>
#                         <p>If you have any questions, feel free to reply to this email.</p>
#                         <br>
#                         <p>Best Regards,</p>
#                         <p>The Hiring Team</p>
#                         <p>{}</p>
#                     </div>
#                 </body>
#             </html>
#         """.format(
#             name, jobTitle, hotelName
#         )

#         send_email(
#             subject=subject,
#             body=body,
#             sender=from_email,
#             recipients=to,
#             password=password,
#         )

#         return True, "Email sent successfully."

#     except Exception as ex:
#         logging.error(f"Error sending email: {ex}")
#         return False, "{}".format(ex)
