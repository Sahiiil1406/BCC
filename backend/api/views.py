from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Event, User
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm
import os
from django.conf import settings
import hashlib
from django.views.decorators.http import require_POST
from .auth import generate_token, admin_required


EVENTS_DIR = os.path.join(settings.BASE_DIR, "frontend", "events", "2025")
os.makedirs(EVENTS_DIR, exist_ok=True)

def home(request):
    return JsonResponse({"message": "Welcome to the Events API"})


# List all events
def event_list(request):
    events = Event.objects.all().values()
    events_list = list(events)
    return JsonResponse({"events": events_list})

# Create a new event
@csrf_exempt
def event_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            starts_at = parse_datetime(data.get('startsAt'))
            ends_at = parse_datetime(data.get('endsAt'))
            
            if not starts_at or not ends_at:
                return JsonResponse({"error": "Invalid date format"}, status=400)
                
            event = Event.objects.create(
                title=data.get('title'),
                location=data.get('location'),
                variations=data.get('variations'),
                layout=data.get('layout'),
                sponsor=data.get('sponsor'),
                image=data.get('image'),
                startsAt=starts_at,
                endsAt=ends_at,
                permalink=data.get('permalink'),
                price=data.get('price'),
                razorpay_Id=data.get('razorpay_Id')
            )
            
            return JsonResponse({
                "message": "Event created successfully",
                "id": event.id
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

# Update an existing event
@csrf_exempt
def event_update(request, pk):
    try:
        event = get_object_or_404(Event, id=pk)
        
        if request.method == 'PUT' or request.method == 'PATCH':
            try:
                data = json.loads(request.body)
                
                if 'title' in data:
                    event.title = data['title']
                if 'location' in data:
                    event.location = data['location']
                if 'variations' in data:
                    event.variations = data['variations']
                if 'layout' in data:
                    event.layout = data['layout']
                if 'sponsor' in data:
                    event.sponsor = data['sponsor']
                if 'image' in data:
                    event.image = data['image']
                if 'startsAt' in data:
                    starts_at = parse_datetime(data['startsAt'])
                    if starts_at:
                        event.startsAt = starts_at
                if 'endsAt' in data:
                    ends_at = parse_datetime(data['endsAt'])
                    if ends_at:
                        event.endsAt = ends_at
                if 'permalink' in data:
                    event.permalink = data['permalink']
                if 'price' in data:
                    event.price = data['price']
                if 'razorpay_Id' in data:
                    event.razorpay_Id = data['razorpay_Id']
                
                event.save()
                return JsonResponse({"message": "Event updated successfully"})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        
        return JsonResponse({"error": "Only PUT or PATCH methods allowed"}, status=405)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid ID format"}, status=400)

# Delete an event
@csrf_exempt
def event_delete(request, pk):
    try:
        event = get_object_or_404(Event, id=pk)
        
        if request.method == 'DELETE':
            event.delete()
            return JsonResponse({"message": "Event deleted successfully"})
        
        return JsonResponse({"error": "Only DELETE method allowed"}, status=405)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid ID format"}, status=400)

# Get a single event
@csrf_exempt
def event_detail(request, pk):
    try:
        event = get_object_or_404(Event, id=pk)
        
        if request.method == 'GET':
            event_data = {
                'id': event.id,
                'title': event.title,
                'location': event.location,
                'variations': event.variations,
                'layout': event.layout,
                'sponsor': event.sponsor,
                'image': event.image,
                'startsAt': event.startsAt.isoformat(),
                'endsAt': event.endsAt.isoformat(),
                'permalink': event.permalink,
                'price': event.price,
                'razorpay_Id': event.razorpay_Id,
            }
            return JsonResponse(event_data)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid ID format"}, status=400)

@csrf_exempt
@admin_required
def event_create_file(request):
    if request.method == "OPTIONS":
        # Handle CORS preflight request
        response = JsonResponse({"message": "CORS preflight successful"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == 'POST':
        try:
            # Print request body for debugging
            print("Received POST request with body:", request.body.decode('utf-8'))

            # Parse JSON data
            data = json.loads(request.body)

            # Debugging print
            print("Parsed JSON data:", data)

            # Validate and parse dates
            starts_at = parse_datetime(data.get('startsAt'))
            ends_at = parse_datetime(data.get('endsAt'))
            if not starts_at or not ends_at:
                print("Invalid date format")
                return JsonResponse({"error": "Invalid date format"}, status=400)

            # Generate filename
            safe_permalink = data.get('permalink', "").replace("/", "-")
            safe_permalink = safe_permalink[:-1]
            filename = f"{starts_at.strftime('%m-%d')}{safe_permalink}.md"
            filepath = os.path.join(EVENTS_DIR, filename)

            # Format variations
            variations_list = data.get('variations', [])
            if not isinstance(variations_list, list):
                return JsonResponse({"error": "Variations should be a list"}, status=400)
            formatted_variations = "\n".join([f"- {v.strip()}" for v in variations_list])

            # Generate Markdown content
            markdown_content = f"""---
title: "{data.get('title')}"
location: {data.get('location')}
variations:
{formatted_variations}
layout: event
sponsor: {data.get('sponsor')}
image: {data.get('image')}
startsAt: {data.get('startsAt')}
endsAt: {data.get('endsAt')}
permalink: /events/{data.get('permalink')}/
payment:
  price: {data.get('payment', {}).get('price')}
  razorpay: {data.get('payment', {}).get('razorpay')}
---

## Event Details
{data.get('details')}

## What's Included
{data.get('whats_included')}
"""

            # Save to Markdown file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(markdown_content)

            print("File saved successfully:", filepath)

            return JsonResponse({
                "message": "Event saved successfully",
                "file": filename
            }, status=201)

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    print("Method not allowed:", request.method)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

# Hash password utility
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create superuser command
def create_superuser(email, password):
    # Check if user exists
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        user.password = hash_password(password)
        user.is_admin = True
        user.save()
    else:
        User.objects.create(
            email=email,
            password=hash_password(password),
            is_admin=True
        )
    return User.objects.get(email=email)

@csrf_exempt
@require_POST
def admin_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required'}, status=400)
    
    try:
        user = User.objects.get(email=email)
        if user.password == hash_password(password):
            if not user.is_admin:
                return JsonResponse({'error': 'User is not an admin'}, status=403)
                
            token = generate_token(user.id, user.is_admin)
            return JsonResponse({
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

# Example of protected admin route
@csrf_exempt
@admin_required
def admin_dashboard(request):
    # Only admins can access this
    return JsonResponse({'message': 'Welcome to admin dashboard'})