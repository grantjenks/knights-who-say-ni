# Knights Who Say Ni

Ni! Ni! Ni!

1. Send me an email with your username.

2. Give me a shrubbery i.e. pay up.

3. Receive license code by email.

4. Configure software with username and license code.


## Quick Start

```bash
$ pip install knightswhosayni

$ python -m knightswhosayni.main [path/to/src] [module-name] [prefix] [license-key]

$ tox -e py

$ python -m build

$ twine upload dist/*
```


## License Users


### Option 1: Using Code

```python
import builtins
builtins.[prefix]LICENSE_USER = '[username]'
builtins.[prefix]LICENSE_CODE = '[license code]'
```


### Option 2: Using Environment Variables

```bash
export [prefix]LICENSE_USER=[username]
export [prefix]LICENSE_CODE=[license code]
```


### Option 3: Using License File

```config
# [prefix.lower()]license.ini
[prefix.strip('_')]
LICENSE_USER=[username]
LICENSE_CODE=[license code]
```


### Example

Given:

* prefix -- `'PACKAGE_NAME_V1_'`

* username -- `name@example.com`

```python
import builtins
builtins.PACKAGE_NAME_V1_LICENSE_USER = 'name@example.com'
builtins.PACKAGE_NAME_V1_LICENSE_CODE = 'e385cf4c-be9a-4389-82ba-bfa85b8ad17c'
```

```bash
export PACKAGE_NAME_V1_LICENSE_USER=name@example.com
export PACKAGE_NAME_V1_LICENSE_CODE=e385cf4c-be9a-4389-82ba-bfa85b8ad17c
```

```config
# package_name_v1_license.ini
[PACKAGE_NAME_V1]
LICENSE_USER=name@example.com
LICENSE_CODE=e385cf4c-be9a-4389-82ba-bfa85b8ad17c
```


## Caveats

Maybe this package is a bad idea. But here's how I got here:

1. I occassionally make useful packages.

2. People use them and occassionally contribute (that's good!).

3. Rarely people donate to the projects (the amounts are tiny).

4. I thought about using GitHub Donors but felt like it required a whole online
   "personality". I like making friends but thought maybe old-school software
   licensing could work.

5. Real encryption using RSA or whatnot introduces a dependency that is too
   heavy (my libraries typically have no dependencies).

6. I don't want to force code to call a web server either every time it runs
   (privacy issues and whatnot).

7. I still believe most people are willing to "do the right thing" especially
   if it's more annoying to "do the wrong thing".

8. I still want to produce Open Source software so if you want to steal the
   code, it's about as easy as ctrl-c ctrl-v. BUT, I'm going to bet that losing
   the easiness of "pip install thing" is Annoying Enough(TM).

9. Hence, the Knights Who Say Ni are my paradigm. They're troublesome enough to
   bring them a shrubbery but not so troublesome that RSA encryption, and
   license servers, and lawyers need be involved.

Put into practice, the package works in four parts:

1. The `__license__.py` file is added to the Python package for distribution.

2. The `__init__.py` file of the Python package is modified for a new encoding.

3. License checks are injected into the Python package source files.

4. The Python package source files are encrypted, err, obfuscated, err,
   obscured, err, encoded with the new encoding.

Which achieves three things:

1. License checks occur on import of the source files.

2. The source files in the package are hard to change.

3. Changes to the package's `__init__.py` break the encoding.

Which I'm hoping is just Annoying Enough(TM) to motivate paying for a license
rather than working around it.

Some things this does not guard against:

1. Making your own keygen -- correct, RSA is great but too heavyweight.

2. Decoding the source code -- correct, it's already Open Source online.

3. Vendoring the unobfuscated code -- correct, but then no pip updates.
