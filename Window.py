import tkinter as tk
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os
from tkinter import filedialog
import pyautogui

filename = []


def setFont():
    fontselcted = font_select.get("active")
    print(fontselcted)
    message_content.config(font=(fontselcted, 10))


# TODO solve this
def choose_file_to_attach():
    global filename  # set "filename" as global var
    filename = filedialog.askopenfilenames()  # create a dialog for files to attach
    attach_lable_path.configure(text=filename)  # set the path of the chosen files in a label


def getinfo():
    # ----------- get info --------
    sender = str(from_entry.get())
    reciver = str(to_entry.get())
    title_msg = str(title_message_entry.get())
    msg_content = str(message_content.get("1.0", "end"))
    password = str(pyautogui.password(title='Enter Password',
                                      text='Enter the password of the mail you want to send the mail from'))
    # open a pyautogui password dialog to ask for the sender password
    if "gmail" in sender:
        ans = pyautogui.confirm(
            text='Note!\nif you want to send a mail from gmail you need to enable lees secure apps \n('
                 'https://myaccount.google.com/lesssecureapps)\nor enable two steps verification\nand '
                 'then grant a special password for this service\n at your account settings\npress quit '
                 'to stop the sending process\npress ok to continue', buttons=['OK', 'QUIT'])
            # set a message for the less secure apps in gmail
        if ans == 'QUIT':
            return
        if ans == 'OK':
            server = smtplib.SMTP('smtp.gmail.com', 587)
        else:
            return
    elif "hotmail" in sender:
        server = smtplib.SMTP('smtp.live.com', 587)
    elif "outlook" in sender:
        server = smtplib.SMTP('smtp.office365.com', 537)
    elif "yahoo" in sender:
        server = smtplib.SMTP('smtp.mail.yahoo.com', 465)
    else:
        pyautogui.alert(
            text='your email server is not supported in this service, or the email address is not correct (supported servers:Gmail,Hotmail,Outlook and Yahoo)')  # send a message that the mail address if the sender is not supported
    server.ehlo()
    server.starttls() # create an encrypted connection with the server with TLS method
    server.ehlo()
    while (True):
        try:
            server.login(sender, password)  # try to login to server with sender credentials
            break
        except smtplib.SMTPAuthenticationError:
            password = str(pyautogui.password(title='Error: wrong password', text='please enter again your password'))  # send a message to enter the password again because the app coludn't connect to the server

    # subject = title_msg
    # body = msg_content
    # signture = "Sent by Ofer's mail sender Copyright Reserved Ofer Ovadia 2019 "
    # msg = f"{subject}\n\n{body}\n\n\n\n{signature}"

    msg = MIMEMultipart()
    msg['Subject'] = title_msg
    signature = "\n\n\n\n\n\nSent by Ofer's mail sender Copyright Reserved Ofer Ovadia 2019 "
    text = MIMEText(msg_content + signature)
    msg.attach(text)
    if filename is not None:
        for x in filename:  # attaches every file that choose to be attached
            part = MIMEBase('application', "octet-stream")
            with open(x, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=os.path.basename(x))
            msg.attach(part)
    while True:
        try:
            img_data = open("mail-photo.png", 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename("mail-photo.png"))
            msg.attach(image)
        except FileNotFoundError:
            ok_or_not = pyautogui.confirm(title='File Not Found',
                                          text='The file mail-photo.png not found please read the read me.txt file',
                                          buttons=['OK', 'CONTINUE WITHOUT THE IMAGE'])
            if ok_or_not == 'OK':
                return
            elif ok_or_not == 'CONTINUE WITHOUT THE IMAGE':
                passwithposto = pyautogui.password(title='enter password',
                                                   text='enter the special password to skip the image')
                special_pass = "Mike Golf"
                if passwithposto == special_pass:
                    break
                else:
                    pyautogui.alert(text="WORNG PASSWORD")
    server.sendmail(sender, reciver, str(msg))  # send the mail from the send to the reciver with message (title text and files)
    pyautogui.alert(text='Email Sent!')  # send a message that the email sent
    server.quit()  # stop the connection with the server


