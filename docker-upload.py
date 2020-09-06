import os
import subprocess

path = str(input('Enter path: ')).strip().rstrip('/')
if os.path.exists(path):
    os.chdir(path)
    version = str(input('Enter version number: ')).strip()
    repository_url = str(input('Enter repository url: ')).strip().rstrip('/')
    project_name = str(input('Enter project name: ')).strip()
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
else:
    print('Path does not exist!')