import streamlit as st
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Excelerate Analytics, LLC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Custom CSS for dark blue theme
def load_css():
    st.markdown(
        """
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Root variables for dark blue theme */
    :root {
        --primary-dark: #0f172a;
        --primary-blue: #1e293b;
        --secondary-blue: #334155;
        --accent-blue: #3b82f6;
        --light-blue: #60a5fa;
        --gold: #fbbf24;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --success: #10b981;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 4rem 0 6rem 0;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        position: relative;
    }
    
    .hero-title {
        font-size: 6rem;
        font-weight: 1200;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        text-shadow: 0 4px 20px rgba(15, 23, 42, 0.5);
        line-height: 1.1;
    }
    
    .hero-highlight {
        font-size: 2rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        text-shadow: 0 4px 20px rgba(15, 23, 42, 0.5);
        line-height: 1.1;
        background: linear-gradient(45deg, #fbbf24, #60a5fa);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtext {
        font-size: 1.4rem;
        color: #fbbf24;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .hero-description {
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-bottom: 2.5rem;
        text=align: center;
    }
    
    /* Value propositions */
    .value-props {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .value-prop {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .value-prop:hover {
        transform: translateY(-5px);
        background: rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .value-prop h3 {
        color: #f8fafc;
        font-size: 1.2rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    .value-prop p {
        color: #cbd5e1;
        margin: 0;
    }
    
    /* Trust indicators */
    .trust-section {
        background: #1e293b;
        padding: 3rem 0;
        text-align: center;
        border-radius: 20px;
        margin: 3rem 0;
    }
    
    .trust-items {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .trust-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .trust-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    .trust-label {
        font-weight: 600;
        color: #cbd5e1;
    }
    
    /* Form styling */
    .stForm {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.5) !important;
        color: #f8fafc !important;
        border: 2px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #60a5fa) !important;
        color: #f8fafc !important;
        padding: 18px 40px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(45deg, #60a5fa, #3b82f6) !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.2) !important;
        border: 1px solid #10b981 !important;
        color: #10b981 !important;
        border-radius: 12px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.2) !important;
        border: 1px solid #ef4444 !important;
        color: #fca5a5 !important;
        border-radius: 12px !important;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    
    /* Benefits section */
    .benefits-container {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .benefit-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
    }
    
    .benefit-icon {
        width: 24px;
        height: 24px;
        background: linear-gradient(45deg, #10b981, #60a5fa);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        flex-shrink: 0;
        color: #f8fafc;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* Footer */
    .footer {
        background: #171923;
        color: #cbd5e1;
        padding: 2rem 0;
        text-align: center;
        border-radius: 20px;
        margin-top: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem !important;
        }
        
        .value-props {
            grid-template-columns: 1fr !important;
        }
        
        .trust-items {
            grid-template-columns: 1fr !important;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def validate_email(email):
    """Validate email format"""
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number"""
    clean_phone = re.sub(r"[\s\-\(\)\.]+", "", phone)
    return len(clean_phone) >= 10


def send_consultation_email(
    first_name, last_name, email, phone, company, revenue, challenge
):
    """Send email notifications for consultation requests"""
    try:
        # Email configuration (you'll need to set these up)
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)
        sender_email = st.secrets.get("SENDER_EMAIL", "your-email@gmail.com")
        sender_password = st.secrets.get("SENDER_PASSWORD", "your-app-password")
        recipient_email = st.secrets.get(
            "RECIPIENT_EMAIL", "michael@excelerateanalytics.com"
        )

        # Create message to business owner
        business_msg = MIMEMultipart()
        business_msg["From"] = sender_email
        business_msg["To"] = recipient_email
        business_msg["Subject"] = f"🚀 New Analytics Consultation Request - {company}"
        business_msg["Reply-To"] = email

        business_body = f"""
NEW CONSULTATION REQUEST RECEIVED!

Contact Information:
━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {first_name} {last_name}
📧 Email: {email}
📞 Phone: {phone}
🏢 Company: {company}
💰 Revenue Range: {revenue or "Not specified"}

Challenge Description:
━━━━━━━━━━━━━━━━━━━━━━━━
{challenge}

━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Submitted: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

Next Steps:
1. Review their challenge description
2. Contact them within 24 hours
3. Schedule their free strategy session

Reply directly to this email to contact {first_name}.
        """

        business_msg.attach(MIMEText(business_body, "plain"))

        # Create confirmation message to prospect
        prospect_msg = MIMEMultipart()
        prospect_msg["From"] = sender_email
        prospect_msg["To"] = email
        prospect_msg["Subject"] = (
            "Your Free Analytics Consultation Request - Excelerate Analytics"
        )

        prospect_body = f"""Hi {first_name},

Thank you for requesting a free analytics strategy session with Excelerate Analytics!

We've received your consultation request and will contact you within 24 hours to schedule your complimentary 45-minute session.

During your session, we'll:
✅ Audit your current data and analytics setup
✅ Identify your biggest profit opportunities
✅ Create a custom roadmap to increase revenue and reduce costs
✅ Provide actionable steps you can implement immediately

What to Expect Next:
━━━━━━━━━━━━━━━━━━━━━━━━
1. We'll call you within 24 hours to schedule your session
2. Your free consultation will be scheduled at your convenience
3. We'll send you a calendar invite with all the details

Questions? Simply reply to this email or call us at (702) 445-2266.

Looking forward to helping you transform your data into your biggest competitive advantage!

Best regards,
Michael Bacon
Excelerate Analytics, LLC
michael@excelerateanalytics.com
(702) 445-2266

P.S. This consultation is normally $500 but it's completely free with no obligation. We're confident you'll find immediate value in our session!
        """

        prospect_msg.attach(MIMEText(prospect_body, "plain"))

        # Send emails
        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)

            # Send to business owner
            server.sendmail(sender_email, recipient_email, business_msg.as_string())

            # Send confirmation to prospect
            server.sendmail(sender_email, email, prospect_msg.as_string())

        logger.info(f"Emails sent successfully for {first_name} {last_name}")
        return True

    except Exception as e:
        logger.error(f"Failed to send emails: {str(e)}")
        return False


