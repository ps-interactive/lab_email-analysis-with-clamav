import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_stealth_phish():
    # --- CONFIGURATION ---
    filename = "Vendor_Invoice_7732.pdf" 
    sender = "billing@trusted-vendor.net"
    recipient = "accounts@globomantics.com"
    subject = "Invoice #7732 - Payment Pending"

    # --- 1. BUILD THE FAKE PDF CONTENT ---
    # We use a valid PDF Object structure.
    # ClamAV parses "stream" blocks inside PDFs and scans them.
    
    pdf_header = b"%PDF-1.7\n"
    
    # This looks like a standard PDF object to the parser
    # We wrap the EICAR string in 'stream' tags
    malicious_stream = (
        b"1 0 obj\n"
        b"<< /Length 68 >>\n"
        b"stream\n"
        b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*\n"
        b"endstream\n"
        b"endobj\n"
    )
    
    pdf_footer = b"\n%%EOF\n"

    # Combine to make the payload
    # 'file' command sees %PDF (Header) -> Says "PDF Document"
    # 'clamscan' sees 'stream' -> Extracts it -> Finds EICAR -> Says "Infected"
    malicious_payload = pdf_header + malicious_stream + pdf_footer

    # --- 2. CONSTRUCT THE EMAIL ---
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = email.utils.formatdate(localtime=True)

    body = """
    Hello Team,

    Please find the attached invoice for the services rendered in Q3. 
    Ensure this is processed by Friday to avoid late fees.

    Best,
    Vendor Billing Team
    """
    msg.attach(MIMEText(body, 'plain'))

    # --- 3. ATTACH THE PAYLOAD ---
    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(malicious_payload)
    
    # Encode in Base64 
    encoders.encode_base64(attachment)
    
    # Set headers 
    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(attachment)

    # --- 4. SAVE FILE ---
    output_file = "/home/ubuntu/lab/stealth_invoice.eml"
    with open(output_file, 'w') as f:
        f.write(msg.as_string())

    print(f"[+] Generated '{output_file}'")
    print(f"[+] Attachment: {filename} (PDF Header + Hidden Stream EICAR)")

if __name__ == "__main__":
    create_stealth_phish()
