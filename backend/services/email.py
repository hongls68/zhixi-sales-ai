"""
智析 AI - 邮件发送服务
"""
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_FROM,
    FRONTEND_URL,
    VERIFICATION_CODE_EXPIRE_MINUTES
)


def generate_verification_code(length: int = 6) -> str:
    """生成数字验证码"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def create_verification_email(email: str, code: str, token: str = None) -> MIMEMultipart:
    """
    创建验证邮件
    
    Args:
        email: 收件人邮箱
        code: 验证码
        token: 验证令牌（用于链接验证）
    
    Returns:
        MIMEMultipart 邮件对象
    """
    # 邮件主题
    subject = "【智析 AI】邮箱验证"
    
    # 构建验证链接
    if token:
        verify_url = f"{FRONTEND_URL}/auth/verify?token={token}"
    else:
        verify_url = None
    
    # 邮件正文（HTML 格式）
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #409eff, #00d4ff);
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .welcome {{
                font-size: 18px;
                color: #303133;
                margin-bottom: 20px;
            }}
            .code-box {{
                background-color: #f0f9ff;
                border: 2px dashed #409eff;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            }}
            .code {{
                font-size: 32px;
                font-weight: bold;
                color: #409eff;
                letter-spacing: 8px;
            }}
            .info {{
                color: #606266;
                font-size: 14px;
                line-height: 1.8;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #409eff, #00d4ff);
                color: #ffffff;
                text-decoration: none;
                padding: 12px 30px;
                border-radius: 6px;
                margin: 20px 0;
                font-weight: 500;
            }}
            .footer {{
                background-color: #f5f7fa;
                padding: 20px 30px;
                text-align: center;
                color: #909399;
                font-size: 12px;
            }}
            .warning {{
                color: #e6a23c;
                font-size: 13px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>智析 AI</h1>
            </div>
            <div class="content">
                <p class="welcome">欢迎注册智析 AI！</p>
                <p class="info">您的邮箱验证码如下：</p>
                
                <div class="code-box">
                    <span class="code">{code}</span>
                </div>
                
                <p class="info">
                    该验证码 <strong>{VERIFICATION_CODE_EXPIRE_MINUTES} 分钟内有效</strong>，<br>
                    请勿将验证码泄露给他人。
                </p>
                
                {f'<p class="info">或者点击以下链接直接验证：<br><a href="{verify_url}" class="button">验证邮箱</a></p>' if verify_url else ''}
                
                <p class="warning">
                    ⚠️ 如果您没有注册智析 AI，请忽略此邮件。
                </p>
            </div>
            <div class="footer">
                <p>© 2024 智析 AI. All rights reserved.</p>
                <p>本邮件由系统自动发送，请勿直接回复。</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = email
    
    # 添加 HTML 内容
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    return msg


def send_verification_email(email: str, code: str, token: str = None) -> bool:
    """
    发送验证邮件
    
    Args:
        email: 收件人邮箱
        code: 验证码
        token: 验证令牌
    
    Returns:
        是否发送成功
    """
    try:
        # 创建邮件
        msg = create_verification_email(email, code, token)
        
        # 连接 SMTP 服务器
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()  # 启用 TLS 加密
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(f"邮件发送失败：SMTP 认证失败，请检查邮箱授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"邮件发送失败：SMTP 错误 - {e}")
        return False
    except Exception as e:
        print(f"邮件发送失败：{e}")
        return False


def send_test_email(to_email: str, content: str) -> bool:
    """
    发送测试邮件
    
    Args:
        to_email: 收件人邮箱
        content: 邮件内容
    
    Returns:
        是否发送成功
    """
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "【智析 AI】测试邮件"
        msg['From'] = SMTP_FROM
        msg['To'] = to_email
        
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"测试邮件发送失败：{e}")
        return False