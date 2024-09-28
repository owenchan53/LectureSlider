import cv2 as cv
import time
import os
from PIL import Image
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, FileResponse
from .models import Video
from .forms import VideoForm

def index(request):
    last_video= Video.objects.last()
    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    
    context= {"video": last_video, "form": form }
    
    return render(request, "lecturesliderwebapp/index.html", context)

def convert(request, vid_id):
    try:
        vid = Video.objects.get(id=vid_id)
        vid_path = os.path.join(settings.MEDIA_ROOT, str(vid.vid_file))

        index = 1
        video_capture = cv.VideoCapture(vid_path)
        ret, previous_frame = video_capture.read()
        if not ret:
            return render(request, 'lecturesliderwebapp/error.html', {'message': 'Could not read video'})

        last_screenshot_time = time.time()
        screenshots = []

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            previous_frame_gray = cv.cvtColor(previous_frame, cv.COLOR_BGR2GRAY)
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame_diff = cv.absdiff(previous_frame_gray, frame_gray)
            threshold = 30
            _, thresholded_frame = cv.threshold(frame_diff, threshold, 255, cv.THRESH_BINARY)
            changed_no = cv.countNonZero(thresholded_frame)

            current_time = time.time()
            if current_time - last_screenshot_time >= 5 and changed_no > 1000:
                screenshot_filename = os.path.join(settings.MEDIA_ROOT, f'slide{index}.png')
                cv.imwrite(screenshot_filename, frame)
                screenshots.append(screenshot_filename)
                index += 1
                last_screenshot_time = current_time

        video_capture.release()
        
        if screenshots:
            first = Image.open(screenshots[0])
            first = first.convert("RGB")
            others = [Image.open(file).convert("RGB") for file in screenshots[1:]]
            pdf_filename = os.path.join(settings.MEDIA_ROOT, "slides.pdf")
            first.save(pdf_filename, save_all=True, append_images=others)

        for s in screenshots:
            os.remove(s)

        return render(request, 'lecturesliderwebapp/converted.html', {'pdf_file': pdf_filename})
    except Exception as e:
        return render(request, 'lecturesliderwebapp/error.html', {'message': str(e)})
    
def download(request, file_path):
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="slides.pdf"'
    return response