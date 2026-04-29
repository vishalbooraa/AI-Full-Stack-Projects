from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    response = supabase.table("teachers")\
        .select("username")\
        .eq("username", username)\
        .execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    if check_teacher_exists(username):
        return {"error": "Username already exists"}

    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers")\
        .select("teacher_id, username, password, name")\
        .eq("username", username)\
        .execute()

    if not response.data:
        return None

    teacher = response.data[0]

    if check_pass(password, teacher["password"]):
        return teacher

    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name, face_embedding, voice_embedding=None):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(teacher_id, sub_id, sub_name, sub_section):
    data = {
        "teacher_id": teacher_id,
        "subject_code": sub_id,
        "name": sub_name,
        "section": sub_section
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects") \
        .select("*, subject_students(count), attendance_logs(date)") \
        .eq("teacher_id", teacher_id) \
        .execute()

    subjects = response.data

    for sub in subjects:
        # student count
        sub["total_students"] = (
            sub["subject_students"][0]["count"]
            if sub.get("subject_students") and len(sub["subject_students"]) > 0
            else 0
        )

        # class count (based on date)
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len(set([log["date"] for log in attendance]))
        sub["total_classes"] = unique_sessions

        # cleanup
        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_from_subject(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response=supabase.table("subject_students").select("*,subjects(*)").eq("student_id", student_id).execute()
    print("Subjects for student_id", student_id, ":", response.data)
    return response.data

def get_attendance_logs(student_id):
    response=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id", student_id).execute()
    print("Attendance logs for student_id", student_id, ":", response.data)
    return response.data