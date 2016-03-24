from threading import Thread
from router.router import Router
from log.loggersetup import LoggerSetup
from email.mime.text import MIMEText
import logging
import smtplib


class RegisterPublicKey(Thread):
    """
    Sends the Public-Key of the Router to a given Email-Address.
    This is only possible if the key has been read from the wizard-page.
    """""

    def __init__(self, router: Router, config):
        """
        :param router: Router-object
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude, contact,...}
        """
        Thread.__init__(self)
        self.router = router
        self.config = config
        self.daemon = True

    def run(self):
        """
        The Public-Key is send with the Router_node_name to a given email-address.
        """
        logging.info("%sRegister PublicKey ...", LoggerSetup.get_log_deep(1))
        if self.router.node_name == "" or self.router.public_key == "":
            logging.warning("%s[!] The PublicKey doesn't exist", LoggerSetup.get_log_deep(2))
            return
        # message that is send: node-name and public-key
        msg = MIMEText("#" + self.router.node_name + "\n" + self.router.public_key)
        mailserver = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        logging.info("%sLogin " + self.config["email"], LoggerSetup.get_log_deep(2))
        mailserver.login(self.config["email"], self.config["email_password"])
        logging.info("%s[+] Login successful", LoggerSetup.get_log_deep(3))
        logging.info("%sSend Public-Key ...", LoggerSetup.get_log_deep(2))
        mailserver.sendmail(self.config["email"], self.config["key_email"], msg.as_string())
        logging.info("%s[+] Send Public-Key successfully", LoggerSetup.get_log_deep(3))

        mailserver.quit()
