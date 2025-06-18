from datetime import timedelta
import datetime
from django.utils import timezone

def generar_horarios_disponibles():
    horarios_disponibles = []
    ahora = timezone.now()
    dia_actual = ahora.date()

    for i in range(15):  # Genera horarios para los próximos 15 días
        dia = dia_actual + timedelta(days=i)
        if dia.weekday() < 5:  # De lunes a viernes
            for hora in range(9, 17, 2):  # Desde las 9 am hasta las 5 pm, intervalos de 2 horas
                hora_inicio = timezone.make_aware(datetime(dia.year, dia.month, dia.day, hora))
                hora_fin = hora_inicio + timedelta(hours=2)
                horarios_disponibles.append((hora_inicio, hora_fin))
    
    return horarios_disponibles