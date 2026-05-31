# 📊 Bebeto Bets Bot

Bot de Telegram para compartir apuestas deportivas, estadísticas y picks en tiempo real.

---

## ✨ Features

✅ Publicación de apuestas simples y combinadas
✅ Cálculo automático de cuotas combinadas
✅ Historial de picks
✅ Estadísticas automáticas (winrate, wins, loses)
✅ Botones interactivos de Telegram
✅ SQLite persistente
✅ Deploy 24/7 en Railway
✅ Sistema admin protegido

---


## 📋 Bets activas

```text
⏳ #12

📌 Betis gana (1.80)
📌 Over 2.5 goles (1.70)

💰 Cuota: 3.06
📊 Resultado: pendiente
```

---

## 📈 Estadísticas

```text
📊 Estadísticas

📌 Total apuestas: 52
✅ Aciertos: 38
❌ Fallos: 14
📈 Winrate: 73.08%
```

---

# 🚀 Tech Stack

* Python
* python-telegram-bot
* SQLite
* Railway

---

# ⚙️ Instalación local

## 1️⃣ Clonar repositorio

```bash

git clone https://github.com/MitoNacho/telegram-bets-bot.git

```

---

## 2️⃣ Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```


## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Variables de entorno

### Windows CMD

```bash
set TOKEN=TU_TOKEN
set ADMIN_ID=TU_ID
```

### PowerShell

```powershell
$env:TOKEN="TU_TOKEN"
$env:ADMIN_ID="TU_ID"
```

---

## 5️⃣ Ejecutar bot

```bash
python main.py
```

---

# ☁️ Deploy en Railway

1. Crear proyecto en Railway
2. Conectar repositorio GitHub
3. Añadir variables:

| KEY      | VALUE       |
| -------- | ----------- |
| TOKEN    | token_bot   |
| ADMIN_ID | telegram_id |

4. Crear Volume persistente:

```text
/data
```

5. Deploy automático 🚀

---

# 🤖 Comandos

| Comando         | Descripción                  |
| --------------- | ---------------------------- |
| `/start`        | Iniciar bot                  |
| `/bets`         | Ver apuestas activas         |
| `/recientes`    | Ver historial                |
| `/estadisticas` | Ver estadísticas             |
| `/apuesta`      | Crear apuesta (admin)        |
| `/resultado`    | Actualizar resultado (admin) |
| `/reset`        | Resetear apuestas (admin)    |

---

# 🔒 Seguridad

Las funciones de administración están protegidas mediante:

```python
ADMIN_ID
```

El token del bot se gestiona mediante variables de entorno.

---


# 🧠 Autor

Desarrollado por Nacho Naves 

---


