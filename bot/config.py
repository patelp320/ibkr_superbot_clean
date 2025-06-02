import os

# Email settings
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO  = os.getenv("EMAIL_TO")

# IB Gateway API connection
IB_HOST = os.getenv("IB_HOST", "localhost")
IB_PORT = int(os.getenv("IB_PORT", "4002"))
