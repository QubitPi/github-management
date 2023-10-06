GitHub Management <sup>![Python Version Badge is Missing](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)</sup>
=================

Scripts
-------

### Setup

1. Install Python GraphQL client library: `pip3 install "gql[all]"`
2. `git clone https://github.com/QubitPi/github-management.git`
3. `cd github-management`
4. [Create a GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
   with the following scrope

   ![Error loading scope.png](./scope.png)

5. Make the token an OS environment variable with

  ```bash
  export GITHUB_MANAGEMENT_TOKEN=ghp_MyTygnyo0HHsdfewf2efqwf34dwee1f82pp1pu
  ```

6. You are all set!

### Managing Repo Labels

This script refresh a GitHub repo with [most up-to-date labels](./github-labels.json):

```bash
python3 managing-repo-labels.py -h
python3 managing-repo-labels.py -o QubitPi -r my-repo
```

GitHub Actions Workflows
------------------------

### YAML & Markdown Link

This was inspired by [Sous Chefs' linting action] and includes 3 checks

1. [YAML lint](https://github.com/marketplace/actions/yaml-lint-action) which requires a
   [config file](https://github.com/paion-data/astraios/blob/master/.yamllint) at project root
2. [Markdown lint](https://github.com/marketplace/actions/markdownlint-mdl-action) (no config file needed)
3. [Markdown link check](https://github.com/gaurav-nelson/github-action-markdown-link-check) with a config files 
   [1](https://github.com/paion-data/astraios/blob/master/.mdlrc) and
   [2](https://github.com/paion-data/astraios/blob/master/markdownlint.rb) both at project root

Here is an example:

```yml
---
name: My GitHub Workflow

"on":
  pull_request:
  push:
    branches:
      - master

jobs:
  yml-md-style:
    uses: QubitPi/github-actions-workflows/.github/workflows/yml-and-md-style-checks.yml@master
```

### UI Code Style Check

It is a common pattern for all frontend projects to check code syltes with

- [Prettier](https://qubitpi.github.io/prettier/docs/en/install.html), and
- [ESLint](https://www.npmjs.com/package/eslint)

```yml
---
name: My GitHub Workflow

"on":
  pull_request:
  push:
    branches:
      - master

jobs:
  code-style:
    uses: QubitPi/github-actions-workflows/.github/workflows/ui-code-style.yml@master
```

### Cypress E2E Tests in Parallel with Spec File Granularity

Running Cypress E2E tests are very time-consuming, especially when software becomes large with tens of spec files. 
Although Cypress offers ["dashboard" feature](https://on.cypress.io/cloud), which claims to offer parallel testing 
capabilities, it is better to confine all CI/CD logics, including testing, inside one realm. Unfortunately, GitHub 
Actions offers limited parallelism which make things a little hard.

What we would like to achieve is the following

- All CI/CD logics, including tests, stays in GitHub Actions
- Each `spec.ts` file is a workflow job, so that CI/CD can parallelize E2E tests at test file granularity
- All E2E tests run (an in parallel as well) in two environments: dev & prod
- No code duplication, i.e. configuration in dev tests never repeats in prod tests

[**Cypress E2E Tests**](./.github/workflows/cypress-e2e-tests.yml) allows developers to automate, customize, and 
execute **parallel** end-to-end tests all in GitHub Actions. It provides dependency installation via **yarn**,
scanning of test specs, _running each spec in parallel_, and upload test screenshots and video on test failure.

To setup:

1. Put all **.spec.cy.ts** test files under "cypress/e2e" directory
2. Have a file at the root of project with the name **.env.test**, which will contain all the environment variables used
   during the test. The action will rename the ".env.test" name to the
   regular _.env_ file
3. Place a **test-setup.sh** file under _.github/test-setup.sh_ directory for any pre-test setup. For example, to start
   a [lowdb](https://github.com/typicode/lowdb) server and
   [run e2e only after the server starts](https://www.npmjs.com/package/wait-on):

   ```bash
   #!/bin/bash

   cd packages/lowdb
   yarn install
   yarn start ../../.github/db.json &
   yarn wait-on-server
   ```

   Don't forget to make the script executable by running

   ```bash
   chmod u+x .github/test-setup.sh
   ```
   
4. We assume that the way we package and run web app in the dev & prod environments are very different. The purpose of 
   having dev and prod environment e2e tests is to answer the following question during test:

   **If a test in production environment fails, is this a code bug or simply because our environment got screwed up?**

   For example, when a login page is not showing up, it could be someone's new code put login page into an undesirable 
   state, in which case it's a bug, or our production server puts our app behind a wrong HTTP port, in which case it's 
   a configuration management issue in production environment

   In the case above, if the dev E2E passes while the prod E2E fails, we can quickly spot zoom-in the source of error 
   and save a lot of debugging time.

   We will put the following 3 scripts in GitHub repo's top **package.json**:

   ```json
     "scripts": {
       "e2e": "cypress run",
       "wait-on-dev": "wait-on -c /path/to/wait-on-config.js http-get://localhost:3000/",
       "wait-on-prod": "wait-on -c /path/to/wait-on-config.js http-get://localhost:3000/"
     },
   ```
   
   The `wait-on-dev` and `wait-on-dev` are [wait-on](https://github.com/jeffbski/wait-on) command wrappers that block  
   execution until web app is up and running:

5. Use Cypress E2E Tests workflow:

   ```yaml
   ---
   name: My GitHub Workflow
   
   "on":
      pull_request:
      push:
         branches:
            - master
   
   jobs:
     e2e-tests:
       uses: QubitPi/github-actions-workflows/.github/workflows/cypress-e2e-tests.yml@master
   ```

   When web app is running at port 3000, we will run only **one** E2E spec

License
-------

The use and distribution terms for [github-management](https://github.com/QubitPi/github-management) are covered by the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

<div align="center">
    <a href="https://opensource.org/licenses">
        <img align="center" width="50%" alt="License Illustration" src="https://github.com/QubitPi/QubitPi/blob/master/img/apache-2.png?raw=true">
    </a>
</div>

[Apache License, Version 2.0]: http://www.apache.org/licenses/LICENSE-2.0.html

[Sous Chefs' linting action]: https://github.com/sous-chefs/.github/blob/main/.github/workflows/lint-unit.yml
