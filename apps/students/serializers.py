from .models import Student, PaymentStudent
from rest_framework import serializers
from apps.utils.number_validation import extract_and_normalize_phone


class StudentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.title', read_only=True)
    branch_name = serializers.CharField(source='course.branch.name', read_only=True)
    branch_id = serializers.IntegerField(source='course.branch.id', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'start_mount',
                  'email', 'discount', 'discount_of_cash',
                  'phone', 'whatsapp', 'telegram', 'course', 'studies', 'comment',
                  'recruiter', 'create_at', 'contract', 'full_discount', 'remainder_for_current_mount',
                  'whatsapp',  'payment', 'full_payment',
                  'remainder',
                  'currency',     
                  'course_name',
                  'branch_name',
                  'branch_id']

        extra_kwargs = {
            'id': {'read_only': True},
            'create_at': {'read_only': True},
            'full_discount': {'read_only': True},
            'remainder_for_current_mount': {'read_only': True},
            'payment': {'read_only': True},
            'full_payment': {'read_only': True},
            'remainder': {'read_only': True}
        }

    def validate_phone(self, value):
        return extract_and_normalize_phone(value)
    
    def validate_whatsapp(self, value):
        return extract_and_normalize_phone(value)

    def create(self, validated_data):
        try:
            if validated_data['discount'] and validated_data['discount_of_cash']:
                raise serializers.ValidationError('Вы можете выбрать только один вид скидки ПРОЦЕНТ или CУММУ!!!')
        except KeyError:
            pass
        student = Student(**validated_data)
        student.save()
        return student


class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'payment', 'full_payment',
                  'remainder_for_current_mount',
                  'recruiter', 'contract', 'studies']


class PaymentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStudent
        fields = ['id', 'student', 'sum', 'recruiter', 'date', 'comment', 'currency']
        extra_kwargs = {
            'data': {'read_only': True},
            'currency': {'read_only': True}
        }
