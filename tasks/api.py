import json
import logging  # Import the logging module

from django.db.models import Q
from django.http import JsonResponse

from .models import Task

# Configure logging
logger = logging.getLogger(__name__)

def api_search(request):
    tasksList = []

    try:
        data = json.loads(request.body)
        query = data['query']

        # Log the received query
        logger.info(f"Received search query: {query}")

        tasks = Task.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(long_description__icontains=query))

        for task in tasks:
            obj = {
                'id': task.id,
                'title': task.title,
                'url': f'/tasks/{task.id}/',  # Use f-string for formatting
            }
            tasksList.append(obj)

        # Log the found tasks
        logger.info(f"Found tasks: {tasksList}")

        return JsonResponse({'tasks': tasksList})

    except Exception as e:
        # Log any exceptions that might occur
        logger.error(f"Error in api_search: {str(e)}")
        return JsonResponse({'error': 'An error occurred during the search.'})
