    for filename in os.listdir(known_images_path):
        if filename.endswith((".jpg", ".png")):
            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(os.path.join(known_images_path, filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

