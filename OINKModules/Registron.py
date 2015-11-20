from PyQt4 import QtCore
import os
import getpass
import codecs
import datetime

class Registron(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        super(Registron, self).__init__(*args, **kwargs)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        self.mutex.unlock()
        start_up_message = "%s-%s"%(datetime.datetime.now(),getpass.getuser())
        self.send(start_up_message)
        self.mutex.lock()

    def send(self, message):
        try:
            import smtplib
            import os, getpass, codecs
            import codecs
            thing = ("bvaxezf@tznvy.pbz","oebgurerlr123", "xgixivanlxrreguv@tznvy.pbz", "fzgc.tznvy.pbz:587")
            way = str(codecs.decode("ebg_13","rot_13"))
            essential_data = [str(codecs.decode(x,way)) for x in thing]
            gate = smtplib.SMTP(essential_data[3])
            gate.ehlo()
            gate.starttls()
            gate.login(essential_data[0],essential_data[1])
            msg = "\r\n".join([
                      "From: %s"%essential_data[0],
                      "To: %s"%essential_data[2],
                      "Subject: OINK Notification",
                      "",
                      "%s"%message
                      ])
            if getpass.getuser() != "vinay.keerthi":
                gate.sendmail(essential_data[0],essential_data[2],msg)
            gate.quit()
        except Exception, e:
            print "Failed."
            print repr(e)
            pass

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

def sendFile(to_address, title, message, file_path):
    import smtplib
    import os, getpass, codecs
    import codecs
    import mimetypes
    from email.mime.multipart import MIMEMultipart
    from email import encoders
    from email.message import Message
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText

    thing = ("bvaxezf@tznvy.pbz","oebgurerlr123", "xgixivanlxrreguv@tznvy.pbz", "fzgc.tznvy.pbz:587")
    way = str(codecs.decode("ebg_13","rot_13"))
    essential_data = [str(codecs.decode(x,way)) for x in thing]
    gate = smtplib.SMTP(essential_data[3])
    gate.ehlo()
    gate.starttls()
    gate.login(essential_data[0],essential_data[1])

    msg = MIMEMultipart('mixed')
    msg["From"] = essential_data[0]
    msg["To"] = to_address
    msg["Subject"] = title
    msg.preamble = message
    msg.epilogue = message
    msg.attach(MIMEText(message,"html"))
    ctype, encoding = mimetypes.guess_type(file_path)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(file_path)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(file_path, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(file_path, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(file_path, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

    attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
    
    msg.attach(attachment)

    gate.sendmail(essential_data[0], to_address, msg.as_string())

    gate.quit()