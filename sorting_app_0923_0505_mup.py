# 代码生成时间: 2025-09-23 05:05:52
import django
from django.conf import settings
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Define a model for storing sorting algorithm results
class SortingResult(models.Model):
    input_data = models.JSONField()
    sorted_data = models.JSONField()
    algorithm_used = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SortingResult: {self.algorithm_used}"

"""
Views for handling sorting algorithm requests.
"""
class SortingView(View):
    def post(self, request, *args, **kwargs):
        """
        Endpoint to handle POST requests for sorting algorithms.
        
        It expects a JSON payload with the list of items to be sorted and
        the algorithm to use.
        """
        data = request.POST
        try:
            input_data = json.loads(data.get('data'))
            algorithm = data.get('algorithm')
            if not input_data or not algorithm:
                return JsonResponse({'error': 'Invalid input'}, status=400)

            # Call the sorting function based on the algorithm
            sorted_data = self.sort_data(input_data, algorithm)
            result = SortingResult.objects.create(
                input_data=input_data,
                sorted_data=sorted_data,
                algorithm_used=algorithm
            )
            return JsonResponse({'message': 'Sorting successful', 'result_id': result.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def sort_data(self, input_data, algorithm):
        """
        Apply the specified sorting algorithm to the input data.
        
        Supported algorithms: 'bubble_sort', 'quick_sort', etc.
        """
        if algorithm == 'bubble_sort':
            return self.bubble_sort(input_data)
        elif algorithm == 'quick_sort':
            return self.quick_sort(input_data)
        else:
            raise ValueError(f'Unsupported sorting algorithm: {algorithm}')

    def bubble_sort(self, data):
        """
        Perform bubble sort on the input data.
        """
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

    def quick_sort(self, data):
        """
        Perform quick sort on the input data.
        """
        if len(data) <= 1:
            return data
        else:
            pivot = data[0]
            less = [x for x in data[1:] if x <= pivot]
            greater = [x for x in data[1:] if x > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

"""
Define URL patterns for the sorting application.
"""
urlpatterns = [
    path('sort/', method_decorator(csrf_exempt, name='dispatch')(SortingView.as_view()), name='sort'),
]