def main():
    load_css()

    # Hero Section
    st.markdown(
        """
    <div class="hero-section">
        <h1 class="hero-title">
            Excelerate Analytics, LLC<br><br>
            <span class="hero-highlight">Turn Your Data Into Your Biggest Competitive Advantage</span>
        </h1>
        <p class="hero-subtext">🚀 Get A FREE Strategy Session Worth $500</p>
        <p class="hero-description">
            Discover exactly how to unlock hidden profits in your data and make decisions that drive real growth. 
            No fluff, just actionable insights tailored to your business.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Value Propositions
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="value-prop">
            <h3>📈 Increase Revenue by 15-30%</h3>
            <p>Identify profit opportunities hiding in your data</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="value-prop">
            <h3>💰 Cut Costs by 20-40%</h3>
            <p>Eliminate waste and optimize operations</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="value-prop">
            <h3>🎯 Make Smarter Decisions</h3>
            <p>Stop guessing, start knowing with data-driven insights</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Trust Section
    st.markdown(
        """
    <div class="trust-section">
        <h2>Trusted by Growing Businesses</h2>
        <div class="trust-items">
            <div class="trust-item">
                <div class="trust-number">50+</div>
                <div class="trust-label">Businesses Transformed</div>
            </div>
            <div class="trust-item">
                <div class="trust-number">$2M+</div>
                <div class="trust-label">In Client Savings Generated</div>
            </div>
            <div class="trust-item">
                <div class="trust-number">100%</div>
                <div class="trust-label">Client Satisfaction Rate</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Consultation Form Section
    st.markdown("## Book Your Free Analytics Strategy Session")
    st.markdown("** Normally $500 - Yours FREE for a Limited Time")
    st.markdown(
        "In just 45 minutes, we'll analyze your current data situation and show you exactly how to unlock hidden profits in your business."
    )

    # Two columns for benefits and form
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### What You'll Get In Your Session:")

        # Create benefits using Streamlit components instead of HTML

        # Benefits as individual items
        benefits = [
            "✅ A complete audit of your current data and analytics setup",
            "✅ Custom roadmap to increase revenue and reduce costs",
            "✅ Identification of your biggest profit opportunities",
            "✅ Actionable steps you can implement immediately",
            "✅ No-obligation consultation - zero pressure",
        ]

        for benefit in benefits:
            st.markdown(
                f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 1rem; padding: 1rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; color: #f8fafc;">
                {benefit}
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.form("consultation_form", clear_on_submit=True):
            st.markdown("### Reserve Your Free Session")

            # Form fields
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name *", key="first_name")
            with col_b:
                last_name = st.text_input("Last Name *", key="last_name")

            email = st.text_input("Business Email *", key="email")
            phone = st.text_input(
                "Phone Number *", key="phone", placeholder="(555) 555-5555"
            )
            company = st.text_input("Company Name *", key="company")

            revenue = st.selectbox(
                "Annual Revenue Range",
                ["", "Under $500K", "$500K - $1M", "$1M - $5M", "$5M - $10M", "$10M+"],
                key="revenue",
            )

            challenge = st.text_area(
                "What's your biggest data challenge? *",
                placeholder="e.g., We're not tracking the right metrics, our reports take forever to create, we can't see where we're losing money...",
                height=120,
                key="challenge",
            )

            # Submit button
            submitted = st.form_submit_button("🚀 Book My Free Session Now")

            if submitted:
                # Validation
                errors = []

                if not first_name.strip():
                    errors.append("First name is required")
                if not last_name.strip():
                    errors.append("Last name is required")
                if not email.strip():
                    errors.append("Email is required")
                elif not validate_email(email):
                    errors.append("Please enter a valid email address")
                if not phone.strip():
                    errors.append("Phone number is required")
                elif not validate_phone(phone):
                    errors.append("Please enter a valid phone number")
                if not company.strip():
                    errors.append("Company name is required")
                if not challenge.strip():
                    errors.append("Please describe your biggest data challenge")

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Process successful form submission
                    try:
                        # Log the submission
                        logger.info(
                            f"New consultation request from {first_name} {last_name} ({email}) at {company}"
                        )

                        # Send emails
                        email_sent = send_consultation_email(
                            first_name,
                            last_name,
                            email,
                            phone,
                            company,
                            revenue,
                            challenge,
                        )

                        if email_sent:
                            st.success(
                                f"🎉 Thank you {first_name}! We've received your consultation request and will contact you within 24 hours to schedule your free strategy session."
                            )
                        else:
                            st.success(
                                f"🎉 Thank you {first_name}! We've received your consultation request. If you don't hear from us within 24 hours, please contact us directly at michael@excelerateanalytics.com or (702) 445-2266."
                            )

                        # Optional: Save to a database or CSV file here

                    except Exception as e:
                        logger.error(f"Error processing form: {str(e)}")
                        st.error(
                            "There was an error processing your request. Please try again or contact us directly at michael@excelerateanalytics.com"
                        )

        st.markdown(
            """
        <p style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-top: 1rem;">
            🔒 Your information is secure and will never be shared. We'll contact you within 24 hours to schedule your session.
        </p>
        """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown(
        """
    <div class="footer">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
            <div>
                <h4 style="color: #fbbf24; margin-bottom: 1rem;">Excelerate Analytics, LLC</h4>
                <p>Transforming data into competitive advantages for ambitious businesses.</p>
            </div>
            <div>
                <h4 style="color: #fbbf24; margin-bottom: 1rem;">Contact Info</h4>
                <p>michael@excelerateanalytics.com<br>
                (702) 445-2266<br>
                Las Vegas, NV</p>
            </div>
        </div>
        <p>© 2025 Excelerate Analytics, LLC. All rights reserved.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