win = tk.Tk()
# Title
win.title("Mail Sender")
# Set the window size to 800x800
win.geometry("800x800")
# ------- LABLES ------
title = tk.Label(text="Welcome To Ofer's Mail Sender!", font=("Roboto Light", 16))
title.grid(column=0, row=0)
space = tk.Label()
space.grid(column=0, row=1)
address_from = tk.Label(text="Enter the Email address to send from:", font=("Roboto Light Italic", 14))
address_from.grid(column=0, row=2)
address_to = tk.Label(text="Enter the Email address to send to:", font=("Roboto Light Italic", 14))
address_to.grid(column=0, row=3)
title_message = tk.Label(text="Enter the title of the message:", font=("Roboto Light Italic", 14))
title_message.grid(column=0, row=4)
# ------- Entry Fields --------
from_entry = tk.Entry(width=28)
from_entry.grid(column=1, row=2)
to_entry = tk.Entry(width=28)
to_entry.grid(column=1, row=3)
title_message_entry = tk.Entry(width=28)
title_message_entry.grid(column=1, row=4)
# ------- Text Field ---------
message_content = tk.Text(master=win, height=20, width=40, font=("Roboto Light", 10))
message_content.grid(column=0, row=5)
# --------- Buttons -----------
send = tk.Button(text="Send", font=("Roboto Light", 10), height=4, width=8, command=getinfo)
send.grid(column=2, row=5)
# -------- label frame ---------
attach_frame_lable = tk.LabelFrame(text="attach a file", font=("Roboto Light", 10))
attach_frame_lable.grid(column=0, row=6)
# --------- Attach Button ------------
attach_button = tk.Button(master=attach_frame_lable, text="Attach Files", font=("Roboto Light", 10),
                          command=choose_file_to_attach)
attach_button.grid(column=0, row=7)
# ------------ Attach Label ----------
attach_lable_path = tk.Label(master=attach_frame_lable, text="", font=("Roboto Light", 8))
attach_lable_path.grid(column=0, row=8)
# ---------- Copyright Label -------------
copyrightlb = tk.Label(text="Copyright © 2019 Ofer Ovadia. All Rights Reserved", font=("Roboto Light", 10))
copyrightlb.grid(ipadx=50, ipady=180)
# ------- font selection ---------
font_select = tk.Listbox(selectmode="BROWSE", width=26)
font_select.insert(1, "Roboto Light")
font_select.insert(2, "Times New Roman")
font_select.insert(3, "Roboto Black")
font_select.grid(column=1, row=5)
# ----------- Font Set Button ------------
font_set_button = tk.Button(text="Set Font", width=6, height=3, command=setFont)
font_set_button.grid(column=1, row=6)
# -------- Done or Closed TODO -----------
# TODO add a label of copyright(Done)
# TODO add a label of the less secure apps in gmail(Done, not a label but a message if the to send from is gmail before you send)
# TODO try to pack() both above TODO(Can't pack if you use grid function as well)
# TODO consider to switch from single file attach to multi file attach(Complete the one below before) (DONE, switched)
# TODO fix the problem that you can't send an email from the exe (was an error with photo, fixed, DONE)
# TODO add the signature with the mine(DONE)
# ------------ Unfinished or not Closed TODO -----------------
# TODO fix that if you skip the image it sends a file named "noname"
# TODO after fixing the one above export again without the font staff
# TODO CHANGE THE SKIPPING METHOD IF SENDING THE SOFTWARE TO SOMEONE ELSE
# TODO TRY TO ORGANIZE THE CODE SO NOT EVERY THING WILL BE IN ONE FUNCTION
# TODO add comments to the code (partly done (try to go over the code if there is something else to add))


win.mainloop()
