import csv
import io
from django.shortcuts import render
from django.http import HttpResponse
from .models import Attendance

def upload_csv(request):
    if request.method == 'POST':
        # 1. Grab the file from the webpage
        csv_file = request.FILES.get('utak_csv')
        
        # 2. Check if it's actually a CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Error: This is not a CSV file.")

        # 3. Read and decode the file data
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string) # Skip the first row (the headers)

        # 4. Loop through each row and save to the database
        for row in csv.reader(io_string, delimiter=',', quotechar="|"):
            Attendance.objects.create(
                employee_id=row[0],       # Column 1: ID
                start_date_time=row[1],   # Column 2: Clock In
                end_date_time=row[2],     # Column 3: Clock Out
                source_system='UTAK'
            )
        return HttpResponse("Successfully imported the UTAK logs!")

    return render(request, 'attendance/upload.html')