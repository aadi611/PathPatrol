"""
Email notification service for PathPatrol
Sends emails on complaint status updates
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


class EmailService:
    """Handle email notifications"""
    
    def __init__(self):
        """Initialize email service with SMTP settings"""
        # Configure these in .env file
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "pathpatrol@example.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.enabled = bool(self.sender_password)  # Only enable if password set
    
    def send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        """Send an email"""
        if not self.enabled:
            print("⚠️ Email service not configured. Set SMTP credentials in .env")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            # Add HTML body
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False
    
    def send_complaint_status_update(
        self, 
        user_email: str, 
        user_name: str, 
        complaint_id: int, 
        location: str,
        old_status: str, 
        new_status: str
    ) -> bool:
        """Send complaint status update email"""
        
        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔧',
            'resolved': '✅',
            'rejected': '❌'
        }
        
        subject = f"PathPatrol: Complaint #{complaint_id} - Status Updated to {new_status.title()}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; }}
                .header {{ background: #3B82F6; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ padding: 20px; color: #333; }}
                .status-badge {{ display: inline-block; padding: 10px 20px; border-radius: 5px; font-weight: bold; margin: 10px 0; }}
                .status-resolved {{ background: #10B981; color: white; }}
                .status-in_progress {{ background: #F59E0B; color: white; }}
                .status-pending {{ background: #6B7280; color: white; }}
                .status-rejected {{ background: #EF4444; color: white; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                .button {{ display: inline-block; background: #3B82F6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛣️ PathPatrol Update</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name},</h2>
                    <p>Your complaint has been updated!</p>
                    
                    <div style="background: #F3F4F6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p><strong>Complaint ID:</strong> #{complaint_id}</p>
                        <p><strong>Location:</strong> {location}</p>
                        <p><strong>Status Update:</strong></p>
                        <p>
                            <span class="status-badge status-{old_status}">{status_emoji.get(old_status, '')} {old_status.replace('_', ' ').title()}</span>
                            →
                            <span class="status-badge status-{new_status}">{status_emoji.get(new_status, '')} {new_status.replace('_', ' ').title()}</span>
                        </p>
                    </div>
                    
                    {'<p style="color: #10B981; font-size: 18px; font-weight: bold;">🎉 Your complaint has been resolved! Thank you for helping make our roads safer.</p>' if new_status == 'resolved' else ''}
                    
                    <p>Thank you for using PathPatrol to report road issues!</p>
                    
                    <a href="http://localhost:8501" class="button">View Your Complaints</a>
                </div>
                <div class="footer">
                    <p>PathPatrol - Mapping Problems, Paving Solutions</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_welcome_email(self, user_email: str, user_name: str, username: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to PathPatrol! 🛣️"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; }}
                .header {{ background: #3B82F6; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ padding: 20px; color: #333; }}
                .feature {{ background: #F3F4F6; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .button {{ display: inline-block; background: #3B82F6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛣️ Welcome to PathPatrol!</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name},</h2>
                    <p>Thank you for joining PathPatrol! Your account has been created successfully.</p>
                    
                    <div style="background: #F3F4F6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p><strong>Username:</strong> {username}</p>
                        <p><strong>Email:</strong> {user_email}</p>
                    </div>
                    
                    <h3>What you can do:</h3>
                    <div class="feature">📸 <strong>Report Potholes:</strong> Upload photos and track complaints</div>
                    <div class="feature">🗺️ <strong>View Map:</strong> See all complaints on interactive map</div>
                    <div class="feature">📊 <strong>Track Progress:</strong> Monitor status of your reports</div>
                    <div class="feature">📈 <strong>View Statistics:</strong> See community impact</div>
                    
                    <p>Help us make roads safer for everyone!</p>
                    
                    <a href="http://localhost:8501" class="button">Get Started</a>
                </div>
                <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
                    <p>PathPatrol - Mapping Problems, Paving Solutions</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_assignment_notification(
        self,
        moderator_email: str,
        moderator_name: str,
        complaint_id: int,
        location: str,
        description: str
    ) -> bool:
        """Notify moderator when complaint is assigned"""
        subject = f"PathPatrol: New Complaint Assigned - #{complaint_id}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; }}
                .header {{ background: #F59E0B; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ padding: 20px; color: #333; }}
                .button {{ display: inline-block; background: #F59E0B; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛡️ New Assignment</h1>
                </div>
                <div class="content">
                    <h2>Hello {moderator_name},</h2>
                    <p>A new complaint has been assigned to you:</p>
                    
                    <div style="background: #FEF3C7; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #F59E0B;">
                        <p><strong>Complaint ID:</strong> #{complaint_id}</p>
                        <p><strong>Location:</strong> {location}</p>
                        <p><strong>Description:</strong> {description}</p>
                    </div>
                    
                    <p>Please review and update the status accordingly.</p>
                    
                    <a href="http://localhost:8501" class="button">View Complaint</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(moderator_email, subject, html_body)


# Singleton instance
email_service = EmailService()
