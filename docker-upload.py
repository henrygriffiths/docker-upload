import os
import subprocess
import json

path = str(input('Enter path (empty for cwd): ')).strip().rstrip('/')
if path == '':
    path = '.'
if os.path.exists(path):
    os.chdir(path)
    repository_url = None
    project_name = None
    image_name = None
    useconfig = 'n'
    if os.path.exists('./' + 'docker-upload-config.json'):
        while True:
            useconfig = str(input('Would you like to load settings from the config file? (y/n)')).lower()
            if useconfig in ['y', 'yes']:
                config = json.load(open('./' + 'docker-upload-config.json'))
                repository_url = str(config['repository_url'])
                project_name = str(config['project_name'])
                image_name = str(config['image_name'])
                break
            elif useconfig in ['n', 'no']:
                break
            else:
                print('Input not understood, please try again')
                continue
    version = str(input('Enter version number: ')).strip()
    if repository_url is None:
        repository_url = str(input('Enter repository url: ')).strip().rstrip('/')
    if project_name is None:
        project_name = str(input('Enter project name: ')).strip()
    if image_name is None:
        image_name = str(input('Enter image name: ')).strip()
    print('Creating tag with version: ' + str(version))
    subprocess.run(['git', 'tag', version])
    print('Pushing tag to git')
    subprocess.run(['git', 'push', 'origin', version])
    print('Building docker image')
    subprocess.run(['docker', 'build', '--pull', '--rm', '-f', 'dockerfile', '-t', image_name + ':' + version, '.'])
    print('Tagging docker image')
    subprocess.run(['docker', 'tag', image_name + ':' + version, repository_url + '/' + project_name + '/' + image_name + ':' + version])
    print('Pushing docker image')
    subprocess.run(['docker', 'push', repository_url + '/' + project_name + '/' + image_name + ':' + version])
    print('Done!')
    if useconfig in ['n', 'no']:
        while True:
            saveconfig = str(input('Would you like to save these settings to a config file? (y/n): ')).lower()
            if saveconfig in ['y', 'yes']:
                json.dump({'repository_url': repository_url, 'project_name': project_name, 'image_name': image_name}, open('docker-upload-config.json', "w"))
                print('Config saved!')
                break
            elif saveconfig in ['n', 'no']:
                break
            else:
                print('Input not understood, please try again')
                continue
else:
    print('Path does not exist!')