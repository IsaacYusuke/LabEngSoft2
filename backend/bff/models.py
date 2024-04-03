from django.db import models

# Create your models here.


class Roles(models.IntegerChoices):
    ADMIN = 0, "Administrador"
    PATIENT = 1, "Paciente"
    DOCTOR = 2, "Médico"
    NUTRITIONIST = 3, "Nutricionista"
    PSYCHOLOGIST = 4, "Psicólogo"
    PERSONAL_TRAINER = 5, "Personal Trainer"
    OTHERS = 6, "Outros"
