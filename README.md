# centinela-3.0
Sistema de monitoreo y respuesta automática para servidores Linux.

Centinela 3.0 es un proyecto personal desarrollado como parte de mi proceso de aprendizaje en Linux, DevOps, Redes y Ciberseguridad. Su objetivo es detectar eventos sospechosos en los registros de autenticación del sistema, registrar la actividad en una base de datos PostgreSQL y aplicar medidas automáticas de mitigación.

---

## Funcionalidades

### Monitoreo de logs

Analiza continuamente el archivo `auth.log` de Linux para detectar eventos relacionados con intentos de acceso no autorizados.

### Detección de actividad sospechosa

Identifica patrones como:

* Failed password
* Invalid user
* Connection reset
* Connection closed
* Disconnected

### Registro persistente

Almacena direcciones IP e historial de intentos en PostgreSQL utilizando operaciones UPSERT para detectar reincidencia.

### Lista blanca (Whitelist)

Permite excluir direcciones IP confiables para evitar bloqueos accidentales.

### Bloqueo automático

Cuando una IP supera el umbral definido, Centinela ejecuta reglas de `iptables` para bloquear futuras conexiones.

### Alertas

Genera notificaciones para informar eventos relevantes y acciones de mitigación.

---

## Tecnologías utilizadas

* Python 3
* PostgreSQL
* Docker
* Docker Compose
* Linux (Ubuntu Server)
* Git
* GitHub Actions
* AWS EC2

---

## Arquitectura simplificada

```text
Servidor Linux
      │
      ▼
 auth.log
      │
      ▼
 Centinela 3.0
      │
 ┌────┴────┐
 ▼         ▼
PostgreSQL Alertas
      │
      ▼
Registro histórico
```

---

## Aprendizajes obtenidos

Durante el desarrollo de este proyecto se aplicaron conceptos relacionados con:

* Administración de servidores Linux.
* Automatización mediante Python.
* Persistencia de datos con PostgreSQL.
* Variables de entorno y gestión segura de configuraciones.
* Dockerización de aplicaciones.
* Integración y despliegue continuo mediante GitHub Actions.
* Fundamentos de monitoreo y respuesta ante eventos de seguridad.

---

## Estado del proyecto

MVP funcional desplegado en AWS EC2.

Actualmente sirve como base para el desarrollo de Centinela 4.0, una nueva versión orientada a una arquitectura más modular y escalable.

---

## Autor

Jhenmiller Samaniego Merge

Estudiante de Ingeniería de Sistemas | Linux | Redes Cisco | AWS | DevOps | Ciberseguridad
