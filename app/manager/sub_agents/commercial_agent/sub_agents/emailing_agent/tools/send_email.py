"""
Send email tool for Gmail integration.
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .gmail_utils import get_gmail_service


def create_html_template(body: str, email_type: str = "general") -> str:
    """
    Create a professional HTML email template matching the voice assistant UI design.
    
    Args:
        body (str): Main email content
        email_type (str): Type of email (general, billing, technical, promotional)
    
    Returns:
        str: HTML formatted email
    """
    # Color scheme matching the website design
    color_schemes = {
        "general": {
            "primary_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "secondary_gradient": "linear-gradient(135deg, #0267fe 0%, #764ba2 100%)",
            "accent_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "bg_primary": "#0f0f23",
            "bg_secondary": "#1a1a3e",
            "glass_bg": "rgba(255, 255, 255, 0.1)",
            "glass_border": "rgba(255, 255, 255, 0.2)",
            "text_primary": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)"
        },
        "billing": {
            "primary_gradient": "linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%)",
            "secondary_gradient": "linear-gradient(135deg, #28a745 0%, #20c997 100%)",
            "accent_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "bg_primary": "#0f1419",
            "bg_secondary": "#1a2332",
            "glass_bg": "rgba(78, 205, 196, 0.1)",
            "glass_border": "rgba(78, 205, 196, 0.2)",
            "text_primary": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)"
        },
        "technical": {
            "primary_gradient": "linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)",
            "secondary_gradient": "linear-gradient(135deg, #dc3545 0%, #c82333 100%)",
            "accent_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "bg_primary": "#1a0f0f",
            "bg_secondary": "#2d1b1b",
            "glass_bg": "rgba(255, 107, 107, 0.1)",
            "glass_border": "rgba(255, 107, 107, 0.2)",
            "text_primary": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)"
        },
        "promotional": {
            "primary_gradient": "linear-gradient(135deg, #b202fe 0%, #764ba2 100%)",
            "secondary_gradient": "linear-gradient(135deg, #6f42c1 0%, #9d02fe 100%)",
            "accent_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "bg_primary": "#140f23",
            "bg_secondary": "#261a3e",
            "glass_bg": "rgba(178, 2, 254, 0.1)",
            "glass_border": "rgba(178, 2, 254, 0.2)",
            "text_primary": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)"
        }
    }
    
    colors = color_schemes.get(email_type, color_schemes["general"])
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alyssa - Your AI Assistant</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        </style>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: {colors['bg_primary']}; color: {colors['text_primary']}; line-height: 1.6;">
        <div style="width: 100%; background: {colors['bg_primary']}; padding: 40px 20px;">
            <!-- Background Effect -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%); pointer-events: none;"></div>
            
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; position: relative; z-index: 1;">
                <!-- Header -->
                <tr>
                    <td style="text-align: center; padding: 40px 30px; background: {colors['primary_gradient']}; border-radius: 20px 20px 0 0; position: relative; overflow: hidden;">
                        <!-- Glass effect overlay -->
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: {colors['glass_bg']}; backdrop-filter: blur(20px); border: 1px solid {colors['glass_border']};"></div>
                        <div style="position: relative; z-index: 2;">
                            <h1 style="color: {colors['text_primary']}; margin: 0; font-size: 2.5rem; font-weight: 700; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">Alyssa</h1>
                            <p style="color: {colors['text_secondary']}; margin: 10px 0 0 0; font-size: 1rem; font-weight: 300;">Your AI Voice Assistant</p>
                        </div>
                    </td>
                </tr>
                
                <!-- Content -->
                <tr>
                    <td style="padding: 40px 30px; background: {colors['bg_secondary']}; border-left: 1px solid {colors['glass_border']}; border-right: 1px solid {colors['glass_border']};">
                        <div style="background: {colors['glass_bg']}; border: 1px solid {colors['glass_border']}; backdrop-filter: blur(20px); border-radius: 16px; padding: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
                            <div style="color: {colors['text_primary']}; line-height: 1.6; font-size: 16px;">
                                {body}
                            </div>
                        </div>
                    </td>
                </tr>
                
                <!-- CTA Section (if promotional) -->
                {'<tr><td style="padding: 30px; background: ' + colors['bg_secondary'] + '; border-left: 1px solid ' + colors['glass_border'] + '; border-right: 1px solid ' + colors['glass_border'] + '; text-align: center;"><a href="#" style="display: inline-block; padding: 16px 32px; background: ' + colors['accent_gradient'] + '; color: white; text-decoration: none; border-radius: 25px; font-weight: 500; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3); transition: all 0.3s ease;">Get Started</a></td></tr>' if email_type == 'promotional' else ''}
                
                <!-- Footer -->
                <tr>
                    <td style="background: {colors['bg_secondary']}; padding: 30px; text-align: center; border-radius: 0 0 20px 20px; border: 1px solid {colors['glass_border']}; border-top: none;">
                        <div style="background: {colors['glass_bg']}; border: 1px solid {colors['glass_border']}; backdrop-filter: blur(10px); border-radius: 12px; padding: 20px;">
                            <p style="margin: 0; color: {colors['text_secondary']}; font-size: 14px; font-weight: 500;">
                                <strong style="color: {colors['text_primary']};">Need Support?</strong><br>
                                📞 1-800-ALYSSA-1 | 📧 support@alyssa-ai.com
                            </p>
                            <p style="margin: 15px 0 0 0; color: rgba(255, 255, 255, 0.5); font-size: 12px;">
                                © 2024 Alyssa AI Assistant. Connecting you to the future.
                            </p>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    return html_template


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
    email_type: str = "general",
    use_html: bool = True,
) -> dict:
    """
    Send a professional email via Gmail matching the voice assistant UI design.

    Args:
        to (str): Recipient email address
        subject (str): Email subject line
        body (str): Email body content
        cc (str): CC recipients (comma-separated if multiple)
        bcc (str): BCC recipients (comma-separated if multiple)
        email_type (str): Type of email (general, billing, technical, promotional)
        use_html (bool): Whether to use HTML formatting

    Returns:
        dict: Information about the sent email or error details
    """
    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Gmail. Please check credentials.",
            }

        # Create message
        if use_html:
            message = MIMEMultipart('alternative')
            
            # Create both plain text and HTML versions
            text_part = MIMEText(body, 'plain')
            html_part = MIMEText(create_html_template(body, email_type), 'html')
            
            message.attach(text_part)
            message.attach(html_part)
        else:
            message = MIMEText(body)

        # Add professional subject prefix based on email type with AI branding
        subject_prefixes = {
            "billing": "[ALYSSA AI - BILLING]",
            "technical": "[ALYSSA AI - TECH SUPPORT]",
            "promotional": "[ALYSSA AI - SPECIAL]",
            "general": "[ALYSSA AI]"
        }
        
        prefixed_subject = f"{subject_prefixes.get(email_type, '[ALYSSA AI]')} {subject}"
        
        message['to'] = to
        message['subject'] = prefixed_subject
        message['from'] = "Alyssa AI Assistant <noreply@alyssa-ai.com>"
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        send_result = service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        return {
            "status": "success",
            "message": "Professional AI assistant email sent successfully",
            "message_id": send_result["id"],
            "thread_id": send_result.get("threadId", ""),
            "email_type": email_type,
        }

    except Exception as e:
        return {"status": "error", "message": f"Error sending email: {str(e)}"}
