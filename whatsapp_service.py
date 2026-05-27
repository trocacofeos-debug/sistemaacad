from twilio.rest import Client
import threading
import time

from database import (
    listar_reservas_pendentes_whatsapp,
    buscar_usuario_por_uid,
    marcar_whatsapp_enviado
)

# =========================
# TWILIO CONFIG
# =========================

ACCOUNT_SID = "AC4a82b76828a604e6d3a18963e591c3ea"
AUTH_TOKEN = "798d12bdb981e5b256f333420ec25d24"

FROM_NUMBER = "whatsapp:+14155238886"


# =========================
# ENVIAR WHATSAPP
# =========================

def enviar_whatsapp(numero, mensagem):

    try:

        client = Client(
            ACCOUNT_SID,
            AUTH_TOKEN
        )

        message = client.messages.create(

            body=mensagem,

            from_=FROM_NUMBER,

            to=f"whatsapp:{numero}"
        )

        print("WhatsApp enviado:", message.sid)

        return True

    except Exception as e:

        print("ERRO WHATSAPP:", e)

        return False


# =========================
# VERIFICAR RESERVAS
# =========================

def verificar_lembretes():

    try:

        reservas = listar_reservas_pendentes_whatsapp()

        for reserva in reservas:

            usuario = buscar_usuario_por_uid(
                reserva["aluno_uid"]
            )

            if not usuario:
                continue

            telefone = usuario.get("telefone")

            if not telefone:
                continue

            mensagem = (
                f"Olá {reserva['aluno_nome']} 👋\n\n"
                f"Lembrete do seu horário:\n"
                f"📅 {reserva['data']}\n"
                f"⏰ {reserva['hora']}\n\n"
                f"Te esperamos 😊"
            )

            enviado = enviar_whatsapp(
                telefone,
                mensagem
            )

            if enviado:

                marcar_whatsapp_enviado(
                    reserva["id"]
                )

    except Exception as e:

        print("ERRO LEMBRETES:", e)


# =========================
# LOOP AUTOMÁTICO
# =========================

def iniciar_whatsapp_service():

    def loop():

        while True:

            verificar_lembretes()

            time.sleep(60)

    thread = threading.Thread(
        target=loop,
        daemon=True
    )

    thread.start()