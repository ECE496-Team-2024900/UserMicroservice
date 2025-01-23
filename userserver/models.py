# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AvailableSlots(models.Model):
    clinician = models.ForeignKey('Clinicians', models.DO_NOTHING)
    start_time_of_availability = models.CharField()
    end_time_of_availability = models.CharField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'available_slots'


class Clinicians(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'clinicians'


class Patients(models.Model):
    medical_ref_number = models.IntegerField(primary_key=True)
    first_name = models.CharField()
    last_name = models.CharField()
    phone_num = models.IntegerField()
    medical_device_id = models.CharField(blank=True, null=True)
    email = models.CharField()
    date_of_birth = models.DateField()

    class Meta:
        managed = False
        db_table = 'patients'