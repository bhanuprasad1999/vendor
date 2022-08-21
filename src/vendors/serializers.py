from vendors.models import *
from rest_framework import serializers


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = VendorModel
        fields = ['id', 'name', 'location', 'skills', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'] = SkillSerializer(
            many=True, required=False, context=self.context)

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        object = VendorModel.objects.create(**validated_data)
        for skill in skills_data:
            t, _ = Skills.objects.get_or_create(skill_name=skill["skill_name"])
            object.skills.add(t)
            print(skills_data)
        return object

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', [])
        instance.name = validated_data.get(
            'name', instance.name)
        instance.location = validated_data.get(
            'location', instance.location)
        instance.rating = validated_data.get(
            'rating', instance.rating)
        vendor = VendorModel.objects.get(id=instance.id)
        skill_list = [x for x in vendor.skills.all()]
        for tag in skills_data:
            s, _ = Skills.objects.get_or_create(skill_name=tag["skill_name"])
            if s in skill_list:
                skill_list.remove(s)
            vendor.skills.add(s)
        for i in skill_list:
            vendor.skills.remove(i)
        return instance
