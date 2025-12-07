# Use official PHP + Apache image
FROM php:8.2-apache

# Enable Apache mod_rewrite (optional but recommended)
RUN a2enmod rewrite

# Copy all PHP files to Apache folder
COPY . /var/www/html/

# Set permissions (avoid 403 errors)
RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html

# Expose the default web port
EXPOSE 80