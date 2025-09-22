from django.shortcuts import render
import requests, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user_message = body.get("message", "")
            
            # Combinar el system prompt con el mensaje del usuario
            system_prompt = """
            Eres un asistente experto en probabilidad, estadística y minería de datos.
            """
            
            # Mensaje completo combinando contexto y pregunta del usuario
            full_message = f"{system_prompt}\n\nPregunta del usuario: {user_message}"
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            
            payload = {
                "contents": [
                    {
                        "role": "user", 
                        "parts": [{"text": full_message}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            data = response.json()
            
            # Mejor manejo de la respuesta
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    reply = parts[0].get("text", "No se pudo obtener respuesta.")
                else:
                    reply = "Respuesta vacía del modelo."
            else:
                reply = "No se recibieron candidatos de respuesta."
            
            return JsonResponse({"reply": reply})
            
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Error: Formato JSON inválido"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"reply": f"Error de conexión: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"reply": f"Error inesperado: {str(e)}"}, status=500)
    
    return JsonResponse({"reply": "Método no permitido"}, status=405)
