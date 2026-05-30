import os
import re
import time
import psycopg2

# CONFIGURACION BASICA PARA EL MONITOREO DE LOGS Y BLOQUEO DE IPS SOSPECHOSAS
LOG_PATH = "/var/log/auth.log"
# Cargamos la IP de confianza desde el entorno
MI_IP_SEGURA = os.getenv("MI_IP_SEGURA")  # ACA IRA LA IP SEGURA


def enviar_telegram(mensaje):
    # ACA IRA LA LOGICA DEL BOT DE TELEGRAM, PERO POR AHORA SOLO ENVIAMOS MENSAJES
    print(f" [TELEGRAM]: {mensaje}")
    print(
        " Centinela 3.0: Despliegue automático exitoso desde GitHub Actions. Monitoreo activo en AWS EC2."
    )


def registrar_y_obtener_intentos(conn, ip):
    try:
        cur = conn.cursor()
        # USAMOS UPSERT PARA PODER REGISTRAR EL PRIMER INTENTO U ACTUALIZAR LOS SIGUIENTES DE MANERA EFICIENTE
        query = """
        INSERT INTO ataques (ip, intentos, ultimo_ataque)
        VALUES (%s, 1, CURRENT_TIMESTAMP)
        ON CONFLICT (ip) 
        DO UPDATE SET intentos = ataques.intentos + 1, ultimo_ataque = CURRENT_TIMESTAMP
        RETURNING intentos;
        """
        cur.execute(query, (ip,))
        intentos = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return intentos
    except Exception as e:
        print(f" Error de DB: {e}")
        conn.rollback()
        return 1


def monitorear():
    print(" [SISTEMA] Centinela 3.0 con bloqueo de IP iniciado..")
    print("CENTINELA MODO DEFENSA ACTIVA...", flush=True)

    # CONEXION A LA BASE DE DATOS POSTEGRESQL
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",  # usamos esta ip para referirnos a la base de datos local, aunque en un entorno real podria ser una IP privada o un servicio gestionado
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    except Exception as e:
        print(f"❌ Error fatal: No se pudo conectar a la DB: {e}")
        return

    # LECTURA DE LOGS (INTENTOS DE INGRESO)EN TIEMPO REAL Y APLICACION DE FILTROS DE SEGURIDAD PARA DETECTAR IPS SOSPECHOSAS Y BLOQUEARLAS
    try:
        with open(LOG_PATH, "r") as f:
            # VAMOS AL FINAL DEL ARCHIVO PARA SOLO LEER LOS NUEVOS INTENTOS DE INGRESO
            f.seek(0, 2)

            while True:
                linea = f.readline()
                if not linea:
                    time.sleep(0.1)
                    continue

                # EL FILTRO DE SEGURIDAD QUE NOS AYUDARA A DETECTAR IPS SOSPECHOSAS
                # Ahora el bot detectará cualquier tipo de rechazo de SSH
                if any(
                    keyword in linea
                    for keyword in [
                        "Failed password",
                        "Connection closed",
                        "Connection reset",
                        "Invalid user",
                        "Disconnected",
                    ]
                ):
                    # 1. Buscamos la IP con Regex
                    busqueda = re.search(r"(\d{1,3}\.){3}\d{1,3}", linea)

                    if busqueda:  # <--- TODO LO QUE SIGUE DEBE ESTAR DENTRO DE AQUÍ
                        ip_atacante = busqueda.group()

                        # --- INICIO DE LA WHITELIST ---
                        if ip_atacante == MI_IP_SEGURA:
                            print(
                                f"✅ Acceso detectado desde IP segura ({ip_atacante}). Ignorando reglas de bloqueo."
                            )
                            continue
                        # --- FIN DE LA WHITELIST ---

                        # LOGICA DE STRIKES
                        strikes = registrar_y_obtener_intentos(conn, ip_atacante)

                        if strikes == 1:
                            msg = f"🟡 STRIKE 1: IP {ip_atacante} detectada. Registro guardado."
                            print(msg)
                            enviar_telegram(msg)

                        elif strikes == 2:
                            msg = f"🔴 BLOQUEO: IP {ip_atacante} baneada por reincidencia."
                            print(msg)
                            os.system(
                                f"sudo iptables -A INPUT -s {ip_atacante} -j DROP"
                            )
                            enviar_telegram(msg)

                        elif strikes > 2:
                            pass  # Ya está bloqueada, no hacemos nada adicional

    except FileNotFoundError:
        print(f"----Error: No se encontró el archivo en {LOG_PATH}")
    except KeyboardInterrupt:
        print("\n----- Centinela desactivado por el usuario.")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    monitorear()
