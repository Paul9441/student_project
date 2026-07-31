from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Student
from .serializers import StudentSerializer

@extend_schema(
    methods=['GET'],
    summary="List all students",
    description="Retrieve a list of all enrolled students.",
    responses={200: StudentSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    summary="Create a student",
    description="Register a new student record.",
    request=StudentSerializer,
    responses={201: StudentSerializer, 400: OpenApiResponse(description="Bad Request")}
)
@api_view(['GET', 'POST'])
def students(request):

    # GET all students
    if request.method == 'GET':

        students = Student.objects.all()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # CREATE student
    elif request.method == 'POST':

        serializer = StudentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()
            

            return Response(
                {
                    "message": "Student created successfully",
                    "student": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# GET ALL STUDENTS
@extend_schema(
    summary="Get all students",
    description="Retrieve a list of all students.",
    responses={200: StudentSerializer(many=True)}
)
@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#READ ONE
@extend_schema(
    summary="Get student details",
    description="Retrieve detailed information for a specific student by ID.",
    responses={200: StudentSerializer, 404: OpenApiResponse(description="Student not found")}
)
@api_view(['GET'])
def student_detail(request, id):

    try:
        student = Student.objects.get(id=id)

    except Student.DoesNotExist:

        return Response(
            {
                "message": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(student)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


#UPDATE
@extend_schema(
    summary="Update student record",
    description="Update an existing student record by ID.",
    request=StudentSerializer,
    responses={200: StudentSerializer, 400: OpenApiResponse(description="Validation error"), 404: OpenApiResponse(description="Student not found")}
)
@api_view(['PUT'])
def update_student(request, id):

    try:
        student = Student.objects.get(id=id)

    except Student.DoesNotExist:

        return Response(
            {
                "message": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(
        student,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "Student updated successfully",
                "student": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


#DELETE
@extend_schema(
    summary="Delete student record",
    description="Remove a student record from the database by ID.",
    responses={200: OpenApiResponse(description="Student deleted successfully"), 404: OpenApiResponse(description="Student not found")}
)
@api_view(['DELETE'])
def delete_student(request, id):

    try:
        student = Student.objects.get(id=id)

    except Student.DoesNotExist:

        return Response(
            {
                "message": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    student.delete()

    return Response(
        {
            "message": "Student deleted successfully"
        },
        status=status.HTTP_200_OK
    )


