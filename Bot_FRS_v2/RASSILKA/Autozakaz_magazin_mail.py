import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Bot_FRS_v2.INI import ini


class avtozakaz_sent():
    def __init__(self):
        self.ya_mail_aps = ini.ya_mail_aps
        self.avtozakaz_mail = ini.avtozakaz_mail
    def sent(self, spisok_email, mes_zagolovok, mes):
        for email in spisok_email:
            msg = MIMEMultipart()
            msg['From'] = self.avtozakaz_mail
            msg['To'] = email
            msg['Subject'] = mes_zagolovok
            message = mes
            msg.attach(MIMEText(message))
            try:
                mailserver = smtplib.SMTP('smtp.yandex.ru',587)
                mailserver.set_debuglevel(True)
            # Определяем, поддерживает ли сервер TLS
                mailserver.ehlo()
            # Защищаем соединение с помощью шифрования tls
                mailserver.starttls()
            # Повторно идентифицируем себя как зашифрованное соединение перед аутентификацией.
                mailserver.ehlo()
                mailserver.login(self.avtozakaz_mail, self.ya_mail_aps)
                mailserver.sendmail(self.avtozakaz_mail, email ,msg.as_string())
                mailserver.quit()
                print("Письмо успешно отправлено")
            except smtplib.SMTPException:
                print("Ошибка: Невозможно отправить сообщение")
        return

spisok = ["Analitik4U@volcov.ru","soldatovas@volcov.ru", "operanalyst@volcov.ru"]
mes_zagolovok = "Тест рассылки для автозаказа по пятницам"
mes = "Текст сообщения"

avtozakaz_sent = avtozakaz_sent()
avtozakaz_sent.sent(spisok_email=spisok, mes_zagolovok=mes_zagolovok , mes=mes)

