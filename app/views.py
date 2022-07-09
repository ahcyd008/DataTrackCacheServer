from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime, os
import zipfile
import json

from app.utils import store, write_text

base_dirname = 'uploads'


def index(request):
    if not os.path.exists(base_dirname):
        os.mkdir(base_dirname)

    files = os.listdir(base_dirname)
    tags = []
    for name in files:
        if name not in ['.', '..']:
            if os.path.isdir(base_dirname + "/" + name):
                tags.append(name)
    return render(request, 'index.html', {"tags": tags})


def zipDir(zip_file, src_dir, parent_dir):
    files = os.listdir(src_dir)
    for name in files:
        if name not in ['.', '..']:
            cur_name = os.path.join(src_dir, name)
            dst_name = os.path.join(parent_dir, name)
            if os.path.isdir(cur_name):
                zipDir(zip_file, cur_name, os.path.join(parent_dir, dst_name))
            else:
                zip_file.write(cur_name, dst_name)


def download(request, tag):
    zip_file = tag + '.zip'
    z = zipfile.ZipFile(base_dirname + "/" + zip_file, 'w', zipfile.ZIP_DEFLATED)
    zip_dir_name = os.path.join(base_dirname, tag)
    zipDir(z, zip_dir_name, "")
    z.close()
    return redirect("/static/" + zip_file)


@csrf_exempt
def upload(request, tag):
    if not tag:
        tag = "default"
    tag = tag.strip()
    msg = ''
    if request.method == 'POST' and request.body:
        content_type = request.content_type
        file_name = None
        if 'filename' in request.GET.keys():
            file_name = request.GET['filename']
        dir_name = base_dirname + "/" + tag
        print("tag:", tag, "file_name:", file_name)
        if file_name:
            if not os.path.exists(os.path.dirname(os.path.join(dir_name, file_name))):
                os.makedirs(os.path.dirname(os.path.join(dir_name, file_name)))
        else:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        if 'application/json' in content_type:
            if not file_name:
                file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".json"
            save_path = dir_name + "/" + file_name
            try:
                json_obj = json.loads(request.body)
                store(json_obj, save_path)
                return JsonResponse({"ret": True})
            except Exception as e:
                msg = 'save json file error!! ' + e
                pass
        elif 'text/csv' in content_type:
            if not file_name:
                file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".csv"
            save_path = dir_name + "/" + file_name
            try:
                write_text(request.body.decode('utf-8'), save_path)
                return JsonResponse({"ret": True})
            except Exception as e:
                msg = 'save csv file error!! ' + e
                pass
        else:
            if not file_name:
                file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            save_path = dir_name + "/" + file_name
            try:
                with open(save_path, 'wb') as save_file:
                    save_file.write(request.body)
                return JsonResponse({"ret": True})
            except Exception as e:
                msg = 'save file error!! ' + e
                pass
    return JsonResponse({"ret": False, "message": msg})
