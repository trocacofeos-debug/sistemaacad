from firebase_config import db
from datetime import datetime, timedelta
from google.cloud.firestore_v1 import FieldFilter

# =========================
# USUÁRIOS
# =========================

def criar_usuario(uid, nome, telefone, email, tipo="aluno"):
    db.collection("usuarios").document(uid).set({
        "uid": uid,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "tipo": tipo
    })


def buscar_usuario_por_email(email):
    docs = db.collection("usuarios").where("email", "==", email).stream()

    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        return dados

    return None


def buscar_usuario_por_uid(uid):
    doc = db.collection("usuarios").document(uid).get()

    if doc.exists:
        dados = doc.to_dict()
        dados["id"] = doc.id
        return dados

    return None


def listar_usuarios():
    docs = db.collection("usuarios").stream()
    usuarios = []

    for doc in docs:
        dados = doc.to_dict()

        usuarios.append({
            "id": doc.id,
            "uid": dados.get("uid", ""),
            "nome": dados.get("nome", "Sem nome"),
            "telefone": dados.get("telefone", ""),
            "email": dados.get("email", "Sem email"),
            "tipo": dados.get("tipo", "aluno")
        })

    return usuarios


# =========================
# HORÁRIOS AUTOMÁTICOS
# =========================

def gerar_horarios_automaticos(dias=30):
    horarios_fixos = [
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00"
    ]

    docs = db.collection("horarios").stream()
    existentes = set()

    for doc in docs:
        dados = doc.to_dict()
        chave = f"{dados.get('data')}_{dados.get('hora')}"
        existentes.add(chave)

    hoje = datetime.now()

    for i in range(dias):
        data = (hoje + timedelta(days=i)).strftime("%d/%m/%Y")

        for hora in horarios_fixos:
            chave = f"{data}_{hora}"

            if chave not in existentes:
                db.collection("horarios").add({
                    "data": data,
                    "hora": hora,
                    "vagas": 10
                })


def limpar_horarios_passados():
    docs = db.collection("horarios").stream()
    hoje = datetime.now().date()

    for doc in docs:
        dados = doc.to_dict()
        data_str = dados.get("data")

        if not data_str:
            continue

        try:
            data_horario = datetime.strptime(
                data_str,
                "%d/%m/%Y"
            ).date()

            if data_horario < hoje:
                horario_id = doc.id

                # apagar reservas desse horário
                reservas = db.collection("reservas") \
                    .where("horario_id", "==", horario_id) \
                    .stream()

                for reserva in reservas:
                    db.collection("reservas") \
                        .document(reserva.id) \
                        .delete()

                # apagar horário
                db.collection("horarios") \
                    .document(horario_id) \
                    .delete()

        except:
            continue

# =========================
# HORÁRIOS
# =========================

def criar_horario(data, hora, vagas):
    db.collection("horarios").add({
        "data": data,
        "hora": hora,
        "vagas": int(vagas)
    })


def adicionar_horario(data, hora, vagas):
    return criar_horario(data, hora, vagas)


def listar_horarios():
    # limpa horários antigos
    limpar_horarios_passados()

    # garante horários de hoje
    gerar_horarios_automaticos(dias=1)

    docs = db.collection("horarios").stream()
    horarios = []
    hoje = datetime.now().date()

    for doc in docs:
        dados = doc.to_dict()
        data_str = dados.get("data")

        try:
            data_obj = datetime.strptime(
                data_str,
                "%d/%m/%Y"
            ).date()

            # SOMENTE horários de hoje
            if data_obj == hoje:
                horarios.append({
                    "id": doc.id,
                    "data": dados.get("data", "Sem data"),
                    "hora": dados.get("hora", "Sem hora"),
                    "vagas": dados.get("vagas", 0)
                })

        except:
            continue

    horarios.sort(key=lambda x: x["hora"])

    return horarios


def buscar_horario_por_id(horario_id):
    doc = db.collection("horarios").document(horario_id).get()

    if doc.exists:
        dados = doc.to_dict()
        dados["id"] = doc.id
        return dados

    return None


def excluir_horario(horario_id):
    db.collection("horarios").document(horario_id).delete()


def deletar_horario(horario_id):
    return excluir_horario(horario_id)


# =========================
# RESERVAS
# =========================

def criar_reserva(aluno_uid, aluno_nome, horario_id):
    try:
        print("INICIO RESERVA")

        horario_ref = db.collection("horarios").document(horario_id)
        horario_doc = horario_ref.get()

        if not horario_doc.exists:
            print("HORÁRIO NÃO EXISTE")
            return False, "Horário não encontrado"

        horario = horario_doc.to_dict()
        vagas = int(horario.get("vagas", 0))

        print("VAGAS:", vagas)

        if vagas <= 0:
            return False, "Sem vagas disponíveis"

        reservas = db.collection("reservas") \
            .where(filter=FieldFilter("aluno_uid", "==", aluno_uid)) \
            .where(filter=FieldFilter("horario_id", "==", horario_id)) \
            .stream()

        for _ in reservas:
            return False, "Você já reservou este horário"

        data_str = horario.get("data")
        hora_str = horario.get("hora")

        try:
            data_hora = datetime.strptime(
                f"{data_str} {hora_str}",
                "%d/%m/%Y %H:%M"
            )

            aviso_em = data_hora - timedelta(minutes=30)

        except:
            aviso_em = None

        dados_reserva = {
            "aluno_uid": aluno_uid,
            "aluno_nome": aluno_nome,
            "horario_id": horario_id,
            "data": data_str,
            "hora": hora_str,
            "whatsapp_enviado": False
        }

        if aviso_em:
            dados_reserva["aviso_em"] = aviso_em

        db.collection("reservas").add(dados_reserva)

        # diminui vaga
        novas_vagas = max(0, vagas - 1)

        horario_ref.update({
            "vagas": novas_vagas
        })

        print("NOVAS VAGAS:", novas_vagas)
        print("RESERVA OK")

        return True, "Reserva realizada com sucesso"

    except Exception as e:
        print("ERRO FIREBASE:", e)
        return False, str(e)


