# auth

This is a template for python projects.

Exists a branch for aiohttp projects. You can use it replacing `master` by `aiohttp` in next steps.

Set this repo as remote and merge to yours.
And then, replace `auth` with your python package desired name.
```bash
git remote add template https://github.com/pando85/python-project-template.git
git pull --all
git merge template/master 
APP_NAME={desired_name}
mv auth $APP_NAME
find ./ -type f -not -path "./.git/*" -exec sed -i "s/auth/$APP_NAME/g" {} \;
```

For travis magic you need [travis-cli](https://github.com/travis-ci/travis.rb).

If you want to grant travis access to update your requirements you will need to replace `__GITHUB_TOKEN__` with next command:

```bash
# Get token from Github with public repo access
GITHUB_TOKEN={token}
SECURE_SECRET=$(travis encrypt GITHUB_TOKEN=$GITHUB_TOKEN)
sed -i "s/__GITHUB_TOKEN__/$SECURE_SECRET/g" .travis.yml
```

To get dockerhub build working when merge something into master you will need to replace `__DOCKERHUB_TOKEN__` with next command:


```bash
# Get token from dockerhub repo-> Build Settings -> Build triggers -> Trigger token
DOCKERHUB_TOKEN_TRIGGER={token}
SECURE_SECRET=$(travis encrypt DOCKERHUB_TOKEN=$DOCKERHUB_TOKEN_TRIGGER)
sed -i "s/__DOCKERHUB_TOKEN__/$SECURE_SECRET/g" .travis.yml
```

## Lint

Lint: `make lint`

## Dev

Run app: `make run`

## Tests

Run tests: `make test`

### Production

**Warning**: aiohttp is [slower with gnunicorn](https://docs.aiohttp.org/en/stable/deployment.html#start-gunicorn). Basic `python -m my_app` execution is prefered.
