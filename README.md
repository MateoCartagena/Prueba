## Diagrama 

![POST](img/diagrama.png)



## Monitoreo y trazabilidad 

¿Qué herramientas utilizarías?

Kiali: Para visualizar la topología del Service Mesh (Istio), mostrando interacciones, latencias y errores entre servicios.
Jaeger: Para trazabilidad distribuida, rastreando el flujo de solicitudes a través de los componentes del sistema.
Prometheus: Para recolectar y almacenar métricas de rendimiento y estado de SolicitudService y API Gateway (Kong).
Grafana: Para crear dashboards que integren métricas de Prometheus y trazas de Jaeger.
¿Qué métricas y trazas capturarías?

Métricas (Prometheus):
Latencia de solicitudes: Tiempo de respuesta de endpoints REST (/solicitudes, /solicitudes/{id}) y llamadas SOAP.
Tasa de errores: Porcentaje de respuestas HTTP 4xx/5xx en SolicitudService y Kong.
Estado del Circuit Breaker: Estado abierto/cerrado para las llamadas al Sistema de Certificación (SOAP).
Límite de tasa: Número de solicitudes bloqueadas por rate limiting en Kong.
Trazas (Jaeger):
ID de solicitud (X-Request-ID): Identificador único propagado en cabeceras HTTP para rastrear el flujo desde el cliente, pasando por Kong, SolicitudService, Sistema Académico (REST) y Sistema de Certificación (SOAP).
Tiempos de servicio: Duración de cada interacción entre servicios (e.g., REST a Sistema Académico, SOAP a Sistema de Certificación).
Errores específicos: Detalles de fallos, como timeouts en SOAP o JWT inválidos.

