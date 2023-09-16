GitHub Management <sup>![Python Version Badge is Missing](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)</sup>
=================

Scripts
-------

### Setup

1. `git clone https://github.com/QubitPi/github-management.git`
2. `cd github-management`
3.[Create a GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  with the following scrope

  ![Error loading scope.png](./scope.png)

4. Make the token an OS environment variable with

  ```bash
  export GITHUB_MANAGEMENT_TOKEN=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
  ```

5. You are all set!

### Deleting All Labels of a Repo

```bash
python3 delete-all-labels.py -h
python3 delete-all-labels.py -o QubitPi -r my-repo
```

### Create Labels for [Documentation Fork](https://github.com/QubitPi#i-learn-technologies-everyday-through-open-source-)

```bash
python3 create-label-documentation-fork.py -h
python3 create-label-documentation-fork.py -o QubitPi -r my-repo
```

Github Actions Workflows
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

### Cypress E2E Tests

**Cypress E2E Tests** offers developers Actions that provide a way to automate, customize, and execute end-to-end tests 
within a GitHub project. 

This action helps ease the setup of Cypress in a GitHub Action. The action provides dependency installation via
**yarn**, scanning of test specs, _running each spec in parallel_, and upload test screenshots and video on test
failure.

The example below is a very simple setup:

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

4. Use Cypress E2E Tests workflow:

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

License
-------

The use and distribution terms for ***github-actions-workflows*** are covered by the
[Apache License, Version 2.0][Apache License, Version 2.0].

<div align="center">
    <a href="https://opensource.org/licenses">
        <img align="center" width="50%" alt="License Illustration" src="https://github.com/QubitPi/QubitPi/blob/master/img/apache-2.png?raw=true">
    </a>
</div>

[Apache License, Version 2.0]: http://www.apache.org/licenses/LICENSE-2.0.html

[Sous Chefs' linting action]: https://github.com/sous-chefs/.github/blob/main/.github/workflows/lint-unit.yml

License
-------

The use and distribution terms for [github-management](https://github.com/QubitPi/github-management) are covered by the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

<div align="center">
    <a href="https://opensource.org/licenses">
        <img align="center" width="50%" alt="License Illustration" src="https://github.com/QubitPi/QubitPi/blob/master/img/apache-2.png?raw=true">
    </a>
</div>
