# Space ship

ITMO project

[Prerequisites](#logbook)

[Entities](#entities)
  * [Recital](#entities-recital)
  * [Logbook](#entities-logbook)
  * [Relations](#entities-relations)

[Running databases](#running-databases)
  * [Recital](#running-databases-recital)
  * [Logbook](#running-databases-logbook)
  * [Relations](#running-databases-relations)

[Filling](#filling)
  * [Logbook](#filling-logbook)

[API](#api)
  * [Logbook](#api-logbook)

## Prerequisites

### mongo server

Для установки на Ubuntu:

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org

### cassandra server

Для установки из debian packages (**изменить версию с 311x на актуальную**)

    echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
    curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
    sudo apt-get update
    sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
    sudo apt-get install cassandra

### neo4j server

Установка производится так:

    wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
    echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list
    sudo apt update
    sudo apt install neo4j

#### cassandra-driver

Модуль для python, с помощью которого идет взаимодействие с БД

Устанавливается командой (может занять несколько минут)

    pip install cassandra-driver

### pymongo

Модуль для python, с помощью которого идет взаимодействие с базой данных, содержащей информацию о корабле (работающей на технологии Mongo DB) для обеспечения консистентности хранимых данных при их изменении

Устанавливается командой 
    
    pip install pymongo

### py2neo

Модуль для python, с помощью которого идет взаимодействие с базой данных, содержащей информацию об организации деятельности экипажа (работающей на технологии neo4j) для обеспечения консистентности хранимых данных при их изменении

Устанавливается командой 

    pip install py2neo

### neomodel

ODM для python, с помощью которого идет взаимодействие с neo4j

Устанавливается командой

    pip install neomodel

### maven

Система сборки для создания jar-архива с пользовательскими функциями для neo4j

Устанавливается например так

    sudo apt-get install maven

## Entities

<h3 id="entities-recital">
Recital
</h3>

Информация о составе корабля и его экипажа

Поскольку каждому экземпляру сущности автоматически присваивается object id, и именно он используется в дальнейшем для ссылки на экземпляры сущностей в том числе и из других баз данных, далее в описании сущностей он указываться не будет.

* department - сущность для представления департамента в информационной системе

|property|data type|description|
|--------|---------|-----------|
|name|string|Название департамента|
|hrefToVkCommunity|string|Ссылка на сообщество вконтакте|

* people - сущность для представления члена экипажа корабля

|property|data type|description|
|--------|---------|-----------|
|name|string|Имя члена экипажа|
|surname|string|Фамилия члена экипажа|
|patronymic|string|Отчество члена экипажа|
|department|object id|Ссылка на департамент в котором числится член экипажа|
|phoneNumber|string|Номер телефона|
|specialization|object id|Ссылка на специализацию, присвоенную члену экипажа|

* properties - материальное имущество корабля (**технические средства**, **мебель**, **средства вооружения** и т.д.)

|property|data type|description|
|--------|---------|-----------|
|name|string|Название предмета|
|type|object id|Ссылка на тип, к которому принадлежит элемент имущества|
|dateOfAdmission|string|Дата поступления на корабль, внесения в списки имущества и, соответственно, введения в эксплуатацию|
|comissioningDate|object id|Дата прекращения эксплуатации элемента имущества, исключения из списков корабля, и, в некоторых случаях, выброса во внешнюю среду|
|department|object id|Ссылка на департамент в котором числится предмет|

* propertyTypes - типы материального имущества корабля

|property|data type|description|
|--------|---------|-----------|
|name|string|Название типа имущества (**laptop**, **table**, **laser gun**, **big fragging gun**, etc)|
|description|string|Описание типа имущества|

* specializations - специальности членов экипажа

|property|data type|description|
|--------|---------|-----------|
|name|string|Название специальности (**electrician**, **doctor**, **first engineer**, **second engineer**, etc)|

* states - возможные состояния систем корабля

|property|data type|description|
|--------|---------|-----------|
|name|string|Название состояния (**ready**, **repair**, **working**, etc)|
|description|string|Описание состояния|

* systems - системы, имеющиеся на корабле

|property|data type|description|
|--------|---------|-----------|
|name|string|Название системы (**fuel system**, **main engine**, **spare engine**, **main thrusters**, **spare thrusters**, **power system**, etc)|
|type|object id|Тип системы корабля|
|serialNumber|double|Серийный номер, присвоенный заводом-изготовителем|
|dateOfLaunch|date|Дата запуска системы|
|dateOfLastChecking|date|Дата последней проверки системы|
|personInCharge|object id|Ссылка на сущность, представляюшую человека, ответственного за обеспечение нормального режима работы системы|
|state|object id|Ссылка на состояние, присвоенное системе|

* systemTypes - типы систем, имеющихся на корабле

|property|data type|description|
|--------|---------|-----------|
|name|string|Название типа систем (**fuel**, **engine**, **thrusters**, **hydraulic**, etc)|
|description|string|Описание типа системы корабля|

* sensors - источники данных об окружающей обстановке

|property|data type|description|
|--------|---------|-----------|
|name|string|Название сенсора (**MINAS_MORGUL_T400**, **STADDLE_N23**, **VALMAR_17**, etc)|
|location|object id|Ссылка на объект, представляюший расположение сенсора|

* boats - информационные модели судов меньшего размера, хранящихся на корабле и предназначенных для следования к местам совершения операций во внешней среде без изменения курса корабля

|property|data type|description|
|--------|---------|-----------|
|name|string|Название судна|
|capacity|integer|Количество человек, которое может принять судно|

* locations - возможные расположения сенсоров корабля

|property|data type|description|
|--------|---------|-----------|
|name|string|Название места расположения, которое должно давать представление о том, где находится сенсор (**top edge**, **bottom edge**, **left side**, etc)|
 

<h3 id="entities-logbook">
Logbook
</h3>

Журналы с данными о работе корабля

* system_test - предназначена для записи результатов тестирования систем корабля

|property|data type|description|
|--------|---------|-----------|
|date|date|Дата, для которой актуально приведенное состояние системы|
|time|time|Временная отметка, для которой актуально приведенное состояние системы|
|system id|12 bytes|Идентификатор системы, состояние которой было зафиксировано|
|result|int|Результат теста, может принимать значения от 0 до 100|

* control_action - описывает команду, когда-либо выданную системе управления кораблем (например, повернуть налево или снять показания датчиков космического излучения по левому борту)

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, определяющая момент получения команды|
|mac_address|6 bytes|MAC-адрес устройства, выдавшего команду|
|user_id|12 bytes|Идентификатор пользователя, выдавшего команду|
|command|text|Выданная команда (например, **get**)|
|params|text|Параметры, уточняющие, к какому результату должна привести команда (например, **--sensor=MINAS_MORGUL T400 --value_name=cold_dark_matter_concentration**)|
|result|text|Результат работы команды (например, **23.235715395881783 TeV**)|

* position - содержит историю перемещения корабля в космическом пространстве

|property|data type|description|
|--------|---------|-----------|
|date|date|Дата, определяющая момент получения команды|
|time|timestamp|Временная отметка, определяющая момент получения команды|
|x|double|Координата корабля по оси OX, которая направлена от Земли в сторону планеты не-Марс|
|y|double|Координата корабля по оси OY, которая перпендикулярна оси OX и направлена в сторону созвездия Кассиопея|
|z|double|Координата корабля по оси OZ|
|speed|double|Линейная скорость корабля|
|attack_angle|double|Угол между продольной осью корабля и осью OX|
|direction_angle|double|Угол между проекцией продольной осью корабля на плоскость XOY и осью OX|

* sensors_data - содержит данные о состоянии внешней среды, поставляемые сенсорами, расположенными по периметру корабля

|property|data type|description|
|--------|---------|-----------|
|date|date|Дата, определяющая момент получения данных от сенсора|
|time|timestamp|Временная отметка, определяющая момент получения данных от сенсора|
|source_id|12 bytes|Идентификатор сенсора, предоставившего данные|
|event|text|Наименование события, ставшего причиной фиксирования данных (например, **request**)|
|value_name|text|Название измеренной величины (например, **space_radiation**)|
|value|double|Значение измеренной величины|
|units|text|Единицы измерения (например, **eV** - сокрашение от электрон-вольт|

* shift_state - хранит обстановку в области, доверенной некоторой смене, на данный момент времени

|property|data type|description|
|--------|---------|-----------|
|date|date|Дата, для которой характерны данные о смене|
|time|timestamp|Временная отметка, для которой характерны данные о смене|
|shift_id|16 bytes|Идентификатор смены, для которой характерно зафикисированное состояние на некоторый момент времени|
|warning_level|text|Уровень опасности в районе, доверенном смене (может принимать значения **lowest**, **low**, **medium**, **heigh**, **highest**)|
|remaining_cartridges|double|Оставшиеся патроны (в процентах)|
|remaining_air|double|Оставшийся воздух (в процентах)|
|remaining_electricity|double|Оставшееся электричество (в процентах)|
|comment|text|Необязательный комментарий от работников смены|

* operation_state - содержит описание состояния операции на некоторый момент времени

|property|data type|description|
|--------|---------|-----------|
|date|date|Дата, для которой характерны данные об операции|
|time|timestamp|Временная отметка, для которой характерны данные об операции|
|boat_id|12 bytes|Необязательный идентификатор машины, зарезервированной для выполнения операции|
|operation_id|16 bytes|Идентификатор операции|
|operation_status|text|Состояние операции на данный момент времени (например, **detaching_from_ship**)|
|distance_to_the_ship|double|Расстояние от судна, предназначенного для операции, до корабля|
|zenith|double|Зенитный угол, задающий положение судна, предназначенного для операции, относительно корабля|
|azimuth|double|Азимутальный угол, задающий положение судна, предназначенного для операции, относительно корабля|
|hydrogenium|double|Процентное содержание водорода в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|helium|double|Процентное содержание гелия в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|...|double|115 полей, содержащих данные о процентном содержании химических элементов в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|oganesson|double|Процентное содержание оганесона в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|comment|double|Необязательный комментарий от участников команды, выполняющей операцию|

<h3 id="entities-relations">
Relations
</h3>

Информация о служебных взаимоотношениях экипажа

* person - представление члена экипажа в рамках графической модели данных

|property|data type|description|
|--------|---------|-----------|
|ident|two ints <sup>[1](#relations-two-ints-note)</sup>|Идентификатор члена экипажа, соответствующий 12 - байтному идентификатору в базе данных, содержащей информацию о корабле (основанной на Mongo DB)|
|controlled|reference|Связь с сущностью Department, отображающая отношение главенствования над департаментом (DIRECTOR)|
|executor|reference|Связь с сущностью Operation, отображающая отношение исполнения операции (EXECUTOR)|
|headed|reference|Связь с сущностью Operation, отображающая отношение руководства операцией (HEAD)|
|worker|reference|Связь с сущностью Shift, отображающая отношение рядового участника смены (WORKER)|
|chief|reference|Связь с сущностью Shift, отображающая отношение ответственного за смену (CHIEF)|

* department - представление департамента в рамках графической модели данных

|property|data type|description|
|--------|---------|-----------|
|ident|two ints <sup>[1](#relations-two-ints-note)</sup>|Идентификатор департамента|
|shifts|reference|Связь с сущностью Shift, отображающая отношение организации смены департаментом (INCORPORATION)|
|operations|reference|Связь с сущностью Operation, отображающая отношение организации операции департаментом (INCORPORATION)|
|controller|reference|Связь с сущностью Person, отображающая отношение руководства департаментом (DIRECTOR)|

* operation - сущность, содержащая основные сведения о планируемой или уже осуществленной операции

|property|data type|description|
|--------|---------|-----------|
|ident|16 bytes|Идентификатор операции|
|name|text|Название операции|
|start|datetime|Дата и время начала операции|
|end|datetime|Дата и время окончания операции|
|department|reference|Связь с сущностью Operation, отображающая отношение организации операции департаментом (INCORPORATION)|
|requirement|reference|Связь с сущностью Requirement, отображающая отношение использования набора требований по специализации личного состава для операции (USER)|
|persons|reference|Связь с сущностью Operation, отображающая отношение исполнения операции (EXECUTOR)|
|head|reference|Связь с сущностью Operation, отображающая отношение руководства операцией (HEAD)|

* shift - сущность, содержащая основные сведения о прошедшей или предстоящей смене

|property|data type|description|
|--------|---------|-----------|
|ident|16 bytes|Идентификатор смены|
|start|datetime|Дата и время начала смены|
|end|datetime|Дата и время окончания смены|
|department|reference|Связь с сущностью Operation, отображающая отношение организации операции департаментом (INCORPORATION)|
|requirement|reference|Связь с сущностью Requirement, отображающая отношение использования набора требований по специализации личного состава для смены (USER)|
|persons|reference|Связь с сущностью Operation, отображающая отношение исполнения операции (EXECUTOR)|
|head|reference|Связь с сущностью Operation, отображающая отношение руководства операцией (HEAD)|

* requirement - набор требований к подготовке личного состава персонала для выполнения операции или образования смены

|property|data type|description|
|--------|---------|-----------|
|ident|16 bytes|Идентификатор набора|
|name|text|Название набора|
|content|array of jsons|Массив объектов json, каждый из которых имеет по крайней мере два поля: **ident** - идентификатор специальности из mongo db <sup>[1](#relations-two-ints-note)</sup> и **quantity** - количество сотрудников с такой специальностью|
|requirement|reference|Связь с сущностью Requirement, отображающая отношение использования набора требований по специализации личного состава для смены (USER)|
|operations|reference|Связь с сущностью Operation, отображающая отношение использования операцией набора требований (USER)|
|shifts|reference|Связь с сущностью Shift, отображающая отношение использования операцией набора требований (USER)|

<h4 id="relations-two-ints-note">
Note about two ints
</h4>

Значения в базе данных neo4j, соответствующие индексам mongodb хранятся в виде пар значений целочисленного типа. Для перевода такой пары обратно в 12-байтный индекс, необходимы вычислить значение

    item[0] * 2^48 + item[1]

И интерпретировать его как 12-байтный индекс

Например, если имеем mongo - идентификатор

    5abfdba6ee6b7f5eec83a1ca

То можем его отобразить в целочисленном представлении

    28085592993066680294893134282

Или, если разбить на два числа, то получится

    (99780070403691, 140045671702986)

Обратное преобразование выглядит как

    (int(math.pow(2, 48)) * 99780070403691 + 140045671702986).to_bytes(12, byteorder='big').hex()

Описанный механизм работает подобно механизму преобразования даты и времени из используемого ODM в число с плавающей точкой для сохранения в базе данных.

Преобразование может быть сделано при помощи пользовательской функции space_ship.get_hex_ident - для этого необходимо скопировать файл `neo4j_functions-1.0.0.jar` из папки relations/functions/target в папку plugins, соответствующую серверу neo4j (например, `/var/lib/neo4j/plugins`). Далее функцию можно вызывать в предложениях по выборке данных, например, так:

    match (n:Person) return space_ship.get_hex_ident(n.ident);

Перекомпиляция исходного кода и запуск тестов делаются с помощью команды

    mvn clean package

## Running databases

<h3 id="running-databases-recital">
Mongo DB
</h3>

Запуск сервера

    sudo service mongod start

<h3 id="running-databases-logbook">
Logbook
</h3>

Запуск сервера

    sudo service cassandra start

Выполнить команду, которая должна завершиться выводом информации о сервере с зеленым словом 'active'

    sudo service cassandra status

Для проверки статуса кластера выполнить

    sudo nodetool status

Должна вывести результат, начинающийся с сочетания **UN** (Up and Normal) в случае успеха
  
<h3 id="running-databases-relations">
Relations
</h3>

Выполнить команду

    sudo service neo4j start

Веб-интерфейс станет доступен (стандартно) по адресу

    http://localhost:7474

## Filling

<h3 id="filling-logbook">
Logbook
</h3>


После запуска сервера необходимо сначала инициализировать базу данных соответствующими таблицами (параметры для подключения к базе данных автоматически считаются из **databases.config** - это поведение может быть изменено при помощи переменных окружения)

    python3 initialize.py
  
Заполнить базу данных значениями, если они были заранее сгенерированы

    python3 fill.py
  
В противном случае сначла сгенерировать значения
  
    python3 generators/main.py
  
В скрипте можно изменять объем данных для генерации
  
Далее можно проверить что все прошло успешно запуском ряда простых манипуляций с данными

    python3 explore.py

## API

<h3 id="api-logbook">
Logbook
</h3>

В системе предусмотрена работа с содержимым базы данных при помощи API, предоставляемого разработчиком ODM cassandra driver. Однако, в соответствии с заданием была реализована возможность работы с БД на её "родном" языке.

Так, для выборки значений из базы данных можно воспользоваться функцией **select**, содержащейся в одноименном файле в папке native.

    select('position', [['x', 10], ['y', 10], ['speed'], ['time']])

В том числе есть возможность исполнения скрипта с помощью командной строки

    python3 native/select.py position x=10 y=10 speed time
    python3 native/select.py position date='2018-04-03' time='20:43:03.426852000' speed

Формат результата

    [{'date': Date(17624), 'time': Time(74583426852000), 'speed': 1488.0}]

Существует аналогичный скрипт для операции **update**

Пример вызова функции

    update('position', [['date', '2018-04-03'], ['time', '20:43:03.426852000']], [['speed', 200]])

Пример вызова скрипта

    python3 native/update.py position date='2018-04-03' time='20:43:03.426852000' 'speed->1488'

Указанные функции и скрипты предназначены для формирования запроса на языке cql и передачи его в СБД.