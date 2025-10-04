# streamlit run main.py
import streamlit as st
import paho.mqtt.client as mqtt
import json

st.set_page_config(page_title="ROS2 알림 모니터", layout="wide")
st.title("📡 ROS2 → MQTT 알림 모니터링")

# 세션 상태 초기화
if "alerts" not in st.session_state:
    st.session_state["alerts"] = []

# MQTT 설정
BROKER = "localhost"   # 브로커 IP로 변경 가능
PORT = 1883
TOPIC = "robot/alerts"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.toast("✅ MQTT 브로커 연결 성공", icon="🟢")
        client.subscribe(TOPIC)
    else:
        st.error("MQTT 연결 실패")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    try:
        parsed = json.loads(data)
    except:
        parsed = {"message": data}
    st.session_state["alerts"].append(parsed)

# MQTT 클라이언트 시작
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

# Streamlit UI
st.subheader("실시간 알림 내역")
alert_container = st.empty()

while True:
    if st.session_state["alerts"]:
        latest = st.session_state["alerts"][-1]
        alert_container.warning(f"🚨 [{latest.get('type', 'unknown')}] {latest.get('message', '')}")
    st.sleep(1)
