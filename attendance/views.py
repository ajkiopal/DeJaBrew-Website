import csv
import io
import os
from django.shortcuts import render
from .models import Attendance, ImportHistory
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('utak_csv')
        
        fs = FileSystemStorage(location='media/uploads')
        filename = fs.save(csv_file.name, csv_file)

        success_count = 0
        error_count = 0
        skipped_duplicates = 0
        error_log = []

        csv_file.seek(0)
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        try:
            next(io_string) 
        except StopIteration:
            return HttpResponse("Error: The CSV file is empty!")

        for row in csv.reader(io_string, delimiter=','):
            try:
                emp_id = row[0]
                start = row[1]
                end = row[2]

                if Attendance.objects.filter(employee_id=emp_id, start_date_time=start).exists():
                    skipped_duplicates += 1
                    continue

                Attendance.objects.create(
                    employee_id=emp_id,
                    start_date_time=start,
                    end_date_time=end,
                    source_system='UTAK'
                )
                success_count += 1

            except Exception as e:
                error_count += 1
                error_log.append(f"Row error: {str(e)}")

        ImportHistory.objects.create(
            filename=csv_file.name,
            success_count=success_count,
            error_count=error_count,
            status='Completed'
        )

        context = {
            'success': success_count,
            'errors': error_count,
            'duplicates': skipped_duplicates,
            'log': error_log
        }
        return render(request, 'attendance/summary.html', context)

    return render(request, 'attendance/upload.html')

def import_history(request):
    history = ImportHistory.objects.all().order_by('-date_uploaded')
    return render(request, 'attendance/history.html', {'history': history})