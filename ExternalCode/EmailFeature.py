
import smtplib
from datetime import timedelta, date

from_emailID='testmailpythonpro@gmail.com'
password='zfedfjfgeypkfiiz'
to_emailID='testmailpythonpro@gmail.com'

class EmailFeature:

    def sending_mail(df):
        try:
         acc_num=df.account_id
         balance=str(df.balance)

         df.apply(EmailFeature.sending_mail, axis=1)
         df.query("TransactionType == 'Cash'").iloc[0,:][['account_id','balance', '']]

         end_date = str(date.today() + timedelta(days=10))

         smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
         smtpObj.ehlo()
         smtpObj.starttls()

         result = smtpObj.login(from_emailID, password)

         message_body = "Subject: Alert! Please maintain sufficient balance in your bank account \n\n Dear "+acc_num+", \n\n" \
                            "    Your current balance is "+balance+". As per the bank policy, Customers need to maintain an average minimum monthly balance of Rs 800 to keep their savings bank account active. "+ '\n' +"    Please make sure you maintain the minimum balance in your account by "+end_date+" or might face a penalty. "+ '\n\n' +" Thanks."

         smtpObj.sendmail(from_emailID, to_emailID, message_body)
         smtpObj.quit()
        except:
         print("Error in sending mails to accounts")

