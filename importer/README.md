# Importer

This is a Django app which uses celery to download images from a
collection on loc.gov. It also uploads those images to an S3 bucket.

## Prerequisites

1. If uploading to S3 bucket, AWS S3 bucket created and your environment is configured for the awscli tool
1. If running in dev mode, HTTP access to tile-dev.loc.gov and dev.loc.gov

## Usage

1. Start the Python shell:

    ```bash
    $ docker-compose up
    $ docker exec -it concordia_importer_1 bash
    root@62e3ebef4de2:/app# python3 ./manage.py shell
    ```

1. Run some test imports:

    ```Python console
    Python 3.6.5rc1 (default, Mar 14 2018, 06:54:23) [GCC 7.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from importer.importer.tasks import download_async_campaign, check_completeness
    >>> result = download_async_campaign.delay("https://www.loc.gov/collections/clara-barton-papers/?fa=partof:clara+barton+papers:++diaries+and+journals,+1849-1911")
    >>> result.ready()
    >>> result.get()
    >>> result2 = check_completeness.delay()
    >>> result2.ready()
    >>> result2.get()
    ```

To count the files and check disk usage in `/concordia_images` after download is
complete:

```console
$ docker exec -it concordia_app_1 bash
$ find /concordia_images -type f | wc -l
$ df -kh
```

## Integration

After the images have been downloaded in the docker environment:

1. Copy the images from the docker volume to the running docker app container.

    ```bash
    $ ubuntu@ip-172-31-94-65:~/concordia$ sudo docker exec -it concordia_app_1 bash
    $ root@6eca4f3cd16d:/app# cp -R /concordia_images/mss* concordia/static/img/
    ```

1. Run the migrations in the docker app to load Clara Barton Diaries and Branch
   Rickey collections to concordia.

    ```bash
    $ root@6eca4f3cd16d:/app# python3 ./manage.py migrate
    ```
