# Usar una imagen ligera y segura de Node.js
FROM node:18-alpine

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar solo los archivos de dependencias (Optimización de la caché de Docker)
COPY package*.json ./

# Instalar dependencias sin dependencias de desarrollo
RUN npm install --omit=dev

# Copiar solo los archivos necesarios usando .dockerignore
COPY . . 

# Crear un usuario no root y ajustar permisos en una sola instrucción RUN
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

# Cambiar al usuario no root para mayor seguridad
USER appuser

# Exponer el puerto de la aplicación
EXPOSE 3000

# Ejecutar la aplicación
CMD ["node", "index.js"]