def adicionar_reserva(aluno_uid, aluno_nome, horario_id):
    return criar_reserva(aluno_uid, aluno_nome, horario_id)


def reservar_horario(aluno_uid, aluno_nome, horario_id):
    return criar_reserva(aluno_uid, aluno_nome, horario_id)

def buscar_reserva_do_aluno(aluno_uid):
    docs = db.collection("reservas") \
        .where("aluno_uid", "==", aluno_uid) \
        .stream()

    for doc in docs:
        dados = doc.to_dict()

        return {
            "id": doc.id,
            "aluno_uid": dados.get("aluno_uid", ""),
            "aluno_nome": dados.get("aluno_nome", ""),
            "horario_id": dados.get("horario_id", ""),
            "data": dados.get("data", ""),
            "hora": dados.get("hora", "")
        }

    return None


def listar_reservas():
    docs = db.collection("reservas").stream()


def listar_reservas():
    docs = db.collection("reservas").stream()
    reservas = []

    for doc in docs:
        dados = doc.to_dict()

        reservas.append({
            "id": doc.id,
            "aluno_uid": dados.get("aluno_uid", ""),
            "aluno_nome": dados.get("aluno_nome", "Sem nome"),
            "horario_id": dados.get("horario_id", None),
            "data": dados.get("data", ""),
            "hora": dados.get("hora", ""),
            "whatsapp_enviado": dados.get("whatsapp_enviado", False)
        })

    return reservas


def listar_reservas_pendentes_whatsapp():
    agora = datetime.now()

    docs = db.collection("reservas") \
        .where("whatsapp_enviado", "==", False) \
        .stream()

    pendentes = []

    for doc in docs:
        dados = doc.to_dict()

        aviso_em = dados.get("aviso_em")

        if aviso_em and aviso_em <= agora:
            dados["id"] = doc.id
            pendentes.append(dados)

    return pendentes


def marcar_whatsapp_enviado(reserva_id):
    db.collection("reservas").document(reserva_id).update({
        "whatsapp_enviado": True
    })


def excluir_reserva(reserva_id):
    reserva_ref = db.collection("reservas").document(reserva_id)
    reserva_doc = reserva_ref.get()

    if not reserva_doc.exists:
        return False

    reserva = reserva_doc.to_dict()
    horario_id = reserva.get("horario_id")

    if horario_id:
        horario_ref = db.collection("horarios").document(horario_id)
        horario_doc = horario_ref.get()

        if horario_doc.exists:
            horario = horario_doc.to_dict()
            vagas = horario.get("vagas", 0)

            horario_ref.update({
                "vagas": vagas + 1
            })

    reserva_ref.delete()

    return True


def deletar_reserva(reserva_id):
    return excluir_reserva(reserva_id)

# =========================
# RELATÓRIOS / DASHBOARD
# =========================

def total_usuarios():
    docs = db.collection("usuarios").stream()
    return sum(1 for _ in docs)


def total_alunos():
    docs = db.collection("usuarios") \
        .where("tipo", "==", "aluno") \
        .stream()

    return sum(1 for _ in docs)


def total_admins():
    docs = db.collection("usuarios") \
        .where("tipo", "==", "admin") \
        .stream()

    return sum(1 for _ in docs)


def total_horarios():
    docs = db.collection("horarios").stream()
    return sum(1 for _ in docs)


def total_reservas():
    docs = db.collection("reservas").stream()
    return sum(1 for _ in docs)


def reservas_do_dia():
    hoje = datetime.now().strftime("%d/%m/%Y")

    docs = db.collection("reservas") \
        .where("data", "==", hoje) \
        .stream()

    reservas = []

    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        reservas.append(dados)

    return reservas


def horarios_com_vagas():
    docs = db.collection("horarios").stream()
    horarios = []

    for doc in docs:
        dados = doc.to_dict()

        if dados.get("vagas", 0) > 0:
            dados["id"] = doc.id
            horarios.append(dados)

    return horarios


def horarios_lotados():
    docs = db.collection("horarios").stream()
    horarios = []

    for doc in docs:
        dados = doc.to_dict()

        if dados.get("vagas", 0) <= 0:
            dados["id"] = doc.id
            horarios.append(dados)

    return horarios


def dashboard():
    return {
        "total_usuarios": total_usuarios(),
        "total_alunos": total_alunos(),
        "total_admins": total_admins(),
        "total_horarios": total_horarios(),
        "total_reservas": total_reservas(),
        "reservas_hoje": len(reservas_do_dia()),
        "horarios_com_vagas": len(horarios_com_vagas()),
        "horarios_lotados": len(horarios_lotados())
    }

def listar_reservas_completas():
    reservas = []

    docs = db.collection("reservas").stream()

    for doc in docs:
        dados = doc.to_dict()

        reservas.append({
            "id": doc.id,
            "aluno_uid": dados.get("aluno_uid", ""),
            "aluno_nome": dados.get("aluno_nome", "Sem nome"),
            "horario_id": dados.get("horario_id", ""),
            "data": dados.get("data", ""),
            "hora": dados.get("hora", "")
        })

    return reservas