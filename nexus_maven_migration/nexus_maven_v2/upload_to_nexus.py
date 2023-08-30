import requests

import search_dependencies

import os


def log(msg):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    log_file_name = f"logs/log-upload.log"
    log_file = open(log_file_name, "a+")
    print(msg)
    log_file.writelines(f"{msg}\n")
    log_file.close()


def upload(base_path, url, repository, user, password):
    if not url.endswith("/"):
        url = url + '/'

    nexusApi = url + 'service/rest/v1/components'

    log(f"Listing dependencies at {base_path}")
    dependencies = search_dependencies.list_folder_recursively(base_path)
    log(f"It was found {len(dependencies)} valid dependencies. Lets begin the upload process.")

    processed = 0
    total = len(dependencies)
    success = 0
    errors = 0

    log('Uploading...')

    for dependency in dependencies:
        result = upload_dependency(dependency, url=nexusApi, user=user, password=password,
                                   repository=repository)
        processed += 1
        if result.get('code') != 204:
            errors += 1
            log(f"Fail to upload the dependency ${dependency} and  {result}.")
        else:
            success += 1
        if processed % 10 == 0:
            log(
                f"Progress {(processed / float(total)) * 100}%. Total processed: {processed} with {success} success and {errors} errors.")

    if errors > 0:
        msg = f"Finished! {processed} dependencies were processed with {success} success and {errors} errors." \
              f"The details can be found in /logs."
        log(msg)
    else:
        msg = f"Finished! {processed} dependencies were processed with {success} success and no errors."
        log(msg)
    return msg


def upload_dependency(dependency, url, user, password, repository='maven-releases'):
    if len(dependency) < 2:
        return {'code': 0, 'msg': 'Invalid Dependency! The dependency needs at least the POM file and one artifact.'}

    params = (
        ('repository', repository),
    )

    files = {
        'maven2.generate-pom': (None, 'false')
    }

    asset = 0

    if "artifact" in dependency:
        asset += 1
        files[f"maven2.asset{asset}"] = (dependency.get('artifact'), open(dependency.get('artifact'), 'rb'))
        files[f"maven2.asset{asset}.extension"] = (None, dependency.get('artifact.ext'))

    if "pom" in dependency:
        asset += 1
        files[f"maven2.asset{asset}"] = (dependency.get('pom'), open(dependency.get('pom'), 'rb'))
        files[f"maven2.asset{asset}.extension"] = (None, 'pom')

    if "sources" in dependency:
        asset += 1
        files[f"maven2.asset{asset}"] = (dependency.get('sources'), open(dependency.get('sources'), 'rb'))
        files[f"maven2.asset{asset}.extension"] = (None, 'jar')
        files[f"maven2.asset{asset}.classifier"] = (None, 'sources')

    if "javadoc" in dependency:
        asset += 1
        files[f"maven2.asset{asset}"] = (dependency.get('javadoc'), open(dependency.get('javadoc'), 'rb'))
        files[f"maven2.asset{asset}.extension"] = (None, 'jar')
        files[f"maven2.asset{asset}.classifier"] = (None, 'javadoc')

    result = requests.post(url, params=params, auth=(user, password), files=files, verify=False)

    return {'code': result.status_code, 'msg': result.text}


if __name__ == '__main__':
    base_path = r'D:\res'
    url = 'http://localhost:8931'
    repository = 'maven_zjhost'
    user = 'admin'
    password = 's'
    upload(base_path, url, repository, user, password)
