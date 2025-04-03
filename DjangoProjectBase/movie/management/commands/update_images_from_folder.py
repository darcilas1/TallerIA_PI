import os
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.conf import settings

class Command(BaseCommand):
    help = "Update movie images in the database from the media folder"

    def handle(self, *args, **kwargs):
        #  Ruta donde están las imágenes
        images_folder = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')

        #  Verifica si la carpeta de imágenes existe
        if not os.path.exists(images_folder):
            self.stderr.write(f"Image folder '{images_folder}' not found.")
            return

        updated_count = 0

        #  Recorremos todas las películas
        for movie in Movie.objects.all():
            #  Construimos el nombre esperado del archivo de imagen
            image_filename = f"m_{movie.title}.png"
            image_path = os.path.join(images_folder, image_filename)

            #  Si la imagen existe, la asignamos a la película
            if os.path.exists(image_path):
                movie.image = f"movie/images/{image_filename}"  # Ruta relativa en `MEDIA_URL`
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title}")

        # Muestra el resultado final
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movie images."))
