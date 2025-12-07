import gradio as gr
import requests
import yaml
from traffic_agent import TrafficAgent
from PIL import Image
import os

# =============================
# 自动将 11.tif 转为 11.png
# =============================
if os.path.exists("11.tif"):
    try:
        img = Image.open("11.tif")
        img.save("11.png")
        print("成功：已自动将 11.tif 转换为 11.png")
    except Exception as e:
        print("警告：11.tif 转换失败 ->", e)

LOGO_FILE = "11.png" if os.path.exists("11.png") else None

# =============================
# 读取配置
# =============================
with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

agent = TrafficAgent()

# =============================
# CSS：动态科技背景
# =============================
CUSTOM_CSS = """
/* 动态背景 */
body {
    margin: 0;
    padding: 0;
    background: linear-gradient(-45deg, #001F3F, #003A70, #0056A6, #0086D1);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 顶部毛玻璃卡片 */
#top-card {
    background: rgba(255, 255, 255, 0.55);
    padding: 25px 10px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    margin-bottom: 12px;
    box-shadow: 0 4px 26px rgba(0,0,0,0.28);
}

/* Logo */
#logo img {
    width: 120px;
    display: block;
    margin: auto;
}

/* 标题 */
#main-title {
    text-align: center;
    color: #ffffff;
    font-size: 34px;
    font-weight: 900;
    text-shadow: 0 0 10px rgba(0,150,255,0.9);
}

#sub-title {
    text-align: center;
    color: #BCE0FF;
    font-size: 14px;
    margin-top: -10px;
}

/* Chatbot 美化 */
.gr-chatbot {
    background: rgba(255,255,255,0.35) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.22);
}

/* 输入框 */
textarea, input {
    background: rgba(255,255,255,0.55) !important;
    border-radius: 12px !important;
}

/* 按钮 */
button {
    background: #006BFF !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
    height: 48px !important;
    box-shadow: 0 0 14px rgba(0,120,255,0.6);
}
"""

# =============================
# Chatbot 处理函数（核心修复）
# =============================
def chat_fn(message, history):
    """处理新消息并返回完整聊天记录"""
    response = agent.ask(message)

    if history is None:
        history = []

    history.append([message, response])
    return history


# =============================
# UI
# =============================
with gr.Blocks(css=CUSTOM_CSS, title="河南大学人工智能学院 · 智能交通问答系统") as demo:

    # 顶部毛玻璃卡片
    with gr.Row(elem_id="top-card"):
        with gr.Column():
            logo_html = f'<div id="logo"><img src="file/{LOGO_FILE}"></div>' if LOGO_FILE else ""
            gr.HTML(f"""
            {logo_html}
            <h1 id="main-title">河南大学人工智能学院 · 智能交通问答系统</h1>
            <p id="sub-title">HENU · School of Artificial Intelligence · TrafficQA System</p>
            """)

    chatbot = gr.Chatbot(label="智能交通问答窗口", height=480)

    msg_box = gr.Textbox(
        label="请输入你的交通问题：",
        placeholder="例如：预测明天早高峰交通拥堵趋势？",
        lines=2
    )

    submit_btn = gr.Button("发送 🚀")

    submit_btn.click(chat_fn, inputs=[msg_box, chatbot], outputs=chatbot)
    msg_box.submit(chat_fn, inputs=[msg_box, chatbot], outputs=chatbot)

    gr.Markdown(
        """
        <div style='text-align:center; color:white; margin-top:20px;'>
        © 2025 河南大学人工智能学院 · Intelligent Traffic Assistant  
        </div>
        """
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
