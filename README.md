# Система пропускного контроля
Данный репозиторий содержит реализацию системы пропускного контроля с распознаванием лиц.
Проект был реализован на языке Python и развернут в кластере K3S. В качестве базы данных
используется PostgreSQL сервер, размещенный в Yandex cloud.

## Структура модулей
Монорепозиторий состоит из трех частей:
- реализация edge-стороны (находится в папке **edge**)
- реализация cloud-стороны (находится в папке **cloud**)
- манифесты для развертывания приложения в кластере (находится в папке **manifests**)

Cloud-сторона состоит из одного модуля, в котором производится обмен данных с PosgtreSQL сервером и выполняется
обработка запросов, приходящих с edge-стороны.

Edge-сторона имеет 2 режима работы:
- *live* (распознавание изображений в реальном времени)
- *benchmark* (тестирование производительности системы на заранее заданном наборе изображений)

Таким образом, edge-сторона состоит из трех модулей:
- `core` (отвечает за распознавание изображений и за взаимодействие с сервером)
- `live` (отвечает за получение изображений с камеры)
- `benchmark` (отвечает за загрузку изображений из папки с тестовым датасетом и измерением производительности)

Код edge-стороны организован таким образом, что к `core` модулю могут обращаться другие модули, но не наоборот.
Модули `live` и `benchmark` используют в своей работе компоненты `core` модуля, в свою очередь
определяя источники данных и реализуя дополнительную логику.

В папке **manifests** содержатся следующие файлы:
- `cloud.yaml` (отвечает за развертывание cloud-стороны)
- `edge.yaml` (отвечает за развертывание edge-стороны)
- `config.yaml` (содержит конфигурационные данные, используемые в `edge.yaml` и `cloud.yaml`)
- `secret.yaml` (заготовка, в которую нужно вставить учетные данные сервера yandex.cloud, 
используемые в `edge.yaml` и `cloud.yaml`)

## Развертывание системы
Ниже будет описан процесс развертывания кластера с данным приложением, состоящего из трех узлов: 
- *control plane* (узел, содержащий плоскость управления кластером)
- *cloud* (узел с cloud-стороной)
- *edge* (узел с edge-стороной)

Edge- и cloud-сторона развертывались на виртуальных машинах с использованием программы multipass.  
Установить multipass можно следуя [официальному руководству](https://multipass.run/install).

После установки multipass необходимо выполнить следующие команды:

Для плоскости управления (control plane):

    multipass launch -n control-plane -c 2 -m 2G -d 10G --bridged
    multipass exec control-plane -- sudo swapoff -a
    multipass exec control-plane -- curl -sfL https://get.k3s.io | sh -
    multipass exec control-plane -- sudo cat /var/lib/rancher/k3s/server/node-token

Для cloud-стороны:

    multipass launch -n cloud -c 2 -m 1G -d 15G --bridged
    multipass exec cloud -- sudo swapoff -a
    multipass exec cloud -- curl -sfL https://get.k3s.io | K3S_URL=https://<control_plane_ip>:6443 K3S_TOKEN=<token> sh -
    multipass exec cloud -- sudo kubectl apply -f https://raw.githubusercontent.com/TurboGoose/turnstile-client/main/manifests/config.yaml
    multipass exec cloud -- sudo kubectl apply -f <path_to_your_secret_postgres_credentials>
    multipass exec cloud -- sudo kubectl apply -f https://raw.githubusercontent.com/TurboGoose/turnstile-client/main/manifests/cloud.yaml

Для edge-стороны:

    multipass launch -n edge -c 1 -m 1G -d 15G --bridged --mount <path_to_dataset>:~/dataset
    multipass exec edge -- sudo swapoff -a
    multipass exec edge -- curl -sfL https://get.k3s.io | K3S_URL=https://<control_plane_ip>:6443 K3S_TOKEN=<token> sh -
    multipass exec edge -- sudo kubectl apply -f https://raw.githubusercontent.com/TurboGoose/turnstile-client/main/manifests/config.yaml
    multipass exec edge -- sudo kubectl apply -f <path_to_your_secret_with_postgres_credentials>
    multipass exec edge -- sudo kubectl apply -f https://raw.githubusercontent.com/TurboGoose/turnstile-client/main/manifests/edge.yaml

Проверить состояние кластера можно следующими командами:

    multipass exec control-plane -- sudo kubectl get nodes
    multipass exec control-plane -- sudo kubectl get pods