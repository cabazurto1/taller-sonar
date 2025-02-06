FROM php:7.4-apache

# Instalar extensiones necesarias
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Configurar Apache para usar el directorio public/
COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Activar mod_rewrite para que .htaccess funcione correctamente
RUN a2enmod rewrite

# Establecer el directorio de trabajo y copiar archivos
WORKDIR /var/www/html
COPY . /var/www/html

# Exponer el puerto 80
EXPOSE 80

CMD ["apache2-foreground"]
