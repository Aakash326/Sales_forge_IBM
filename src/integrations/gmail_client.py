"""
Gmail API Integration for Sales Forge Platform
Provides email sending capabilities for automated outreach
"""

import base64
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("⚠️ Gmail integration requires google-api-python-client. Install with: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
    raise

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

logger = logging.getLogger(__name__)

class GmailClient:
    """
    Gmail API client for sending emails from Sales Forge platform
    """
    
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        """
        Initialize Gmail client
        
        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load access token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2
        
        Returns:
            bool: True if authentication successful
        """
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    logger.error(f"Credentials file not found: {self.credentials_path}")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.authenticated = True
            logger.info("✅ Gmail authentication successful")
            return True
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            return False
    
    def create_message(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        from_email: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict]] = None,
        html_body: Optional[str] = None
    ) -> Dict:
        """
        Create email message
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            from_email: Sender email (optional, uses authenticated account)
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of attachment dicts with 'path' and 'filename'
            html_body: HTML version of email body
            
        Returns:
            Dict: Email message ready to send
        """
        if html_body:
            msg = MIMEMultipart('alternative')
        elif attachments:
            msg = MIMEMultipart()
        else:
            msg = MIMEText(body)
            msg['to'] = to
            msg['subject'] = subject
            if from_email:
                msg['from'] = from_email
            return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
        
        # Multipart message
        msg['to'] = to
        msg['subject'] = subject
        if from_email:
            msg['from'] = from_email
        
        if cc:
            msg['cc'] = ', '.join(cc)
        if bcc:
            msg['bcc'] = ', '.join(bcc)
        
        # Add text parts
        if body:
            msg.attach(MIMEText(body, 'plain'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                if 'path' in attachment and os.path.exists(attachment['path']):
                    with open(attachment['path'], 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    
                    encoders.encode_base64(part)
                    filename = attachment.get('filename', os.path.basename(attachment['path']))
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {filename}'
                    )
                    msg.attach(part)
        
        return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    
    def send_email(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        from_email: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict]] = None,
        html_body: Optional[str] = None
    ) -> Dict:
        """
        Send email via Gmail API
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            from_email: Sender email (optional)
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of attachment dicts
            html_body: HTML version of email body
            
        Returns:
            Dict: Response from Gmail API or error info
        """
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Gmail authentication failed"}
        
        try:
            message = self.create_message(
                to=to,
                subject=subject,
                body=body,
                from_email=from_email,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                html_body=html_body
            )
            
            result = self.service.users().messages().send(
                userId='me', body=message
            ).execute()
            
            logger.info(f"✅ Email sent successfully to {to}")
            return {
                "success": True,
                "message_id": result.get('id'),
                "to": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            }
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            logger.error(f"Gmail API error: {error_details}")
            return {
                "success": False,
                "error": f"Gmail API error: {error_details.get('error', {}).get('message', 'Unknown error')}",
                "error_code": e.resp.status
            }
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_sales_outreach_email(
        self,
        lead_data: Dict,
        outreach_content: Dict,
        template_type: str = "initial_outreach"
    ) -> Dict:
        """
        Send personalized sales outreach email
        
        Args:
            lead_data: Lead information (name, email, company, etc.)
            outreach_content: Generated outreach content from agents
            template_type: Type of outreach template
            
        Returns:
            Dict: Send result
        """
        
        # Extract lead information
        contact_name = lead_data.get('contact_name', 'there')
        contact_email = lead_data.get('contact_email')
        company_name = lead_data.get('company_name', 'your company')
        
        if not contact_email:
            return {"success": False, "error": "No contact email provided"}
        
        # Generate personalized subject
        subject = self._generate_subject(lead_data, outreach_content, template_type)
        
        # Generate email body
        body = self._generate_email_body(lead_data, outreach_content, template_type)
        html_body = self._generate_html_body(lead_data, outreach_content, template_type)
        
        # Send email
        return self.send_email(
            to=contact_email,
            subject=subject,
            body=body,
            html_body=html_body
        )
    
    def _generate_subject(self, lead_data: Dict, outreach_content: Dict, template_type: str) -> str:
        """Generate personalized email subject"""
        
        company_name = lead_data.get('company_name', 'your company')
        contact_name = lead_data.get('contact_name', '').split()[0] if lead_data.get('contact_name') else ''
        
        subjects = {
            "initial_outreach": f"Strategic opportunity for {company_name}",
            "follow_up": f"Following up on {company_name}'s growth initiatives",
            "strategic_proposal": f"Strategic proposal for {company_name}",
            "roi_focused": f"ROI opportunity: {company_name} growth acceleration"
        }
        
        # Use custom subject from outreach content if available
        if outreach_content.get('email_subject'):
            return outreach_content['email_subject']
        
        return subjects.get(template_type, f"Partnership opportunity for {company_name}")
    
    def _generate_email_body(self, lead_data: Dict, outreach_content: Dict, template_type: str) -> str:
        """Generate personalized email body (plain text)"""
        
        contact_name = lead_data.get('contact_name', '').split()[0] if lead_data.get('contact_name') else 'there'
        company_name = lead_data.get('company_name', 'your company')
        
        # Use custom email from outreach content if available
        if outreach_content.get('personalized_email'):
            return outreach_content['personalized_email']
        
        # Generate template-based email
        body = f"""Hi {contact_name},

I hope this email finds you well. I've been researching {company_name} and I'm impressed by your work in the {lead_data.get('industry', 'industry')}.

"""
        
        # Add pain points if identified
        if lead_data.get('pain_points'):
            body += "I noticed you might be facing challenges with:\n"
            for pain_point in lead_data.get('pain_points', [])[:2]:
                body += f"• {pain_point}\n"
            body += "\n"
        
        # Add value proposition
        body += """We've helped similar companies achieve:
• 40% improvement in operational efficiency
• 60% reduction in manual processes
• 25% increase in revenue growth

"""
        
        # Add CTA
        body += f"""Would you be open to a brief 15-minute conversation about how we could help {company_name} achieve similar results?

I'm available for a call this week at your convenience.

Best regards,
Sales Team

P.S. I'd be happy to share a case study of how we helped a similar company in your industry."""
        
        return body
    
    def _generate_html_body(self, lead_data: Dict, outreach_content: Dict, template_type: str) -> str:
        """Generate personalized HTML email body"""
        
        contact_name = lead_data.get('contact_name', '').split()[0] if lead_data.get('contact_name') else 'there'
        company_name = lead_data.get('company_name', 'your company')
        
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .highlight {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 15px 0; }}
        .benefits {{ background: #f1f8e9; padding: 15px; border-radius: 8px; }}
        .cta {{ background: #1976d2; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; display: inline-block; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Strategic Opportunity for {company_name}</h2>
    </div>
    
    <p>Hi {contact_name},</p>
    
    <p>I hope this email finds you well. I've been researching <strong>{company_name}</strong> and I'm impressed by your work in the {lead_data.get('industry', 'industry')}.</p>
"""
        
        # Add pain points if identified
        if lead_data.get('pain_points'):
            html += '<div class="highlight">'
            html += '<h3>Challenges We Can Address:</h3><ul>'
            for pain_point in lead_data.get('pain_points', [])[:2]:
                html += f"<li>{pain_point}</li>"
            html += '</ul></div>'
        
        # Add benefits
        html += '''
    <div class="benefits">
        <h3>Results We've Delivered:</h3>
        <ul>
            <li><strong>40% improvement</strong> in operational efficiency</li>
            <li><strong>60% reduction</strong> in manual processes</li>
            <li><strong>25% increase</strong> in revenue growth</li>
        </ul>
    </div>
    
    <p>Would you be open to a brief 15-minute conversation about how we could help {company_name} achieve similar results?</p>
    
    <a href="mailto:sales@example.com?subject=Meeting Request - {company_name}" class="cta">Schedule a Call</a>
    
    <p>I'm available for a call this week at your convenience.</p>
    
    <p>Best regards,<br>
    <strong>Sales Team</strong></p>
    
    <p><em>P.S. I'd be happy to share a case study of how we helped a similar company in your industry.</em></p>
    
</body>
</html>
'''
        
        return html
    
    def get_sent_emails(self, query: str = "", max_results: int = 10) -> List[Dict]:
        """
        Get sent emails from Gmail
        
        Args:
            query: Gmail search query
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List of sent email information
        """
        if not self.authenticated:
            if not self.authenticate():
                return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['SENT'],
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            sent_emails = []
            
            for message in messages:
                msg_detail = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata',
                    metadataHeaders=['To', 'Subject', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
                
                sent_emails.append({
                    'id': message['id'],
                    'to': headers.get('To', ''),
                    'subject': headers.get('Subject', ''),
                    'date': headers.get('Date', ''),
                    'thread_id': msg_detail.get('threadId', '')
                })
            
            return sent_emails
            
        except Exception as e:
            logger.error(f"Failed to retrieve sent emails: {e}")
            return []

    def setup_credentials(self, client_id: str, client_secret: str) -> bool:
        """
        Setup Gmail API credentials programmatically
        
        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            
        Returns:
            bool: True if credentials created successfully
        """
        
        credentials_data = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        try:
            with open(self.credentials_path, 'w') as f:
                json.dump(credentials_data, f, indent=2)
            
            logger.info(f"✅ Gmail credentials saved to {self.credentials_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            return False


def create_gmail_client(credentials_path: str = "gmail_credentials.json") -> GmailClient:
    """
    Factory function to create Gmail client
    
    Args:
        credentials_path: Path to Gmail credentials file
        
    Returns:
        GmailClient: Configured Gmail client
    """
    return GmailClient(credentials_path=credentials_path)