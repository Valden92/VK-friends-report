# VK-friends-report
*Это консольное приложение, позволяющее получить список подписчиков (друзей) для переданного ID пользователя VK и генерирующее отчет в форматах CSV, TSV или JSON.*
 ***
 
**Версия Python:** 3.9
 
**Среда, в которой написана программа:** Windows 10
 
**Модули, используемые для работы:** os, sys, datetime.datetime, csv, json, requests
 
**Модули, используемые для тестирования:** unittest и unittest.TestCase
 
**Модули, требующие дополнительной установки:** requests 
 
>*Для установки можно использовать меденжер пакетов pip. Подробнее можно прочитать тут: https://pypi.org/project/requests/*
 
 
## Подготовка к использованию программы
*Для начала работы с парсером данных, пользователю требуется заполучить токен и ID человека, чей список друзей нужно получить.* 
  
 ### Получение токена:
  
 Для взаимодествия с Вконтакте используется их открытый API VK *(Подробнее тут: https://dev.vk.com/guide )*.
  
 Чтобы пользоваться API VK требуется токен, благодаря которому сервер идентифицирует от чьего имени поступает запрос на сервер.
  
 **Получение токена можно разделить на две части:**
  - регистрация своего приложения;
  - получение токена в этом приложении.
  
 Создать приложение можно на этой странице: https://vk.com/editapp?act=create
  
 *Создавать приложение лучше на платформе **Standalone-приложения**. Это позволит получить наибольшие возможности, чем в иных вариантах выбора.*
  
 Создав приложение и перейдя на вкладку настроек, нужно скопировать **ID приложения** и подставить в эту ссылку:
  
 >https://oauth.vk.com/authorize?client_id={ID_Приложения}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline&response_type=token&v=5.131
  
В scope перечисляются разрешения для приложения (подробный список разрешений: https://vk.com/dev/permissions ). Нам нужно только friends и offline (*offline позволяет создать бессрочный токен*). Также можно указать более актуальную версию API (например: v=5.131).
  
Перейдя по сформированной ссылке, откроется диалоговое окно, в котором будут показаны разрешения для вашего токена (нужно будет согласиться). После чего произойдёт переадресация на страницу, в адресной строке которой будет **access_token**. С помощью данного токена можно выполнять запросы к API VK. **Сохрани его.**
  
### Получение ID пользователя:
  
Для получения ID пользователя достаточно перейти на его профиль VK, открыть любую фотографию и в адресной строке первые цифры после **photo** и до **нижнего подчеркивания** будут являться идентификатором пользователя. Или можно воспользоваться любым сторонним сервисом, скопировав туда url главной странички пользователя.
  
## Взаимодействие с программой

>*Для завершения работы с программой достаточно ввести в любой момент вместо ввода данных **"Q"** (или **"q"**).*
  
### Что подается на вход:
  
  - Токен (access_token), позволяющий от вашего лица выполнять запросы к API VK.
  - Идентификатор пользователя (ID), для которого будет формироваться запрос к серверу на получение списка друзей.
  - Формат выходного файла CSV, TSV или JSON (*по умолчанию CSV*).
  - Путь для сохранения отчета (*по умолчанию в корне с программой создаться папака REPORTS*)

### Что будет на выходе:
  
- После удачного ввода Токена и ID пользователя в консоль выведется статус соединения.
- Если соединение с API VK было установлено удачно, выведется общее количество аккаунтов для предоставленного ID.
>*Если по какой-то причине для ID количество пользователей оказалось равным 0, то программа предложит либо завершить работу, либо начать вводить данные с самого начала.*
- После выбора формата отчета, в консоль выведется выбранный формат конечного файла.
- После выбора пути сохранения отчета, выбранный путь выведется на экран.
- В конце программа сообщит о запуске извелечения данных и будет выводить в консоль количество сохраненных пользователей.
- После извлечения данных, в консоль выведется: количество удачно извлеченных пользователей и количество деактивированных аккаунтов, которые не содержат полезной информации, а так же наименование отчета (report.*формат*).
