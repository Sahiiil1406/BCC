from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Event
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm

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
