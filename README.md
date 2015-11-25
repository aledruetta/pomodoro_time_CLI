# Pomodoro Time CLI

Una aplicación en línea de comandos para la técnica *Pomodoro*.

### Usando Pomodoro Time CLI

Pomodoro divide el tiempo de trabajo/estudio/concentración en bloques de 25 minutos, con pausas de 5 a 15 minutos. Las pausas breves se intercalan entre cada uno de los ciclos de trabajo, mientras que las más extensas lo hacen una vez a cada 4 ciclos:

> 25' + 5' + 25' + 5' + 25' + 5' + 25' + *15'* ...

Pomodoro Time CLI fue escrito en *Python3* y sólo ha sido testado en *Ubuntu Linux*. La aplicación se encuentra en un estado muy temprano de desarrollo. Cada ciclo será señalizado por medio de una señal sonora y una notificación del sistema. El usuario puede optar por continuar trabajando, descansar o finalizar la aplicación.

### Requisitos previos

    - python 3.x
    - [pygame](http://pygame.org)

### Instalando y ejecutando Pomodoro Time CLI

Abra el terminal y ejecute los siguientes comandos:

<!-- language: lang-bash -->

    $ git clone git@github.com:aledruetta/pomodoro_time_CLI.git
    $ cd path/to/pomodoro_time_CLI
    $ python3 pomodoro.py

### Screenshots

- Rejoj:

![Pomodoro Time CLI working](images/pomodoro_time_CLI.png)

- Notificaciones:

![Notificaciones](images/notify.png)

## Próximos pasos

    - Implementar un sistema de etiquetas (tags) e informe de tiempo dedicado a cada tarea.

