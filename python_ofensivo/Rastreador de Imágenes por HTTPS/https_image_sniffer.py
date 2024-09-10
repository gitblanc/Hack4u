#!/usr/bin/env python3

from mitmproxy import http

def response(packet):
    content_type = print(packet.response.headers.get("content-type", "-")) # para los que no tienen un valor (None)

    try:
        if "image" in content_type:
            url = packet.request.url
            extension = content_type.split("/")[-1]
            
            if extension == "jpeg": # para evitar errores de previsualización de jpeg
                extension = "jpg" 

            file_name = f"images/{url.replace('/', '_').replace(':', '_')}.{extension}"
            image_data = packet.response.content

            with open(file_name, "wb") as f:
                f.write(image_data)

            print(f"[+] Imagen guardada: {file_name}")
    except:
        pass