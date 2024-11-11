import face_recognition

def check_face_exist(path, image_name):
    test_image = path + image_name
    image = face_recognition.load_image_file(test_image)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 1:
        message = True
    else:
        message = False
    return message
